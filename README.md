<div align="center">
    <a href="https://github.com/elliotkillick/qubes-video-companion">
        <img width="160" src="icons/logo.png" alt="Logo" />
    </a>
</div>

<h3 align="center">
    Qubes Video Companion
</h3>

<p align="center">
    Securely stream webcams and share screens across virtual machines
</p>

<div align="center">
    <img src="https://img.shields.io/github/v/release/elliotkillick/qubes-video-companion?style=flat-square" alt="Version">
    <img src="https://img.shields.io/gitlab/pipeline/elliotkillick/qubes-video-companion/master?style=flat-square" alt="GitLab pipeline" />
    <a href="https://www.qubes-os.org">
        <img src="https://img.shields.io/badge/Made%20for-Qubes%20OS-63a0ff?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAACE0lEQVR4Ae2Vg5JdQRiE56HyQrGTQmzbTgqxbdu2bWvN09vLf3E1OlfTVV/pYvobqpCQHMyqMziy%2bizKCVr4rfIlLPuXIBGrzuKjytWw3Dspm5J6fvduLm2XG42lCDSp4m8PZbP4XpaoJLDkTzb2%2bU8Cl3BbvYljn7%2bQQb1Qx5W96mO7XOCf1xLERIXL7VJmM6NGB1z4YVsehpQk%2bK9qAhOUSZadMhqsltvtbIoz9JDfiQgyYQ1ZReYe1ZSYsBt3Ju8F5h0BVpzOaLCIAz3VWNkvmQgsPgGM2Q303QD0XIc7OgJoZep%2bYOExgDObbKDvhhfD5kTnaw1ZfgqYzHEHbAJ6rGP5FjQFhIlkxgFgyQnXN4XccCyOlZykmYeBoVulNLEVECbtAeZwAJ6Pn8px5h9D1fAdQO/1MuuOBQTlKVI8TwV6FoNAEAgCQSAIBIEgEATINw/lr8YjIJQ5LH%2bdIF4B4bhF8YsEGXJbR%2bC0pkREtqsM02sdjmsU15t9kcA9Ak2q0xTfzjKRFNObff8Swt8E26WawL68vsRlAhNG70RN7/Wo0y4t/FDWEZFbBgKggEnxSPkIS%2b0hUQwCF5WfyC3lVUD47VvkmlcB4aVPifWkzpuAUOd7NQ5mKFBHHhi%2bB79JN98i55MJ8CG70ult%2bOfzSrV%2bP0QgwWEUiZOkJkXxCrJT5XpY8iGRR49S5KrK8YQ0AG5m/ZMNiwL6AAAAAElFTkSuQmCC&style=flat-square" alt="Made for Qubes OS" />
    </a>
</div>

## About

Qubes Video Companion is a tool for securely streaming webcams and sharing screens across virtual machines.

It accomplishes this by creating a uni-directional flow of raw video that is passed from one virtual machine to another through file descriptors thereby allowing both machines to be completely air-gapped with no networking stacks exposed. This design makes the side of the video sending virtual machine 100% immune to attack and only leaves a very small attack surface on the side of the video receiving virtual machine.

The project emphasizes correctness and security all the while also sporting superb performance by maintaining a small footprint of the available computational resources and low latency even at Full HD and greater resolutions at 30 or more frames per second.

## Installation

**WIP: Currently in the process of being streamlined as part of core Qubes OS**

**For testers (thank you for your help!), please use the build scripts in the `build` directory of this repo to build the required Qubes Video Companion package(s). Install them in `sys-usb` and any other AppVM for receiving the video. Also, ensure that at minimum in the Qubes RPC policies in `qubes-rpc/policies` are installed into Dom0 at `/etc/qubes-rpc/policy`.**

Qubes Video Companion is available for installation on Qubes OS in packaged form for both Fedora (.rpm) and Debian (.deb). To get it, simply install the `qubes-video-companion` package as shown below!

### Run the following commands in Dom0 (AdminVM)
`sudo qubes-dom0-update qubes-video-companion`

### Run the following commands in a TemplateVM or AppVM

#### Fedora
`sudo dnf install qubes-video-companion`

#### Debian
`sudo apt update && sudo apt install qubes-video-companion`

## Usage

### Webcam

Simply run the following command in the virtual machine of the webcam stream recipient:

`qubes-video-companion webcam`

A secure confirmation dialog will appear asking where the webcam stream is to be sourced from. If the webcam device is attached to `sys-usb` then select that qube as the target, if instead the webcam is attached to `dom0` then select that as the target. Afterwards, confirm the operation by clicking `OK`.

### Screen Sharing

Simply run the following command in the virtual machine of the screen sharing recipient:

`qubes-video-companion screenshare`

A secure confirmation dialog will appear asking where the screen to share is to be sourced from. Select any qube as the target screen, this could be a regular unprivileged qube such as `personal` or a [DisposableVM](https://www.qubes-os.org/doc/disposablevm/), or the ultimately trusted `dom0` (caution is advised to avoid information disclosure. Afterwards, confirm the operation by clicking `OK`.

Note that confirmation isn't required when a VM wants to view the screen of a DisposableVM it launched itself because the parent VM already has full control over the DisposableVM.

### Preview

At this point, install and open an application such as Cheese (packaged as `cheese`) to preview the webcam or screen shared video stream. You're all set!

## Security

Here is a review of the security concerns webcams entail that Qubes users either no longer have to worry about or have been greatly mitigated thanks to Qubes Video Companion. It also goes over some of the lengths this project went to in order to create a ["reasonably secure"](https://www.qubes-os.org) end product.

- An unspoofable system tray icon and notification appears when webcam streaming or screen sharing is taking place to serve as a clear and persistent indication to the user of what is being shared
    - This tray icon and notification is created by the video sender so it's impossible for an attacker to forcefully obfuscate or remove it
    - This is especially important for screen sharing because whereas most webcams have an indicator light to inform the user of when they are in use; screen sharing has no such mechanism
- One-way only communication from the video sending machine to the video receiving machine thus guaranteeing the security of the sender
    - This is crucial because the sender, typically `sys-usb`, has a lot of exposed hypervisor and hardware attack surface
        - This is due to having all USB devices in the form of the entire [USB controller PCI device](https://www.qubes-os.org/doc/device-handling-security/#pci-security) passed through to it
        - Additionally, for PCI passthrough `sys-usb` must be an HVM (as opposed to a PVH) domain which is far more complex and has proven to be the source of many more vulnerabilities in the Xen hypervisor
        - These vulnerabilities are very real and common, case in point:
            - XSA-373 of [QSB #069-2021](https://github.com/QubesOS/qubes-secpack/blob/master/QSBs/qsb-069-2021.txt): "`A malicious guest may be able to elevate its privileges to that of the host, cause host or guest Denial of Service (DoS), or cause information leaks.`"
            - XSA-325 of [QSB #063-2020](https://github.com/QubesOS/qubes-secpack/blob/master/QSBs/qsb-063-2020.txt): HVM domains such as `sys-usb` may cause a use-after-free leading to a crash for which privilege escalation cannot be ruled out
            - XSA-337 of [QSB #059-2020](https://github.com/QubesOS/qubes-secpack/blob/master/QSBs/qsb-059-2020.txt): "`A malicious HVM with a PCI device (such as sys-net or sys-usb in the default Qubes OS configuration) can potentially compromise the whole system.`"
            - XSA-321 of [QSB #058-2020](https://github.com/QubesOS/qubes-secpack/blob/master/QSBs/qsb-058-2020.txt): A vulnerability with the same level of impact as the previous one this time only affecting Intel processors
    - If a USB keyboard and mouse is in use (as opposed to PS/2 peripherals commonly used internally in laptops), `sys-usb` is responsible for routing the input of those devices to `dom0`
        - In this scenario, `sys-usb` compromise is essentially equivalent to `dom0` compromise through keyboard/mouse input injection thus making it all the more important that we protect `sys-usb`
            - For example, an attacker could quickly inject the global default XFCE keyboard shortcut `ALT+F2` to open `xfce4-appfinder --collapsed` followed by an arbitrary command to gain control of `dom0`
    - Other times, this is of ultimate concern because the most highly privileged virtual machine in the system, `dom0`, is in control of the USB devices
        - Although, passing through of individual USB devices with USBIP over Qubes RPC from `dom0` was never a possibility in Qubes for security reasons
- The attack surface of the video receiving machine is crafted to be as small as possible
    - GStreamer [`capsfilter`](https://gstreamer.freedesktop.org/documentation/coreelements/capsfilter.html) (capabilities filter) is used to create a singular, small, homogeneous attack surface for accepting video
        - Video dimensions and frame rate capabilities are sanitized upon being pass to the video receiver to prevent the injection of additional capabilities
    - Only high quality and robust GStreamer ["Base" and "Good" plugins](https://gitlab.freedesktop.org/gstreamer/gstreamer/-/raw/master/README) are used to minimize the possibility of bugs
        - Additionally, only the most common and battle-hardened GStreamer components and formats are used
    - Any complex operations (such as video conversions where necessary) are done on the side of the sending machine where the video data is still inherently trusted
    - Only small parts of two kernel modules ever touch untrusted video data: [`v4l2loopback`](https://github.com/umlaeute/v4l2loopback) and the Video4Linux2 (V4L2) driver in mainline Linux
        - This is a massive improvement to what it would have been previously using USBIP over Qubes RPC for passing through a USB webcam device thereby exposing the entire Linux USB stack to a potential attacker
    - Kernel modules are reloaded between Qubes Video Companion sessions to ensure a clean state
- The video dimensions and FPS parameters are sanitized by the video receiver to ensure they contain no extraneous GStreamer capabilities
- No TCP/IP networking stacks are exposed
    - Communication is performed through file descriptors that run between virtual machines using the simple point-to-point protocol that is [Qubes RPC](https://www.qubes-os.org/doc/qrexec/) (built upon Xen vchan under the hood)
- Mitigates vulnerabilities in the webcam firmware
    - With Qubes Video Companion, the virtual machine receiving the webcam video stream never has direct hardware access to the webcam device thus rendering firmware tinkering impossible
    - Firmware vulnerabilities as demonstrated in [this paper](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-brocker.pdf) could allow an attacker to disable the webcam LED indicator or even perform a VM escape (or at least an escape to `sys-usb`)
    - Here is a good [WIRED article](https://www.wired.com/story/firmware-hacks-vulnerable-pc-components-peripherals/) on the state of firmware security and why it must not be trusted
- Ability to separate the video and microphone capabilities that many webcams feature
    - Webcam microphones are often very sensitive picking up lots of background noise which serves as an information leak should the virtual machine it's being passed through to be compromised
        - This mitigates listening to keystrokes as a method of keylogging the entire system
            - Public implementations for conducting this type of attack in practice [already exist](https://github.com/shoyo/acoustic-keylogger) so it's not an unrealistic concern
            - This also serves as a mitigation for other types of [acoustic side-channel attacks](https://en.wikipedia.org/wiki/Acoustic_cryptanalysis) (e.g. encryption key extraction through acoustic machine emanations)
        - Removes the possibility of hearing background conversations
    - Instead, connect only the desired microphone such as one that comes as part of a headset or even none at all using PulseAudio (please see the FAQ)
- Conscious effort was made to base this project only on software with good security track records
    - GStreamer instead of FFmpeg
- Allows for better isolation of complex (and unfortunately often proprietary) video conferencing software often used with webcams that is commonly the subject of many critical vulnerabilities (e.g. Zoom)
    - Such as the recent remote code execution (RCE) [vulnerability discovered in Zoom](https://blog.malwarebytes.com/exploits-and-vulnerabilities/2021/04/zoom-zero-day-discovery-makes-calls-safer-hackers-200000-richer/)
- As has been well noted [here](https://github.com/QubesOS/qubes-issues/issues/2079#issuecomment-226942065), this project does _not_ solve the privacy issue of an already compromised (as a result of a malicious USB device) `sys-usb` sniffing the webcam video stream and leaking that data to other USB devices
    - Leaking data over the network is already prevented through air-gapping `sys-usb`
    - However, the unidirectional communication of video data from `sys-usb` this project institutes 100% guarantees that it cannot be compromised in the first place through the use of a webcam
        - This assumes that the webcam itself isn't backdoored perhaps through a [supply chain attack](https://en.wikipedia.org/wiki/Supply_chain_attack) which have been on the rise lately (e.g.  SolarWinds compromise)
- All Git release tags are signed by the project maintainer's PGP key
    - All commits by the maintainer are also always signed with their PGP key
    - Should signing ever cease, assume compromise
    - Current maintainer 1: [Elliot Killick](https://github.com/elliotkillick) <a href="https://keybase.io/elliotkillick" target="_blank"><img src="https://img.shields.io/keybase/pgp/elliotkillick?style=flat-square" alt="PGP key" /></a>
        - PGP key: 018F B9DE 6DFA 13FB 18FB 5552 F9B9 0D44 F83D D5F2
    - Current maintainer 2: [Demi Marie Obenour](https://github.com/DemiMarie) (Key not attached to Keybase account)
        - PGP key: 8F3B D112 BD78 566D EABA 584F CFA7 7693 4CEF 6E3F
        - [Signed proof](https://github.com/elliotkillick/qubes-video-companion/pull/17#issuecomment-837702694)

## Frequently Asked Questions (FAQ)

### What about audio?

In Qubes OS, audio is handled securely through the use of simple PulseAudio sinks.

The microphone of a webcam can be utilized by configuring it as the recording device for the desired qube in the `Recording` tab of the `Volume Control` application in `dom0`. Then, simply connect the microphone to the desired qube in the `Qubes Devices` system tray app at the bottom-right of the screen.

Audio is out of scope for this project in particular.

### Why GStreamer instead of FFmpeg?

- GStreamer has a much better security track record than FFmpeg
    - Even a broad search for all CVEs containing the term ["GStreamer"](https://nvd.nist.gov/vuln/search/results?query=gstreamer) shows far fewer vulnerabilities than what has specifically been assigned to the [FFmpeg project](https://www.cvedetails.com/product/6315/Ffmpeg-Ffmpeg.html?vendor_id=3611)
- FFmpeg isn't included in the base Fedora repositories due to patent issues
    - Where FFmpeg is monolithic; GStreamer is modular allowing for the patent unencumbered components to be included in Fedora base repositories
- GStreamer (at least the base and good plugins which is all we're using) has more efficient, clean and performant code
- GStreamer has better cross-platform support for future development ([Source](https://github.com/FNA-XNA/FAudio/pull/161))
- GStreamer has superior documentation
- FFmpeg has its advantages in some areas, but for this project, GStreamer is the way to go
    - FFmpeg is more flexible and easier to use (more "magic")
    - It has better and more special effects for video editing
    - Supports a wider range of formats and codecs

### How does it work?

A basic overview is provided in the About section of this `README`.

For information on the GStreamer pipeline, check out [`pipeline.md`](doc/pipeline.md) and the accompanying diagrams in the [`visualizations`](doc/visualizations) folder. This will provide insight to the thought process that went into some of the design decisions made in this project along with illustrations of the pipeline internals.

The user interface components are created with GTK 3, GObject and AppIndicator (because GTK deprecated `GtkStatusIcon`).

### Why can I perceive some latency in the video playback?

**This issue will likely be fixed by switching entirely to MJPEG instead of the raw YUV video format for streaming video. See issues [#16](https://github.com/elliotkillick/qubes-video-companion/issues/16) and [#13](https://github.com/elliotkillick/qubes-video-companion/issues/13).**

This means the CPU is at its limit (nearing or at 100% usage). To check this, install GNOME System Monitor (packaged as `gnome-system-monitor`) in the video receiving VM and assess the CPU usage for each of the processes and overall in the resources graph.

It's important to remember that for security reasons, qubes do not have access to the GPU and therefore, must rely entirely on the CPU even for graphical workloads.

To fix the latency, do one or more of the following:

1. Remove or shrink the size of any windows playing back the video stream being shared to the video receiving VM
    - Just like in video editing, playing back raw, unencoded video in realtime is a very computationally expensive task that takes much more processing power than recording and in this case even sharing the video across VMs combined
    - For example, in OBS, right-click the video preview and uncheck `Enable preview` when recording
2. Pause any videos from playing (e.g. YouTube videos) in any of the VMs
3. Assign more vCPUs to the video receiving VM
    - The video rendering workload lends decently to multithreading so the more vCPUs the better
    - The vCPU count can be changed in the settings for that qube
4. Reduce the resolution and/or frame rate the webcam is recording at to a supported lower quality setting

## Contributing

You can start by giving this project a star! High quality PRs are also welcome! Take a look at the issue tracker if you're looking for things that need improvement. Other improvements such as more elegant ways of completing a task, code cleanup and other fixes are also welcome.

Alternatively, for ideas on what you can contribute to the wider Qubes OS project, take a look at the ["help wanted"](https://github.com/QubesOS/qubes-issues/labels/help%20wanted) Qubes issues and available [GSoC projects](https://www.qubes-os.org/gsoc/).

The [video camera icon](https://commons.wikimedia.org/wiki/File:Video_camera_icon.svg) used in the project logo is by Рытикова Людмила licensed under the [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/) license. As a result, the logo as a whole is under the same license. The portion of the logo surrounding the video camera icon is by Max Andersen, used with written permission.

This project is the product of an independent effort that is not officially endorsed by Qubes OS.

## Tested Working Applications

- [Cheese](https://wiki.gnome.org/Apps/Cheese)
- Chromium-based browsers (e.g. Brave and Google Chrome)
- Firefox
    - This [patch](https://github.com/umlaeute/v4l2loopback/pull/435) for `v4l2loopback` is necessary to get this working
- Open Broadcaster Software (OBS)
    - For the `Video Capture Device (V4L2)` source click on the `Properties` settings cog and use video format `Planar YUV 4:2:0` (as opposed to `YV12 (Emulated)`) and uncheck `Use buffering` for optimal performance
- Zoom

## Webcam Hardware Compatibility List (HCL)

This is the list of webcams confirmed to work with Qubes Video Companion.

The model of a given webcam can be found by running `v4l2-ctl --list-devices` in the virtual machine with the webcam device attached.

- Logitech C922 Pro Stream Webcam
- SunplusIT Inc Integrated Camera

## Mailing List Thread

- [Original announcement](https://groups.google.com/g/qubes-users/c/nRUjKErIRUQ)

## End Goals

- Implement a solution for secure webcam utilization that sufficiently addresses the concerns brought up in this in-depth paper on webcam firmware security: [iSeeYou: Disabling the MacBook Webcam Indicator LED](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-brocker.pdf) ([Google Scholar](https://scholar.google.ca/scholar?q=iSeeYou%3A+Disabling+the+MacBook+Webcam+Indicator)) by Johns Hopkins University
    - The end product should be capable of fully protecting at risk individuals such as those documented in the case studies of this [MIT paper](https://courses.csail.mit.edu/6.857/2014/files/03-jayaram-lui-nguyen-zakarian-preventing-covert-webcam-hacking) in practice (assuming they are Qubes users)
- Effectively solve two long-standing Qubes issues making using a webcam in Qubes OS a dodgy, insecure and computationally expensive (in CPU and RAM) experience:
    - Cannot use a USB camera: [#4035](https://github.com/QubesOS/qubes-issues/issues/4035)
    - Feature: Trusted stream for webcam input: [#2079](https://github.com/QubesOS/qubes-issues/issues/2079)
- Add secure screen sharing functionality between qubes
    - Feature: Screen sharing between AppVMs: [#6426](https://github.com/QubesOS/qubes-issues/issues/6426)
