#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Calculate some size and free size of folders and mount points.
Functions:
  - getHumanSize
  - getBlockSize
  - getSizes
  - getUsedSize
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
import re
import os
from stat import *
from execute import *

def _getMountPoint(device):
  """
  Finds the mount point of 'device' or None if not mounted
  Copied from 'mounting' module to break circular dependencies
  """
  mountpoint = None
  for line in execGetOutput('mount', shell = False):
    p, _, mp, _ = line.split(' ', 3) # 3 splits max, _ is discarded
    if os.path.islink(p):
      p = os.path.realpath(p)
    if p == device:
      mountpoint = mp
      break
  return mountpoint

def getHumanSize(size):
  """
  Returns the human readable format of the size in bytes
  """
  units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  unit = 0
  sizeHuman = float(size)
  while sizeHuman > 1024 and unit < len(units) - 1:
    unit += 1
    sizeHuman = sizeHuman / 1024
  return "{0:.1f}{1}".format(sizeHuman, units[unit])

def getBlockSize(path):
  """
  Returns the block size of the underlying filesystem denoted by 'path'.
  """
  if S_ISBLK(os.stat(path).st_mode):
    lines = execGetOutput(['/sbin/blockdev', '--getbsz', path], shell = False)
    if lines:
      blockSize = int(lines[0])
    else:
      blockSize = None
  else:
    st = os.statvfs(path)
    blockSize = st.f_frsize
  return blockSize

def getSizes(path, withHuman = True):
  """
  Computes the different sizes of the fileystem denoted by path (either a device or a file in filesystem).
  Return the following sizes (in a dictionary):
    - size (total size)
    - free (total free size)
    - uuFree (free size for unprivileged users)
    - used (size - free)
    - uuUsed (size - uuFree)
  + all of them with the corresponding 'Human' suffix.
  """
  if S_ISBLK(os.stat(path).st_mode):
    mountpoint = _getMountPoint(path)
    if mountpoint:
      # mounted, so will use mountpoint to get information about different sizes
      path = mountpoint
    else:
      # not mounted, so only the full size could be get
      diskDevice = re.sub(r'^.*/([^/]+?)[0-9]*$', r'\1', path)
      device = re.sub(r'^.*/([^/]+)$', r'\1', path)
      blockSize = int(open('/sys/block/{0}/queue/logical_block_size'.format(diskDevice), 'r').read().strip())
      size = int(open('/sys/class/block/{0}/size'.format(device), 'r').read().strip()) * blockSize
      return {
          'size':size, 'sizeHuman':getHumanSize(size),
          'free':None, 'freeHuman':None,
          'uuFree':None, 'uuFreeHuman':None,
          'used':None, 'usedHuman':None,
          'uuUsed':None, 'uuUsedHuman':None
        }
  st = os.statvfs(path)
  size = st.f_blocks * st.f_frsize
  free = st.f_bfree * st.f_frsize
  uuFree = st.f_bavail * st.f_frsize # free size for unpriviliedge users
  used = size - free
  uuUsed = size - uuFree # used size appear differently for commun users than from root user
  if withHuman:
    return {
        'size':size, 'sizeHuman':getHumanSize(size),
        'free':free, 'freeHuman':getHumanSize(free),
        'uuFree':uuFree, 'uuFreeHuman':getHumanSize(uuFree),
        'used':used, 'usedHuman':getHumanSize(used),
        'uuUsed':uuUsed, 'uuUsedHuman':getHumanSize(uuUsed)
      }
  else:
    return {
        'size':size, 'sizeHuman':None,
        'free':free, 'freeHuman':None,
        'uuFree':uuFree, 'uuFreeHuman':None,
        'used':used, 'usedHuman':None,
        'uuUsed':uuUsed, 'uuUsedHuman':None
      }

def getUsedSize(path, blocksize = None, withHuman = True):
  """
  Returns the size of the space used by files and folders under 'path'.
  If 'blocksize' is specified, mimic the space that will be used if the blocksize of the underlying filesystem where the one specified.
  This could be useful if used to transfer files from one directory to another when the target filesystem use another blocksize.
  Returns a tuple with (size, sizeHuman)
  """
  if blocksize:
    cmd = """echo $((($(find '{0}' -type f -print0 | du -l -B {1} --files0-from=- | cut -f1 | tr "\\n" "+")0)*{1}))""".format(path, blocksize)
    lines = execGetOutput(cmd, shell = True)
    size = lines[-1]
  else:
    cmd = ['/bin/du', '-c', '-s', '-B', '1', path]
    lines = execGetOutput(cmd, shell = False)
    size, _ = lines[-1].split()
  size = int(size)
  if withHuman:
    return {'size':size, 'sizeHuman':getHumanSize(size)}
  else:
    return {'size':size, 'sizeHuman':None}

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertEquals('7.4GB', getHumanSize(7923593216L))
  print '/'
  stats = getSizes('/')
  print stats
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] > 0)
  assertTrue(stats['uuFree'] > 0)
  assertTrue(stats['used'] > 0)
  assertTrue(stats['uuUsed'] > 0)
  print '/dev/sda1'
  stats = getSizes('/dev/sda1') # mounted
  print stats
  assertTrue(stats['size'] > 0)
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] > 0)
  assertTrue(stats['uuFree'] > 0)
  assertTrue(stats['used'] > 0)
  assertTrue(stats['uuUsed'] > 0)
  print '/dev/sda2'
  stats = getSizes('/dev/sda2') # extended partition, could never have been mounted
  print stats
  assertTrue(stats['size'] > 0)
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] == None)
  assertTrue(stats['uuFree'] == None)
  assertTrue(stats['used'] == None)
  assertTrue(stats['uuUsed'] == None)
  print 'getUsedSize(.)'
  stats1 = getUsedSize('.')
  print stats1
  assertTrue(stats1['size'] > 0)
  print 'getUsedSize(., 524288)'
  stats2 = getUsedSize('.', 524288)
  print stats2
  assertTrue(stats2['size'] > 0)
  assertTrue(stats2['size'] > stats1['size'])
