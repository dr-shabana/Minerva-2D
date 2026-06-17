/*
 * This file is part of PyMinerva, Minerva' Python scripting plugin.
 *
 * SPDX-FileCopyrightText: 2013 Alex Turbov <i.zaufi@gmail.com>
 * SPDX-FileCopyrightText: 2014-2016 Boudewijn Rempt <boud@valdyas.org>
 * SPDX-FileCopyrightText: 2021 L. E. Segovia <amy@amyspark.me>
 *
 * SPDX-License-Identifier: LGPL-2.0-only OR LGPL-3.0-only
 */

#ifndef __PYMINERVA2D_MODULE_H__
#define  __PYMINERVA2D_MODULE_H__

#include <Python.h>
#include "config.h"

#if SIP_VERSION >= 0x0500000
#define PYMINERVA2D_INIT PyInit_krita
#else
#define PYMINERVA2D_INIT PyInit_pyminerva2d
#endif

/**
 * Initializer for the built-in Python module.
 */
PyMODINIT_FUNC PYMINERVA2D_INIT();

#endif
