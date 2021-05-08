#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

import struct
import os
import sys

def main(argv):
    if len(argv) != 1:
        raise RuntimeError('should not have any arguments')
    s = struct.Struct('=HHH')
    if s.size != 6:
        raise AssertionError('bug')
    untrusted_input = os.read(0, 6)
    if len(untrusted_input) != 6:
        raise RuntimeError('wrong number of bytes read')
    untrusted_width, untrusted_height, untrusted_fps = s.unpack(untrusted_input)
    del untrusted_input
    if untrusted_width > 4096 or untrusted_height > 4096 or untrusted_fps > 4096:
        raise RuntimeError('excessive width, height, and/or fps')
    width, height, fps = untrusted_width, untrusted_height, untrusted_fps
    del untrusted_width, untrusted_height, untrusted_fps
    print('Receiving video stream at {}x{} {} FPS...'.format(width, height, fps),
          file=sys.stderr)
    os.execv('/usr/bin/gst-launch-1.0', (
        'gst-launch-1.0',
        'fdsrc',
        '!',
        'queue',
        '!',
        'capsfilter', 
        'caps=video/x-raw,'
        'width={},'
        'height={},'
        'framerate={}/1,'
        'format=I420,'
        'colorimetry=2:4:7:1,'
        'chroma-site=none,'
        'interlace-mode=progressive,'
        'pixel-aspect-ratio=1/1,'
        'max-framerate={}/1,'
        'views=1'.format(width, height, fps, fps),
        '!',
        'rawvideoparse',
        'use-sink-caps=true',
        '!',
        'v4l2sink',
        'device=/dev/video0',
        'sync=false',
    ))
if __name__ == '__main__':
    main(sys.argv)
