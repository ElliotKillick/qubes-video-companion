#!/bin/bash

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

local_dir="$(dirname "$(readlink -f "$0")")"
cd "$local_dir" || exit # Change into directory of this script

# Author PGP key initial source
#gpg --keyserver keys.openpgp.org --recv-keys 018FB9DE6DFA13FB18FB5552F9B90D44F83DD5F2

gpg --import author.asc

cd .. || exit

latest_version_tag="$(git describe --abbrev=0)"

# Fix "gpg.program=qubes-gpg-client-wrapper" causing "git verify-tag" to fail in cases where Qubes Split GPG is in use
# Set "gpg.program=gpg" locally for this repo
git config gpg.program gpg

if ! git verify-tag "$latest_version_tag"; then
    echo "Failed to verify Qubes Video Companion author PGP key!" >&2
    exit 1
fi
git checkout "$latest_version_tag"

#latest_version="$(echo "$latest_version_tag" | tr -d v)"
latest_version="1.0.0" # Temporary until versions are updated in package metadata

cd .. || exit
tar cvzf "qubes-video-companion_$latest_version.orig.tar.gz" qubes-video-companion
sudo apt-get -y install devscripts pandoc
cd qubes-video-companion || exit
debuild || true
debuild -- clean

echo "Run the following command one directory up from the qubes-video-companion directory to install the package: sudo apt install ./qubes-video-companion_$latest_version-1_all.deb" >&2
