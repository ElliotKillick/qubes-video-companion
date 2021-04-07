#!/bin/bash

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

# Generate visualizations from gst-launch-1.0 command outputted DOT files

# Only the PAUSED -> PLAYING edge GStreamer visualizations are kept in doc/visualizations because including all of them would result in a lot of redundant information and be overly verbose
# The PAUSED -> PLAYING edge was picked for display in the documentation because it shows what the GStreamer pipeline looks like when it is running

# Create DOT files by putting this in the video sender (Qubes RPC service) and receiver scripts:
# Get visualizations (Must create directory)
#export GST_DEBUG_DUMP_DOT_DIR="$HOME/visualizations"

# This script is not installed, it's just used in development for making the visualizations

[ "$DEBUG" == 1 ] && set -x

set -E # Enable function inheritance of traps
trap exit ERR

local_dir="$(dirname "$(readlink -f "$0")")"
doc_visualizations_dir="$(readlink -f "$local_dir/../doc/visualizations")"

cd "$local_dir/visualizations" || exit

for visualization in *; do
    # Filter out non-files and workaround shell issue of no files being present leading to the literal interprataion of * as a filename
    if [ -f "$visualization" ]; then
        dot -Tpdf "$visualization" > "$doc_visualizations_dir/${visualization%.*}.pdf"
    fi
done

rm -f ./*
