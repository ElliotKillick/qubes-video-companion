#!/usr/bin/python3

"""Get and compare supported webcam formats"""

import subprocess

def main():
    """Program entry point"""

    # For testing
    file = open("scripts/video-formats", 'r')
    webcam_supported_formats = file.read().replace('\t', '').splitlines()

    # Can't use capture_output because Python version in dom0 is too old
    #webcam_supported_formats = subprocess.run(['v4l2-ctl', '--list-formats-ext'],
    #                                          stdout=subprocess.PIPE).\
    #                                          stdout.decode('utf-8').\
    #                                          replace('\t', '').splitlines()

    webcam_formats_parser = WebcamFormatsParser(webcam_supported_formats)
    webcam_formats_parser.get_best_format()

class WebcamFormatsParser():
    """
    Parse webcam supported formats

    Output from: v4l2-ctl --device /dev/video0 --list-formats-ext
    """

    formats = ""
    formats_len = 0
    line_idx = 0

    def __init__(self, formats):
        self.formats = formats
        self.formats_len = len(formats)

        while self.line_idx < self.formats_len:
            line = self.formats[self.line_idx]

            if line.startswith("Index"):
                self.index()

            self.line_idx = self.line_idx + 1

    def index(self):
        """Parse each pixel format by index value"""

        # We must use a while loop because Python's for loop doesn't
        # allow changing the index while inside the loop
        # Python's for loop is like other languages foreach loop
        while self.line_idx < self.formats_len:
            line = self.formats[self.line_idx]

            if line.startswith("Pixel Format"):
                print(line.split()[2].replace("'", ""))

            if line.startswith("Size"):
                self.size()

            self.line_idx = self.line_idx + 1

    def size(self):
        """Parse size value (video dimensions)"""

        print(str(self.formats[self.line_idx]).split()[2])
        self.line_idx += 1
        self.fps()

    def fps(self):
        """Parse FPS values for size"""

        while self.line_idx < self.formats_len:
            line = self.formats[self.line_idx]

            if line.startswith("Interval"):
                # Remove all FPS values that are not a whole number
                if "." in line and ".0" not in line:
                    self.line_idx = self.line_idx + 1
                    continue

                # Capture portion of line with FPS
                line = line.split()[3]
                # Remove decimals with all zeros and junk opening bracket captured with FPS
                line = line.split(".")[0].replace("(", "")

                print(line)
            else:
                break

            self.line_idx = self.line_idx + 1

    def get_best_format(self):
        """
        Select best video format

        Prefer MJPG over YUV formats
        Prefer 1920x1080 and go down from there
        Prefer 30 FPS and go down from there
        """

        # TODO: Implement get_best_format()

        pass

if __name__ == '__main__':
    main()
