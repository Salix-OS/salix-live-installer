#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
SaLT functions:
  - getSaLTVersion
  - isSaLTLiveEnv
  - isSaLTLiveCloneEnv
  - getSaLTLiveMountPoint
  - getSaLTRootDir
  - getSaLTIdentFile
  - getSaLTBaseDir
  - listSaLTModules
  - installSaLTModule
"""
import os
import glob
import re
from execute import execCall

def getSaLTVersion():
  """
  Returns the SaLT version if run in a SaLT Live environement
  """
  _checkLive()
  return open('/mnt/salt/salt-version', 'r').read().strip()

def isSaLTLiveEnv():
  """
  Returns True if it is executed in a SaLT Live environment, False otherwise
  """
  return os.path.isfile('/mnt/salt/salt-version') and os.path.isfile('/mnt/salt/tmp/distro_infos')

def _checkLive():
  if not isSaLTLiveEnv():
    raise Exception('Not in SaLT Live environment.')

def isSaLTLiveCloneEnv():
  """
  Returns Trus if it is exectued in a SaLT LiveClone environment, False otherwise
  """
  if not isSaLTLiveEnv():
    return False
  else:
    moduledir = '{0}/{1}/{2}/modules'.format(getSaLTLiveMountPoint(), getSaLTBaseDir(), getSaLTRootDir())
    return os.path.isfile(moduledir + '/01-clone.salt')

def getSaLTLiveMountPoint():
  """
  Returns the SaLT source mount point path. It could be the mountpoint of the optical drive, or the USB stick for example.
  """
  _checkLive()
  try:
    # format:
    # mountpoint:device
    ret = open('/mnt/salt/tmp/distro_infos', 'r').read().splitlines()[0].split(':', 1)[0]
  except:
    ret = None
  return ret

def getSaLTRootDir():
  """
  Returns the SaLT ROOT_DIR, so the name of the directory containing the modules.
  This is not a full path but relative to the BASEDIR.
  """
  _checkLive()
  ret = None
  for line in open('/mnt/salt/etc/salt.cfg', 'r').read().splitlines():
    if line.startswith('ROOT_DIR='):
      ret = line.split('=', 1)[1]
      break
  return ret

def getSaLTIdentFile():
  """
  Returns the SaLT IDENT_FILE, so the name of the file located at the root of a filesystem containing some SaLT information for this Live session.
  This is not a full path but relative to the mount point.
  """
  _checkLive()
  ret = None
  for line in open('/mnt/salt/etc/salt.cfg', 'r').read().splitlines():
    if line.startswith('IDENT_FILE='):
      ret = line.split('=', 1)[1]
      break
  return ret

def getSaLTBaseDir():
  """
  Returns the SaLT BASEDIR, so the name of the directory containing all files for this Live session.
  This is not a full path but relative to the mount point.
  """
  _checkLive()
  mountpoint = getSaLTLiveMountPoint()
  identfile = getSaLTIdentFile()
  ret = None
  if mountpoint and identfile:
    for line in open('{0}/{1}'.format(mountpoint, identfile), 'r').read().splitlines():
      if line.startswith('BASEDIR='):
        ret = line.split('=', 1)[1]
        break
  if ret != None and len(ret) == 0:
    ret = '.' # for not having empty path. GNU is ok having a path like a/b//c/d but it's preferable to have a/b/./c/d if possible
  return ret

def listSaLTModules():
  """
  Returns a list of modules names for this Live session.
  """
  _checkLive()
  moduledir = '{0}/{1}/{2}/modules'.format(getSaLTLiveMountPoint(), getSaLTBaseDir(), getSaLTRootDir())
  return sorted(map(lambda(x): re.sub(r'.*/([^/]+).salt$', r'\1', x), glob.glob('{0}/*.salt'.format(moduledir))))

def installSaLTModule(moduleName, targetMountPoint):
  """
  Install the module 'moduleName' of this Live session into the targetMountPoint.
  """
  _checkLive()
  if not os.path.isdir('/mnt/salt/mnt/{1}'.format(moduleName)):
    raise IOError("The module '{0}' does not exists".format(moduleName))
  if not os.path.isdir(targetMountPoint):
    raise IOError("The target mount point '{0}' does not exists".format(targetMountPoint))
  # TODO Pythonic way ??
  execCall(['cp', '--preserve', '-r', '-f', '/mnt/salt/mnt/{1}/*'.format(moduleName), targetMountPoint], shell = False)
