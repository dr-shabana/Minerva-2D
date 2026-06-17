/*
 * SPDX-FileCopyrightText: 2021 Alvin Wong <alvin@alvinhc.com>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

extern "C" {
    __declspec(dllimport) int minerva2d_main(int argc, char **argv);
}

int main(int argc, char **argv)
{
    return minerva2d_main(argc, argv);
}
