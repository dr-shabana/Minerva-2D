/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2006 Cyrille Berger <cberger@cberger.net>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef COLORS_H
#define COLORS_H

#include <QObject>
#include <QVariant>

class MinervaExtensionsColors : public QObject
{
    Q_OBJECT
public:
    MinervaExtensionsColors(QObject *parent, const QVariantList &);
    ~MinervaExtensionsColors() override;
};

#endif
