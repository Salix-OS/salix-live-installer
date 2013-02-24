#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Common functions for Salix Live Installer.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import os
import sys

def print_err(*args):
  sys.stderr.write(' '.join(map(str, args)) + "\n")

if os.environ.get('DISPLAY'):
  from commongtk import *
else:
  from commoncurses import *

