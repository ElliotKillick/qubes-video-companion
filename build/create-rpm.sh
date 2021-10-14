#!/bin/bash

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
set -euo pipefail # Error checking
trap exit ERR

package_type="${1-vm}"
case $package_type in
(dom0)
    echo "To build for Qubes R4.0 dom0 ensure that this script is running in a Fedora 25 AppVM (the same version as dom0)!" >&2
    echo "Install the Fedora 25 template in dom0 by running this command: sudo qubes-dom0-update qubes-template-fedora-25" >&2;;
(vm) :;;
(*) printf 'Bad package type %q (must be "dom0" or "vm")\n' "$package_type" >&2; exit 1;;
esac

case $0 in
(/*) local_dir=${0%/*}/;;
(*/*) local_dir=./${0%/*};;
(*) local_dir=.;;
esac
cd "$local_dir" || exit # Change into directory of this script
pwd

# Author PGP key initial source
#gpg --keyserver keys.openpgp.org --recv-keys 018FB9DE6DFA13FB18FB5552F9B90D44F83DD5F2
author_fpr=018FB9DE6DFA13FB18FB5552F9B90D44F83DD5F2
gpg --import author.asc

cd .. || exit

version_tag=$(git describe --abbrev=0)
expected_hash=$(git rev-parse -q --verify --end-of-options "refs/tags/$version_tag^{tag}")

hash_len=${#expected_hash}
if [ "$hash_len" -ne 40 ] && [ "$hash_len" -ne 64 ]; then
    echo "---> Bad Git hash value (wrong length); failing" >&2
    exit 1
elif ! [[ "$expected_hash" =~ ^[a-f0-9]+$ ]]; then
    echo "---> Bad Git hash value (bad character); failing" >&2
    exit 1
fi

verify_git_obj () {
    local content newsig_number
    content=$(git -c gpg.program=gpg "verify-$1" --raw -- "$2" 2>&1 >/dev/null) &&
    newsig_number=$(printf %s\\n "$content" | grep -c '^\[GNUPG:] NEWSIG') &&
    [ "$newsig_number" = 1 ] && {
        printf %s\\n "$content" |
        grep -q "^\\[GNUPG:] VALIDSIG $author_fpr "
    }
}

if verify_git_obj tag "$expected_hash"; then
    echo "---> Good tag $expected_hash\n"
elif [ "0$VERBOSE" -ge 1 ]; then
    echo "---> Signed tag $expected_hash cannot be verified"
    exit 1
fi

git checkout "$expected_hash^{commit}"
#latest_version="$(echo "$latest_version_tag" | tr -d v)"
latest_version='1.0.0' # Temporary until versions are updated in package metadata
pkg_name=qubes-video-companion-$latest_version
if :; then
    git archive --format=tar.gz "--output=$pkg_name.tar.gz" "--prefix=$pkg_name/"  -- "$expected_hash^{commit}"
else
    escaped_version=${pkg_name//\\/\\\\}
    escaped_version=${escaped_version//&/\\&}
    git ls-files -z |
    tar --null -czf "$pkg_name.tar.gz" \
        --transform "s,^,${escaped_version//,/\\,}/," -T -
fi
#sudo dnf -y install rpm-build rpmdevtools pandoc
rpmdev-setuptree
cp -- "$pkg_name.tar.gz" ~/rpmbuild/SOURCES

if [ "$package_type" != "dom0" ]; then
    cp rpm_spec/qubes-video-companion.spec.in "$HOME/rpmbuild/SPECS"
    rpmbuild -ba ~/rpmbuild/SPECS/qubes-video-companion.spec.in
    echo "Run the following command to install the package: sudo dnf install ~/rpmbuild/RPMS/noarch/$pkg_name-1.fcXX.noarch.rpm" >&2
else
    cp rpm_spec/qubes-video-companion-dom0.spec.in "$HOME/rpmbuild/SPECS"
    rpmbuild -ba ~/rpmbuild/SPECS/qubes-video-companion-dom0.spec.in
    echo "Transfer this package to dom0 and install, see here: https://www.qubes-os.org/doc/how-to-copy-from-dom0/" >&2
    echo "In dom0, run the following command to install the package: sudo dnf install ./$pkg_name-1.fcXX.noarch.rpm" >&2
fi
