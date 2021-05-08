#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

"""Main service class for video sources"""

# GI requires version declaration before importing
# pylint: disable=wrong-import-position

import gi
import struct
import sys
import tray_icon
import notification
from typing import Optional, NoReturn

gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

class Service(object):
    _quitting: bool
    _element: Optional[Gst.Element]
    _tray_icon: tray_icon.TrayIcon
    __slots__: tuple[str, str, str] = ('_quitting', '_tray_icon', '_element')

    """Qubes Video Companion service base class"""
    def __init__(self, target_domain: str, remote_domain: str):
        self._quitting = False
        self._element = None
        icon = self.icon()
        notification_ui = notification.Notification()
        self._tray_icon = tray_icon_ui = tray_icon.TrayIcon(icon)

        notification_ui.video_source = self.video_source()
        notification_ui.requested_target = target_domain
        notification_ui.remote_domain = remote_domain
        notification_ui.show(icon)

        tray_icon_ui.video_source = self.video_source()
        tray_icon_ui.requested_target = target_domain
        tray_icon_ui.remote_domain = remote_domain
        tray_icon_ui.create()
        tray_icon_ui.show()

    def video_source(self) -> str:
        """
        Returns the video source
        """
        raise NotImplementedError("Pure virtual method called!")

    def icon(self) -> str:
        """
        Returns the icon name
        """
        raise NotImplementedError("Pure virtual method called!")

    def pipeline(self, width: int, height: int, fps: int) -> list[str]:
        """
        Return a set-up GStreamer pipeline
        """
        raise NotImplementedError("Pure virtual method called!")

    def parameters(self) -> list[int, int, int]:
        """
        Compute the parameters.  Return a (width, height, fps) tuple.
        """
        raise NotImplementedError('parameters')

    def quit(self) -> None:
        if self._quitting:
            return
        self._quitting = True
        self._element.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def msg_handler(self, bus: Gst.Bus, msg: Gst.Message) -> None:
        elemnt = self._element
        if msg.type == Gst.MessageType.EOS:
            print('End of stream, exiting', file=sys.stderr)
            self.quit()
        elif msg.type == Gst.MessageType.ERROR:
            print('Fatal error:', msg.parse_error(), file=sys.stderr)
            self.quit()
        elif msg.type == Gst.MessageType.CLOCK_LOST:
            print('Clock lost, resetting', file=sys.stderr)
            element.set_state(Gst.State.PAUSED)
            element.set_state(Gst.State.PLAYING)

    def start_transmission(self) -> None:
        """
        Start video transmission
        """
        width, height, fps = self.parameters()
        sys.stdout.buffer.write(struct.pack('=HHH', width, height, fps))
        sys.stdout.buffer.flush()
        Gst.init()
        element = self._element = Gst.parse_launchv(self.pipeline(width, height, fps))
        bus = element.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.msg_handler)
        element.set_state(Gst.State.PLAYING)

    @classmethod
    def main(self) -> NoReturn:
        """Program entry point"""

        import argparse, re, qubesdb, os
        argparse.ArgumentParser().parse_args()

        qube_re = re.compile('^[A-Za-z][A-Za-z0-9_-]{1,30}$')
        target_domain = qubesdb.QubesDB().read('/name').decode('ascii', 'strict')
        remote_domain = os.getenv('QREXEC_REMOTE_DOMAIN')
        if not qube_re.match(target_domain):
            print('Invalid target qube name %r, failing' % target_domain,
                  file=sys.stderr)
            sys.exit(1)
        if not qube_re.match(remote_domain):
            print('Invalid remote qube name %r, failing' % remote_domain,
                  file=sys.stderr)
            sys.exit(1)
        s = self(target_domain, remote_domain)
        s.start_transmission()
        Gtk.main()
