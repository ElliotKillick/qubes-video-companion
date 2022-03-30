#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

import os
import struct
import sys

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

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
    if not untrusted_input:
        raise RuntimeError('can not read from stream')
    if len(untrusted_input) != input_size:
        raise RuntimeError('wrong number of bytes read')
    untrusted_width, untrusted_height, untrusted_fps = s.unpack(untrusted_input)
    del untrusted_input

    screen = Gdk.Display().get_default().get_default_screen()
    if untrusted_width > screen.width() or untrusted_height > screen.height() or untrusted_fps > 4096:
        print('warning: excessive width, height, and/or fps')
    width, height, fps = untrusted_width, untrusted_height, untrusted_fps
    del untrusted_width, untrusted_height, untrusted_fps

    return width, height, fps

if __name__ == '__main__':
    main(sys.argv)
