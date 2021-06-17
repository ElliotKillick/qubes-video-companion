#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

"""Webcam video source module"""

import sys
import re
import subprocess
from service import Service

class Webcam(Service):
    """Webcam video source class"""

    def __init__(self):
        self.main(self)

    def video_source(self) -> str:
        return 'webcam'

    def icon(self) -> str:
        return 'camera-web'

    def parameters(self):
        mjpeg_re = re.compile(rb"\t\[[0-9]+]: 'MJPG' \(Motion-JPEG, compressed\)\Z")
        fmt_re = re.compile(rb"\t\[[0-9]+]: ")
        dimensions_re = re.compile(rb"\t\tSize: Discrete [0-9]+x[0-9]+\Z")
        interval_re = re.compile(rb"\t\t\tInterval: Discrete [0-9.]+s \([0-9]+\.0+ fps\)\Z")
        proc = subprocess.run(('v4l2-ctl', '--list-formats-ext'),
                              stdout=subprocess.PIPE,
                              check=True,
                              env={'PATH': '/bin:/usr/bin', 'LC_ALL': 'C'})
        emit = False
        formats = []
        for i in proc.stdout.split(b'\n'):
            if mjpeg_re.match(i):
                emit = True
            elif fmt_re.match(i):
                emit = False
            elif dimensions_re.match(i):
                width, height = map(int, i[17:].split(b'x'))
            elif interval_re.match(i):
                fps = int(i[22:].split(b'(', 1)[1].split(b'.', 1)[0])
                formats.append((width, height, fps))
            elif i in (b'', b'ioctl: VIDIOC_ENUM_FMT', b'\tType: Video Capture'):
                continue
            else:
                print('Cannot parse output %r of v4l2ctl' % i, file=sys.stderr)
        formats.sort(key=lambda x: x[0] * x[1] * x[2], reverse=True)
        return formats[0]

    def pipeline(self, width: int, height: int, fps: int):
        caps = ('width={0},'
                'height={1},'
                'framerate={2}/1,'
                'format=I420,'
                'interlace-mode=progressive,'
                'pixel-aspect-ratio=1/1,'
                'max-framerate={2}/1,'
                'views=1'.format(width, height, fps))
        return [
            'v4l2src',
            '!',
            'queue',
            '!',
            'capsfilter',
            'caps=image/jpeg,colorimetry=(string)2:4:7:1,chroma-site=none,' + caps,
            '!',
            'jpegdec',
            '!',
            'capsfilter',
            'caps=video/x-raw,' + caps,
            '!',
            'fdsink',
        ]

if __name__ == '__main__':
    webcam = Webcam()
