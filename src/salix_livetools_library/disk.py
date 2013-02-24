#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Get information from the system disks and partitions.
For now it only handles (S/P)ATA disks and partitions, RAID and LVM are not supported yet.
/proc and /sys should be mounted to retrieve information.
Functions:
  - getDisks
  - getDiskInfo
  - getPartitions
  - getSwapPartitions
  - getPartitionInfo
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *
from fs import *
from freesize import *
import glob
import re
import os
from stat import *

def getDisks():
  """
  Returns the disks devices (without /dev/) connected to the computer. 
  RAID and LVM are not supported yet.
  """
  ret = []
  for l in open('/proc/partitions', 'r').read().splitlines():
    if re.search(r' sd[^0-9]+$', l):
      ret.append(re.sub(r'.*(sd.*)', r'\1', l))
  return ret

def getDiskInfo(diskDevice):
  """
  Returns a dictionary with the following disk device's info:
    - model: model name
    - size: size in bytes
    - sizeHuman: human readable size
    - removable: whether it is removable or not
  diskDevice should no be prefixed with '/dev/'
  """
  if S_ISBLK(os.stat('/dev/{0}'.format(diskDevice)).st_mode):
    modelName = open('/sys/block/{0}/device/model'.format(diskDevice), 'r').read().strip()
    blockSize = int(open('/sys/block/{0}/queue/logical_block_size'.format(diskDevice), 'r').read().strip())
    size = int(open('/sys/block/{0}/size'.format(diskDevice), 'r').read().strip()) * blockSize
    sizeHuman = getHumanSize(size)
    try:
      removable = int(open('/sys/block/{0}/removable'.format(diskDevice), 'r').read().strip()) == 1
    except:
      removable = False
    return {'model':modelName, 'size':size, 'sizeHuman':sizeHuman, 'removable':removable}
  else:
    return None

def getPartitions(diskDevice, skipExtended = True, skipSwap = True):
  """
  Returns partitions matching exclusion filters.
  """
  if S_ISBLK(os.stat('/dev/{0}'.format(diskDevice)).st_mode):
    parts = [p.replace('/sys/block/{0}/'.format(diskDevice), '') for p in glob.glob('/sys/block/{0}/{0}*'.format(diskDevice))]
    fsexclude = [False]
    if skipExtended:
      fsexclude.append('Extended')
    if skipSwap:
      fsexclude.append('swap')
    return [part for part in parts if getFsType(part) not in fsexclude]
  else:
    return None

def getSwapPartitions():
  """
  Returns partition devices with Linux Swap type.
  """
  ret = []
  for diskDevice in getDisks():
    parts = [p.replace('/sys/block/{0}/'.format(diskDevice), '') for p in glob.glob('/sys/block/{0}/{0}*'.format(diskDevice))]
    ret.extend([part for part in parts if getFsType(part) == 'swap'])
  return ret

def getPartitionInfo(partitionDevice):
  """
  Returns a dictionary with the partition information:
    - fstype
    - label
    - size
    - sizeHuman
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/{0}'.format(partitionDevice)).st_mode):
    fstype = getFsType(partitionDevice)
    label = getFsLabel(partitionDevice)
    diskDevice = re.sub('[0-9]*', '', partitionDevice)
    blockSize = int(open('/sys/block/{0}/queue/logical_block_size'.format(diskDevice), 'r').read().strip())
    size = int(open('/sys/block/{0}/{1}/size'.format(diskDevice, partitionDevice), 'r').read().strip()) * blockSize
    sizeHuman = getHumanSize(size)
    return {'fstype':fstype, 'label':label, 'size':size, 'sizeHuman':sizeHuman}
  else:
    return None

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
  disks = getDisks()
  assertTrue(len(disks) > 0)
  assertEquals('sda', disks[0])
  diskInfo = getDiskInfo('sda')
  assertTrue(diskInfo['model'] != '')
  assertTrue(diskInfo['size'] > 0)
  assertTrue('B' in diskInfo['sizeHuman'])
  assertFalse(diskInfo['removable'])
  assertTrue(len(getPartitions('sda')) > 0)
  assertTrue(len(getSwapPartitions()) > 0)
  partInfo = getPartitionInfo('sda1')
  assertTrue(partInfo['fstype'] != '')
  assertTrue(partInfo['label'] != '')
  assertTrue(partInfo['size'] > 0)
  assertTrue('B' in partInfo['sizeHuman'])
