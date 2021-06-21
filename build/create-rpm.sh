#!/bin/bash

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

if [ "$1" == "dom0" ]; then
    echo "To build for Qubes R4.0 dom0 ensure that this script is running in a Fedora 25 AppVM (the same version as dom0)!" >&2
    echo "Install the Fedora 25 template in dom0 by running this command: sudo qubes-dom0-update qubes-template-fedora-25" >&2
    package_type="dom0"
fi

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
cp -r qubes-video-companion "qubes-video-companion-$latest_version"
tar cvzf "qubes-video-companion-$latest_version.tar.gz" "qubes-video-companion-$latest_version"
sudo dnf -y install rpm-build rpmdevtools pandoc
rpmdev-setuptree
cp "qubes-video-companion-$latest_version.tar.gz" "$HOME/rpmbuild/SOURCES"
cp qubes-video-companion/rpm_spec/* "$HOME/rpmbuild/SPECS"

if [ "$package_type" != "dom0" ]; then
    cp qubes-video-companion/rpm_spec/qubes-video-companion.spec.in "$HOME/rpmbuild/SPECS"
    rpmbuild -ba ~/rpmbuild/SPECS/qubes-video-companion.spec.in
    echo "Run the following command to install the package: sudo dnf install ~/rpmbuild/RPMS/noarch/qubes-video-companion-$latest_version-1.fcXX.noarch.rpm" >&2
else
    cp qubes-video-companion/rpm_spec/qubes-video-companion.spec.in "$HOME/rpmbuild/SPECS"
    rpmbuild -ba ~/rpmbuild/SPECS/qubes-video-companion-dom0.spec.in
    echo "Transfer this package to dom0 and install, see here: https://www.qubes-os.org/doc/how-to-copy-from-dom0/" >&2
    echo "In dom0, run the following command to install the package: sudo dnf install ./qubes-video-companion-$latest_version-1.fcXX.noarch.rpm" >&2
fi
