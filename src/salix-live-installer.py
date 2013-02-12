#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                                                             #
# Salix installer will install Salix on your computer from the comfort of     #
# SalixLive's graphic environment.                                            #
#                                                                             #
# Copyright Pierrick Le Brun <akuna~at~salixos~dot~org>.                      #
#                                                                             #
# This program is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU General Public License                 #
# as published by the Free Software Foundation; either version 2              #
# of the License, or (at your option) any later version.                      #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program; if not, write to the Free Software                 #
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA. #
#                                                                             #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import gettext
import gobject
import gtk
import gtk.glade
import os
import sys
import glob
import re
from datetime import *
import salix_livetools_library as sltl

APP = 'salix-live-installer'
VERSION = '0.4'
MIN_SALT = '0.2.1'

class SalixLiveInstaller:
  def __init__(self, is_test = False, is_test_clone = False):
    self.is_test = is_test
    self.is_test_clone = is_test_clone
    builder = gtk.Builder()
    for d in ('.', '/usr/share/salix-live-installer', '../share/salix-live-installer'):
      if os.path.exists(d + '/salix-live-installer.glade'):
        builder.add_from_file(d + '/salix-live-installer.glade')
        break
    # Get a handle on the glade file widgets we want to interact with
    self.AboutDialog = builder.get_object("about_dialog")
    self.AboutDialog.set_version(VERSION)
    self.Window = builder.get_object("main_window")
    self.ProgressWindow = builder.get_object("progress_dialog")
    self.InstallProgressBar = builder.get_object("install_progressbar")
    self.TimeTab = builder.get_object("time_tab")
    self.KeyboardTab = builder.get_object("keyboard_tab")
    self.LocaleTab = builder.get_object("locale_tab")
    self.PartitionTab = builder.get_object("partition_tab")
    self.UsersTab = builder.get_object("users_tab")
    self.PackagesTab = builder.get_object("packages_tab")
    self.TimeCheck = builder.get_object("time_check")
    self.KeyboardCheck = builder.get_object("keyboard_check")
    self.LocaleCheck = builder.get_object("locale_check")
    self.PartitionCheck = builder.get_object("partition_check")
    self.UsersCheck = builder.get_object("users_check")
    self.PackagesCheck = builder.get_object("packages_check")
    self.TimeCheckMarker = builder.get_object("time_check_marker")
    self.KeyboardCheckMarker = builder.get_object("keyboard_check_marker")
    self.LocaleCheckMarker = builder.get_object("locale_check_marker")
    self.PartitionCheckMarker = builder.get_object("partition_check_marker")
    self.UsersCheckMarker = builder.get_object("users_check_marker")
    self.PackagesCheckMarker = builder.get_object("packages_check_marker")
    self.IntroBox = builder.get_object("intro_box")
    self.TimeBox = builder.get_object("time_box")
    self.KeyboardBox = builder.get_object("keyboard_box")
    self.LocaleBox = builder.get_object("locale_box")
    self.PartitioningBox = builder.get_object("partitioning_box")
    self.MainPartitionBox = builder.get_object("main_partition_box")
    self.LinuxPartitionBox = builder.get_object("linux_partition_box")
    self.WindowsPartitionBox = builder.get_object("windows_partition_box")
    self.RecapPartitionBox = builder.get_object("recap_partition_box")
    self.UsersBox = builder.get_object("users_box")
    self.PackagesBox = builder.get_object("packages_box")
    self.KeyboardList = builder.get_object("keyboard_list")
    self.KeyboardListStore = builder.get_object("keymap_list_store")
    self.KeyboardSelection = builder.get_object("keyboard_selection")
    self.LocaleList = builder.get_object("locale_list")
    self.LocaleListStore = builder.get_object("locale_list_store")
    self.LocaleSelection = builder.get_object("locale_selection")
    self.MainPartitionList = builder.get_object("main_partition_list")
    self.MainPartitionListStore = builder.get_object("main_partition_list_store")
    self.MainFormatCombobox = builder.get_object("main_format_combobox")
    self.LinuxPartitionList = builder.get_object("linux_partition_list")
    self.LinuxPartitionListStore = builder.get_object("linux_partition_list_store")
    self.WindowsPartitionList = builder.get_object("win_partition_list")
    self.WindowsPartitionListStore = builder.get_object("win_partition_list_store")
    self.RecapPartitionList = builder.get_object("recap_partition_list")
    self.RecapPartitionListStore = builder.get_object("recap_partition_list_store")
    self.YesNoDialog = builder.get_object("yes_no_dialog")
    self.YesNoLabel = builder.get_object("yes_no_label")
    self.LinuxNewSysComboCell = builder.get_object("linux_newsys_renderer_combo")
    self.LinuxNewSysColumn = builder.get_object("linux_newsys_column")
    self.LinuxFormatListStore = builder.get_object("linux_format_list_store")
    self.LinuxNewMountComboCell = builder.get_object("linux_newmount_renderer_combo")
    self.LinuxNewMountColumn = builder.get_object("linux_newmount_column")
    self.LinuxMountListStore = builder.get_object("linux_mountpoint_list_store")
    self.LinuxPartitionApply = builder.get_object("linux_partition_apply")
    self.WindowsPartitionApply = builder.get_object("windows_partition_apply")
    self.WinMountComboCell = builder.get_object("win_newmount_renderer_combo")
    self.WinMountColumn = builder.get_object("win_newmount_column")
    self.WinMountListStore = builder.get_object("win_mountpoint_list_store")
    self.MainPartRecapLabel = builder.get_object("main_part_recap_label")
    self.LinPartRecapLabel = builder.get_object("lin_part_recap_label")
    self.WinPartRecapLabel = builder.get_object("win_part_recap_label")
    self.SwapPartRecapLabel = builder.get_object("swap_part_recap_label")
    self.CoreRadioButton = builder.get_object("core_radiobutton")
    self.CoreHBox = builder.get_object("core_hbox")
    self.BasicRadioButton = builder.get_object("basic_radiobutton")
    self.BasicHBox = builder.get_object("basic_hbox")
    self.FullRadioButton = builder.get_object("full_radiobutton")
    self.PackagesApplyButton = builder.get_object("packages_apply")
    self.TimeApplyButton = builder.get_object("time_apply")
    self.KeyboardApplyButton = builder.get_object("keyboard_apply")
    self.LocaleApplyButton = builder.get_object("locale_apply")
    self.CloneLoginEventbox = builder.get_object("clone_login_eventbox")
    self.UsersEventbox = builder.get_object("users_eventbox")
    self.CloneLoginCheckbutton = builder.get_object("clone_login_checkbutton")
    self.CloneLoginUndo = builder.get_object("clone_login_undo")
    self.CloneLoginApply = builder.get_object("clone_login_apply")
    self.RootPass1Entry = builder.get_object("root_pass1_entry")
    self.RootPass2Entry = builder.get_object("root_pass2_entry")
    self.UserPass1Entry = builder.get_object("user_pass1_entry")
    self.UserPass2Entry = builder.get_object("user_pass2_entry")
    self.UserLoginEntry = builder.get_object("user_login_entry")
    self.UserVisibleCheckButton = builder.get_object("user_visible_checkbutton")
    self.RootVisibleCheckButton = builder.get_object("root_visible_checkbutton")
    self.ExternalDeviceCheckButton = builder.get_object("external_device_checkbutton")
    self.NumLockCheckButton = builder.get_object("numlock_checkbutton")
    self.IBusCheckButton = builder.get_object("ibus_checkbutton")
    self.RootPassCreated = builder.get_object("root_pass_created")
    self.NewUserLogin = builder.get_object("new_user_login")
    self.UsersApplyButton = builder.get_object("users_apply")
    self.RootPassApplyButton = builder.get_object("rootpass_apply")
    self.InstallButton = builder.get_object("install_button")
    self.YearCombobox = builder.get_object("year_combobox")
    self.MonthCombobox = builder.get_object("month_combobox")
    self.DayCombobox = builder.get_object("day_combobox")
    self.ContinentZoneCombobox = builder.get_object("continent_zone_combobox")
    self.CountryZoneCombobox = builder.get_object("country_zone_combobox")
    self.YearListStore = builder.get_object("year_list_store")
    self.MonthListStore = builder.get_object("month_list_store")
    self.DayListStore = builder.get_object("day_list_store")
    self.ContinentZoneListStore = builder.get_object("continent_zone_list_store")
    self.CountryZoneListStore = builder.get_object("country_zone_list_store")
    self.NTPCheckButton = builder.get_object("ntp_checkbutton")
    self.ManualTimeBox = builder.get_object("manual_time_box")
    self.HourSpinButton = builder.get_object("hour_spinbutton")
    self.MinuteSpinButton = builder.get_object("minute_spinbutton")
    self.SecondSpinButton = builder.get_object("second_spinbutton")
    self.TimeZoneBox = builder.get_object("time_zone_box")
    self.ContextLabel = builder.get_object("context_label")
    self.LayoutColumn = builder.get_object("layout_column")
    self.TypeColumn = builder.get_object("type_column")
    self.LocaleColumn = builder.get_object("locale_column")
    self.DescriptColumn = builder.get_object("descript_column")
    self.MainDiskColumn = builder.get_object("main_disk_column")
    self.MainPartColumn = builder.get_object("main_part_column")
    self.MainSizeColumn = builder.get_object("main_size_column")
    self.MainFormatColumn = builder.get_object("main_format_column")
    self.LinuxPartColumn = builder.get_object("linux_part_column")
    self.LinuxSizeColumn = builder.get_object("linux_size_column")
    self.LinuxOldSysColumn = builder.get_object("linux_oldsys_column")
    self.LinuxNewSysColumn = builder.get_object("linux_newsys_column")
    self.LinuxNewMountColumn = builder.get_object("linux_newmount_column")
    self.WinPartColumn = builder.get_object("win_part_column")
    self.WinSizeColumn = builder.get_object("win_size_column")
    self.WinOldSysColumn = builder.get_object("win_oldsys_column")    
    self.WinNewMountColumn = builder.get_object("win_newmount_column")
    # Initialize the contextual help box
    self.context_intro = _("Contextual help.")
    self.on_leave_notify_event(None)
    # Prevent tab switching
    self.switch_tab_lock = False
    # Indicate if the partition wizard is done or not
    self.partition_done = False
    # Initialize the lock system preventing the Install button to be activated prematurely
    self.configurations = {'time':False, 'keyboard':False, 'locale':False, 'partitions':False, 'user':False, 'root':False, 'packages':False}
    self.get_current_config()
    self.build_data_stores()
    self.update_install_button()
    # Connect signals
    self.add_custom_signals()
    builder.connect_signals(self)
  
  # General contextual help
  def on_leave_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(self.context_intro)
  def on_intro_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("General usage."))
  def on_about_link_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("About Salix Installer."))
  def on_context_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Contextual help."))
  def on_button_quit_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Exit Salix Installer."))
  def on_install_button_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))
  def on_launch_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))
  
  # Time contextual help
  def on_time_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the time settings."))
  def on_ntp_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Use Network Time Protocol daemon to synchronize time via Internet."))
  def on_time_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel time settings."))
  def on_time_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Activate the time settings after options have been defined."))
  def on_manual_time_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Set the date & time manually if you do not use NTP service."))
  def on_timezone_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Set the time zone."))

  # Keyboard contextual help
  def on_keyboard_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the keyboard settings."))
  def on_keyboard_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight your favorite keyboard layout \
from this \nlist before clicking on the 'Select keyboard' button."))
  def on_numlock_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want your numeric keypad \
to be activated during the boot process."))
  def on_ibus_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want iBus to be \
activated during the boot process. IBus is an input method (IM) framework for multilingual input."))
  def on_keyboard_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel keyboard layout selection."))
  def on_keyboard_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the keyboard layout."))
  def on_keyboard_selection_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("This is the keyboard layout you have selected. \
'None' will be displayed until you have confirmed that selection."))

  # Locale contextual help
  def on_locale_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the language settings."))
  def on_locale_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight your language from this list before \
clicking on the 'Select language' button."))
  def on_locale_selection_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("This is the system language you have selected. \
'None' will be displayed until you have confirmed that selection. "))
  def on_locale_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel language selection."))
  def on_locale_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the system language."))

  # Partitions contextual help
  def on_partition_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the partitions settings."))
  def on_main_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Highlight the partition from this list before \
clicking on the 'Select partition' button."))
  def on_external_device_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want your external disk drive(s) \
to be displayed in the list above. "))
  def on_main_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your selection after highlighting the partition."))
  def on_main_format_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("The filesystem that will be used to format Salix main partition."))
  def on_linux_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to modify the \
filesystem of a partition and/or if you wish to assign its mount point.\
You can either choose one of the suggested mount points or enter \
your own. You must configure all the desired partitions before clicking \
on the 'Apply settings' button. Any unset parameters will be ignored. "))
  def on_linux_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm the Linux partition(s) settings from the list."))
  def on_win_partition_list_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to assign \
the mount point of a partition. You must configure all the \
desired partitions before clicking on the 'Apply settings' button. \
Any unset parameters will be ignored. "))
  def on_windows_partition_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm the Windows partition(s) settings from the list above."))
  def on_partition_recap_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Summary of your partition(s) settings."))
  def on_partition_recap_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel all partition(s) settings."))

  # Users contextual help
  def on_users_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the users and passwords settings."))
  def on_clone_login_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Salix Live Installer has detected a \
LiveClone customized environment. You can transfer your existing LiveClone \
login accounts along with matching personnal directories to the installation \
target or you can wipe them out & create a complete new login account instead."))
  def on_clone_login_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Transfer existing users."))
  def on_clone_login_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel users transfer."))
  def on_users_eventbox_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("A Linux system can manage many registered users and requires each \
one to log in, and to produce some form of authentication (usually a \
login name coupled with a password) before allowing the user access \
to system resources."))
  def on_user_login_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must define your login name which should only include \
alphanumerical characters with no space or upper case letters. "))
  def on_user_pass1_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Choose a password or passphrase to be coupled with your login \
name. Your password or passprase should include a mix of upper \
and lower case letters, numbers, and even symbols (such as the \
@, !, and &)"))
  def on_user_pass2_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must retype your password as a confirmation \
of your choice."))
  def on_user_visible_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
  def on_users_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Create new user."))
  def on_users_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel new user creation."))
  def on_root_pass1_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("On Linux systems, the superuser, or root, is a special user account\
used for system administration. Here you must set its password or\
passphrase. Remember, this password or passphrase should include \
a mix of upper and lower case letters, numbers, and even symbols \
(such as the @, !, and &)"))
  def on_root_pass2_entry_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Here you must retype the superuser (root) password as a \
confirmation of your choice."))
  def on_root_visible_checkbutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
  def on_rootpass_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Apply new root password."))
  def on_rootpass_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel new root password."))

  # Packages contextual help
  def on_packages_tab_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Access the packages selection."))
  def on_core_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>Core installation:</b>\n\
Only the minimum essentials for a console system to start are \
included. A graphical environment is not provided. This is ideal \
if you are an experienced user and want to customize your \
installation for any specific purpose, such as a web server, \
file server etc. "))
  def on_basic_radiobutton_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_markup(_("<b>Basic installation:</b>\n\
This installs only a basic desktop environment, with very few extra applications \
installed on top, such as a web browser and the gslapt package manager. Ideal \
for advanced users that would like to install a lightweight system and \
add their own choice of applications. "))
  def on_full_radiobutton_enter_notify_event(self, widget, data=None):
    if self.is_liveclone:
      self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Salix Live Installer has detected a LiveClone customized environment. \
Core and Basic installation modes are therefore not available. \n\
You can only perform a full installation: all software \
included in your customized LiveClone will be installed."))
    else:
      self.ContextLabel.set_markup(_('<b>Full installation:</b>\n\
Everything that is included in the iso is installed. That includes a complete \
desktop environment and a complete selection of matching applications, \
always following the "one application per task" rationale. '))
  def on_packages_apply_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Confirm your packages selection."))
  def on_packages_undo_enter_notify_event(self, widget, data=None):
    self.ContextLabel.set_text(_("Cancel all packages selection."))

  # What to do when Salix Installer logo is clicked
  def on_about_link_clicked(self, widget, data=None):
    self.AboutDialog.show()

  # What to do when the about dialog quit button is clicked
  def on_about_dialog_close(self, widget, data=None):
    self.AboutDialog.hide()
    return True

  # What to do when the exit X on the main window upper right is clicked
  def gtk_main_quit(self, widget, data=None):
    self.on_button_quit_clicked(widget, data)

  # What to do when the Salix Installer quit button is clicked
  def on_button_quit_clicked(self, widget, data=None):
    gtk.main_quit()

  def get_current_config(self):
    print 'Gathering current configuration…',
    if self.is_test:
      self.is_live = True
      self.is_liveclone = self.is_test_clone
      self.salt_version = MIN_SALT
      self.is_salt_ok = True
    else:
      self.is_live = sltl.isSaLTLiveEnv()
      if self.is_live:
        self.is_liveclone = sltl.isSaLTLiveCloneEnv()
        self.salt_version = sltl.getSaLTVersion()
        self.is_salt_ok = sltl.isSaLTVersionAtLeast(MIN_SALT)
      else:
        self.is_liveclone = False
        self.salt_version = ''
        self.is_salt_ok = False
    if self.is_live and not self.is_salt_ok:
      error_dialog(_("<b>Sorry!</b>\n\nYou need at least version {0} of SaLT installed to continue.\nYou have version {1}.\n\nInstallation will not be possible".format(MIN_SALT, self.salt_version)))
      self.is_live = False
      self.is_liveclone = False
    self.cur_tz = sltl.getDefaultTimeZone()
    if '/' in self.cur_tz:
      self.cur_tz_continent = self.cur_tz.split('/', 1)[0]
      self.cur_tz_city = self.cur_tz.split('/', 1)[1]
    else:
      self.cur_tz = None
      self.cur_tz_continent = None
      self.cur_tz_city = None
    self.cur_use_ntp = sltl.isNTPEnabledByDefault()
    self.cur_km = sltl.findCurrentKeymap()
    self.cur_use_numlock = sltl.isNumLockEnabledByDefault()
    self.cur_use_ibus = sltl.isIbusEnabledByDefault()
    self.cur_locale = sltl.getCurrentLocale()
    self.install_mode = None
    print ' Done'

  def build_data_stores(self):
    print 'Building choice lists…',
    self.ContinentZoneListStore.clear()
    self.ContinentZoneListStore.append([_("Select...")])
    self.ContinentZoneCombobox.set_active(0)
    for continent in sltl.listTZContinents():
      self.ContinentZoneListStore.append([continent])
    self.CountryZoneListStore.clear()
    self.YearListStore.clear()
    for y in range(2000, 2051):
      self.YearListStore.append([y])
    self.MonthListStore.clear()
    for m in [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'),
        _('July'), _('August'), _('September'), _('October'), _('November'), _('December')]:
      self.MonthListStore.append([m])
    self.DayListStore.clear()
    for d in range(1, 32):
      self.DayListStore.append([d])
    self.KeyboardListStore.clear()
    for km in sltl.listAvailableKeymaps():
      self.KeyboardListStore.append(km)
    self.LocaleListStore.clear()
    for l in sltl.listAvailableLocales():
      self.LocaleListStore.append(l)
    print ' Done'

  def add_custom_signals(self):
    self.KeyboardList.get_selection().connect('changed', self.on_keyboard_list_changed_event)
    self.LocaleList.get_selection().connect('changed', self.on_locale_list_changed_event)

  def update_install_button(self):
    self.InstallButton.set_sensitive(not (self.is_test or False in self.configurations.values()))

  def hide_all_tabs(self):
    self.IntroBox.hide()
    self.TimeBox.hide()
    self.KeyboardBox.hide()
    self.LocaleBox.hide()
    self.PartitioningBox.hide()
    self.MainPartitionBox.hide()
    self.RecapPartitionBox.hide()
    self.UsersBox.hide()
    self.PackagesBox.hide()
    self.TimeTab.set_relief(gtk.RELIEF_NONE)
    self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
    self.LocaleTab.set_relief(gtk.RELIEF_NONE)
    self.PartitionTab.set_relief(gtk.RELIEF_NONE)
    self.UsersTab.set_relief(gtk.RELIEF_NONE)
    self.PackagesTab.set_relief(gtk.RELIEF_NONE)

  def on_time_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.time_settings()
      self.TimeTab.set_relief(gtk.RELIEF_HALF)
      self.TimeBox.show()

  def on_keyboard_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.keyboard_settings()
      self.KeyboardTab.set_relief(gtk.RELIEF_HALF)
      self.KeyboardBox.show()
      selection = self.KeyboardList.get_selection().get_selected_rows()[1]
      if selection:
        self.KeyboardList.scroll_to_cell(selection[0], None, True, 0.5)

  def on_locale_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.locale_settings()
      self.LocaleTab.set_relief(gtk.RELIEF_HALF)
      self.LocaleBox.show()
      selection = self.LocaleList.get_selection().get_selected_rows()[1]
      if selection:
        self.LocaleList.scroll_to_cell(selection[0], None, True, 0.5)

  def on_partition_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.partitions_settings()
      self.PartitionTab.set_relief(gtk.RELIEF_HALF)
      if self.partition_done:
        self.RecapPartitionBox.show()
      else:
        self.PartitioningBox.show()

  def on_users_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.users_settings()
      self.UsersTab.set_relief(gtk.RELIEF_HALF)
      self.UsersBox.show()

  def on_packages_tab_clicked(self, widget, data=None):
    if not self.switch_tab_lock:
      self.hide_all_tabs()
      self.packages_settings()
      self.PackagesTab.set_relief(gtk.RELIEF_HALF)
      self.PackagesBox.show()

  def time_settings(self):
    self.ContinentZoneCombobox.set_active(0)
    index = 1
    for continent in sltl.listTZContinents():
      if continent == self.cur_tz_continent:
        self.ContinentZoneCombobox.set_active(index)
        break
      index += 1
    self.time_set_cities_list()
    self.NTPCheckButton.set_active(self.cur_use_ntp)
    self.ManualTimeBox.set_sensitive(not self.cur_use_ntp)
    year, month, day, hour, minute, second, __, __, __ = datetime.now().timetuple()
    index = 0
    for y in self.YearListStore:
      if year == y[0]:
        self.YearCombobox.set_active(index)
        break
      index += 1
    self.MonthCombobox.set_active(month - 1)
    self.DayCombobox.set_active(day - 1)
    self.HourSpinButton.set_value(hour)
    self.MinuteSpinButton.set_value(minute)
    self.SecondSpinButton.set_value(second)
  def time_set_cities_list(self):
    self.CountryZoneListStore.clear()
    self.CountryZoneListStore.append([_("Select...")])
    self.CountryZoneCombobox.set_active(0)
    if self.cur_tz_continent:
      cities = sltl.listTZCities(self.cur_tz_continent)
      if cities:
        index = 1
        for city in cities:
          self.CountryZoneListStore.append([city])
          if city == self.cur_tz_city:
            self.CountryZoneCombobox.set_active(index)
          index += 1
  def on_continent_zone_combobox_changed(self, widget, data=None):
    if self.ContinentZoneCombobox.get_active() > 0:
      continent = self.ContinentZoneCombobox.get_active_text()
      if continent != self.cur_tz_continent:
        self.cur_tz_continent = continent
        self.cur_tz_city = None
    self.time_set_cities_list()
  def on_country_zone_combobox_changed(self, widget, data=None):
    if self.CountryZoneCombobox.get_active() > 0:
      self.cur_tz_city = self.CountryZoneCombobox.get_active_text()
      self.cur_tz = self.cur_tz_continent + '/' + self.cur_tz_city
  def on_ntp_checkbutton_toggled(self, widget, data=None):
    self.cur_use_ntp = self.NTPCheckButton.get_active()
    self.ManualTimeBox.set_sensitive(not self.cur_use_ntp)
  def on_time_apply_clicked(self, widget, data=None):
    self.ManualTimeBox.set_sensitive(False)
    self.NTPCheckButton.set_sensitive(False)
    self.TimeZoneBox.set_sensitive(False)
    self.TimeApplyButton.set_sensitive(False)
    self.configurations['time'] = True
    self.update_install_button()
    self.TimeCheck.show()
    self.TimeCheckMarker.hide()
  def on_time_undo_clicked(self, widget, data=None):
    self.TimeCheck.hide()
    self.TimeCheckMarker.show()
    self.ManualTimeBox.set_sensitive(True)
    self.NTPCheckButton.set_sensitive(True)
    self.TimeZoneBox.set_sensitive(True)
    self.TimeApplyButton.set_sensitive(True)
    self.time_settings()
    self.configurations['time'] = False
    self.update_install_button()

  def keyboard_settings(self):
    index = 0
    for km in self.KeyboardListStore:
      if km[0] == self.cur_km:
        self.KeyboardList.get_selection().select_path(index)
        break
      index += 1
    self.NumLockCheckButton.set_active(self.cur_use_numlock)
    self.IBusCheckButton.set_active(self.cur_use_ibus)
  def on_keyboard_list_changed_event(self, selection, data=None):
    model, it = selection.get_selected()
    if it:
      self.cur_km = model.get_value(it, 0)
    else:
      self.cur_km = None
  def on_numlock_checkbutton_toggled(self, widget, data=None):
    self.cur_use_numlock = self.NumLockCheckButton.get_active()
  def on_ibus_checkbutton_toggled(self, widget, data=None):
    self.cur_use_ibus = self.IBusCheckButton.get_active()
  def on_keyboard_apply_clicked(self, widget, data=None):
    if self.cur_km:
      self.KeyboardList.set_sensitive(False)
      self.KeyboardApplyButton.set_sensitive(False)
      self.NumLockCheckButton.set_sensitive(False)
      self.IBusCheckButton.set_sensitive(False)
      model, it = self.KeyboardList.get_selection().get_selected()
      self.KeyboardSelection.set_text('{0} ({1})'.format(model.get_value(it, 0), model.get_value(it, 1)))
      self.configurations['keyboard'] = True
      self.update_install_button()
      self.KeyboardCheck.show()
      self.KeyboardCheckMarker.hide()
  def on_keyboard_undo_clicked(self, widget, data=None):
    self.KeyboardList.set_sensitive(True)
    self.KeyboardApplyButton.set_sensitive(True)
    self.NumLockCheckButton.set_sensitive(True)
    self.IBusCheckButton.set_sensitive(True)
    self.KeyboardSelection.set_text(_('None'))
    self.configurations['keyboard'] = False
    self.update_install_button()
    self.KeyboardCheck.hide()
    self.KeyboardCheckMarker.show()

  def locale_settings(self):
    index = 0
    for l in self.LocaleListStore:
      if l[0] + '.utf8' == self.cur_locale:
        self.LocaleList.get_selection().select_path(index)
        break
      index += 1
  def on_locale_list_changed_event(self, selection, data=None):
    model, it = selection.get_selected()
    if it:
      self.cur_locale = model.get_value(it, 0)
    else:
      self.cur_locale = None
  def on_locale_apply_clicked(self, widget, data=None):
    if self.cur_locale:
      self.LocaleList.set_sensitive(False)
      self.LocaleApplyButton.set_sensitive(False)
      model, it = self.LocaleList.get_selection().get_selected()
      self.LocaleSelection.set_text('{0} ({1})'.format(model.get_value(it, 0), model.get_value(it, 1)))
      self.configurations['locale'] = True
      self.update_install_button()
      self.LocaleCheck.show()
      self.LocaleCheckMarker.hide()
  def on_locale_undo_clicked(self, widget, data=None):
    self.LocaleList.set_sensitive(True)
    self.LocaleApplyButton.set_sensitive(True)
    self.LocaleSelection.set_text(_('None'))
    self.configurations['locale'] = False
    self.update_install_button()
    self.LocaleCheck.hide()
    self.LocaleCheckMarker.show()

  def partitions_settings(self):
    pass
  def on_main_partition_apply_clicked(self, widget, data=None):
    pass
  def on_linux_partition_apply_clicked(self, widget, data=None):
    pass
  def on_windows_partition_apply_clicked(self, widget, data=None):
    pass
  def on_modify_partition_button_clicked(self, widget, data=None):
    pass
  def on_do_not_modify_partition_button_clicked(self, widget, data=None):
    pass
  def on_partition_recap_undo_clicked(self, widget, data=None):
    pass

  def users_settings(self):
    pass
  def on_clone_login_apply_clicked(self, widget, data=None):
    pass
  def on_clone_login_undo_clicked(self, widget, data=None):
    pass
  def on_users_apply_clicked(self, widget, data=None):
    pass
  def on_users_undo_clicked(self, widget, data=None):
    pass
  def on_rootpass_apply_clicked(self, widget, data=None):
    pass
  def on_rootpass_undo_clicked(self, widget, data=None):
    pass

  def packages_settings(self):
    if not self.install_mode:
      self.CoreRadioButton.set_sensitive(not self.is_liveclone)
      self.CoreHBox.set_sensitive(not self.is_liveclone)
      self.BasicRadioButton.set_sensitive(not self.is_liveclone)
      self.BasicHBox.set_sensitive(not self.is_liveclone)
  def on_packages_apply_clicked(self, widget, data=None):
    self.CoreRadioButton.set_sensitive(False)
    self.BasicRadioButton.set_sensitive(False)
    self.FullRadioButton.set_sensitive(False)
    self.PackagesApplyButton.set_sensitive(False)
    if self.CoreRadioButton.get_active():
      self.install_mode = 'core'
    elif self.BasicRadioButton.get_active():
      self.install_mode = 'basic'
    elif self.FullRadioButton.get_active():
      self.install_mode = 'full'
    self.configurations['packages'] = True
    self.update_install_button()
    self.PackagesCheck.show()
    self.PackagesCheckMarker.hide()
  def on_packages_undo_clicked(self, widget, data=None):
    self.install_mode = None
    self.packages_settings()
    self.FullRadioButton.set_sensitive(True)
    self.PackagesApplyButton.set_sensitive(True)
    self.configurations['packages'] = False
    self.update_install_button()
    self.PackagesCheck.hide()
    self.PackagesCheckMarker.show()



  ###################################################################

  # What to do when the liveclone login checkbutton is toggled
  def on_clone_login_checkbutton_toggled(self, widget, data=None):
    if self.CloneLoginCheckbutton.get_active() == True:
      users_undo(self)
      rootpass_undo(self)
      self.UsersEventbox.set_sensitive(False)
      self.CloneLoginUndo.set_sensitive(True)
      self.CloneLoginApply.set_sensitive(True)
    else:
      self.UsersEventbox.set_sensitive(True)
      self.CloneLoginUndo.set_sensitive(False)
      self.CloneLoginApply.set_sensitive(False)

  # What to do when the user's password visible checkbutton is toggled
  def on_user_visible_checkbutton_toggled(self, widget, data=None):                
    if self.UserVisibleCheckButton.get_active() == True :
      self.UserPass1Entry.set_visibility(True)
      self.UserPass2Entry.set_visibility(True)
    if self.UserVisibleCheckButton.get_active() == False :
      self.UserPass1Entry.set_visibility(False)
      self.UserPass2Entry.set_visibility(False)
              
  # What to do when the root's password visible checkbutton is toggled
  def on_root_visible_checkbutton_toggled(self, widget, data=None):
    if self.RootVisibleCheckButton.get_active() == True :
      self.RootPass1Entry.set_visibility(True)
      self.RootPass2Entry.set_visibility(True)
    if self.RootVisibleCheckButton.get_active() == False :
      self.RootPass1Entry.set_visibility(False)
      self.RootPass2Entry.set_visibility(False)
                      
  # What to do when the external device checkbutton is toggled
  def on_external_device_checkbutton_toggled (self, widget, data=None):
    global show_external_device
    if self.ExternalDeviceCheckButton.get_active() == True :
      show_external_device = 'yes'
    else :
      show_external_device = 'no'
    partition_list_initialization ()
                      
  # What to do when a combo line is edited in the Linux New system column
  def on_linux_newsys_renderer_combo_edited(self, widget, row_number, new_text):
    # Retrieve the selected Linux partition row iter
    linuxnewsyschoice = self.LinuxPartitionList.get_selection()
    self.LinuxPartitionListStore, iter = linuxnewsyschoice.get_selected()
    # Set the new partition row value on the fifth column (4)
    if new_text in ('ext2', 'ext3', 'ext4', 'reiserfs', 'xfs', 'jfs', 'Select...' ):
      self.LinuxPartitionListStore.set_value(iter, 4, new_text)
      if new_text != _("Select..."):
        self.LinuxPartitionListStore.set_value(iter, 6, 'gtk-yes')
      else:
        self.LinuxPartitionListStore.set_value(iter, 6, 'gtk-edit')
    self.LinuxPartitionApply.set_sensitive(True)

  def on_linux_newsys_renderer_combo_editing_started(self, widget, path, data):
    self.LinuxPartitionApply.set_sensitive(False)

  def on_linux_newsys_renderer_combo_editing_canceled(self, data):
    self.LinuxPartitionApply.set_sensitive(True)

  # What to do when a combo line is edited in the Linux mountpoint column
  def on_linux_newmount_renderer_combo_edited(self, widget, row_number, new_text):
    # Retrieve the selected Linux partition row iter
    linuxnewmountchoice = self.LinuxPartitionList.get_selection()
    self.LinuxPartitionListStore, iter = linuxnewmountchoice.get_selected()
    # Set the new partition row value on the sixth column (5)
    self.LinuxPartitionListStore.set_value(iter, 5, new_text)
    if new_text != _("Select..."):
      self.LinuxPartitionListStore.set_value(iter, 7, 'gtk-yes')
    else:
      self.LinuxPartitionListStore.set_value(iter, 7, 'gtk-edit')
    self.LinuxPartitionApply.set_sensitive(True)

  def on_linux_newmount_renderer_combo_editing_started(self, widget, path, data):
    self.LinuxPartitionApply.set_sensitive(False)

  def on_linux_newmount_renderer_combo_editing_canceled(self, data):
    self.LinuxPartitionApply.set_sensitive(True)

  # What to do when a combo line is edited in the Windows mountpoint column
  def on_win_newmount_renderer_combo_edited(self, widget, row_number, new_text,):
    # Retrieve the selected Windows partition row iter
    windowsnewmountchoice = self.WindowsPartitionList.get_selection()
    self.WindowsPartitionListStore, iter = windowsnewmountchoice.get_selected()
    # Set the new mountpoint row value on the fifth column (4)
    self.WindowsPartitionListStore.set_value(iter, 4, new_text)
    if new_text != _("Select..."):
      self.WindowsPartitionListStore.set_value(iter, 5, 'gtk-yes')
    else:
      self.WindowsPartitionListStore.set_value(iter, 5, 'gtk-edit')
    self.WindowsPartitionApply.set_sensitive(True)

  def on_win_newmount_renderer_combo_editing_started(self, widget, path, data):
    self.WindowsPartitionApply.set_sensitive(False)

  def on_win_newmount_renderer_combo_editing_canceled(self, data):
    self.WindowsPartitionApply.set_sensitive(True)

  # CONFIGURATION APPLY BUTTONS ###

  def on_install_button_clicked(self, widget, data=None):
    pass

  # What to do when the yes button of the YesNo Confirmation Needed dialog is clicked
  def on_confirm_button_clicked(self, widget, data=None):
    pass

  # What to do when the yes button of the YesNo Confirmation Needed dialog is 'released'
  def on_confirm_button_released(self, widget, data=None):
    pass

  # What to do when the no button of the YesNo dialog is clicked
  def on_do_not_confirm_button_clicked(self, widget, data=None):
    pass

# Info window skeleton:
def info_dialog(message, parent = None):
  """
  Display an information message.

  """
  dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_INFO, buttons = gtk.BUTTONS_OK, flags = gtk.DIALOG_MODAL)
  dialog.set_markup(message)
  global result_info
  result_info = dialog.run()
  dialog.destroy()

# Error window skeleton:
def error_dialog(message, parent = None):
  """
  Displays an error message.
  """
  dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE, flags = gtk.DIALOG_MODAL)
  dialog.set_markup(message)
  global result_error
  result_error = dialog.run()
  dialog.destroy()

# Launch the application
if __name__ == '__main__':        
  # If no root privilege, displays error message and exit
  is_test = (len(sys.argv) > 1 and sys.argv[1] == '--test')
  if is_test:
    is_clone = (len(sys.argv) > 2 and sys.argv[2] == '--clone')
    gettext.install(APP, './locale', True)
    gtk.glade.bindtextdomain(APP, './locale')
  else:
    is_clone = False
    gettext.install(APP, '/usr/share/locale', True)
    gtk.glade.bindtextdomain(APP, '/usr/share/locale')
  gtk.glade.textdomain(APP)

  if not is_test and os.getuid() != 0:
    error_dialog(_("<b>Sorry!</b> \n\nRoot privileges are required to run this program. "))
    sys.exit(1)
  print 'Salix Live Installer v' + VERSION
  # show the gui and wait for signals
  SalixLiveInstaller(is_test, is_clone)
  gtk.main()
