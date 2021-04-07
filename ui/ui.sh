#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

create_ui() {
    video_sender="$1"

    DISPLAY=:0 /usr/share/qubes-video-companion/ui/main.py -s "$video_sender" -t "$(hostname)" -r "$QREXEC_REMOTE_DOMAIN" &> /dev/null &
}

remove_ui() {
    pid="$1"

    if [ "$pid" ]; then
        kill "$pid"
    fi
}
