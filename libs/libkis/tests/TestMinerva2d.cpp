/* SPDX-FileCopyrightText: 2017 Boudewijn Rempt <boud@valdyas.org>

   SPDX-License-Identifier: LGPL-2.0-or-later
*/
#include "TestMinerva.h"
#include <QTest>

#include <MinervaVersionWrapper.h>
#include <Minerva.h>
#include <Window.h>
#include <Document.h>

#include <testui.h>

void TestMinerva::initTestCase()
{
    Minerva::instance();
}

void TestMinerva::testMinerva()
{
    Minerva *krita = Minerva::instance();
    QVERIFY2(krita, "Could not create krita instance.");
    QCOMPARE(minerva2d->batchmode(), false);
    minerva2d->setBatchmode(true);
    QCOMPARE(minerva2d->batchmode(), true);

    QVERIFY(minerva2d->filters().size() > 0);
    QVERIFY(minerva2d->filter(minerva2d->filters().first()) != 0);

    //QVERIFY(minerva2d->generators().size() > 0);
    //QVERIFY(minerva2d->generator(minerva2d->generators().first()) != 0);

    QStringList profiles = minerva2d->profiles("RGBA", "U8");
    QVERIFY(profiles.size() != 0);
    Document *doc = minerva2d->createDocument(100, 100, "test", "RGBA", "U8", profiles.first());
    QVERIFY(doc);
    QCOMPARE(minerva2d->documents().size(), 1);


}

void TestMinerva::cleanupTestCase()
{
    if (m_win) {
        m_win->close();
    }
    QTest::qWait(1000);
}


KISTEST_MAIN(TestMinerva)

