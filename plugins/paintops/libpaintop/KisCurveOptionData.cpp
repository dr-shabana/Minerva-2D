/*
 *  SPDX-FileCopyrightText: 2022 Dmitry Kazakov <dimula73@gmail.com>
 *
 *  SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "KisCurveOptionData.h"

KisCurveOptionData::KisCurveOptionData(const QString &prefix,
                                       const KoID &id,
                                       Checkability checkability,
                                       std::optional<bool> isChecked,
                                       const std::pair<qreal, qreal> &valueRange)
    : KisCurveOptionDataCommon(prefix,
                               id,
                               checkability == Checkability::Checkable ||
                                   (checkability == Checkability::CheckableIfHasPrefix && !prefix.isEmpty()),
                               isChecked ? *isChecked : checkability == Checkability::NotCheckable,
                               valueRange.first,
                               valueRange.second,
                               new KisMinervaSensorPack(checkability))
{
}

KisCurveOptionData::KisCurveOptionData(const KoID &id,
                                       Checkability checkability,
                                       std::optional<bool> isChecked,
                                       const std::pair<qreal, qreal> &valueRange)
    : KisCurveOptionData("", id, checkability, isChecked, valueRange)
{
}

KisMinervaSensorData &KisCurveOptionData::sensorStruct()
{
    return dynamic_cast<KisMinervaSensorPack *>(sensorData.data())->sensorsStruct();
}

const KisMinervaSensorData &KisCurveOptionData::sensorStruct() const
{
    return dynamic_cast<const KisMinervaSensorPack*>(sensorData.constData())->constSensorsStruct();
}
