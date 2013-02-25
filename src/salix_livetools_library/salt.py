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
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
import os
import glob
import re
import subprocess
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
  return "/mnt/salt{0}".format(ret)

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
      if line.startswith('basedir='):
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
  return '/mnt/salt/mnt/modules/{0}'.format(moduleName)

def installSaLTModule(moduleName, moduleSize, targetMountPoint, callback, callback_args = (), interval = 10, completeCallback = None):
  """
  Install the module 'moduleName' from this Live session into the targetMountPoint.
  'moduleSize' is the uncompressed size of the module expressed in bytes.
  The 'callback' function will be called each 'interval' seconds with the pourcentage (0 ≤ x ≤ 1) of progression (based on used size of target partition) as first argument and all value of callback_args as next arguments
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
    def _run(self, *args, **kwargs):
      cmd = args[0]
      self._p = subprocess.Popen(cmd)
      self._p.wait()
    def start(self, cmd):
      self._t = Thread(target=self._run, args=(cmd,))
      self._t.start()
    def is_running(self):
      return self._t and self._t.is_alive()
    def stop(self):
      if self._p:
        self._p.kill()
        self._p = None
  init_size = get_used_size(targetMountPoint)
  actual_size = init_size
  t = ExecCopyTask()
  t.start(['cp', '--preserve', '-r', '-f', '--remove-destination', '{0}/.'.format(src), targetMountPoint + '/'])
  while t.is_running():
    for x in range(interval):
      sleep(1)
      if not t.is_running():
        break
    if t.is_running():
      actual_size = get_used_size(targetMountPoint)
      diff_size = float(actual_size - init_size)
      if diff_size < 0: # is this possible?
        diff_size = 0
      p = diff_size / moduleSize
      if p > 1:
        p = 1
      if not callback(p, *callback_args):
        t.stop()
  if completeCallback:
    completeCallback()
