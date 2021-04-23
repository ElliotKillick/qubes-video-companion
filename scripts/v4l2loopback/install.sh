#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

# Fedora requires this due to there being no v4l2loopback package because it's a kernel module
# https://fedoraproject.org/wiki/Package_maintainers_wishlist?rd=PackageMaintainers/WishList#T-W
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/XPNXY6RYUPBDF5STIBQVLGRWNJ6AYKO7/#DWPK323DNTKDH7SDPQGNDSKBIEQKRKN4

# Debian (stable) also requires this because the package provided is very out-of-date and doesn't even install correctly (whereas later versions do)

[ "$DEBUG" == 1 ] && set -x

clone_dir="/tmp"

exit_clean() {
    exit_code="$?"

    rm -rf "$clone_dir/v4l2loopback"

    exit "$exit_code"
}

set -E # Enable function inheritance of traps
trap exit_clean EXIT
trap exit ERR

local_dir="$(dirname "$(readlink -f "$0")")"

# Package dependencies installed by package manager

# Author PGP key initial source
#gpg --keyserver keyring.debian.org --recv-keys 7405E745574809734800156DB65019C47F7A36F8

gpg --import "$local_dir/author.asc"

cd "$clone_dir" || exit
git clone https://github.com/umlaeute/v4l2loopback
cd v4l2loopback || exit

latest_version_tag="$(git describe --abbrev=0)"

# Fix "gpg.program=qubes-gpg-client-wrapper" causing "git verify-tag" to fail in cases where Qubes Split GPG is in use
# Set "gpg.program=gpg" locally for this repo
git config gpg.program gpg

if ! git verify-tag "$latest_version_tag"; then
    echo "Failed to verify v4l2loopback author PGP key!" >&2
    exit 1
fi
git checkout "$latest_version_tag"

make
sudo make install
