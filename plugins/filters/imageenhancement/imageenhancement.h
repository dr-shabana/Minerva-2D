/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2004 Cyrille Berger <cberger@cberger.net>
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef IMAGEENHANCEMENT_H
#define IMAGEENHANCEMENT_H

#include <QObject>
#include <QVariant>

class MinervaImageEnhancement : public QObject
{
    Q_OBJECT
public:
    MinervaImageEnhancement(QObject *parent, const QVariantList &);
    ~MinervaImageEnhancement() override;
};

#endif
