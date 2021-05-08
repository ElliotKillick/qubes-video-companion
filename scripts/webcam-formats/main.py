#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

"""Configure the best video format for any given webcam device"""

import webcam_formats

def main():
    """Program entry point"""

    # For testing
    # Perhaps make unit tests for this; although it would be better to use V4L2 ioctls
    #file = open("scripts/webcam-formats/webcam-formats", 'r')
    #webcam_supported_formats = file.read().replace('\t', '').splitlines()

    # Can't use capture_output because Python version in dom0 is too old
    webcam_supported_formats = subprocess.run(['v4l2-ctl', '--list-formats-ext'],
                                              stdout=subprocess.PIPE).\
                                              stdout.decode('utf-8').\
                                              replace('\t', '').splitlines()

    webcam_settings = webcam_formats.WebcamFormats(webcam_supported_formats)
    webcam_settings.configure_webcam_best_format()

if __name__ == '__main__':
    main()
