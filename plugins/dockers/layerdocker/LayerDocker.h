/*
 *  SPDX-FileCopyrightText: 2009 Boudewijn Rempt <boud@valdyas.org>
 *
 *  SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef _DEFAULT_DOCKERS_H
#define _DEFAULT_DOCKERS_H

#include <QObject>
#include <QVariant>


/**
 * Template of view plugin
 */
class MinervaLayerDockerPlugin : public QObject
{
    Q_OBJECT
public:
    MinervaLayerDockerPlugin(QObject *parent, const QVariantList &);
    ~MinervaLayerDockerPlugin() override;

};

#endif
