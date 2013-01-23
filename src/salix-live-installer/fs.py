#!/usr/bin/env python
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
from execute import *
import os
from stat import *
import re

def getFsType(partitionDevice):
  """
  Returns the file system type for that partition.
  'partitionDevice' should no be prefilled with '/dev/'.
  Returns 'Extended' if the partition is an extended partition and has no filesystem.
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/%s' % partitionDevice).st_mode):
    try:
      fstype = execGetOutput(['/sbin/blkid', '-c', '/dev/null', '-s', 'TYPE', '-o', 'value', '/dev/%s' % partitionDevice])[0]
    except subprocess.CalledProcessError as e:
      fstype = 'Extended'
  else:
    fstype = False
  return fstype

def getFsLabel(partitionDevice):
  """
  Returns the label for that partition (if any).
  'partitionDevice' should no be prefilled with '/dev/'.
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/%s' % partitionDevice).st_mode):
    try:
      label = execGetOutput(['/sbin/blkid', '-c', '/dev/null', '-s', 'LABEL', '-o', 'value', '/dev/%s' % partitionDevice])[0]
    except subprocess.CalledProcessError as e:
      label = ''
  else:
    label = False
  return label

def makeFs(partitionDevice, fsType, label=None, options=None, force=False):
  """
  Creates a filesystem on the device.
  'partitionDevice' should no be prefilled with '/dev/'.
  'fsType' could be ext2, ext3, ext4, xfs, reiserfs, jfs, btrfs, ntfs, fat16, fat32, swap
  Use 'options' to force passing these options to the creation process (use a list)
  Use 'force=True' if you want to force creating the filesystem and if 'partitionDevice' is a full path to a file (not a block device).
  """
  if force and os.path.exists(partitionDevice):
    path = partitionDevice
  else:
    path = '/dev/{0}'.format(partitionDevice)
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
  "ExtX block size: 4k per default in /etc/mke2fs.conf"
  cmd = '/sbin/mkfs.ext{0:d}'.format(version)
  if not options:
    options = []
  if label:
    if len(label) > 16: # max 16 bytes
      label = label[0:15]
    options.append('-L')
    options.append(label)
  if force:
    options.append('-F')
  return execCall([cmd].extend(options))

def _makeXfs(path, label, options, force):
  "http://blog.peacon.co.uk/wiki/Creating_and_Tuning_XFS_Partitions"
  cmd = '/sbin/mkfs.xfs'
  if not options:
    options = ['-l', 'size=64m,lazy-count=1', '-f']
    # -f is neccessary to have this or you cannot create XFS on a non-empty partition or disk
  if label:
    if len(label) > 12: # max 12 chars
      label = label[0:11]
    options.append('-L')
    options.append(label)
  return execCall([cmd].extend(options))

def _makeReiserfs(path, label, options, force):
  cmd = '/sbin/mkfs.reiserfs'
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
  return execCall([cmd].extend(options))

def _makeJfs(path, label, options, force):
  cmd = '/sbin/mkfs.jfs'
  if not options:
    options = ['-f'] # if not specified, will ask to continue
  if label:
    if len(label) > 16: # max 16 chars
      label = label[0:15]
    options.append('-L')
    options.append(label)
  if force:
    pass # no need to do anything
  return execCall([cmd].extend(options))

def _makeBtrfs(path, label, options, force):
  cmd = '/sbin/mkfs.btrfs'
  if not options:
    options = []
  if label:
    options.append('-L')
    options.append(label) # no restriction on size
  if force:
    pass # no need to do anything
  return execCall([cmd].extend(options))

def _makeNtfs(path, label, options, force):
  cmd = '/sbin/mkfs.ntfs'
  if not options:
    options = ['-Q']
  if label:
    if len(label) > 32: # 32 chars max
      label = label[0:31]
    options.append('-L')
    options.append(label)
  if force:
    options.append('-F')
  return execCall([cmd].extend(options))

def _makeFat(path, is32, label, options, force):
  cmd = '/sbin/mkfs.vfat'
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
  return execCall([cmd].extend(options))

def _makeSwap(path, label, options, force):
  cmd = '/sbin/mkswap'
  if not options:
    options = ['-f'] # it is neccessary to have this or you cannot create a swap on a non-empty partition or disk
  if label:
    options.append('-L') # I didn't find any restriction in the label size
    options.append(label)
  if force:
    pass # nothing to do, writing to a file is always ok
  return execCall([cmd].extend(options))

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
  # TODO : add Unit Test for making filesystems
