#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

# Fedora requires this due to there being no v4l2loopback package because it's a kernel module
# https://fedoraproject.org/wiki/Package_maintainers_wishlist?rd=PackageMaintainers/WishList#T-W
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/XPNXY6RYUPBDF5STIBQVLGRWNJ6AYKO7/#DWPK323DNTKDH7SDPQGNDSKBIEQKRKN4

# Debian (stable) also requires this because the package provided is very out-of-date and doesn't even install correctly (whereas later versions do)

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

local_dir="$(dirname "$(readlink -f "$0")")"

# Package dependencies installed by package manager

# Author PGP key initial source
#gpg --keyserver keyring.debian.org --recv-keys 7405E745574809734800156DB65019C47F7A36F8

gpg --import "$local_dir/author.asc"

cd /tmp || exit
git clone https://github.com/umlaeute/v4l2loopback
cd v4l2loopback || exit

latest_version_tag="$(git describe --abbrev=0)"
if ! git verify-tag "$latest_version_tag"; then
    echo "Failed to verify v4l2loopback author PGP key!" >&2
    exit 1
fi
git checkout "$latest_version_tag"

make
sudo make install

cd .. || exit
rm -rf v4l2loopback
