#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Get information about filesystem, create them, ...
For now it only handles (S/P)ATA disks and partitions. RAID and LVM are not supported.
/proc and /sys should be mounted for getting information
Functions:
  - getFsType
  - getFsLabel
  - makeFs
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *
from freesize import getSizes
import os
from stat import *
import re

def getFsType(partitionDevice):
  """
  Returns the file system type for that partition.
  'partitionDevice' should no be prefixed with '/dev/' if it's a block device.
  It can be a full path if the partition is contained in a file.
  Returns 'Extended' if the partition is an extended partition and has no filesystem.
  """
  if os.path.exists('/dev/{0}'.format(partitionDevice)) and S_ISBLK(os.stat('/dev/{0}'.format(partitionDevice)).st_mode):
    path = '/dev/{0}'.format(partitionDevice)
  elif os.path.isfile(partitionDevice):
    path = partitionDevice
  else:
    fstype = False
    path = False
  if path:
    try:
      fstype = execGetOutput(['/sbin/blkid', '-s', 'TYPE', '-o', 'value', path], shell = False)
      if fstype:
        fstype = fstype[0]
      else:
        fstype = False
    except subprocess.CalledProcessError as e:
      fstype = False
    if not fstype:
      # is it a real error or is it an extended partition?
      try:
        filetype = execGetOutput(['/usr/bin/file', '-s', path], shell = False)
        if 'extended partition table' in filetype:
          fstype = 'Extended'
      except subprocess.CalledProcessError:
        pass
  return fstype

def getFsLabel(partitionDevice):
  """
  Returns the label for that partition (if any).
  'partitionDevice' should no be prefixed with '/dev/' if it is a block device.
  It can be a full path if the partition is contained in a file.
  """
  if os.path.exists('/dev/{0}'.format(partitionDevice)) and S_ISBLK(os.stat('/dev/{0}'.format(partitionDevice)).st_mode):
    path = '/dev/{0}'.format(partitionDevice)
  elif os.path.isfile(partitionDevice):
    path = partitionDevice
  else:
    label = False
    path = False
  if path:
    try:
      label = execGetOutput(['/sbin/blkid', '-s', 'LABEL', '-o', 'value', path], shell = False)
      if label:
        label = label[0]
      else:
        label = ''
    except subprocess.CalledProcessError as e:
      label = False
  return label

def makeFs(partitionDevice, fsType, label=None, force=False, options=None):
  """
  Creates a filesystem on the device.
  'partitionDevice' should no be prefixed with '/dev/' if it is a block device.
  'fsType' could be ext2, ext3, ext4, xfs, reiserfs, jfs, btrfs, ntfs, fat16, fat32, swap
  Use 'force=True' if you want to force the creation of the filesystem and if 'partitionDevice' is a full path to a file (not a block device).
  Use 'options' to force these options on the creation process (use a list)
  """
  if force and os.path.exists(partitionDevice):
    path = partitionDevice
  else:
    path = '/dev/{0}'.format(partitionDevice)
    if not os.path.exists(path):
      raise IOError('{0} does not exist'.format(path))
    if not S_ISBLK(os.stat(path).st_mode):
      raise IOError('{0} is not a block device'.format(path))
  if fsType not in ('ext2', 'ext3', 'ext4', 'xfs', 'reiserfs', 'jfs', 'btrfs', 'ntfs', 'fat16', 'fat32', 'swap'):
    raise Exception('{0} is not a recognized filesystem.'.format(fsType))
  if fsType in ('ext2', 'ext3', 'ext4'):
    return _makeExtFs(path, int(fsType[3]), label, options, force)
  elif fsType == 'xfs':
    return _makeXfs(path, label, options, force)
  elif fsType == 'reiserfs':
    return _makeReiserfs(path, label, options, force)
  elif fsType == 'jfs':
    return _makeJfs(path, label, options, force)
  elif fsType == 'btrfs':
    return _makeBtrfs(path, label, options, force)
  elif fsType == 'ntfs':
    return _makeNtfs(path, label, options, force)
  elif fsType in ('fat16', 'fat32'):
    return _makeFat(path, fsType == 'fat32', label, options, force)
  elif fsType == 'swap':
    return _makeSwap(path, label, options, force)
  return None # should not append

def _makeExtFs(path, version, label, options, force):
  """
  ExtX block size: 4k per default in /etc/mke2fs.conf
  """
  cmd = ['/sbin/mkfs.ext{0:d}'.format(version)]
  if not options:
    options = []
  if label:
    if len(label) > 16: # max 16 bytes
      label = label[0:15]
    options.append('-L')
    options.append(label)
  if force:
    options.append('-F')
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeXfs(path, label, options, force):
  """
  http://blog.peacon.co.uk/wiki/Creating_and_Tuning_XFS_Partitions
  """
  cmd = ['/sbin/mkfs.xfs']
  if not options:
    options = ['-f'] # -f is neccessary to have this or you cannot create XFS on a non-empty partition or disk
    if os.path.isfile(path):
      size = os.stat(path).st_size
    else:
      size = getSizes(path)['size']
    if size > 104857600: # > 100M
      options.extend(['-l', 'size=64m,lazy-count=1']) # optimizations
  if label:
    if len(label) > 12: # max 12 chars
      label = label[0:11]
    options.append('-L')
    options.append(label)
  cmd.extend(options)
  cmd.append(path)
  print 'cmd={0}'.format(cmd)
  return execCall(cmd, shell = False)

def _makeReiserfs(path, label, options, force):
  cmd = ['/sbin/mkfs.reiserfs']
  if not options:
    options = []
  if label:
    if len(label) > 16: # max 16 chars
      label = label[0:15]
    options.append('-l')
    options.append(label)
  if force:
    options.append('-f')
    options.append('-f') # twice for no confirmation
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeJfs(path, label, options, force):
  cmd = ['/sbin/mkfs.jfs']
  if not options:
    options = ['-f'] # if not specified, will ask to continue
  if label:
    if len(label) > 16: # max 16 chars
      label = label[0:15]
    options.append('-L')
    options.append(label)
  if force:
    pass # no need to do anything
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeBtrfs(path, label, options, force):
  cmd = ['/sbin/mkfs.btrfs']
  if not options:
    options = []
  if label:
    options.append('-L')
    options.append(label) # no restriction on size
  if force:
    pass # no need to do anything
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeNtfs(path, label, options, force):
  cmd = ['/sbin/mkfs.ntfs']
  if not options:
    options = ['-Q']
  if label:
    if len(label) > 32: # 32 chars max
      label = label[0:31]
    options.append('-L')
    options.append(label)
  if force:
    options.append('-F')
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeFat(path, is32, label, options, force):
  cmd = ['/sbin/mkfs.vfat']
  if is32:
    size = ['-F', '32']
  else:
    size = ['-F', '16']
  if not options:
    options = size
  else:
    options.extend(size)
  if label:
    if len(label) > 11: # 8+3 bytes max
      label = label[0:10]
    options.append('-n')
    options.append(label)
  if force:
    options.append('-I') # permit to use whole disk
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

def _makeSwap(path, label, options, force):
  cmd = ['/sbin/mkswap']
  if not options:
    options = ['-f'] # it is neccessary to have this or you cannot create a swap on a non-empty partition or disk
  if label:
    options.append('-L') # I didn't find any restriction in the label size
    options.append(label)
  if force:
    pass # nothing to do, writing to a file is always ok
  cmd.extend(options)
  cmd.append(path)
  return execCall(cmd, shell = False)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  part = 'sda1'
  fstype = getFsType(part)
  label = getFsLabel(part)
  print '{0}: {1} ({2})'.format(part, fstype, label)
  assertTrue(fstype)
  assertTrue(len(fstype) > 0)
  assertTrue(label)
  assertTrue(len(label) > 0)
  for ft in ('ext2', 'ext4', 'xfs', 'reiserfs', 'jfs', 'btrfs', 'ntfs', 'fat16', 'fat32', 'swap'):
    f = '{0}.fs'.format(ft)
    if ft == 'btrfs':
      size = 300 # btrfs minimum size is 256M
    else:
      size = 50
    execCall(['dd', 'if=/dev/zero', 'of={0}'.format(f), 'bs=1M', 'count={0:d}'.format(size)], shell = False)
    assertEquals(0, makeFs(f, ft, 'test_{0}'.format(ft), True))
    if ft in ('fat16', 'fat32'):
      expectedFt = 'vfat'
    else:
      expectedFt = ft
    assertEquals(expectedFt, getFsType(f))
    assertEquals('test_{0}'.format(ft), getFsLabel(f))
    os.unlink(f)
