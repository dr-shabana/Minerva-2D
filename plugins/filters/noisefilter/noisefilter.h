/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2006 Cyrille Berger <cberger@cberger.net>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef NOISEFILTER_H
#define NOISEFILTER_H

#include <QObject>
#include <QVariant>
#include "filter/kis_filter.h"

class KisConfigWidget;

class MinervaNoiseFilter : public QObject
{
    Q_OBJECT
public:
    MinervaNoiseFilter(QObject *parent, const QVariantList &);
    ~MinervaNoiseFilter() override;
};

class KisFilterNoise : public KisFilter
{
public:
    KisFilterNoise();
public:

    void processImpl(KisPaintDeviceSP device,
                     const QRect& applyRect,
                     const KisFilterConfigurationSP config,
                     KoUpdater* progressUpdater
                     ) const override;
    static inline KoID id() {
        return KoID("noise", i18n("Random Noise"));
    }
    KisFilterConfigurationSP defaultConfiguration(KisResourcesInterfaceSP resourcesInterface) const override;
    KisConfigWidget * createConfigurationWidget(QWidget* parent, const KisPaintDeviceSP dev, bool useForMasks) const override;
};

#endif
