#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Calculate some size and free size of folders and mount points.
Functions:
  - getHumanSize
  - getSizes
"""
import re
import os
from stat import *

def getHumanSize(size):
  "Returns the human readable format of the size in bytes"
  units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
  unit = 0
  sizeHuman = float(size)
  while sizeHuman > 1024 and unit < len(units) - 1:
    unit += 1
    sizeHuman = sizeHuman / 1024
  return "%.1f%s" % (sizeHuman, units[unit])

def getSizes(path):
  """
  Returns the following sizes (in a dictionary):
    - size (total size)
    - free (total free size)
    - uuFree (free size for unprivileged users)
    - used (size - free)
    - uuUsed (size - uuFree)
  + all of them with the corresponding 'Human' suffix.
  """
  if S_ISBLK(os.stat(path).st_mode):
    mountpoint = None
    for line in open('/proc/mounts').read().splitlines():
      p, mp, _ = line.split(' ', 2) # 2 splits max, _ is discarded
      if p == path:
        mountpoint = mp
        break
    if mountpoint:
      # mounted, so will use mountpoint to get information about different sizes
      path = mountpoint
    else:
      # not mounted, so only the full size could be get
      diskDevice = re.sub(r'^.*/([^/]+?)[0-9]*$', r'\1', path)
      device = re.sub(r'^.*/([^/]+)$', r'\1', path)
      blockSize = int(open('/sys/block/%s/queue/logical_block_size' % diskDevice, 'r').read().strip())
      size = int(open('/sys/class/block/%s/size' % device, 'r').read().strip()) * blockSize
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
  return {
      'size':size, 'sizeHuman':getHumanSize(size),
      'free':free, 'freeHuman':getHumanSize(free),
      'uuFree':uuFree, 'uuFreeHuman':getHumanSize(uuFree),
      'used':used, 'usedHuman':getHumanSize(used),
      'uuUsed':uuUsed, 'uuUsedHuman':getHumanSize(uuUsed)
    }

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertEquals('7.4GB', getHumanSize(7923593216L))
  stats = getSizes('/')
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] > 0)
  assertTrue(stats['uuFree'] > 0)
  assertTrue(stats['used'] > 0)
  assertTrue(stats['uuUsed'] > 0)
  stats = getSizes('/dev/sda1')
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] > 0)
  assertTrue(stats['uuFree'] > 0)
  assertTrue(stats['used'] > 0)
  assertTrue(stats['uuUsed'] > 0)
  stats = getSizes('/dev/sda5') # extended partition, could never have been mounted
  assertTrue(stats['size'] > 0)
  assertTrue(stats['free'] == None)
  assertTrue(stats['uuFree'] == None)
  assertTrue(stats['used'] == None)
  assertTrue(stats['uuUsed'] == None)
