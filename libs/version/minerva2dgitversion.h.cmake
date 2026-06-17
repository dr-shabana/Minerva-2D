/* This file is part of the KDE project
 * SPDX-FileCopyrightText: 2013 Dmitry Kazakov <dimula73@gmail.com>
 * SPDX-FileCopyrightText: 2014 Jarosław Staniek <staniek@kde.org>
 *
 * SPDX-License-Identifier: LGPL-2.0-or-later
 */

#ifndef __MINERVA2D_GIT_VERSION_H
#define __MINERVA2D_GIT_VERSION_H

/**
 * @def MINERVA2D_GIT_SHA1_STRING
 * @ingroup MinervaMacros
 * @brief Indicates the git sha1 commit which was used for compilation of Minerva
 */
#cmakedefine MINERVA2D_GIT_SHA1_STRING "@MINERVA2D_GIT_SHA1_STRING@"

/**
 * @def MINERVA2D_GIT_BRANCH_STRING
 * @ingroup MinervaMacros
 * @brief Indicates the git branch name which was used for compilation of Minerva
 */
#cmakedefine MINERVA2D_GIT_BRANCH_STRING "@MINERVA2D_GIT_BRANCH_STRING@"

/**
 * @def MINERVA2D_GIT_DESCRIBE_STRING
 * @ingroup MinervaMacros
 * @brief Indicates the git describe string
 */
#cmakedefine MINERVA2D_GIT_DESCRIBE_STRING "@MINERVA2D_GIT_DESCRIBE_STRING@"

#endif /* __MINERVA2D_GIT_VERSION_H */
