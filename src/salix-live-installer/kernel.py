#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions for getting kernel parameters
"""
import os

def has_kernel_param(param):
  """
  Defines if the kernel parameter param has been defined on the kernel command line or not
  """
  if os.path.exists('/proc/cmdline'):
    cmdline = open('/proc/cmdline', 'r').read().split()
    for chunk in cmdline:
      if param == chunk.split('=', 1)[0]:
        return True
  return False

def get_kernel_param_value(param):
  """
  Return the value of the kernel parameter, None if this param has no value and False if this param does not exist
  """
  if os.path.exists('/proc/cmdline'):
    cmdline = open('/proc/cmdline', 'r').read().split()
    for chunk in cmdline:
      paramMap = chunk.split('=', 1)
      if param == paramMap[0]:
        if len(paramMap) > 1:
          return paramMap[1]
        else:
          return None
  return False

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  # it is supposed that the /proc/cmdline always have "ro" and "root=XXX" parameters.
  assertTrue(has_kernel_param('ro'))
  assertTrue(has_kernel_param('root'))
  assertFalse(has_kernel_param('nonexistant'))
  assertNotEquals('', get_kernel_param_value('root'))
  assertEquals(None, get_kernel_param_value('ro'))
  assertEquals(False, get_kernel_param_value('nonexistant'))
