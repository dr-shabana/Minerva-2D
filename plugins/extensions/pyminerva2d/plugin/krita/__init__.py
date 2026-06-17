#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from __future__ import print_function

import pyminerva2d
import os
import sys

# Look for PyQt
try:
    if pyminerva2d.qt_major_version() == 5:
        from PyQt5 import QtCore
    else:
        from PyQt6 import QtCore
except ImportError:
    print("Python cannot find the Qt%d bindings." % pyminerva2d.qt_major_version(), file=sys.stderr)
    print("Please make sure that the needed packages are installed.", file=sys.stderr)
    raise

import builtins

# Disallow importing a conflicting version of PyQt,
# which would load a conflicting version of Qt and crash Minerva when used.
pyqt_wrong = "PyQt" + ("6" if pyminerva2d.qt_major_version() == 5 else "5")
pyqt_wrong_casefolded = pyqt_wrong.casefold()
import_real = builtins.__import__
def importAvoidWrongPyQtHack(name, globals=None, locals=None, fromlist=(), level=0):
    name_casefolded = name.casefold()
    if name_casefolded == pyqt_wrong_casefolded or \
        name_casefolded.startswith(pyqt_wrong_casefolded+"."):

        raise(ModuleNotFoundError(
            f"This version of Minerva is not compatible with {pyqt_wrong}!",
            name=name))
    else:
        return import_real(name, globals, locals, fromlist, level)
builtins.__import__ = importAvoidWrongPyQtHack

from .api import *
from .decorators import *
from .dockwidgetfactory import *
from PyMinerva import krita

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

minerva2d_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, minerva2d_path)
print("%s added to PYTHONPATH" % minerva2d_path, file=sys.stderr)

# Shows nice looking error dialog if an unhandled exception occurs.
import excepthook
excepthook.install()

builtins.i18n = Minerva.minerva2d_i18n
builtins.i18nc = Minerva.minerva2d_i18nc
builtins.Scripter = Minerva.instance()
builtins.Application = Minerva.instance()
builtins.Minerva = Minerva.instance()


def qDebug(text):
    '''Use KDE way to show debug info

        TODO Add a way to control debug output from partucular plugins (?)
    '''
    plugin = sys._getframe(1).f_globals['__name__']
    pyminerva2d.qDebug('{}: {}'.format(plugin, text))


@pyminerva2dEventHandler('_pluginLoaded')
def on_load(plugin):
    if plugin in init.functions:
        # Call registered init functions for the plugin
        init.fire(plugin=plugin)
        del init.functions[plugin]
    return True


@pyminerva2dEventHandler('_pluginUnloading')
def on_unload(plugin):
    if plugin in unload.functions:
        # Deinitialize plugin
        unload.fire(plugin=plugin)
        del unload.functions[plugin]
    return True


@pyminerva2dEventHandler('_pyminerva2dLoaded')
def on_pyminerva2d_loaded():
    qDebug('PYKRITA LOADED')
    return True


@pyminerva2dEventHandler('_pyminerva2dUnloading')
def on_pyminerva2d_unloading():
    qDebug('UNLOADING PYKRITA')
    return True
