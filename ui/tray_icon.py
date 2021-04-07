#!/usr/bin/python3

# Copyright (C) 2021 Elliot Killick <elliotkillick@zohomail.eu>
# Licensed under the MIT License. See LICENSE file for details.

"""Tray icon user interface module"""

# Use AppIndicator3 because GTK deprecated GtkStatusIcon
# https://stackoverflow.com/questions/41917903/gtk-3-statusicon-replacement

# GI requires version declaration before importing
# pylint: disable=wrong-import-position

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Prefer AyatanaAppIndicator becuase it's under active development
# This is opposed to AppIndicator which is abandonware
# Fallback on old AppIndicator for Qubes R4.0 dom0 which uses Fedora 25
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except (ImportError, ValueError):
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as AppIndicator

import user_interface

class TrayIcon(user_interface.UserInterface):
    """Tray icon user interface component"""

    def __init__(self):
        self.indicator = None

    def create(self):
        """Create tray icon"""

        category = AppIndicator.IndicatorCategory.APPLICATION_STATUS
        self.indicator = AppIndicator.Indicator.new(self.app, self.video_source_to_icon(), category)
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu())

    def menu(self):
        """Create tray icon menu"""

        menu = Gtk.Menu()

        header = Gtk.MenuItem.new_with_label(self.app)
        label = Gtk.MenuItem.get_child(header)
        label.set_markup('<b>' + label.get_text() + '</b>')
        menu.append(header)

        entry = Gtk.MenuItem.new_with_label(self.build_message())
        menu.append(entry)
        menu.show_all()

        return menu

    @staticmethod
    def show():
        """Show tray icon"""

        # pylint: disable=line-too-long
        # FIXME: The following warning appears: Gdk-CRITICAL **: gdk_window_thaw_toplevel_updates: assertion 'window->update_and_descendants_freeze_count > 0' failed
        # This seems to be an issue in AppIndicator that others are also experiencing

        # The fix seems to be here but implementing that locally would probably
        # be difficult without overriding AppIndicator methods to patch it:
        # https://github.com/dorkbox/SystemTray/issues/19

        # Create an issue or make a pull request on the Ayatana version
        # of AppIndicator that's currently being maintained to fix this
        Gtk.main()

    @staticmethod
    def close():
        """Remove tray icon"""

        Gtk.main_quit()
