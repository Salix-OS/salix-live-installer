#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to generate fstab entries:
  - createFsTab
  - addFsTabEntry
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *
import os

def createFsTab(fstabMountPoint):
  """
  Generates an empty /etc/fstab file
  """
  try:
    os.mkdir('{0}/etc'.format(fstabMountPoint))
  except:
    pass
  open('{0}/etc/fstab'.format(fstabMountPoint), 'w').close()

def addFsTabEntry(fstabMountPoint, device, mountPoint, fsType = None, options = None, dumpFlag = 0, fsckOrder = 0):
  """
  Add a line to /etc/fstab
  If fsType is None, then it will be guessed from the device by using blkid
  If options is None, then it will be guessed from the fsType like this:
    - 'proc', 'sysfs', 'devpts', 'tmpfs', 'swap' |=> 'defaults'
    - 'ext2', 'ext3', 'ext4', 'xfs', 'reiserfs', 'btrfs', 'jfs' |=> 'defaults,noatime'
    - 'ntfs' |=> 'umask=000'
    - 'vfat' |=> 'defaults,utf8,umask=0,shortname=mixed'
  """
  if not fsType:
    lines = execGetOutput(['/sbin/blkid', '-c', '/dev/null', '-s', 'TYPE', '-o', 'value', device])
    if len(lines) > 0:
      fsType = lines[0]
    else:
      raise IOError('Cannot determine the filesystem of {0}'.format(device))
  if not options:
    defaultOptions = {
        'def':'defaults',
        'linux':'defaults,noatime',
        'ntfs':'umask=000',
        'fat':'defaults,utf8,umask=0,shortname=mixed'
      }
    defaultOptionsPerFs = {
        'proc':'def', 'sysfs':'def', 'devpts':'def', 'tmpfs':'def', 'swap':'def',
        'ext2':'linux', 'ext3':'linux', 'ext4':'linux', 'xfs':'linux', 'reiserfs':'linux', 'btrfs':'linux', 'jfs':'linux',
        'ntfs':'ntfs',
        'vfat':'fat'
      }
    if fsType in defaultOptionsPerFs:
      options = defaultOptions[defaultOptionsPerFs[fsType]]
    else:
      options = defaultOptions['def']
  if fsType == 'ntfs':
    fsType = 'ntfs-3g'
  fp = open('{0}/etc/fstab'.format(fstabMountPoint), 'a')
  fp.write('{device:20}{mountPoint:20}{fsType:15}{options:20}{dumpFlag:10}{fsckOrder:2}\n'.format(device = device, mountPoint = mountPoint, fsType = fsType, options = options, dumpFlag = dumpFlag, fsckOrder = fsckOrder))
  fp.close()

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
  if os.path.exists('./etc/fstab'):
    try:
      os.unlink('./etc/fstab')
      os.rmdir('./etc')
    except:
      pass
  createFsTab('.')
  assertTrue(os.path.exists('./etc/fstab'))
  addFsTabEntry('.', '/dev/sda1', '/', 'ext4', 'defaults', 1, 1)
  addFsTabEntry('.', '/dev/sda1', '/root', None, None, 1, 2)
  lines = open('./etc/fstab', 'r').read().splitlines()
  assertEquals(2, len(lines))
  line1, line2 = lines
  dev, mp, fs, opts, dump, fsck = line1.split()
  assertEquals('/dev/sda1', dev)
  assertEquals('/', mp)
  assertEquals('ext4', fs)
  assertEquals('defaults', opts)
  assertEquals('1', dump)
  assertEquals('1', fsck)
  dev, mp, fs, opts, dump, fsck = line2.split()
  assertEquals('/dev/sda1', dev)
  assertEquals('/root', mp)
  assertTrue(len(fs) > 0)
  assertTrue(len(opts) > 0)
  assertEquals('1', dump)
  assertEquals('2', fsck)
  try:
    os.unlink('./etc/fstab')
    os.rmdir('./etc')
  except:
    pass
