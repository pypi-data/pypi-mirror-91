# Copyright (C) 2010-2017 - Andreas Maier
# CONRAD is developed as an Open Source project under the GNU General Public License (GPL-3.0)

import glob
import os
import threading
import time
import warnings
from os.path import join
from pathlib import Path

import jpype
from jpype import (JClass, JPackage, JProxy, attachThreadToJVM,
                   detachThreadFromJVM, getDefaultJVMPath, isJVMStarted, java,
                   shutdownJVM, startJVM)

from . import _download_conrad, _extend_conrad_classes
from . import _windowlistener as wl

try:
    from jpype import JavaException as JException
except Exception:
    from jpype import JException


module_path = os.path.dirname(__file__)


def assert_pyconrad_initialization():
    if not PyConrad().is_java_initialized():
        raise PyConradNotInitializedError(
            'pyconrad was not initialized! Use pyconrad.setup_pyconrad()!')


class PyConradNotInitializedError(Exception):
    pass


def setup_pyconrad(max_ram='60G', min_ram='200M', dev_dirs=None):
    """ Launches JVM for execution of CONRAD code

    Keyword Arguments:
        max_ram {str} -- Maximum heap size for JVM (default: {'60G'})
        min_ram {str} -- Minimum heap size for JVM (default: {'200M'})
        dev_dirs {list} -- List of directories/JARs for Java runtime path.
        Can be used to make custom CONRAD directory or own Java code available (default: {[]}).
        Can be set by the environment variable `CONRAD_DEV_DIRS` (a ';'-separated list)
    """

    PyConrad().setup(max_ram, min_ram, dev_dirs)


def start_gui():
    PyConrad().start_conrad()


def start_reconstruction_pipeline_gui():
    PyConrad().start_reconstruction_filter_pipeline()


def terminate_pyconrad():
    PyConrad().terminate_pyconrad()


def is_initialized():
    return PyConrad().is_initialized


def is_gui_started():
    return PyConrad().is_gui_started


class PyConrad:
    # Namespaces
    classes, ij, java = None, None, None

    __conrad_path = None
    __conrad_repo_set = None

    __is_gui_started = None

    __gui_instance = None
    __gui_thread = None
    ___instance = None

    __imported_namespaces = []

    def __new__(cls, *args, **kwargs):
        if not cls.___instance:
            cls.___instance = super().__new__(
                cls, *args, **kwargs)
        cls.jvm_args = None
        return cls.___instance

    @staticmethod
    def get_instance():
        if PyConrad.___instance is None:
            PyConrad.___instance = PyConrad()
        return PyConrad.___instance

    def setup(self, max_ram="18G", min_ram="200M", dev_dirs=None):

        if not dev_dirs:
            if 'CONRAD_DEV_DIRS' in os.environ:
                dev_dirs = os.environ['CONRAD_DEV_DIRS'].split(';')
            else:
                dev_dirs = []

        if not self.is_java_initialized():
            try:
                curr_directory = os.getcwd()
                conrad_source_and_libs = self.__import__libs(dev_dirs)

                if not os.path.exists(self.__conrad_path):
                    _download_conrad.download_conrad()
                os.chdir(self.__conrad_path)

                self.jvm_args = conrad_source_and_libs + f" -Xmx{max_ram}", f"-Xmn{min_ram}"
                startJVM(getDefaultJVMPath(),
                         # '-ea', #TODO: make work with assertions
                         conrad_source_and_libs,
                         f"-Xmx{max_ram}", f"-Xmn{min_ram}", convertStrings=True)
                os.chdir(curr_directory)

                self._check_jre_version()
                self.classes = JPackage("edu")
                self.ij = JPackage("ij")
                self.java = java
                _extend_conrad_classes.extend_all_classes()
                self.classes.stanford.rsl.conrad.utils.Configuration.loadConfiguration()

            except JException as ex:
                print(ex)
        else:
            # raise Exception("JVM already started")
            warnings.warn("JVM already started")

    def start_conrad(self):
        if not self.is_java_initialized():
            raise PyConradNotInitializedError()
        if self.__gui_thread is None:
            self.__gui_thread = threading.Thread(target=self.__start_ij_gui)
            self.__gui_thread.start()
            while not self.__is_gui_started:
                time.sleep(1)
        else:
            print("Some GUI is already started")

    def start_reconstruction_filter_pipeline(self):
        if self.__gui_thread is None:
            self._context_class_loader = jpype.java.lang.Thread.currentThread().getContextClassLoader()
            self.__gui_thread = threading.Thread(target=self.__start_rfp_gui)
            self.__gui_thread.start()
            while not self.__is_gui_started:
                time.sleep(1)
        else:
            print("Some GUI is already started")

    @staticmethod
    def is_java_initialized():
        return isJVMStarted()

    def terminate_pyconrad(self):
        if self.is_initialized:
            java.lang.System.exit(0)
            shutdownJVM()
        self.__is_gui_started = False

    def __start_rfp_gui(self):
        attachThreadToJVM()
        self.__gui_instance = JPackage("edu").stanford.rsl.apps.gui
        listener = wl.WindowListener()
        proxy = JProxy(java.awt.event.WindowListener, inst=listener)
        self.__gui_instance.ReconstructionPipelineFrame.startConrad(proxy)
        self.__is_gui_started = True

        try:
            conrad_class = JClass('edu.stanford.rsl.conrad.utils.CONRAD')
            conrad_class.classLoaderForPyconrad = self._context_class_loader
        except Exception:
            pass
        detachThreadFromJVM()

        while self.__is_gui_started:
            time.sleep(1)

    def __start_ij_gui(self):
        attachThreadToJVM()
        self.__gui_instance = JPackage("edu").stanford.rsl.apps.gui
        listener = wl.WindowListener()
        proxy = JProxy(java.awt.event.WindowListener, inst=listener)

        ij = JPackage("ij").ImageJ()
        ij.addWindowListener(proxy)
        JPackage("edu").stanford.rsl.conrad.utils.Configuration.loadConfiguration()
        self.__is_gui_started = True

        detachThreadFromJVM()
        while self.__is_gui_started:
            time.sleep(1)

    def __import__libs(self, dev_dirs):
        # if user forgets the brackets
        if isinstance(dev_dirs, str):
            dev_dirs = [dev_dirs]

        # check whether CONRAD + RSL can be found nearby
        # yes: navigate there
        # no: use conrad.jar
        # list directories, check whether CONRAD/RSL are there
        self.conrad_repo_set = False
        extra_libs = ""
        dev_src = []
        for dev in dev_dirs:
            dev_path = Path(dev)

            if not dev_path.exists():
                continue

            subdirs = [x for x in dev_path.iterdir() if x.is_dir()]
            dev_src.append(str(dev_path))
            for d in subdirs:
                dev_src.append(dev_path.joinpath(d))
            if dev_path.match("CONRAD"):
                self.__conrad_path = str(dev_path)
                self.__conrad_repo_set = True
                dev_lib = dev_path.joinpath("lib")
                dev_classes = dev_path.joinpath(
                    "classes", "production", "CONRAD")
                extra_libs = list(dev_lib.joinpath(fn)
                                  for fn in dev_lib.iterdir() if ".jar" == fn.suffix)
                extra_libs.insert(0, dev_classes)
                extra_libs = ";".join(map(str, extra_libs))

        if self.__conrad_repo_set:
            src = ";".join(map(str, dev_src))
            s = f"-Djava.class.path={src};{extra_libs}"
        else:
            self.__conrad_path = _download_conrad.conrad_jar_dir()
            dev_src.extend(g for g in glob.glob(join(_download_conrad.conrad_jar_dir(), '*.jar')) if 'conrad_' not in g)
            dev_src.append(_download_conrad.conrad_jar_file())
            src = ";".join(map(str, dev_src))
            s = f"-Djava.class.path={src};{extra_libs}"

        # Unix-like systems use : instead of ; to separate classpaths
        if os.name != "nt":  # Windows
            s = s.replace(";", ":")
        return s

    def terminate(self):
        if self.is_gui_started():
            self.__terminate_pyconrad()
        shutdownJVM()

    @property
    def is_gui_started(self):
        return self.__is_gui_started

    def enumval_from_int(self, enum_name, value_int):
        return self[enum_name].values()[int(value_int)]

    def enumval_from_string(self, enum_name, value_string):
        return self[enum_name].valueOf(value_string)

    @property
    def is_initialized(self):
        return self.is_java_initialized()

    def _check_jre_version(self):
        '''
        Check JRE version. We need >1.8
        '''
        jre_version = java.lang.System.getProperty("java.version").split('.')

        if jre_version and len(jre_version) > 2:
            if jre_version[0].isdigit() and jre_version[1].isdigit():
                if int(jre_version[0]) > 1:
                    # format 9.0.1
                    assert int(
                        jre_version[0]) >= 8, "pyCONRAD needs a Jave Runtime Enviroment with version 1.8 or greater"
                else:
                    # format 1.8.0
                    assert int(
                        jre_version[0]) == 1, "pyCONRAD needs a Jave Runtime Enviroment with version 1.8 or greater"
                    assert int(
                        jre_version[1]) >= 8, "pyCONRAD needs a Jave Runtime Enviroment with version 1.8 or greater"
