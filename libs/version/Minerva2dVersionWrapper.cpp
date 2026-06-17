/*
 *  SPDX-FileCopyrightText: 2015 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */
#include "MinervaVersionWrapper.h"

#include <minerva2dversion.h>
#include <kritagitversion.h>

QString MinervaVersionWrapper::versionString(bool checkGit)
{
    QString kritaVersion = QStringLiteral(MINERVA2D_VERSION_STRING);
    QString version = kritaVersion;

    if (checkGit) {
#ifdef MINERVA2D_GIT_SHA1_STRING
        QString gitVersion = QStringLiteral(MINERVA2D_GIT_SHA1_STRING);
        version = QStringLiteral("%1 (git %2)").arg(kritaVersion, gitVersion);
#endif
    }
    return version;
}

bool MinervaVersionWrapper::isDevelopersBuild()
{
    // Qt6 is not considered stable yet, don't present it as such.
#if defined(MINERVA2D_STABLE) && QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
    return false;
#else
    return true;
#endif
}
