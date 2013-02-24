#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Common curses functions for Salix Live Installer.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import re
from common import *

def info_dialog(message, title = None, parent = None):
  """
  Displays an information message.

  """
  if title:
    print title
    print re.sub(r'^', r'  ', message)
  else:
    print message

def error_dialog(message, title = None, parent = None):
  """
  Displays an error message.
  """
  if title:
    print_err("Error: {0}".format(title))
    print_err(re.sub(r'^', r'  ', message))
  else:
    print_err("Error: {0}".format(message))
