#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to handle keyboard layout:
  - findCurrentKeymap
  - listAvailableKeymaps
  - isNumLockEnabledByDefault
  - isIbusEnabledByDefault
  - setDefaultKeymap
  - setNumLockDefault
  - setIbusDefault
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
import os
import re
import glob
from kernel import *
from chroot import *
from execute import checkRoot

_keymapsLocation = ['/usr/share/salixtools/keymaps', '/mnt/salt/lib/keymaps', 'keymaps']

def findCurrentKeymap(mountPoint = None):
  """
  Find the currently used console keymaps (as loaded by 'loadkeys') by looking in:
    - /etc/rc.d/rc.keymap, or
    - in the 'keyb=' kernel parameter
  The detected keymap is then checked against the first column of one of the files: {0}
  Returns None if not found
  """.format(' '.join(_keymapsLocation))
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  kmFile = None
  keymap = None
  for kml in _keymapsLocation:
    if mountPoint:
      kml = mountPoint + kml
    if os.path.isfile(kml):
      kmFile = kml
      break
  if kmFile:
    # first, try parsing /etc/rc.d/rc.keymap
    try:
      for line in open('{0}/etc/rc.d/rc.keymap'.format(mountPoint), 'rb').read().decode('utf8').splitlines():
        if '.map' in line:
          keymap = re.sub(r'^.* ([^ ]+)\.map$', r'\1', line)
          break
    except:
      pass
    if not keymap:
      # second, try to read from the kernel parmeters
      keybParam = getKernelParamValue('keyb')
      if keybParam:
        keymap = keybParam
  if keymap:
    # verify that the detected keymap actually exists
    if not keymap in [line.split('|', 1)[0] for line in open(kmFile, 'r').read().splitlines() if line and line[0] != '#']:
      keymap = None
  return keymap

def listAvailableKeymaps(mountPoint = None):
  """
  Returns a list of couple (keymap, keyboardType).
  'keymap' is a Console keymap as found in /usr/share/kbd/
  'keyboardType' is either 'azerty', 'qwerty', 'qwertz', etc and is there only for information
  The keymaps are extracted from one of the files: {0}
  """.format(' '.join(_keymapsLocation))
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  kmFile = None
  keymaps = []
  for kml in _keymapsLocation:
    if mountPoint:
      kml = mountPoint + kml
    if os.path.isfile(kml):
      kmFile = kml
      break
  if kmFile:
    for keymap in sorted([line.split('|', 1)[0] for line in open(kmFile, 'r').read().splitlines() if line and line[0] != '#']):
      keyboardType = '-'
      typePosition = 6 # usr/share/kbd/keymaps/i386/azerty => 6
      if mountPoint:
        typePosition += len(mountPoint.spli('/') - 1)
      kmPath = glob.glob('{0}/usr/share/kbd/keymaps/*/*/{1}.map.gz'.format(mountPoint, keymap))
      if kmPath:
        keyboardType = kmPath[0].split('/')[typePosition]
        if keyboardType == 'all':
          # then use the machine type ('mac' for example)
          keyboardType = kmPath[0].split('/')[typePosition - 1]
      keymaps.append((keymap, keyboardType))
  return keymaps

def isNumLockEnabledByDefault(mountPoint = None):
  """
  Returns True if the num lock is enabled by default.
  To do this, the execute bit of /etc/rc.d/rc.numlock is checked.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  return os.access('{0}/etc/rc.d/rc.numlock'.format(mountPoint), os.X_OK)

def isIbusEnabledByDefault(mountPoint = None):
  """
  Returns True if the IBus is enabled by default.
  To do this, the execute bit of /usr/bin/ibus-daemon and /etc/profile.d/ibus.sh are checked.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  return os.access('{0}/usr/bin/ibus-daemon'.format(mountPoint), os.X_OK) and os.access('{0}/etc/profile.d/ibus.sh'.format(mountPoint), os.X_OK)

def setDefaultKeymap(keymap, mountPoint = None):
  """
  Fix the configuration in /etc/rc.d/rc.keymap to use the specified 'keymap'.
  This uses 'keyboardsetup' Salix tool.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = '/'
  ret = execChroot(mountPoint, ['/usr/sbin/keyboardsetup', '-k', keymap, '-z'])
  # This has been forgotten in keyboardsetup
  os.chmod('{0}/etc/rc.d/rc.keymap'.format(mountPoint), 0755)
  return ret

def setNumLockDefault(enabled, mountPoint = None):
  """
  Fix the configuration for default numlock to be activated or not on boot.
  This uses 'keyboardsetup' Salix tool.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = '/'
  cmd = ['/usr/sbin/keyboardsetup', '-n']
  if enabled:
    cmd.append('on')
  else:
    cmd.append('off')
  cmd.append('-z') # must be last option because of a bug in keyboardsetup
  return execChroot(mountPoint, cmd)

def setIbusDefault(enabled, mountPoint = None):
  """
  Fix the configuration for default Ibus activated on boot or not.
  This uses 'keyboardsetup' Salix tool.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = '/'
  cmd = ['/usr/sbin/keyboardsetup', '-i']
  if enabled:
    cmd.append('on')
  else:
    cmd.append('off')
  cmd.append('-z') # must be last option because of a bug in keyboardsetup
  return execChroot(mountPoint, cmd)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
  keymaps = listAvailableKeymaps()
  assertTrue(type(keymaps) == list)
  assertTrue(len(keymaps) > 0)
  keymaps = dict(keymaps) # change it to dictionnary
  assertEquals('azerty', keymaps['fr-latin9'])
  keymap = findCurrentKeymap()
  assertTrue(keymap)
  numlock = isNumLockEnabledByDefault()
  assertTrue(type(numlock) == bool)
  ibus = isIbusEnabledByDefault()
  assertTrue(type(ibus) == bool)
  assertEquals(0, setDefaultKeymap('fr-latin1'))
  assertEquals('fr-latin1', findCurrentKeymap())
  assertEquals(0, setNumLockDefault(True))
  assertTrue(isNumLockEnabledByDefault())
  assertEquals(0, setIbusDefault(True))
  assertTrue(isIbusEnabledByDefault())
  # restore actual keyboard parameters
  setDefaultKeymap(keymap)
  setNumLockDefault(numlock)
  setIbusDefault(ibus)
