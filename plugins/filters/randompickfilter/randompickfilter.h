/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2006 Cyrille Berger <cberger@cberger.net>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef RANDOMPICKFILTER_H
#define RANDOMPICKFILTER_H

#include <QObject>
#include <QVariant>
#include "filter/kis_filter.h"

class KisConfigWidget;

class MinervaRandomPickFilter : public QObject
{
    Q_OBJECT
public:
    MinervaRandomPickFilter(QObject *parent, const QVariantList &);
    ~MinervaRandomPickFilter() override;
};

class KisFilterRandomPick : public KisFilter
{
public:
    KisFilterRandomPick();
public:
    void processImpl(KisPaintDeviceSP device,
                     const QRect& applyRect,
                     const KisFilterConfigurationSP config,
                     KoUpdater* progressUpdater
                     ) const override;
    static inline KoID id() {
        return KoID("randompick", i18n("Random Pick"));
    }

    KisFilterConfigurationSP defaultConfiguration(KisResourcesInterfaceSP resourcesInterface) const override;
public:
    KisConfigWidget * createConfigurationWidget(QWidget* parent, const KisPaintDeviceSP dev, bool useForMasks) const override;

    QRect neededRect(const QRect& rect, const KisFilterConfigurationSP config, int lod = 0) const override;
    QRect changedRect(const QRect& rect, const KisFilterConfigurationSP config, int lod = 0) const override;
};

#endif
