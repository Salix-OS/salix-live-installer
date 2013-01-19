#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Chroot function
"""
from execute import *
import os

def exec_chroot(path, cmd):
  """
  Execute cmd in the chroot defined by path.
  pathes in cmd should be relative to the new root.
  """
  if os.getuid() != 0:
    raise Exception('You need root rights to chroot')
  else:
    chrootcmd = "chroot %s %s" % (path, cmd)
    return exec_call(chrootcmd)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertException(Exception, lambda: exec_chroot("/", "/bin/ls")) # we are not root
