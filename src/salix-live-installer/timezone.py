#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Functions to handle timezones:
  - listTimeZones
  - listTZContinents
  - listTZCountries
  - getDefaultTimeZone
  - setDefaultTimeZone
"""
import os
import glob
import re
import fileinput
import sys
from execute import *

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  checkRoot()
