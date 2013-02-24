#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to handle time zones:
  - listTimeZones
  - listTZContinents
  - listTZCities
  - getDefaultTimeZone
  - setDefaultTimeZone
  - isNTPEnabledByDefault
  - setNTPDefault
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
import os
import glob
import re
from shutil import copyfile
from execute import checkRoot

def listTimeZones(mountPoint = None):
  """
  Returns a dictionary of time zones, by continent.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  tz = {}
  for z in listTZContinents(mountPoint):
    tz[z] = listTZCities(z, mountPoint)
  return tz

def listTZContinents(mountPoint = None):
  """
  Returns a sorted list of continents for time zones.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  return sorted(map(os.path.basename, filter(lambda f: os.path.isdir(f), glob.glob('{0}/usr/share/zoneinfo/[A-Z]*'.format(mountPoint)))))

def listTZCities(continent, mountPoint = None):
  """
  Returns a sorted list of cities for a specific continent's time zone.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  if os.path.isdir('{0}/usr/share/zoneinfo/{1}'.format(mountPoint, continent)):
    return sorted(map(os.path.basename, glob.glob('{0}/usr/share/zoneinfo/{1}/*'.format(mountPoint, continent))))
  else:
    return None

def getDefaultTimeZone(mountPoint = None):
  """
  Returns the default time zone, by reading the /etc/localtime-copied-from symlink.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  tz = None
  if os.path.islink('{0}/etc/localtime-copied-from'.format(mountPoint)):
    tz = re.sub(r'/usr/share/zoneinfo/', '', os.readlink('{0}/etc/localtime-copied-from'.format(mountPoint)))
  return tz

def setDefaultTimeZone(timezone, mountPoint = None):
  """
  Set the default time zone, by copying the correct time zone to /etc/localtime and by setting the /etc/localtime-copied-from symlink.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  checkRoot()
  if '/' in timezone and len(timezone.split('/')) == 2 and os.path.isfile('{0}/usr/share/zoneinfo/{1}'.format(mountPoint, timezone)):
    copyfile('{0}/usr/share/zoneinfo/{1}'.format(mountPoint, timezone), '{0}/etc/localtime'.format(mountPoint))
    if os.path.exists('{0}/etc/localtime-copied-from'.format(mountPoint)):
      os.unlink('{0}/etc/localtime-copied-from'.format(mountPoint))
    os.symlink('/usr/share/zoneinfo/{0}'.format(timezone), '{0}/etc/localtime-copied-from'.format(mountPoint))
  else:
    raise Exception('This time zone: ({0}), is incorrect.'.format(timezone))

def isNTPEnabledByDefault(mountPoint = None):
  """
  ReturnsTrue if the NTP service is enabled by default.
  To do this, the execute bit of /etc/rc.d/rc.ntpd is checked.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  return os.access('{0}/etc/rc.d/rc.ntpd'.format(mountPoint), os.X_OK)

def setNTPDefault(enabled, mountPoint = None):
  """
  Fix the configuration for the default NTP service to be activated on boot or not.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = '/'
  if enabled:
    os.chmod('{0}/etc/rc.d/rc.ntpd'.format(mountPoint), 0755)
  else:
    os.chmod('{0}/etc/rc.d/rc.ntpd'.format(mountPoint), 0644)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
  continents = listTZContinents()
  assertTrue(type(continents) == list)
  assertTrue(len(continents) > 0)
  assertTrue('Europe' in continents)
  cities = listTZCities('Europe')
  assertTrue(type(cities) == list)
  assertTrue(len(cities) > 0)
  assertTrue('Paris' in cities)
  tz = listTimeZones()
  assertTrue(type(tz) == dict)
  assertTrue(len(tz) > 0)
  assertTrue('Europe' in tz)
  assertTrue('Paris' in tz['Europe'])
  deftz = getDefaultTimeZone()
  assertTrue('/' in deftz)
  assertEquals(2, len(deftz.split('/')))
  setDefaultTimeZone('Etc/Zulu')
  tz = getDefaultTimeZone()
  assertTrue('/' in tz)
  assertEquals(2, len(tz.split('/')))
  assertEquals('Etc/Zulu', tz)
  setDefaultTimeZone(deftz)
  ntp = isNTPEnabledByDefault()
  assertTrue(type(ntp) == bool)
  setNTPDefault(True)
  assertTrue(isNTPEnabledByDefault())
  setNTPDefault(False)
  assertFalse(isNTPEnabledByDefault())
  setNTPDefault(ntp)
