#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

# shellcheck source=common.sh
source /usr/share/qubes-video-companion/video/common.sh

if ! test_v4l2loopback; then
    exit 1
fi

# "videodev" is the Video4Linux (V4L) driver (V4L2 is the second version of V4L)
until sudo modprobe -r v4l2loopback videodev; do
    message="Please close any window that has an open video stream so kernel modules can be securely unloaded..."
    echo "$message" >&2
    notify-send "Qubes Video Companion" "$message"

    sleep 10
done
