#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
SaLT functions:
  - getSaLTVersion
  - isSaLTVersionAtLeast
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
from freesize import *
from threading import Thread
from time import sleep

def getSaLTVersion():
  """
  Returns the SaLT version if run in a SaLT Live environment
  """
  _checkLive()
  return open('/mnt/salt/salt-version', 'r').read().strip()

def isSaLTVersionAtLeast(version):
  """
  Returns True if the SaLT version is at least 'version'.
  """
  v = getSaLTVersion()
  def vercmp(v1, v2):
    def _makelist(v):
      lst = [int(x) for x in re.sub(r'[a-z]', '', v.lower()).split('.')]
      while lst[-1] == 0:
        lst.pop()
      return lst
    return _makelist(v1).__ge__(_makelist(v2))
  return vercmp(version, v)

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
  Returns True if it is executed in a SaLT LiveClone environment, False otherwise
  """
  if not isSaLTLiveEnv():
    return False
  else:
    moduledir = '{0}/{1}/{2}/modules'.format(getSaLTLiveMountPoint(), getSaLTBaseDir(), getSaLTRootDir())
    return os.path.isfile(moduledir + '/01-clone.salt')

def getSaLTLiveMountPoint():
  """
  Returns the SaLT source mount point path. It could be the mount point of the optical drive or the USB stick for example.
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
  Returns the SaLT ROOT_DIR, which is the directory containing SaLT modules.
  This is not the full path but a relative path to BASEDIR.
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
  Returns the SaLT IDENT_FILE, which is the file located at the root of a filesystem containing some SaLT information for this Live session.
  This is not the full path but a relative path to the mount point.
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
  Returns the SaLT BASEDIR, which is the directory containing all files for this Live session.
  This is not a full path but a relative path to the mount point.
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
  Returns the list of SaLT modules for this Live session.
  """
  _checkLive()
  moduledir = '{0}/{1}/{2}/modules'.format(getSaLTLiveMountPoint(), getSaLTBaseDir(), getSaLTRootDir())
  return sorted(map(lambda(x): re.sub(r'.*/([^/]+).salt$', r'\1', x), glob.glob('{0}/*.salt'.format(moduledir))))

def getSaLTModulePath(moduleName):
  """
  Get the module full path.
  """
  return '/mnt/salt/mnt/{0}'.format(moduleName)

def installSaLTModule(moduleName, targetMountPoint, callback, interval = 10, completeCallback = None):
  """
  Install the module 'moduleName' from this Live session into the targetMountPoint.
  The 'callback' function will be called each 'interval' seconds with the pourcentage (0 ≤ x ≤ 1) of progression (based on used size of target partition) as argument.
  The 'completeCallback' function will be called after the completion of installation.
  """
  _checkLive()
  src = getSaLTModulePath(moduleName)
  if not os.path.isdir(src):
    raise IOError("The module '{0}' does not exists".format(moduleName))
  if not os.path.isdir(targetMountPoint):
    raise IOError("The target mount point '{0}' does not exists".format(targetMountPoint))
  def get_used_size(p):
    return getSizes(p, False)['used']
  class ExecCopyTask:
    def _start(self, cmd):
      self._stopped = False
      execCall(cmd)
      self.stop()
    def start(self, cmd):
      Thread(target=self._start, args=(cmd)).start()
    def is_running(self):
      return not self._stopped
    def stop(self):
      self._stopped = True
  copy_size = getUsedSize(src, getBlockSize(targetMountPoint), False)['size'] # the source can use a different blocksize than the destination
  init_size = get_used_size(targetMountPoint)
  final_size = init_size + copy_size
  actual_size = init_size
  t = ExecCopyTask(callback, interval, completeCallback)
  t.start(['cp', '--preserve', '-r', '-f', '{0}/*'.format(src), targetMountPoint])
  while t.is_running():
    sleep(interval)
    actual_size = get_used_size(targetMountPoint)
    p = float(actual_size) / final_size
    if p > 1:
      p = 1
    callback(p)
  if completeCallback:
    completeCallback()
