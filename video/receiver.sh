#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

read -r untrusted_width untrusted_height untrusted_fps

# Prevent injection of any additional capabilities to the GStreamer pipeline
# This also removes terminal escape sequences for printing to the terminal
sanitize_cap() {
    local cap_value="$1"

    # Allow only numbers
    echo "$cap_value" | tr -cd 0-9
}

width="$(sanitize_cap "$untrusted_width")"
height="$(sanitize_cap "$untrusted_height")"
fps="$(sanitize_cap "$untrusted_fps")"

if ! { [ "$width" ] || [ "$height" ] || [ "$fps" ]; }; then
    echo -e "Video sender failed to provide necessary parameters for video stream creation! Exiting..." >&2
    exit 1
fi

echo "Receiving video stream at ${width}x${height} ${fps} FPS..." >&2

frame_rate="$fps/1"

gst-launch-1.0 fdsrc ! \
    queue ! \
    capsfilter caps="video/x-raw,width=$width,height=$height,framerate=$frame_rate,format=I420,colorimetry=2:4:7:1,chroma-site=none,interlace-mode=progressive,pixel-aspect-ratio=1/1,max-framerate=$frame_rate,views=1" ! \
    rawvideoparse use-sink-caps=true ! \
    v4l2sink device=/dev/video0 sync=false
