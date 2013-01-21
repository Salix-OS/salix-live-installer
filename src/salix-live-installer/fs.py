#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Get information about filesystem, create them, ...
For now it only handles (S/P)ATA disks and partitions. RAID and LVM are not supported.
/proc and /sys should be mounted for getting information
Functions:
  - getFsType
  - getFsLabel
"""
from execute import *
import os
from stat import *

def getFsType(partitionDevice):
  """
  Returns the file system type for that partition.
  partitionDevice should no be prefilled with '/dev/'.
  Returns 'Extended' if the partition is an extended partition and has no filesystem.
  """
  if S_ISBLK(os.stat('/dev/%s' % partitionDevice).st_mode):
    try:
      fstype = exec_getoutput(['/sbin/blkid', '-c', '/dev/null', '-s', 'TYPE', '-o', 'value', '/dev/%s' % partitionDevice])[0]
    except subprocess.CalledProcessError as e:
      fstype = 'Extended'
  else:
    fstype = False
  return fstype

def getFsLabel(partitionDevice):
  """
  Returns the label for that partition (if any).
  partitionDevice should no be prefilled with '/dev/'.
  """
  if S_ISBLK(os.stat('/dev/%s' % partitionDevice).st_mode):
    try:
      label = exec_getoutput(['/sbin/blkid', '-c', '/dev/null', '-s', 'LABEL', '-o', 'value', '/dev/%s' % partitionDevice])[0]
    except subprocess.CalledProcessError as e:
      label = ''
  else:
    label = False
  return label

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  part = 'sda1'
  fstype = getFsType(part)
  label = getFsLabel(part)
  print '%s: %s (%s)' % (part, fstype, label)
  assertTrue(fstype)
  assertTrue(len(fstype) > 0)
  assertTrue(label)
  assertTrue(len(label) > 0)
