/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2006 Cyrille Berger <cberger@cberger.net>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef WAVEFILTER_H
#define WAVEFILTER_H

#include <QObject>
#include <QVariant>
#include "filter/kis_filter.h"

class KisConfigWidget;

class MinervaWaveFilter : public QObject
{
    Q_OBJECT
public:
    MinervaWaveFilter(QObject *parent, const QVariantList &);
    ~MinervaWaveFilter() override;
};

class KisFilterWave : public KisFilter
{
public:

    KisFilterWave();

public:

    void processImpl(KisPaintDeviceSP device,
                     const QRect& applyRect,
                     const KisFilterConfigurationSP config,
                     KoUpdater* progressUpdater) const override;
    static inline KoID id() {
        return KoID("wave", i18n("Wave"));
    }

    KisFilterConfigurationSP defaultConfiguration(KisResourcesInterfaceSP resourcesInterface) const override;
public:
    QRect changedRect(const QRect& rect, const KisFilterConfigurationSP config = 0, int lod = 0) const override;
    QRect neededRect(const QRect& rect, const KisFilterConfigurationSP config = 0, int lod = 0) const override;

    KisConfigWidget * createConfigurationWidget(QWidget* parent, const KisPaintDeviceSP dev, bool useForMasks) const override;
};

#endif
