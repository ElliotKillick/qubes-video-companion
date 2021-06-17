#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

import sys
import struct
import os
from typing import NoReturn

def main(argv) -> NoReturn:
    if len(argv) != 1:
        raise RuntimeError('should not have any arguments')

    width, height, fps = read_video_parameters()

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
        'width={0},'
        'height={1},'
        'framerate={2}/1,'
        'format=I420,'
        'colorimetry=2:4:7:1,'
        'chroma-site=none,'
        'interlace-mode=progressive,'
        'pixel-aspect-ratio=1/1,'
        'max-framerate={2}/1,'
        'views=1'.format(width, height, fps),
        '!',
        'rawvideoparse',
        'use-sink-caps=true',
        '!',
        'v4l2sink',
        'device=/dev/video0',
        'sync=false',
    ))

def read_video_parameters() -> (int, int, int):
    input_size = 6

    s = struct.Struct('=HHH')
    if s.size != input_size:
        raise AssertionError('bug')

    untrusted_input = os.read(0, input_size)
    if len(untrusted_input) != input_size:
        raise RuntimeError('wrong number of bytes read')
    untrusted_width, untrusted_height, untrusted_fps = s.unpack(untrusted_input)
    del untrusted_input

    if untrusted_width > 4096 or untrusted_height > 4096 or untrusted_fps > 4096:
        raise RuntimeError('excessive width, height, and/or fps')
    width, height, fps = untrusted_width, untrusted_height, untrusted_fps
    del untrusted_width, untrusted_height, untrusted_fps

    return width, height, fps

if __name__ == '__main__':
    main(sys.argv)
