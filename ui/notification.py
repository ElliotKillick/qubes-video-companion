#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

"""Notification user interface module"""

# GI requires version declaration before importing
# pylint: disable=wrong-import-position

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

import user_interface

class Notification(user_interface.UserInterface):
    """Notification user interface component"""

    def __init__(self):
        Notify.init(self.app)

    def show(self):
        """Display notification to the user"""

        Notify.Notification.new(self.app, self.build_message(), self.video_source_to_icon()).show()

    @staticmethod
    def __destroy__():
        Notify.uninit()
