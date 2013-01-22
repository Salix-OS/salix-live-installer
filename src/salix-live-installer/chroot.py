#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Chroot function
"""
from execute import *
import os

def execChroot(path, cmd):
  """
  Execute cmd in the chroot defined by path.
  pathes in cmd should be relative to the new root.
  """
  checkRoot()
  return execCall(['chroot', path, cmd])

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertException(Exception, lambda: execChroot("/", "/bin/ls")) # we are not root
