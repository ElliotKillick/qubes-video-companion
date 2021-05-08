# Video Senders (Qubes RPC Services)

## -q (quiet)
### gst-launch-1.0 needs to be quiet because the debug messages are printed on standard output instead of standard error
- This means the debug info will become part of the video output upon being sent to the `fdsink` element which is unwanted behavior that results in video artifacts

## queue
### Force push mode scheduling which is better for a constant stream of data
- https://gstreamer.freedesktop.org/documentation/additional/design/scheduling.html

## format=I420
### This pixel format was chosen for two reasons
1. I420 seemed to be the default output format for a lot of elements and was always listed at the top of pixel format lists in the GStreamer documentation as well as over places such as on the official FOURCC website which defines these pixel formats
    - So, presumably I420 is the most battle-hardened format which is least likely to contain bugs
    - GStreamer documentation mentions to also prefer I420 over YV12 which are the same but with the V and U planes switched around
2. I420 is directly compatible with many GStreamer elements including `v4l2sink` without needing a leading `videoconvert` (probably followed by a `tee`)
    - This greatly improves performance and security
- https://gstreamer.freedesktop.org/documentation/additional/design/mediatype-video-raw.html
- https://gstreamer.freedesktop.org/documentation/application-development/basics/elements.html
- https://www.fourcc.org/yuv.php

## use-damage=false in `qvc.ScreenShare`
### XDamage causes `ximagesrc` to send out small updates about what parts of the screen has changed as opposed to just sending the whole screen
- This may be preferable on a network because of the decrease in bandwidth and latency but otherwise it just results in very high CPU usage and doesn't fit our use case


## BGRx -> I420 pixel format `videoconvert` in `qvc.ScreenShare`
### `ximagesrc` only outputs in BGRx so it must be converted to I420 which is a supported input format for `v4l2sink` (on the `receiver.py` side)
- This video conversion is done on the side of the sending machine as to ensure the attack surface of the recipient stays as small as possible

# Video Receiver (`receiver.py`)

## capsfilter
### This is used to limit our attack surface to the given capabilities
- All the capabilities after the colorimetry are technically unnecessary for this to be functional but are used to limit our attack surface
- This filter accounts for all the capabilities possible on a raw video stream according to the below documentation
- https://gstreamer.freedesktop.org/documentation/coreelements/capsfilter.html
- https://gstreamer.freedesktop.org/documentation/additional/design/mediatype-video-raw.html
- https://gstreamer.freedesktop.org/documentation/application-development/basics/pads.html#what-capabilities-are-used-for

## colorimetry=2:4:7:1
### This is the default colorimetry format for I420 and the only one that works with it without having to specify a `chroma-site`
- Having `chroma-site` set to `none` reduces our attack surface and likely improves our performance as well

## use-sink-caps=true
### Use the capabilities defined by the previous element, in this case, what is explicitly defined by the capsfilter

## sync=false
### Disable syncing video to the system clock
- This fixes the frame jittering/lagging that happens when passing raw video between machines
- `sync=false` is the default on the `fdsink` sink on the video sender
    - Tried making both sender and receiver `sync=true` but that resulted in jittering again
    - Also tried making only the `fdsink` sink on the sender `sync=true` and the `v4l2sink` sink on the receiver `sync=false` but that resulted in higher CPU usage and greater video latency
- Some times it takes some time to start jittering/lagging depending on what the video source is but it will happen
- I think it's because the two VMs are on slightly different clocks so trying to synchronize to that doesn't work out very well
    - This fix isn't necessary when passing raw video directly between file descriptors on the same machine
- This may be better fixed by passing timestamp information through the raw video itself
    - However, it appears to be that raw video is incapable of holding timestamp information
        - Timestamping is done on raw video in the GStreamer pipeline but once it leaves there (through `fdsink`) any timestamping information may be void (unsure)
        - Although, research has found a few somewhat hacky solutions for FFmpeg that allowed for timestamping on raw video; perhaps GStreamer has something similar
- Or maybe we could synchronize the clocks of the machines better thus allowing us to remove `sync=false`
    - Or even just synchronize the clocks that the GStreamer processes see on each machine right before running them
        - Perhaps using the `datefudge` or `faketime` command which uses `LD_PRELOAD` to manipulate the system time for a given command
