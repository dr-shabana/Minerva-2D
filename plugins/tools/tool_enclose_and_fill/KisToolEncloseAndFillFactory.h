/*
 * KDE. Minerva Project.
 *
 * SPDX-FileCopyrightText: 2022 Deif Lou <ginoba@gmail.com>
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#ifndef KISTOOLENCLOSEANDFILLFACTORY_H
#define KISTOOLENCLOSEANDFILLFACTORY_H

#include <KisToolPaintFactoryBase.h>

#include "KisToolEncloseAndFill.h"

class KisToolEncloseAndFillFactory : public KisToolPaintFactoryBase
{

public:
    KisToolEncloseAndFillFactory()
        : KisToolPaintFactoryBase("KisToolEncloseAndFill")
    {
        setToolTip(i18n("Enclose and Fill Tool"));
        setSection(ToolBoxSection::Fill);
        setActivationShapeId(MINERVA2D_TOOL_ACTIVATION_ID);
        setIconName(koIconNameCStr("minerva2d_tool_enclose_and_fill"));
        setPriority(15);
    }

    ~KisToolEncloseAndFillFactory() override
    {}

    KoToolBase* createTool(KoCanvasBase *canvas) override
    {
        return new KisToolEncloseAndFill(canvas);
    }

};

#endif
