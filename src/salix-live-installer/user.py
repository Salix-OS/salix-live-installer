#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to handle users and groups:
  - listRegularUsers
  - 
"""
from execute import *
import os

def listRegularUsers():
  """
  Returns a sorted list of regular users, i.e. users with id ≥ 1000.
  """
  ret = []
  for line in open('/etc/passwd', 'r').read().splitlines():
    user, _, uid, _ = line.split(':', 3)
    if int(uid) >= 1000:
      ret.append(user)
  return sorted(ret)

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  users = listRegularUsers()
  print users
  assertTrue(len(users) > 0)
