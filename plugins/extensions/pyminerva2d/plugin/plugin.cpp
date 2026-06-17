/*
 * SPDX-FileCopyrightText: 2014 Boudewijn Rempt (boud@valdyas.org)
 *
 *  SPDX-License-Identifier: LGPL-2.0-only
 */

#include "plugin.h"

#include <klocalizedstring.h>
#include <kis_debug.h>
#include <kpluginfactory.h>

#include <kis_preference_set_registry.h>
#include "pyqtpluginsettings.h"

#include <QCoreApplication>

#include <Minerva.h>

K_PLUGIN_FACTORY_WITH_JSON(MinervaPyQtPluginFactory, "kritapyminerva2d.json", registerPlugin<MinervaPyQtPlugin>();)

MinervaPyQtPlugin::MinervaPyQtPlugin(QObject *parent, const QVariantList &)
    : QObject(parent)
    , m_autoReload(false)
{
    dbgScript << "Loading Python plugin";

    PyMinerva::InitResult initResult = PyMinerva::initialize();
    switch (initResult) {
        case PyMinerva::INIT_OK:
            break;
        case PyMinerva::INIT_CANNOT_LOAD_PYTHON_LIBRARY:
            qWarning() << i18n("Cannot load Python library");
            return;
        case PyMinerva::INIT_CANNOT_SET_PYTHON_PATHS:
            qWarning() << i18n("Cannot set Python paths");
            return;
        case PyMinerva::INIT_CANNOT_LOAD_PYMINERVA2D_MODULE:
            qWarning() << i18n("Cannot load built-in pyminerva2d module");
            return;
        default:
            qWarning() << i18n("Unexpected error initializing python plugin.");
            return;
    }

    pluginManager = PyMinerva::pluginManager();

    KisPreferenceSetRegistry *preferenceSetRegistry = KisPreferenceSetRegistry::instance();
    PyQtPluginSettingsFactory* settingsFactory = new PyQtPluginSettingsFactory(pluginManager);

    //load and save preferences
    //if something in minerva2drc is missing, then the default from this load function will be used and saved back to kconfig.
    //this way, cfg.readEntry() in any part won't be able to set its own default
    KisPreferenceSet* settings = settingsFactory->createPreferenceSet();
    KIS_SAFE_ASSERT_RECOVER_RETURN(settings);
    settings->loadPreferences();
    settings->savePreferences();
    delete settings;

    preferenceSetRegistry->add("PyQtPluginSettingsFactory", settingsFactory);

    // Try to import the `pyminerva2d` module
    PyMinerva::Python py = PyMinerva::Python();
    PyObject* pyminerva2dPackage = py.moduleImport("pyminerva2d");
    pyminerva2dPackage = py.moduleImport("krita");

    if (pyminerva2dPackage) {
        dbgScript << "Loaded pyminerva2d, now load plugins";
        pluginManager->scanPlugins();
        pluginManager->tryLoadEnabledPlugins();
        //py.functionCall("_pyminerva2dLoaded", PyMinerva::Python::PYMINERVA2D_ENGINE);
    } else  {
        dbgScript << "Cannot load pyminerva2d module";
    }

    Q_FOREACH (Extension *extension, Minerva::instance()->extensions()) {
        extension->setup();
    }

    // This ensures that QObject's owned by Python are destructed before
    // the destructor of QCoreApplication is called, in order to prevent
    // a crash on exit.
    // See https://github.com/dr-shabana/Minerva-2D/issues/show_bug.cgi?id=417465
    // XXX: Commented out because this still can cause crashes:
    // https://invent.kde.org/graphics/minerva2d/-/commit/a0c29913114164ff3f2ba4e255ccee1c52cb3e86#note_260688
    // connect(QCoreApplication::instance(), &QCoreApplication::aboutToQuit, this, []() { PyMinerva::finalize(); });
}

MinervaPyQtPlugin::~MinervaPyQtPlugin()
{
    // Don't call PyMinerva::finalize here, because that can result in a crash
    // deep inside Qt.
}

#include "plugin.moc"
