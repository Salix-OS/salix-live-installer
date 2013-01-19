#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Launching the boot loader setup tool with some defaults:
  - run_bootsetup
"""
from execute import *

def run_bootsetup(bootloader = 'lilo'):
  try:
    exec_check("bootsetup %s" % bootloader, env = None)
    return True
  except:
    return False

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertTrue(run_bootsetup())
