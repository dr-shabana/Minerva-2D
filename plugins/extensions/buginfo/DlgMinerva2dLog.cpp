/*
 * SPDX-FileCopyrightText: 2017 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "DlgMinervaLog.h"
#include <QStandardPaths>

DlgMinervaLog::DlgMinervaLog(QWidget *parent)
    : DlgBugInfo(parent)
{
    initialize();
}

QString DlgMinervaLog::originalFileName()
{
    return QStandardPaths::writableLocation(QStandardPaths::GenericDataLocation) + "/minerva2d.log";
}

QString DlgMinervaLog::captionText()
{
    return i18nc("Caption of the dialog with Minerva usage log for bug reports", "Minerva Usage Log: please paste this information to the bug report");
}

QString DlgMinervaLog::replacementWarningText()
{
    return "WARNING: The Minerva usage log file doesn't exist.";
}

DlgMinervaLog::~DlgMinervaLog()
{

}
