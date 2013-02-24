#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to handle users and groups:
  - listRegularSystemUsers
  - createSystemUser
  - changePasswordSystemUser
  - checkPasswordSystemUser
  - deleteSystemUser
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from execute import *
from chroot import *
import os
import random
import string
import crypt

_minUIDForRegularUser = 1000

def listRegularSystemUsers(mountPoint = None):
  """
  Returns a sorted list of regular users, i.e. users with id ≥ 1000.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  ret = []
  for line in open('{0}/etc/passwd'.format(mountPoint), 'rb').read().decode('utf-8').splitlines():
    user, _, uid, _ = line.split(':', 3)
    if int(uid) >= _minUIDForRegularUser:
      ret.append(user)
  return sorted(ret)

def createSystemUser(user, group = '', groups = [
  'audio',
  'cdrom',
  'games',
  'floppy',
  'lp',
  'netdev',
  'plugdev',
  'power',
  'scanner',
  'video' ], password = None, shell = '/bin/bash', mountPoint = None):
  """
  Creates a user 'user' in the system under the 'mountPoint'.
  If the 'group' is specified, and is different than __default__, it will be used.
  If the 'group' is '' then the default group will be used.
  If the 'group' is None then a group of the same name of the user will be created for the new user to be part of.
  The newly created user will also be part of the specified 'groups'.
  'password' is clear text password that will be used. If not specified, the password will be deactivated for the created user.
  See "man useradd" for more information.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  cmd = ['/usr/sbin/useradd', '-m']
  if group == '':
    cmd.append('-N')
  elif group:
    cmd.append('-N')
    cmd.append('-g')
    cmd.append(group)
  else:
    cmd.append('-U')
  if groups:
    cmd.append('-G')
    cmd.append(','.join(groups))
  if password:
    salt = '$1${0}$'.format(''.join(random.Random().sample(string.ascii_letters + string.digits, 8)))
    cryptedPwd = crypt.crypt(password, salt)
    cmd.append('-p')
    cmd.append(cryptedPwd)
  if shell:
    cmd.append('-s')
    cmd.append(shell)
  cmd.append(user)
  if not mountPoint or mountPoint == '/':
    return execCall(cmd, shell = False)
  else:
    return execChroot(mountPoint, cmd)

def changePasswordSystemUser(user, password, mountPoint = None):
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if not password:
    raise Exception('A password must be provided.')
  salt = '$1${0}$'.format(''.join(random.Random().sample(string.ascii_letters + string.digits, 8)))
  cryptedPwd = crypt.crypt(password, salt)
  cmd = "echo '{0}:{1}' | /usr/sbin/chpasswd -e".format(user, cryptedPwd)
  if not mountPoint or mountPoint == '/':
    return execCall(cmd, shell = True)
  else:
    return execChroot(mountPoint, cmd, shell = True)

def checkPasswordSystemUser(user, password, mountPoint = None):
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint == None:
    mountPoint = ''
  if not password:
    raise Exception('A password must be provided.')
  users = dict([tuple(line.split(':', 2)[0:2]) for line in open('{0}/etc/shadow'.format(mountPoint), 'r').read().decode('utf-8').splitlines()])
  if user in users:
    cryptedPwd = users[user]
    salt = cryptedPwd[:cryptedPwd.rfind('$') + 1]
    return cryptedPwd == crypt.crypt(password, salt)
  else:
    return False

def deleteSystemUser(user, mountPoint = None):
  """
  Removes the specified 'user' from the system under the 'mountPoint'.
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  cmd = ['/usr/sbin/userdel', '-r', user]
  if not mountPoint or mountPoint == '/':
    return execCall(cmd, shell = False)
  else:
    return execChroot(mountPoint, cmd)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
  users = listRegularSystemUsers()
  print ' '.join(users)
  assertTrue(len(users) > 0)
  testUser = '__test__'
  assertEquals(0, createSystemUser(testUser, password = 'test'))
  assertTrue(testUser in listRegularSystemUsers())
  assertTrue(checkPasswordSystemUser(testUser, 'test', mountPoint = '/'))
  assertFalse(checkPasswordSystemUser(testUser, 'test2'))
  assertEquals(0, deleteSystemUser(testUser))
  assertFalse(testUser in listRegularSystemUsers())
  assertEquals(0, createSystemUser(testUser, mountPoint = '/./')) # to be different than '/' and to really force the chroot ;-)
  assertTrue(testUser in listRegularSystemUsers())
  assertEquals(0, changePasswordSystemUser(testUser, 'test'))
  assertTrue(checkPasswordSystemUser(testUser, 'test'))
  assertFalse(checkPasswordSystemUser(testUser, 'test3'))
  assertEquals(0, deleteSystemUser(testUser, mountPoint = '/./'))
  assertFalse(testUser in listRegularSystemUsers())
