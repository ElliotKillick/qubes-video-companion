#!/usr/bin/python3 --

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Copyright (C) 2021 Demi Marie Obenour <demi@invisiblethingslab.com>
# Licensed under the MIT License. See LICENSE file for details.

"""Service module for video sources"""

# GI requires version declaration before importing
# pylint: disable=wrong-import-position

import sys
import struct
from typing import Optional, NoReturn

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, Gst, Notify

import tray_icon

class Service(object):
    """Qubes Video Companion service base class"""

    _quitting = None # type: bool
    _element = None # type: Optional[Gst.Element]
    _tray_icon = None # type: tray_icon.TrayIcon

    def start_service(self, target_domain: str, remote_domain: str) -> None:
        """Start video sender service"""

        self._quitting = False
        self._element = None
        icon = self.icon()
        msg = self.video_source() + ': ' + target_domain + ' → ' + remote_domain

        app = "Qubes Video Companion"
        Notify.init(app)
        Notify.Notification.new(app, msg, icon).show()

        self._tray_icon = tray_icon.TrayIcon(app, icon, msg)

    def video_source(self) -> str:
        """
        Return the video source
        """
        raise NotImplementedError("Pure virtual method called!")

    def icon(self) -> str:
        """
        Return the icon name
        """
        raise NotImplementedError("Pure virtual method called!")

    def pipeline(self, width: int, height: int, fps: int):
        """
        Return a set-up GStreamer pipeline
        """
        raise NotImplementedError("Pure virtual method called!")

    def parameters(self):
        """
        Compute the parameters.  Return a (width, height, fps) tuple.
        """
        raise NotImplementedError("Pure virtual method called!")

    def quit(self) -> None:
        """Close the pipeline"""

        if self._quitting:
            return
        self._quitting = True
        self._element.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def msg_handler(self, _bus: Gst.Bus, msg: Gst.Message) -> None:
        """Handle pipeline messages"""

        if msg.type == Gst.MessageType.EOS:
            print('End of stream, exiting', file=sys.stderr)
            self.quit()
        elif msg.type == Gst.MessageType.ERROR:
            print('Fatal error:', msg.parse_error(), file=sys.stderr)
            self.quit()
        elif msg.type == Gst.MessageType.CLOCK_LOST:
            print('Clock lost, resetting', file=sys.stderr)
            self._element.set_state(Gst.State.PAUSED)
            self._element.set_state(Gst.State.PLAYING)

    def validate_qube_names(self, target_domain: str, remote_domain: str) -> NoReturn:
        import re

        qube_re = re.compile('^[A-Za-z][A-Za-z0-9_-]{1,30}$')
        if not qube_re.match(target_domain):
            print('Invalid target qube name %r, failing' % target_domain,
                  file=sys.stderr)
            sys.exit(1)
        if not qube_re.match(remote_domain):
            print('Invalid remote qube name %r, failing' % remote_domain,
                  file=sys.stderr)
            sys.exit(1)

    def start_transmission(self) -> None:
        """Start video transmission"""

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
    def main(cls, self) -> NoReturn:
        """Program entry point"""

        import argparse, qubesdb, os
        argparse.ArgumentParser().parse_args()

        try:
            target_domain = qubesdb.QubesDB().read('/name').decode('ascii', 'strict')
        except:
            # dom0 doesn't have a /name value in its QubesDB
            target_domain = 'dom0'
        remote_domain = os.getenv('QREXEC_REMOTE_DOMAIN')

        self.validate_qube_names(target_domain, remote_domain)

        self.start_service(target_domain, remote_domain)
        self.start_transmission()

        Gtk.main()
