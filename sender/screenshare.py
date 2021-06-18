#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

"""Screen sharing video source module"""

# GI requires version declaration before importing
# pylint: disable=wrong-import-position

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from service import Service

class ScreenShare(Service):
    """Screen sharing video souce class"""

    def __init__(self):
        self.main(self)

    def video_source(self) -> str:
        return 'screenshare'

    def icon(self) -> str:
        return 'video-display'

    def parameters(self):
        monitor = Gdk.Display().get_default().get_monitor(0)
        scale, geometry = monitor.get_scale_factor(), monitor.get_geometry()
        return (scale * geometry.width, scale * geometry.height, 30)

    def pipeline(self, width: int, height: int, fps: int):
        caps = ('width={0},'
                'height={1},'
                'framerate={2}/1,'
                'interlace-mode=progressive,'
                'pixel-aspect-ratio=1/1,'
                'max-framerate={2}/1,'
                'views=1'.format(width, height, fps))
        return [
            'ximagesrc',
            'use-damage=false',
            '!',
            'queue',
            '!',
            'capsfilter',
            'caps=video/x-raw,format=BGRx,colorimetry=2:4:7:1,chroma-site=none,' + caps,
            '!',
            'videoconvert',
            '!',
            'capsfilter',
            'caps=video/x-raw,format=I420,colorimetry=2:4:7:1,chroma-site=none,' + caps,
            '!',
            'fdsink',
        ]

if __name__ == '__main__':
    screenshare = ScreenShare()
