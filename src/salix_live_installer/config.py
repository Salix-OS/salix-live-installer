#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Config class helps storing the configuration for the Salix installation.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import sys
from datetime import *
import salix_livetools_library as sltl

class Config:
  """
  Configuration for the installation of Salix
  """
  def __init__(self, min_salt_version, is_test, is_test_clone, use_test_data):
    self.min_salt_version = min_salt_version
    self.is_test = is_test
    self.is_test_clone = is_test_clone
    self.use_test_data = use_test_data
    self.default_format = 'ext4'
    self._get_current_config()
  def _get_current_config(self):
    print 'Gathering current configuration…',
    sys.stdout.flush()
    # Initialize the lock system preventing the Install button to be activated prematurely
    self.configurations = {'time':False, 'keyboard':False, 'locale':False, 'partitions':False, 'clonelogins':False, 'user':False, 'root':False, 'packages':False, 'bootloader':False}
    if self.is_test:
      self.is_live = True
      self.is_liveclone = self.is_test_clone
      self.salt_version = self.min_salt_version
      self.is_salt_ok = True
    else:
      self.is_live = sltl.isSaLTLiveEnv()
      if self.is_live:
        self.is_liveclone = sltl.isSaLTLiveCloneEnv()
        self.salt_version = sltl.getSaLTVersion()
        self.is_salt_ok = sltl.isSaLTVersionAtLeast(self.min_salt_version)
      else:
        self.is_liveclone = False
        self.salt_version = ''
        self.is_salt_ok = False
    if self.is_live and not self.is_salt_ok:
      error_dialog(_("You need at least version {0} of SaLT installed to continue.\nYou have version {1}.\n\nInstallation will not be possible").format(self.min_salt_version, self.salt_version), _("Sorry!"))
      self.is_live = False
      self.is_liveclone = False
    if self.use_test_data:
      self.cur_tz_continent = 'Europe'
      self.cur_tz_city = 'Paris'
      self.cur_tz = self.cur_tz_continent + '/' + self.cur_tz_city
      self.cur_use_ntp = True
      self.cur_time_delta = timedelta()
      self.cur_km = 'fr-latin9'
      self.cur_use_numlock = False
      self.cur_use_ibus = True
      self.cur_locale = 'fr_FR.utf8'
      self.partitions_step = 'recap'
      self.show_external_drives = False
      self.main_partition = 'sda7'
      self.main_format = 'ext4'
      self.partitions = []
      for disk_device in sltl.getDisks():
        disk_info = sltl.getDiskInfo(disk_device)
        if self.show_external_drives or not disk_info['removable']:
          for p in sltl.getPartitions(disk_device):
            self.partitions.append(p)
      self.swap_partitions = sltl.getSwapPartitions()
      self.linux_partitions = []
      self.win_partitions = []
      self.keep_live_logins = self.is_liveclone
      if self.keep_live_logins:
        self.new_login = ''
        self.new_password = ''
        self.new_root_password = ''
      else:
        self.new_login = 'test'
        self.new_password = 'salix'
        self.new_root_password = 'SaliX'
      self.install_mode = 'full'
      self.bootloader = 'lilo'
      self.bootsetup_available = True
      for c in self.configurations:
        self.configurations[c] = True
    else:
      self.cur_tz = sltl.getDefaultTimeZone()
      if '/' in self.cur_tz:
        self.cur_tz_continent = self.cur_tz.split('/', 1)[0]
        self.cur_tz_city = self.cur_tz.split('/', 1)[1]
      else:
        self.cur_tz = None
        self.cur_tz_continent = None
        self.cur_tz_city = None
      self.cur_use_ntp = sltl.isNTPEnabledByDefault()
      self.cur_time_delta = timedelta() # used when NTP is not used
      self.cur_km = sltl.findCurrentKeymap()
      self.cur_use_numlock = sltl.isNumLockEnabledByDefault()
      self.cur_use_ibus = sltl.isIbusEnabledByDefault()
      self.cur_locale = sltl.getCurrentLocale()
      self.partitions_step = 'none' # could be none, main, linux, win or recap
      self.partitions = []
      self.swap_partitions = []
      self.show_external_drives = False
      self.main_partition = None
      self.main_format = None
      self.linux_partitions = None # list of tuple as (device, format, mountpoint)
      self.win_partitions = None # list of tuple as (device, format, mountpoint)
      self.keep_live_logins = self.is_liveclone
      self.new_login = '' # None cannot be used in a GtkEntry
      self.new_password = ''
      self.new_root_password = ''
      self.install_mode = None
      self.bootloader = None
      self.bootsetup_available = sltl.isBootsetupAvailable()
    print ' Done'
    sys.stdout.flush()
