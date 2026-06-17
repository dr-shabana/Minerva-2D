/*
 *  SPDX-FileCopyrightText: 2018 Victor Wåhlström <victor.wahlstrom@initiali.se>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "MinervaDesignerPluginCollection.h"

#include "KisColorSpaceSelectorPlugin.h"

MinervaDesignerPluginCollection::MinervaDesignerPluginCollection(QObject *parent)
    : QObject(parent)
{
    m_widgets.append(new KisColorSpaceSelectorPlugin(this));
}

QList<QDesignerCustomWidgetInterface*> MinervaDesignerPluginCollection::customWidgets() const
{
    return m_widgets;
}
