#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

"""User interface base module"""

import sys

class UserInterface:
    """User interface base class"""

    app = "Qubes Video Companion"
    video_source = ""
    requested_target = ""
    remote_domain = ""

    def build_message(self):
        """Create video stream message for being displayed to the user"""

        return self.video_source + ": " + self.requested_target + " -> " + self.remote_domain
