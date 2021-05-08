# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

import gi
from service import Service
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class ScreenShare(Service):
    def video_source(self) -> str:
        return 'screenshare'

    def icon(self) -> str:
        return 'video-display'

    def parameters(self) -> tuple[int, int, int]:
        monitor = Gdk.Display().get_default().get_monitor(0)
        scale, geometry = monitor.get_scale_factor(), monitor.get_geometry()
        return (scale * geometry.width, scale * geometry.height, 30)

    def pipeline(self, width: int, height: int, fps: int) -> list[str]:
        caps = ('width={},'
                'height={},'
                'framerate={}/1,'
                'interlace-mode=progressive,'
                'pixel-aspect-ratio=1/1,'
                'max-framerate={}/1,'
                'views=1'.format(width, height, fps, fps))
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
    ScreenShare.main()
