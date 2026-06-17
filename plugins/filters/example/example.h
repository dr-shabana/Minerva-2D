/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2004 Cyrille Berger <cberger@cberger.net>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef EXAMPLE_H
#define EXAMPLE_H

#include <QObject>
#include <QVariant>
#include "filter/kis_color_transformation_filter.h"

class MinervaExample : public QObject
{
    Q_OBJECT
public:
    MinervaExample(QObject *parent, const QVariantList &);
    ~MinervaExample() override;
};

class KisFilterInvert : public KisColorTransformationFilter
{
public:
    KisFilterInvert();
public:

    KoColorTransformation* createTransformation(const KoColorSpace* cs, const KisFilterConfigurationSP config) const override;

    static inline KoID id() {
        return KoID("invert", i18n("Invert"));
    }

    bool needsTransparentPixels(const KisFilterConfigurationSP config, const KoColorSpace *cs) const override;
};

#endif
