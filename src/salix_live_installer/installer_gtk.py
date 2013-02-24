#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Graphical Salix Live Installer.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import gettext
import gtk
import gtk.glade
import os
from common import *
from gathergui import *

def run_install(app_name, locale_dir, version, min_salt_version, is_test, is_clone, use_test_data):
  gettext.install(app_name, locale_dir, True)
  gtk.glade.bindtextdomain(app_name, locale_dir)
  gtk.glade.textdomain(app_name)
  if not is_test and os.getuid() != 0:
    error_dialog(_("Root privileges are required to run this program."), _("Sorry!"))
    sys.exit(1)
  GatherGui(version, min_salt_version, is_test, is_clone, use_test_data)
  # indicates to gtk (and gdk) that we will use threads
  gtk.gdk.threads_init()
  # start the main gtk loop
  gtk.main()
