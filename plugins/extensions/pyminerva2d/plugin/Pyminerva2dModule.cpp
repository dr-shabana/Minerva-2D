// This file is part of PyMinerva, Minerva' Python scripting plugin.
//
// SPDX-FileCopyrightText: 2006 Paul Giannaros <paul@giannaros.org>
// SPDX-FileCopyrightText: 2012, 2013 Shaheed Haque <srhaque@theiet.org>
// SPDX-FileCopyrightText: 2013 Alex Turbov <i.zaufi@gmail.com>
// SPDX-FileCopyrightText: 2021 L. E. Segovia <amy@amyspark.me>
//
// SPDX-License-Identifier: LGPL-2.1-only OR LGPL-3.0-only OR LicenseRef-KDE-Accepted-LGPL
//

#include "Pyminerva2dModule.h"

#include "kis_debug.h"

struct module_state {
    PyObject *error;
};

#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))

/// \note Namespace name written in uppercase intentionally!
/// It will appear in debug output from Python plugins...
namespace PYKRITA
{
    PyObject* debug(PyObject* /*self*/, PyObject* args)
    {
        const char* text;

        if (PyArg_ParseTuple(args, "s", &text))
            dbgScript << text;
        Py_INCREF(Py_None);
        return Py_None;
    }

    PyObject* qt_major_version(PyObject* /*self*/, PyObject* args)
    {
        Q_UNUSED(args);
        return PyLong_FromLong(QT_VERSION_MAJOR);
    }
}                                                           // namespace PYKRITA

namespace
{
    PyMethodDef pyminerva2dMethods[] = {
        {
            "qDebug"
            , &PYKRITA::debug
            , METH_VARARGS
            , "True KDE way to show debug info"
        }
        , {
            "qt_major_version"
            , &PYKRITA::qt_major_version
            , METH_VARARGS
            , "Qt major version number"
        }
        , { 0, 0, 0, 0 }
    };
}                                                           // anonymous namespace

//BEGIN Python module registration
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT
    , "pyminerva2d"
    , "The pyminerva2d module"
    , -1
    , pyminerva2dMethods
    , 0
    , 0
    , 0
    , 0
};

#define INITERROR return NULL

PyMODINIT_FUNC PYMINERVA2D_INIT()
{
    PyObject *pyminerva2dModule = PyModule_Create(&moduledef);

    if (pyminerva2dModule == NULL)
        INITERROR;

    PyModule_AddStringConstant(pyminerva2dModule, "__file__", __FILE__);

    return pyminerva2dModule;
}

//END Python module registration

// krita: space-indent on; indent-width 4;
#undef PYMINERVA2D_INIT
