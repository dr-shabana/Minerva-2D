/*
 * SPDX-FileCopyrightText: 2017 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef DLG_MINERVA2D_LOG
#define DLG_MINERVA2D_LOG

#include <KoDialog.h>
#include <dlg_buginfo.h>

class QSettings;

class DlgMinervaLog: public DlgBugInfo
{
    Q_OBJECT
public:
    DlgMinervaLog(QWidget * parent = 0);
    ~DlgMinervaLog() override;


    QString defaultNewFileName() override {
        return "MinervaUsageLog.txt";
    }

    QString originalFileName() override;

public:
    QString replacementWarningText() override;
    QString captionText() override;
};

#endif // DLG_BUGINFO
