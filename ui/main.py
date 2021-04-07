#!/usr/bin/python3

"""Display user interface elements"""

import argparse
import notification
import tray_icon

def main():
    """Program entry point"""

    args = parse_args()
    display_notification(args.video_source, args.requested_target, args.remote_domain)
    display_tray_icon(args.video_source, args.requested_target, args.remote_domain)

def parse_args():
    """Parse command-line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--video-source', type=str, required=True,
                        help='Video stream source')
    parser.add_argument('-t', '--requested-target', type=str, required=True,
                        help='Qrexec requested target')
    parser.add_argument('-r', '--remote-domain', type=str, required=True,
                        help='Qrexec remote domain')
    return parser.parse_args()

def display_notification(video_source, requested_target, remote_domain):
    """Show notification to the user"""

    notification_ui = notification.Notification()
    notification_ui.video_source = video_source
    notification_ui.requested_target = requested_target
    notification_ui.remote_domain = remote_domain
    notification_ui.show()

def display_tray_icon(video_source, requested_target, remote_domain):
    """Show system tray icon to the user"""

    tray_icon_ui = tray_icon.TrayIcon()
    tray_icon_ui.video_source = video_source
    tray_icon_ui.requested_target = requested_target
    tray_icon_ui.remote_domain = remote_domain
    tray_icon_ui.create()
    tray_icon_ui.show()

if __name__ == '__main__':
    main()
