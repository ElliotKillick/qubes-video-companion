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
import sys

class ScreenShare(Service):
    """Screen sharing video souce class"""
    _share_specific_screen = None
    def __init__(self):
        self.main(self)

    def video_source(self) -> str:
        return 'screenshare'

    def icon(self) -> str:
        return 'video-display'

    def get_specific_monitor(self, monitor_id):
        amount_of_monitors = Gdk.Display().get_default().get_n_monitors()
        if monitor_id >= amount_of_monitors:
            return None

        return Gdk.Display().get_default().get_monitor(monitor_id)

    def parse_args(self):
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('screen', type=int, nargs='?', default=None, help='id of the screen to share')

        args = parser.parse_args()
        self._share_specific_screen = args.screen

    def parameters(self):
        if self._share_specific_screen != None:
            monitor = self.get_specific_monitor(self._share_specific_screen)
            if not monitor:
                raise RuntimeError("requested screen to share does not exist")

            scale, geometry = monitor.get_scale_factor(), monitor.get_geometry()
            return (scale * geometry.width, scale * geometry.height, 30)

        else:
            screen = Gdk.Display().get_default().get_default_screen()
            return (screen.width(), screen.height(), 30)

    def pipeline(self, width: int, height: int, fps: int):
        caps = ('width={0},'
                'height={1},'
                'framerate={2}/1,'
                'interlace-mode=progressive,'
                'pixel-aspect-ratio=1/1,'
                'max-framerate={2}/1,'
                'views=1'.format(width, height, fps))
        args = [
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
        if self._share_specific_screen != None:
            monitor = self.get_specific_monitor(self._share_specific_screen)
            if not monitor:
                raise RuntimeError("requested screen to share does not exist")
            geometry = monitor.get_geometry()
            
            args.insert(1, "startx={}".format(geometry.x))
            args.insert(2, "starty={}".format(geometry.y))
            args.insert(3, "endx={}".format(geometry.x+geometry.width-1))
            args.insert(4, "endy={}".format(geometry.y+geometry.height-1))
        
        print(" ".join(args))
        return args

if __name__ == '__main__':
    screenshare = ScreenShare()
