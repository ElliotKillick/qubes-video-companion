#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

# Run this in the VM with the webcam device attached

# Fix V4L2 webcam settings if it changes
# This changed the resolution to 1920x1080 which is the highest my webcam can do
#   - How to find the highest resolution a webcam is capable of?
# This also sets the webcam output format to MJPG which is the most widely supported and best performing one (in terms of latency)
# Why do these settings change by themselves sometimes?
#   - It happens sometimes upon plugging in and out my webcam, restarting my computer, reloading V4l2 related kernel modules etc.
# More research needed

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

webcam_device="/dev/video0"

print_all_webcam_info() {
    v4l2-ctl -d "$webcam_device" --all || [ $? == 255 ] # Ignore 255 error code because this command returns 255 even though no error is reported for an unknown reason (research required)
}

echo "Previous V4L2 device information:" >&2
print_all_webcam_info

# Replace width and height with the highest dimensions your webcam is capable of outputting
v4l2-ctl -d "$webcam_device" --set-fmt-video=pixelformat=MJPG,width=1920,height=1080

echo -e "\nNew V4L2 device information:" >&2
print_all_webcam_info
