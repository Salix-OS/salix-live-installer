#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Get information of the disks and partitions in the system.
For now it only handles (S/P)ATA disks and partitions. RAID and LVM are not supported.
/proc and /sys should be mounted for getting information
Functions:
  - getDisks
  - getDiskInfo
  - getPartitions
  - getSwapPartitions
  - getPartitionInfo
"""
from execute import *
from fs import *
from freesize import *
import glob
import re
import os
from stat import *

def getDisks():
  "Returns the disks devices (without /dev/) connected to the computer. RAID and LVM are not supported yet."
  return execGetOutput(['sed', '-n', '/ sd[^0-9]\+$/ s/.*\(sd.*\)/\\1/ p', '/proc/partitions'])

def getDiskInfo(diskDevice):
  """
  Returns a dictionary with the model name, size in bytes, size in human and if is removable for the disk device.
  diskDevice should no be prefilled with '/dev/'
  dictionary key: model, size, sizeHuman, removable
  """
  if S_ISBLK(os.stat('/dev/%s' % diskDevice).st_mode):
    modelName = open('/sys/block/%s/device/model' % diskDevice, 'r').read().strip()
    blockSize = int(open('/sys/block/%s/queue/logical_block_size' % diskDevice, 'r').read().strip())
    size = int(open('/sys/block/%s/size' % diskDevice, 'r').read().strip()) * blockSize
    sizeHuman = getHumanSize(size)
    try:
      removable = int(open('/sys/block/%s/removable' % diskDevice, 'r').read().strip()) == 1
    except:
      removable = False
    return {'model':modelName, 'size':size, 'sizeHuman':sizeHuman, 'removable':removable}
  else:
    return None

def getPartitions(diskDevice, skipExtended = True, skipSwap = True):
  """
  Returns partitions following exclusion filters.
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/%s' % diskDevice).st_mode):
    parts = [p.replace('/sys/block/%s/' % diskDevice, '') for p in glob.glob('/sys/block/%s/%s*' % (diskDevice, diskDevice))]
    fsexclude = []
    if skipExtended:
      fsexclude.append('Extended')
    if skipSwap:
      fsexclude.append('swap')
    return [part for part in parts if getFsType(part) not in fsexclude]
  else:
    return None

def getSwapPartitions():
  """
  Returns partition devices that are of type Linux Swap.
  """
  checkRoot()
  for diskDevice in getDisks():
    parts = [p.replace('/sys/block/%s/' % diskDevice, '') for p in glob.glob('/sys/block/%s/%s*' % (diskDevice, diskDevice))]
    return [part for part in parts if getFsType(part) == 'swap']

def getPartitionInfo(partitionDevice):
  """
  Returns a dictionary of partion information:
    - fstype
    - label
    - size
    - sizeHuman
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/%s' % partitionDevice).st_mode):
    fstype = getFsType(partitionDevice)
    label = getFsLabel(partitionDevice)
    diskDevice = re.sub('[0-9]*', '', partitionDevice)
    blockSize = int(open('/sys/block/%s/queue/logical_block_size' % diskDevice, 'r').read().strip())
    size = int(open('/sys/block/%s/%s/size' % (diskDevice, partitionDevice), 'r').read().strip()) * blockSize
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
