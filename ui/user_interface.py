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

    def video_source_to_icon(self):
        """Convert video source to icon name"""

        conversion_dict = {
            'webcam': 'camera-web',
            'screenshare': 'video-display'
        }
        try:
            return conversion_dict[self.video_source]
        except KeyError:
            print('Video source does not exist:', self.video_source, file=sys.stderr)
            sys.exit(1)
