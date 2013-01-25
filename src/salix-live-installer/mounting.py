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
from execute import *
import os
from stat import *

def getMountPoint(device):
  """
  Will find the mount point to this 'device' or None if not mounted.
  """
  mountpoint = None
  if S_ISBLK(os.stat(device).st_mode):
    for line in open('/proc/mounts').read().splitlines():
      p, mp, _ = line.split(' ', 2) # 2 splits max, _ is discarded
      if os.path.islink(p):
        p = os.path.realpath(p)
      if p == device:
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

def mountDevice(device, fsType, mountPoint = None):
  """
  Mount the 'device' of 'fsType' filesystem under 'mountPoint'.
  If 'mountPoint' is not specified, '/mnt/.temp/device' will be used.
  Returns False if it fails.
  """
  if not mountPoint:
    mountPoint = '/mnt/.temp/{0}'.format(device)
    if os.path.exists(mountPoint):
      return False
  if not os.path.exists(mountPoint):
    os.path.makedirs(mountPoint)
  return execCall(['mount', '-t', fsType, device, path])

def umountDevice(deviceOrPath, tryLazyUmount = True, deleteMountPoint = True):
  """
  Umount the 'deviceOrPath' which could be a device or a mount point.
  If the umount failed, try again with a lazyUmount if 'tryLazyUmount' is True.
  Will delete the mount point if 'deleteMountPoint' is True.
  Returns False if it fails.
  """
  if S_ISBLK(os.stat(device).st_mode):
    path = getMountPoint(device)
  else:
    path = deviceOrPath
  if os.path.ismounted(path):
    ret = execCall(['umount', path])
    if not ret:
      ret = execCall(['umount', '-l', path])
    if ret and deleteMountPoint:
      # delete the empty directory
      try:
        os.rmdir(path)
      except:
        pass
      # delete the temporary directory if not empty
      if os.path.isdir('/mnt/.temp'):
        try:
          os.rmdir('/mnt/.temp')
        except:
          pass
    return ret
  else:
    return False

# Unit test
if __name__ == '__main__':
  from assertPlus import *
