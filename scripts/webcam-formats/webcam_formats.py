#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

"""Get and compare supported webcam formats"""

import subprocess
from collections import OrderedDict

class WebcamFormats():
    """
    Parse supported webcam formats

    Output from: v4l2-ctl --device /dev/videoX --list-formats-ext
    """

    formats = ""
    formats_len = 0
    video_device = ""

    __line_idx = 0

    pix_fmt = dict()

    selected_format = ""
    selected_size = tuple()
    selected_fps = 0

    def __init__(self, formats, video_device="/dev/video0"):
        self.formats = formats
        self.formats_len = len(self.formats)

        self.video_device = video_device

        while self.__line_idx < self.formats_len:
            line = self.formats[self.__line_idx]

            if line.startswith("Index"):
                self.__index()

            self.__line_idx = self.__line_idx + 1

    def __index(self):
        """Parse each pixel format by index value"""

        # We must use a while loop because Python's for loop doesn't
        # allow changing the index while inside the loop
        # Python's for loop is like other languages foreach loop
        while self.__line_idx < self.formats_len:
            line = self.formats[self.__line_idx]

            if line.startswith("Pixel Format"):
                # Remove removing surrounding single quotes (') junk
                pix_fmt = line.split()[2].replace("'", "")
                self.pix_fmt[pix_fmt] = dict()

            if line.startswith("Size"):
                self.__size()
            else:
                self.__line_idx += 1

    def __size(self):
        """Parse size value (video dimensions)"""

        size = self.formats[self.__line_idx].split()[2]
        # Split size by the "x" in between the dimensions into a tuple
        size = tuple(map(int, size.split("x")))

        last_key = list(self.pix_fmt)[-1]
        self.pix_fmt[last_key][size] = list()

        self.__line_idx += 1
        self.__fps()

    def __fps(self):
        """Parse FPS values for size"""

        while self.__line_idx < self.formats_len:
            line = self.formats[self.__line_idx]

            if line.startswith("Interval"):
                # Remove all FPS values that are not a whole number
                if "." in line and ".0" not in line:
                    self.__line_idx += 1
                    continue

                # Capture portion of line with FPS
                fps = line.split()[3]
                # Remove decimals with all zeros and junk opening bracket captured with FPS
                fps = int(fps.split(".")[0].replace("(", ""))

                last_key = list(self.pix_fmt)[-1]
                last_key2 = list(self.pix_fmt[last_key])[-1]
                self.pix_fmt[last_key][last_key2].append(fps)
            else:
                break

            self.__line_idx += 1

    def find_best_format(self):
        """
        Select best video format

        Prefer MJPG over YUV formats
        Prefer 1920x1080 and go down from there
        Prefer 30 FPS and go down from there

        Prioritize at least (cinematic) 24 FPS over a higher resolution
        """

        best_format = "MJPG"
        best_size = (1920, 1080)
        best_fps = 30

        if best_format in self.pix_fmt:
            self.selected_format = best_format
        else:
            # Otherwise, use the first pixel format specified by the webcam
            self.selected_format = self.pix_fmt[0]

        sizes_sorted = self.pix_fmt[self.selected_format].copy()
        sizes_sorted = OrderedDict(sorted(sizes_sorted.items(), reverse=True))

        for size in sizes_sorted:
            if size[0] > best_size[0] or size[1] > best_size[1]:
                continue
            else:
                self.selected_size = size

            current_selected_fps = 0
            for fps in sizes_sorted[size]:
                if fps > current_selected_fps and fps <= best_fps:
                    current_selected_fps = fps
            if current_selected_fps >= 24:
                self.selected_fps = current_selected_fps
                break

    def configure_webcam_best_format(self):
        """Configure webcam device to use the best format"""

        if self.selected_format == "" or self.selected_size == tuple() or self.selected_fps == 0:
            self.find_best_format()

        subprocess.run(['v4l2-ctl', '--device', self.video_device, '--set-fmt-video', 'pixelformat=' + self.selected_format + ',width=' + str(self.selected_size[0]) + ',height=' + str(self.selected_size[1])])