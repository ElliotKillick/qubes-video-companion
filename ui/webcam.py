import re
from service import Service
import subprocess

class Webcam(Service):
    def video_source(self) -> str:
        return 'webcam'

    def icon(self) -> str:
        return 'camera-web'

    def parameters(self) -> tuple[int, int, int]:
        mjpeg_re = re.compile(rb"\t\[[0-9]+]: 'MJPG' \(Motion-JPEG, compressed\)\Z")
        fmt_re   = re.compile(rb"\t\[[0-9]+]: ")
        dimensions_re = re.compile(rb"\t\tSize: Discrete [0-9]+x[0-9]+\Z")
        interval_re   = re.compile(rb"\t\t\tInterval: Discrete [0-9.]+s \([0-9]+\.0+ fps\)\Z")
        proc = subprocess.run(('v4l2-ctl', '--list-formats-ext'),
                              stdout=subprocess.PIPE,
                              check=True,
                              env={'PATH': '/bin:/usr/bin', 'LC_ALL': 'C'})
        emit = False
        formats = []
        for i in proc.stdout.split(b'\n'):
            if mjpeg_re.match(i):
                emit = True
            elif fmt_re.match(i):
                emit = False
            elif dimensions_re.match(i):
                width, height = map(int, i[17:].split(b'x'))
            elif interval_re.match(i):
                fps = int(i[22:].split(b'(', 1)[1].split(b'.', 1)[0])
                formats.append((width, height, fps))
            elif i in (b'', b'ioctl: VIDIOC_ENUM_FMT', b'\tType: Video Capture'):
                continue
            else:
                print('Cannot parse output %r of v4l2ctl' % i, file=sys.stderr)
        formats.sort(key=lambda x: x[0] * x[1] * x[2], reverse=True)
        return formats[0]

    def pipeline(self, width: int, height: int, fps: int) -> list[str]:
        caps = ('width={},'
                'height={},'
                'framerate={}/1,'
                'format=I420,'
                'interlace-mode=progressive,'
                'pixel-aspect-ratio=1/1,'
                'max-framerate={}/1,'
                'views=1'.format(width, height, fps, fps))
        return [
            'v4l2src',
            '!',
            'queue',
            '!',
            'capsfilter',
            'caps=image/jpeg,colorimetry=2:4:7:1,chroma-site=none,' + caps,
            '!',
            'jpegdec',
            '!',
            'capsfilter',
            'caps=video/x-raw,' + caps,
            '!',
            'fdsink',
        ]

if __name__ == '__main__':
    Webcam.main()
