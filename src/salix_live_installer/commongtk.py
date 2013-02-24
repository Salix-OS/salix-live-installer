#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Common graphical functions for Salix Live Installer.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import gtk

def info_dialog(message, title = None, parent = None):
  """
  Displays an information message.

  """
  dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_INFO, buttons = gtk.BUTTONS_OK, flags = gtk.DIALOG_MODAL)
  if title:
    msg = "<b>{0}</b>\n\n{1}".format(title, message)
  else:
    msg = message
  dialog.set_markup(msg)
  result_info = dialog.run()
  dialog.destroy()
  return result_info

def error_dialog(message, title = None, parent = None):
  """
  Displays an error message.
  """
  dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE, flags = gtk.DIALOG_MODAL)
  if title:
    msg = "<b>{0}</b>\n\n{1}".format(title, message)
  else:
    msg = message
  dialog.set_markup(msg)
  result_error = dialog.run()
  dialog.destroy()
  return result_error
