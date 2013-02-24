#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Function to launch the boot loader setup tool with some defaults:
  - runBootsetup
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *

def runBootsetup(bootloader = 'lilo'):
  try:
    execCheck(['bootsetup', bootloader], env = None)
    return True
  except:
    try:
      execCheck(['lilosetup'], env = None)
      return True
    except:
      return False

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertTrue(runBootsetup())
