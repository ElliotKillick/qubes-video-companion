#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

# shellcheck source=common.sh
source /usr/share/qubes-video-companion/receiver/common.sh

if ! test_v4l2loopback; then
    echo "The v4l2loopback kernel module is not installed. Please run the following script to install it: /usr/share/qubes-video-companion/scripts/v4l2loopback/install.sh"
    exit 1
fi

# exclusive_caps=1: Some applications such as Cheese and Chromium won't detect the video device if it's set to zero
sudo modprobe v4l2loopback card_label="Qubes Video Companion" exclusive_caps=1

# For some reason, AppVMs based off my self-made "kali" qube (which itself is based off the "debian-10" TemplateVM) that are using the 5.x Qubes Linux kernel no longer has the user permitting ACL (or any ACL for that matter) on /dev/video* devices causing a permission error when attempting to write video to the device
# As a workaround, we set the ACL ourselves in case it isn't already applied
# This issue does not occur on the Fedora or Debian AppVMs using the 5.x Qubes Linux kernel, more research is required
sudo setfacl -m user:user:rw /dev/video0
