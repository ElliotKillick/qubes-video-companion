=====================
qubes-video-companion
=====================

NAME
====
qubes-video-companion - securely stream webcams and share screens across virtual machines

SYNOPSIS
========
| qubes-video-companion <video_source>

DESCRIPTION
===========
Qubes Video Companion is a tool for securely streaming webcams and sharing screens across virtual machines.

It accomplishes this by creating a uni-directional flow of raw video that is passed from one virtual machine to another through file descriptors thereby allowing both machines to be completely air-gapped with no networking stacks exposed. This design makes the side of the video sending virtual machine 100% immune to attack and only leaves a very small attack surface on the side of the video receiving virtual machine.

The project emphasizes correctness and security all the while also sporting superb performance by maintaining a small footprint of the available computational resources and low latency even at Full HD and greater resolutions at 30 or more frames per second.

OPTIONS
=======
video_source
    The video source to stream and receive video from. Either "webcam" or "screenshare".

AUTHORS
=======
| Elliot Killick <elliotkillick at zohomail dot eu>
| Demi Marie Obenour <demi at invisiblethingslab dot com>
