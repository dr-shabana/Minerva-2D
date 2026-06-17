/*
 *  SPDX-FileCopyrightText: 2009 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: LGPL-2.0-or-later
 */

#include "LayerDocker.h"


#include <kpluginfactory.h>

#include <KoDockFactoryBase.h>
#include <KoDockRegistry.h>
#include "kis_debug.h"

#include "LayerBox.h"

K_PLUGIN_FACTORY_WITH_JSON(MinervaLayerDockerPluginFactory, "kritalayerdocker.json", registerPlugin<MinervaLayerDockerPlugin>();)

MinervaLayerDockerPlugin::MinervaLayerDockerPlugin(QObject *parent, const QVariantList &)
        : QObject(parent)
{
    KoDockRegistry::instance()->add(new LayerBoxFactory());
}

MinervaLayerDockerPlugin::~MinervaLayerDockerPlugin()
{
}

#include "LayerDocker.moc"
