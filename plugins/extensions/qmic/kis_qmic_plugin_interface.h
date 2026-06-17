/*
 * This file is part of Minerva
 *
 * SPDX-FileCopyrightText: 2020 L. E. Segovia <amy@amyspark.me>
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef MINERVA2D_GMIC_PLUGIN_INTERFACE
#define MINERVA2D_GMIC_PLUGIN_INTERFACE

#include <memory>
#include <QObject>

#include "kis_qmic_interface.h"
#include "kritaqmicinterface_export.h"

#define MINERVA2D_GMIC_PLUGIN_INTERFACE_IID "org.kde.minerva2d.MinervaGmicPluginInterface"

class KRITAQMICINTERFACE_EXPORT KisQmicPluginInterface
{
public:
  KisQmicPluginInterface();
  virtual ~KisQmicPluginInterface();
  virtual int launch(std::shared_ptr<KisImageInterface> iface, bool headless = false) = 0;
};

Q_DECLARE_INTERFACE(KisQmicPluginInterface, MINERVA2D_GMIC_PLUGIN_INTERFACE_IID)

#endif
