#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Help mounting/unmounting a filesystem.
Functions:
  - getMountPoint
  - isMounted
  - mountDevice
  - umountDevice
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *
from fs import getFsType
import os
from stat import *
import re

_tempMountDir = '/mnt/.tempSalt'

def getTempMountDir():
  return _tempMountDir

def getMountPoint(device):
  """
  Find the mount point to this 'device' or None if not mounted.
  """
  mountpoint = None
  path = os.path.abspath(device)
  for line in execGetOutput(['/bin/mount'], shell = False):
    p, _, mp, _ = line.split(' ', 3) # 3 splits max, _ is discarded
    if os.path.islink(p):
      p = os.path.realpath(p)
    if p == path:
      mountpoint = mp
      break
  return mountpoint

def isMounted(device):
  """
  Same as os.path.ismount(path) but using a block device.
  """
  if getMountPoint(device):
    return True
  else:
    return False

def _deleteMountPoint(mountPoint):
  # delete the empty directory
  try:
    os.rmdir(mountPoint)
  except:
    pass
  # delete the temporary directory if not empty
  if os.path.isdir(_tempMountDir):
    try:
      os.rmdir(_tempMountDir)
    except:
      pass

def mountDevice(device, fsType = None, mountPoint = None):
  """
  Mount the 'device' of 'fsType' filesystem under 'mountPoint'.
  If 'mountPoint' is not specified, '{0}/device' will be used.
  Returns False if it fails.
  """.format(_tempMountDir) 
  if not fsType:
    fsType = getFsType(re.sub(r'/dev/', '', device))
  autoMP = False
  if not mountPoint:
    mountPoint = '{0}/{1}'.format(_tempMountDir, os.path.basename(device))
    if os.path.exists(mountPoint):
      return False
    autoMP = True
  if not os.path.exists(mountPoint):
    try:
      os.makedirs(mountPoint)
    except os.error:
      pass
  ret = execCall(['mount', '-t', fsType, device, mountPoint], shell = False)
  if ret != 0 and autoMP:
    _deleteMountPoint(mountPoint)
  return ret

def umountDevice(deviceOrPath, tryLazyUmount = True, deleteMountPoint = True):
  """
  Unmount the 'deviceOrPath' which could be a device or a mount point.
  If umount failed, try again with a lazyUmount if 'tryLazyUmount' is True.
  Will delete the mount point if 'deleteMountPoint' is True.
  Returns False if it fails.
  """
  if S_ISBLK(os.stat(deviceOrPath).st_mode):
    mountPoint = getMountPoint(deviceOrPath)
  else:
    mountPoint = deviceOrPath
  if mountPoint:
    ret = execCall(['umount', mountPoint], shell = False)
    if ret != 0:
       ret = execCall(['umount', '-l', mountPoint], shell = False)
    if ret == 0 and deleteMountPoint:
      _deleteMountPoint(mountPoint)
    return ret
  else:
    return False

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  from fs import *
  checkRoot() # need to be root to mount/umount
  execCall(['dd', 'if=/dev/zero', 'of=ext4.fs', 'bs=1M', 'count=50'], shell = False)
  makeFs('ext4.fs', 'ext4', 'test ext4', True)
  assertFalse(isMounted('ext4.fs'))
  assertEquals(0, mountDevice('ext4.fs'))
  assertTrue(isMounted('ext4.fs'))
  assertEquals('{0}/ext4.fs'.format(_tempMountDir), getMountPoint('ext4.fs'))
  assertEquals(0, umountDevice('ext4.fs'))
  assertFalse(isMounted('ext4.fs'))
  os.unlink('ext4.fs')
