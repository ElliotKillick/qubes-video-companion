#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

# Test if v4l2loopback kernel module is installed
test_v4l2loopback() {
    # Prepend sbin directories to PATH because some distributions don't include it in the user profile by default
    PATH="/usr/local/sbin:/usr/sbin:/sbin:$PATH" modinfo v4l2loopback &> /dev/null
}
