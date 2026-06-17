/*
 *  SPDX-FileCopyrightText: 2015 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "WidgetUtilsDebug.h"

const QLoggingCategory &KRITAWIDGETUTILS_LOG()
{
    static const QLoggingCategory category("minerva2d.lib.widgetutils", QtInfoMsg);
    return category;
}


