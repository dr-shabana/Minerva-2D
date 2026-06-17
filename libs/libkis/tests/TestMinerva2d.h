/* This file is part of the KDE project
   SPDX-FileCopyrightText: 2017 Boudewijn Rempt

   SPDX-License-Identifier: LGPL-2.0-or-later
*/
#ifndef TESTMINERVA2D_H
#define TESTMINERVA2D_H

#include <QObject>
class Window;

class TestMinerva : public QObject
{
    Q_OBJECT
private Q_SLOTS:
    void initTestCase();
    void testMinerva();
    void cleanupTestCase();
private:
    Window *m_win {0};
};

#endif

