/* This file is part of the Minerva libraries
    SPDX-FileCopyrightText: 2003 David Faure <faure@kde.org>
    SPDX-FileCopyrightText: 2003 Lukas Tinkl <lukas@kde.org>
    SPDX-FileCopyrightText: 2004 Nicolas Goutte <goutte@kde.org>
    SPDX-FileCopyrightText: 2015 Jarosław Staniek <staniek@kde.org>

    SPDX-License-Identifier: LGPL-2.0-or-later
*/

#ifndef _MINERVA2D_VERSION_H_
#define _MINERVA2D_VERSION_H_

#include "minerva2dversion_export.h"

// -- WARNING: do not edit values below, instead edit MINERVA2D_* in /CMakeLists.txt --

/**
* @def MINERVA2D_VERSION_STRING
* @ingroup MinervaMacros
* @brief Version of Minerva as string, at compile time
*
* This macro contains the Minerva version in string form. As it is a macro,
* it contains the version at compile time.
*
* @note The version string might contain spaces and special characters,
* especially for development versions of Minerva.
* If you use that macro directly for a file format (e.g. OASIS Open Document)
* or for a protocol (e.g. http) be careful that it is appropriate.
* (Fictional) example: "3.0 Alpha"
*/
#define MINERVA2D_VERSION_STRING "@MINERVA2D_VERSION_STRING@"

/**
 * @def MINERVA2D_STABLE_VERSION_MAJOR
 * @ingroup MinervaMacros
 * @brief Major version of stable Minerva, at compile time
 * MINERVA2D_VERSION_MAJOR is computed based on this value.
*/
#define MINERVA2D_STABLE_VERSION_MAJOR @MINERVA2D_STABLE_VERSION_MAJOR@

/**
 * @def MINERVA2D_STABLE_VERSION_MINOR
 * @ingroup MinervaMacros
 * @brief Minor version of stable Minerva, at compile time
 * MINERVA2D_VERSION_MINOR is computed based on this value.
 */
#define MINERVA2D_STABLE_VERSION_MINOR @MINERVA2D_STABLE_VERSION_MINOR@

/**
 * @def MINERVA2D_VERSION_RELEASE
 * @ingroup MinervaMacros
 * @brief Release version of Minerva, at compile time.
 * 89 for Alpha.
 */
#define MINERVA2D_VERSION_RELEASE @MINERVA2D_VERSION_RELEASE@

/**
 * @def MINERVA2D_ALPHA
 * @ingroup MinervaMacros
 * @brief If defined (1..9), indicates at compile time that Minerva is in alpha stage
 */
#cmakedefine MINERVA2D_ALPHA @MINERVA2D_ALPHA@

/**
 * @def MINERVA2D_BETA
 * @ingroup MinervaMacros
 * @brief If defined (1..9), indicates at compile time that Minerva is in beta stage
 */
#cmakedefine MINERVA2D_BETA @MINERVA2D_BETA@

/**
 * @def MINERVA2D_RC
 * @ingroup MinervaMacros
 * @brief If defined (1..9), indicates at compile time that Minerva is in "release candidate" stage
 */
#cmakedefine MINERVA2D_RC @MINERVA2D_RC@

/**
 * @def MINERVA2D_STABLE
 * @ingroup MinervaMacros
 * @brief If defined, indicates at compile time that Minerva is in stable stage
 */
#cmakedefine MINERVA2D_STABLE @MINERVA2D_STABLE@

/**
 * @ingroup MinervaMacros
 * @brief Make a number from the major, minor and release number of a Minerva version
 *
 * This function can be used for preprocessing when MINERVA2D_IS_VERSION is not
 * appropriate.
 */
#define MINERVA2D_MAKE_VERSION( a,b,c ) (((a) << 16) | ((b) << 8) | (c))

/**
 * @ingroup MinervaMacros
 * @brief Version of Minerva as number, at compile time
 *
 * This macro contains the Minerva version in number form. As it is a macro,
 * it contains the version at compile time. See version() if you need
 * the Minerva version used at runtime.
 */
#define MINERVA2D_VERSION \
    MINERVA2D_MAKE_VERSION(MINERVA2D_STABLE_VERSION_MAJOR,MINERVA2D_STABLE_VERSION_MINOR,MINERVA2D_VERSION_RELEASE)

#endif // _MINERVA2D_VERSION_H_
