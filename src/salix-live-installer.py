#!/usr/bin/env python

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

# version = '0.2.7'

import commands
import subprocess
import os
import gtk
import sys
import gobject
import glob
import shutil

# Internationalization
import locale
import gettext
import gtk.glade
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("salix-live-installer", "/usr/share/locale")
gettext.textdomain("salix-live-installer")
gettext.install("salix-live-installer", "/usr/share/locale", unicode=1)
gtk.glade.bindtextdomain("salix-live-installer", "/usr/share/locale")
gtk.glade.textdomain("salix-live-installer")

# To do => Install log
# To do => Integrate Gparted in installer
# To do => More Error checking process

class SalixLiveInstaller:

    def __init__(self):

        builder = gtk.Builder()
        if os.path.exists("salix-live-installer.glade") :
            builder.add_from_file("salix-live-installer.glade")
        elif os.path.exists("/usr/share/salix-live-installer/salix-live-installer.glade") :
            builder.add_from_file("/usr/share/salix-live-installer/salix-live-installer.glade")
        elif os.path.exists("../share/salix-live-installer/salix-live-installer.glade") :
            builder.add_from_file("../share/salix-live-installer/salix-live-installer.glade")

        # Get a handle on the glade file widgets we want to interact with
        self.Window = builder.get_object("main_window")
        self.ProgressWindow = builder.get_object("progress_dialog")
        self.InstallProgressBar = builder.get_object("install_progressbar")
        self.AboutDialog = builder.get_object("about_dialog")
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
        self.ScimCheckButton = builder.get_object("scim_checkbutton")
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

        # Connect signals
        builder.connect_signals(self)

### INITIALIZATION ###

        # Set the column names
        self.LayoutColumn.set_title(_('Layout'))
        self.TypeColumn.set_title(_('Type'))
        self.LocaleColumn.set_title(_('Locale'))
        self.DescriptColumn.set_title(_('Description'))
        self.MainDiskColumn.set_title(_('Disk'))
        self.MainPartColumn.set_title(_('Partition'))
        self.MainSizeColumn.set_title(_('Size'))
        self.MainFormatColumn.set_title(_('File System'))
        self.LinuxPartColumn.set_title(_('Partition'))
        self.LinuxSizeColumn.set_title(_('Size'))
        self.LinuxOldSysColumn.set_title(_('Current FS'))
        self.LinuxNewSysColumn.set_title(_('Format as:'))
        self.LinuxNewMountColumn.set_title(_('Mount as:'))
        self.WinPartColumn.set_title(_('Partition'))
        self.WinSizeColumn.set_title(_('Size'))
        self.WinOldSysColumn.set_title(_('File System'))
        self.WinNewMountColumn.set_title(_('Mount as:'))

        ### Initialise some global variables ###
        global liveclone_users
        liveclone_users = []
        global login_transfer
        login_transfer = False
        # Initialize the lock system preventing the Install button to be activated prematurely
        global ConfigurationSet
        ConfigurationSet = ['no'] * 7
        # Detect if the installer is running out of a LiveClone or a regular Salix LiveCD
        global liveclone_install
        if os.path.exists("/mnt/live/memory/images/01-clone.lzm") == True :
            liveclone_install = True
            self.CloneLoginEventbox.show()
            self.CoreRadioButton.set_sensitive(False)
            self.CoreHBox.set_sensitive(False)
            self.BasicRadioButton.set_sensitive(False)
            self.BasicHBox.set_sensitive(False)
            self.CloneLoginCheckbutton.set_active(True)
            self.CloneLoginUndo.set_sensitive(True)
            self.CloneLoginApply.set_sensitive(True)

        else:
            liveclone_install = False
            self.CloneLoginEventbox.hide()
        # Prevent switching to another tab until the current configuration is completed or cancelled
        global switch_tab_lock
        switch_tab_lock = ''
        # Control which partition box is shown depending if the configuration is set or not
        global partition_done_lock
        partition_done_lock = ''
        # The other partition lists needs to know what has been chosen as the main partition
        global Selected_Main_Partition
        Selected_Main_Partition = ''
        # Initialise default value for the external device checkbutton
        global show_external_device
        show_external_device = 'no'
        # Initialise default value for Lilosetup execution
        global LaunchLiloSetup
        LaunchLiloSetup = False
        # Initialise default value for the Linux partitions confirmation dialog
        global LinPartConfirmLabel
        LinPartConfirmLabel = ''
        # Initialise default value for NTP configuration settings
        global set_ntp
        set_ntp = 'yes'
            
        # Initialize the passwords entry box to not display characters
        self.UserPass1Entry.set_visibility(False)
        self.UserPass2Entry.set_visibility(False)
        self.RootPass1Entry.set_visibility(False)
        self.RootPass2Entry.set_visibility(False)

        # Initialize the keymap list
        self.KeyboardListStore.clear()
        KeymapsFeedList = []
        global UsedKeyMap
        UsedKeyMap = 'None'
        # Open & parse SalixTools keymaps file
        SalixKeymapList = open('/usr/share/salixtools/keymaps', 'r')
        for line in SalixKeymapList:
            # Nothing interesting in the commented lines
            if '#' not in line:
                # Only retrieve the available keymaps, the first 'argument' of each line
                AvailableKeymap = line.split('|')[0]
                # Put each available keymap in a list
                KeymapsFeedList.append(AvailableKeymap)
        # Prepare the available keymaps list along with their matching type
        global keyb_item
        for keyb_item in KeymapsFeedList:
            # Check if it is the one being used by the environment by parsing rc.keymap:
            if  os.path.exists('/etc/rc.d/rc.keymap'):
                UsedKeymapFile = open('/etc/rc.d/rc.keymap', 'r')
                for line in UsedKeymapFile:
                    if keyb_item +'.map' in line:
                        UsedKeyMap = keyb_item
                UsedKeymapFile.close()
            # Or by parsing /proc/cmdline:
            elif  os.path.exists('/proc/cmdline'):
                UsedKeymapFile = open('/proc/cmdline', 'r')
                for line in UsedKeymapFile:
                    if 'keyb=' + keyb_item + ' ' in line:
                        UsedKeyMap = keyb_item
                UsedKeymapFile.close()
            # Determine if azerty is the type of keyboard
            if os.path.exists('/usr/share/kbd/keymaps/i386/azerty/'+keyb_item+'.map.gz'):
                type = 'azerty'
                # If so, make a set of the keyboard & its corresponding type
                keyb_feedline = (keyb_item, type)
                # And populate the GUI keymap list view
                self.KeyboardListStore.append(keyb_feedline)
            # Determine if dvorak is the type of keyboard
            elif os.path.exists('/usr/share/kbd/keymaps/i386/dvorak/'+keyb_item+'.map.gz'):
                type = 'dvorak'
                # If so, make a set of the keyboard & its corresponding type
                keyb_feedline = (keyb_item, type)
                # And populate the GUI keymap list view
                self.KeyboardListStore.append(keyb_feedline)
            # Determine if qwerty is the type of keyboard
            elif os.path.exists('/usr/share/kbd/keymaps/i386/qwerty/'+keyb_item+'.map.gz'):
                type = 'qwerty'
                # If so, make a set of the keyboard & its corresponding type
                keyb_feedline = (keyb_item, type)
                # And populate the GUI keymap list view
                self.KeyboardListStore.append(keyb_feedline)
            # Determine if qwertz is the type of keyboard
            elif os.path.exists('/usr/share/kbd/keymaps/i386/qwertz/'+keyb_item+'.map.gz'):
                type = 'qwertz'
                # If so, make a set of the keyboard & its corresponding type
                keyb_feedline = (keyb_item, type)
                # And populate the GUI keymap list view
                self.KeyboardListStore.append(keyb_feedline)
            # Detect & set the status of the numlock checkbutton
            global set_numlock
            if os.access('/etc/rc.d/rc.numlock', os.X_OK) == True :
                set_numlock = 'on'
                self.NumLockCheckButton.set_active(True)
            else :
                set_numlock = 'off'
                self.NumLockCheckButton.set_active(False)
            # Detect & set the status of the SCIM checkbutton
            global set_scim
            if os.access('/usr/bin/scim', os.X_OK) == True :
                if os.access('/etc/profile.d/scim.sh', os.X_OK) == True :
                    set_scim = 'on'
                    self.ScimCheckButton.set_active(True)
                else :
                    set_scim = 'off'
                    self.ScimCheckButton.set_active(False)
            else :
                set_scim = 'off'
                self.ScimCheckButton.set_active(False)           
            # Close the opened files
            UsedKeymapFile.close()
        SalixKeymapList.close()

        # Initialize the locale list
        self.LocaleListStore.clear()
        global UsedLocale
        UsedLocale = 'None'
        locale_list = []
        descript_list = []
        # Use non-localized environment to avoid problems
        os.environ['LANG'] = 'en_US'
        # Parse locale output with a basic stripping of relevant lines
        locale_shell_output = "locale -cva | grep -A 2 utf8 | sed -e '/^-/d' -e 's/ *directory.*utf8//' -e 's/^ *title | //'"
        stripped_locale_output = commands.getoutput(locale_shell_output)
        # Break the lines into list items
        locale_output_list = stripped_locale_output.splitlines()
        # Further stripping & categorizing of relevant info
        for item in locale_output_list:
            if 'utf8' in item:
                locale_item = item.replace('locale: ', '')
                # Store the locale
                locale_list.append(locale_item)
                # Check if it is the one being used by the environment:
                UsedLocaleFile = open('/etc/profile.d/lang.sh', 'r')
                for line in UsedLocaleFile:
                    if locale_item in line:
                        UsedLocale = locale_item
                UsedLocaleFile.close()
            else:
                # Store the locale description
                descript_list.append(item)
        # Make a set of the locale & its description
        LocaleFeedList = zip(locale_list,descript_list)
        # Populate the GUI locale list view
        global locale_set
        for locale_set in LocaleFeedList:
            locale_set = list(locale_set)
            self.LocaleListStore.append(locale_set)

        # Initialize continent time zone
        global set_continent_zone
        def set_continent_zone ():
            self.ContinentZoneListStore.clear()
            global continent_zonelist, continent_current_zone, continent_current_zone_index
            continent_zonelist = sorted(glob.glob("/usr/share/zoneinfo/*"))
            continent_current_zone = commands.getoutput("ls -l /etc/localtime-copied-from").split()[-1].split('/')[-2]
            continent_zone_index = 0
            for i in continent_zonelist:
                if os.path.isdir(i):
                    continent_zone_info = i.replace('/usr/share/zoneinfo/', '')
                    self.ContinentZoneListStore.append([continent_zone_info])
                    if continent_current_zone == continent_zone_info:
                        continent_current_zone_index = continent_zone_index
                    continent_zone_index += 1

        global set_country_zone
        def set_country_zone ():
            self.CountryZoneListStore.clear()
            global country_zonelist, country_current_zone_index
            try:
                country_zonelist = sorted(glob.glob("/usr/share/zoneinfo/" + continent_current_zone  + "/*"))
                country_current_zone = commands.getoutput("ls -l /etc/localtime-copied-from").split()[-1].split('/')[-1]
                country_zone_index = 0
                for i in country_zonelist:
                    country_zone_info = i.replace('/usr/share/zoneinfo/' + continent_current_zone + '/', '')
                    self.CountryZoneListStore.append([country_zone_info])
                    if country_current_zone == country_zone_info:
                        country_current_zone_index = country_zone_index
                    country_zone_index += 1
            except:
                pass

        # Initializing the Time comboboxes
        global time_settings_initialization
        def time_settings_initialization() :
            self.NTPCheckButton.set_active(True)
            self.YearListStore.clear()
            years = range(2000,2051)
            current_year = commands.getoutput('date +%Y')
            global current_year_index
            year_index = 0
            for i in years:
                self.YearListStore.append([i])
                if current_year == str(i):
                    current_year_index = year_index
                year_index += 1

            self.MonthListStore.clear()
            global current_month_index, months
            months = [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'),
            _('August'), _('September'), _('August'), _('September'), _('October'), _('November'), _('December')]
            month_index = 0
            current_month = commands.getoutput('date +%m')
            for i in months:
                self.MonthListStore.append([i])
                if int(current_month)-1 == month_index:
                    current_month_index = month_index
                month_index += 1

            self.DayListStore.clear()
            days = range(32)
            global current_day_index
            day_index = 0
            current_day = commands.getoutput('date +%d')
            for i in days:
                self.DayListStore.append([i])
                if str(int(current_day)) == str(i):
                    current_day_index = day_index
                day_index += 1

            global current_hour
            current_hour = int(commands.getoutput('date +%H'))

            global current_minute
            current_minute = int(commands.getoutput('date +%M'))

            global current_second
            current_second = int(commands.getoutput('date +%S'))

            set_continent_zone ()

            set_country_zone ()

        # Initialize the main partitions list.
        global partition_list_initialization
        def partition_list_initialization() :
            global part_feedline_list
            part_feedline_list = []
            self.MainPartitionListStore.clear()
            # Use non-localized environment to avoid problems
            os.environ['LANG'] = 'en_US'
            # Detect all disk drives
            fdisk_output = commands.getoutput('fdisk -l | grep -i disk | grep -v identifier').splitlines()
            # Initialize the different variables
            disk_name = ''
            disk_size = ''
            disk_device = []
            part_name = ''
            part_size = ''
            part_system = ''
            part_feedline = ''
            # Get the relevant partitions info
            for line in fdisk_output:
                if line.startswith('Disk'):
                    disk_device.append(line.split()[1].replace(':', ''))
            for drive in disk_device:
                # Set language again just to be sure
                parted_output = commands.getoutput('LANG=C parted ' + drive + ' print | grep -iv extended | grep -iv swap').splitlines()
                # Parse each line of parted output
                for line in parted_output:
                    # Get the name of each hard drive
                    if 'Model:' in line:
                        model_string = line
                        # Some hard drives insert ATA before their name
                        if 'ATA' in model_string:
                            disk_name = model_string.split()[2]
                        else:
                            disk_name = model_string.split()[1]
                    # Get the size of the disk
                    elif 'Disk' in line:
                        disk_size = line.split()[2]
                    # Get the size & filesystem for each partition of the disk
                    # Here the line will start by a space followed by a number or straight by a number
                    elif line[0:1] == ' ' or line[0:1].isdigit():
                        try :
                            part_name = drive + line.split()[0]
                        except IndexError:
                            continue # Stop process for this line & go straight to the next line
                        part_size = line.split()[3]
                        try :
                            part_system = line.split()[5]
                            # This should not be needed anymore
#                            if 'ext3' in part_system:
#                                part_system = 'ext3/ext4'
                        except IndexError:
                            part_system = 'None'
                        # Check if removable devices should be displayed.
                        if show_external_device == 'yes' :
                            # Put all needed variables in one set per line
                            part_feedline = [disk_name +' (' + disk_size + ')', part_name, part_size, part_system]
                            # Put each set in a list
                            part_feedline_list.append(part_feedline)
                        else :
                            usb_dev = ''
                            firewire_dev = ''
                            dev_root = part_name[5:-1]
                            check_if_usb = 'udevadm info -a -p /sys/block/' + dev_root + ' | grep -m1 /usb'
                            usb_dev = commands.getoutput(check_if_usb)
                            check_if_firewire = 'udevadm info -a -p /sys/block/' + dev_root + ' | grep -m1 /fw-host'
                            firewire_dev = commands.getoutput(check_if_firewire)
                            if '/usb' in usb_dev :
                                pass
                            elif '/fw-host' in firewire_dev :
                                pass
                            else:
                                # Put all needed variables in one set per line
                                part_feedline = [disk_name +' (' + disk_size + ')', part_name, part_size, part_system]
                                # Put each set in a list
                                part_feedline_list.append(part_feedline)
            # Sort the list for the partitions who do not follow the hard drive order
            part_feedline_list.sort()
            # Populate GUI partition list view rows
            for line in part_feedline_list:
                self.MainPartitionListStore.append(line)
            # Set the cursor on the first row
            self.MainPartitionList.set_cursor(0)

        # Initialize the contextual help box
        global context_intro
        context_intro = _("SalixLive Installer will perform a standard installation of Salix Operating \n\
System on your computer from the comfort of SalixLive's graphic environment.")
        self.ContextLabel.set_text(context_intro)

### Callback signals waiting in a constant loop: ###

### WINDOWS MAIN SIGNALS ###

    # General contextual help
    def on_about_link_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("About Salix Installer."))
    def on_about_link_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_context_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Contextual help."))
    def on_context_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_button_quit_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Exit Salix Installer."))
    def on_button_quit_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_install_button_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))
    def on_install_button_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_launch_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Launch Salix installation. This button will not be active until \
all settings are configured correctly."))
    def on_launch_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # Time contextual help
    def on_time_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the time settings."))
    def on_time_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_ntp_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Use Network Time Protocol daemon to synchronize time via Internet."))
    def on_ntp_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_time_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel time settings."))
    def on_time_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_time_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Activate the time settings after options have been defined."))
    def on_time_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_manual_time_eventbox_enter_notify_event(self, widget, data=None):
        self.ContextLabel.set_text(_("Set the date & time manually if you do not use NTP service."))
    def on_manual_time_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
        self.ContextLabel.set_text(context_intro)
    def on_timezone_eventbox_enter_notify_event(self, widget, data=None):
        self.ContextLabel.set_text(_("Set the time zone."))
    def on_timezone_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
        self.ContextLabel.set_text(context_intro)

    # Keyboard contextual help
    def on_keyboard_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the keyboard settings."))
    def on_keyboard_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_keyboard_list_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Highlight your favorite keyboard layout \
from this \nlist before clicking on the 'Select keyboard' button."))
    def on_keyboard_list_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_numlock_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Check this box if you want your numeric keypad \
to be activated during the boot process."))
    def on_numlock_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_scim_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Check this box if you want SCIM to be \
activated during the boot process. The Smart Common Input Method platform (SCIM) \
is an input method platform containing support for more than thirty complex \
languages such as Chinese, Japanese, Korean and many European languages."))
    def on_scim_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_keyboard_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel keyboard layout selection."))
    def on_keyboard_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_keyboard_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm your selection after highlighting the keyboard layout."))
    def on_keyboard_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_keyboard_selection_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("This is the keyboard layout you have selected. \
'None' will be displayed until you have confirmed that selection."))
    def on_keyboard_selection_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # Locale contextual help
    def on_locale_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the language settings."))
    def on_locale_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_locale_list_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Highlight your language from this list before \
clicking on the 'Select language' button."))
    def on_locale_list_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_locale_selection_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("This is the system language you have selected. \
'None' will be displayed until you have confirmed that selection. "))
    def on_locale_selection_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_locale_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel language selection."))
    def on_locale_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_locale_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm your selection after highlighting the system language."))
    def on_locale_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # Partitions contextual help
    def on_partition_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the partitions settings."))
    def on_partition_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_main_partition_list_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Highlight the partition from this list before \
clicking on the 'Select partition' button."))
    def on_main_partition_list_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_external_device_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Check this box if you want your external disk drive(s) \
to be displayed in the list above. "))
    def on_external_device_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_main_partition_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm your selection after highlighting the partition."))
    def on_main_partition_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_main_format_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("The filesystem that will be used to format Salix main partition."))
    def on_main_format_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_linux_partition_list_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to modify the \
filesystem of a partition and/or if you wish to assign its mount point.\
You can either choose one of the suggested mount points or enter \
your own. You must configure all the desired partitions before clicking \
on the 'Apply settings' button. Any unset parameters will be ignored. "))
    def on_linux_partition_list_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_linux_partition_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm the Linux partition(s) settings from the list."))
    def on_linux_partition_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_win_partition_list_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Click on the appropriate 'Select...' cell if you wish to assign \
the mount point of a partition. You must configure all the \
desired partitions before clicking on the 'Apply settings' button. \
Any unset parameters will be ignored. "))
    def on_win_partition_list_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_windows_partition_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm the Windows partition(s) settings from the list above."))
    def on_windows_partition_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_partition_recap_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Summary of your partition(s) settings."))
    def on_partition_recap_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_partition_recap_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel all partition(s) settings."))
    def on_partition_recap_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # Users contextual help
    def on_users_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the users and passwords settings."))
    def on_users_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_clone_login_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Salix Live Installer has detected a \
LiveClone customized environment. You can transfer your existing LiveClone \
login accounts along with matching personnal directories to the installation \
target or you can wipe them out & create a complete new login account instead."))
    def on_clone_login_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_clone_login_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Transfer existing users."))
    def on_clone_login_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_clone_login_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel users transfer."))
    def on_clone_login_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    def on_users_eventbox_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("A Linux system can manage many registered users and requires each \
one to log in, and to produce some form of authentication (usually a \
login name coupled with a password) before allowing the user access \
to system resources."))
    def on_users_eventbox_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_user_login_entry_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Here you must define your login name which should only include \
alphanumerical characters with no space or upper case letters. "))
    def on_user_login_entry_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_user_pass1_entry_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Choose a password or passphrase to be coupled with your login \
name. Your password or passprase should include a mix of upper \
and lower case letters, numbers, and even symbols (such as the \
@, !, and &)"))
    def on_user_pass1_entry_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_user_pass2_entry_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Here you must retype your password as a confirmation \
of your choice."))
    def on_user_pass2_entry_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_user_visible_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
    def on_user_visible_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_users_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Create new user."))
    def on_users_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_users_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel new user creation."))
    def on_users_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    def on_root_pass1_entry_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("On Linux systems, the superuser, or root, is a special user account\
used for system administration. Here you must set its password or\
passphrase. Remember, this password or passphrase should include \
a mix of upper and lower case letters, numbers, and even symbols \
(such as the @, !, and &)"))
    def on_root_pass1_entry_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_root_pass2_entry_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Here you must retype the superuser (root) password as a \
confirmation of your choice."))
    def on_root_pass2_entry_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_root_visible_checkbutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Check this box if you want to be able to see the password you \
are typing."))
    def on_root_visible_checkbutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_rootpass_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Apply new root password."))
    def on_rootpass_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_rootpass_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel new root password."))
    def on_rootpass_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # Packages contextual help
    def on_packages_tab_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Access the packages selection."))
    def on_packages_tab_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_core_radiobutton_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_markup(_("<b>Core installation:</b>\n\
Only the minimum essentials for a console system to start are \
included. A graphical environment is not provided. This is ideal \
if you are an experienced user and want to customize your \
installation for any specific purpose, such as a web server, \
file server etc. "))
    def on_core_radiobutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_basic_radiobutton_enter_notify_event(self, widget, data=None):
		if os.path.exists("/usr/share/lxde") == True :
			self.ContextLabel.set_markup(_("<b>Basic installation:</b>\n\
This installs only the LXDE desktop environment with the Midori \
web browser and the gslapt package manager. Ideal for advanced \
users that would like to install a lightweight LXDE and add their \
own choice of applications."))
		elif os.path.exists("/usr/share/kde4") == True :
			self.ContextLabel.set_markup(_("<b>Basic installation:</b>\n\
This installs only the KDE desktop environment with the Konqueror \
web browser and the gslapt package manager. Ideal for advanced \
users that would like to install a basic KDE and add their \
own choice of applications."))
		else :
			self.ContextLabel.set_markup(_("<b>Basic installation:</b>\n\
This installs only the Xfce desktop environment with the Firefox \
web browser and the gslapt package manager. Ideal for advanced \
users that would like to install a lightweight Xfce and add their \
own choice of applications."))
    def on_basic_radiobutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_full_radiobutton_enter_notify_event(self, widget, data=None):
        if liveclone_install == False :
			if os.path.exists("/usr/share/lxde") == True :
				self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Everything that is included in the iso is installed. That includes the \
LXDE desktop environment, the Midori web browser and Claws-mail \
email client, Gnumeric and Abiword for office work, a Java Runtime \
Environment, the Whaah! media player and Exaile music manager, \
the Gslapt package manager and several other applications, always \
following the 'one application per task' rationale."))
			elif os.path.exists("/usr/share/kde4") == True :
				self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Everything that is included in the iso is installed. That includes the \
KDE desktop environment, the Konqueror web browser and KMail \
email client, KSpread, KWord and the full KOffice suite, a Java Runtime \
Environment, Kaffeine media player and Clementine music manager, \
the Gslapt package manager and several other applications, always \
following the 'one application per task' rationale."))
			else :
				self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Everything that is included in the iso is installed. That includes the \
Xfce desktop environment, the Firefox web browser and Claws-mail \
email client, a complete OpenOffice.org office suite, a Java Runtime \
Environment, the Parole media player and Exaile music manager, \
the Gslapt package manager and several other applications, always \
following the 'one application per task' rationale."))
        elif liveclone_install == True :
            self.ContextLabel.set_markup(_("<b>Full installation:</b>\n\
Salix Live Installer has detected a LiveClone customized environment. \
Core and Basic installation modes are therefore not available. \n\
You can only perform a full installation: all software \
included in your customized LiveClone will be installed."))
    def on_full_radiobutton_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    def on_packages_apply_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Confirm your packages selection."))
    def on_packages_apply_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)
    def on_packages_undo_enter_notify_event(self, widget, data=None):
	self.ContextLabel.set_text(_("Cancel all packages selection."))
    def on_packages_undo_leave_notify_event(self, widget, data=None):
        global context_intro
	self.ContextLabel.set_text(context_intro)

    # What to do when the exit X on the main window upper right is clicked
    def gtk_main_quit(self, widget, data=None):
        gtk.main_quit()

    # What to do when the Salix Installer quit button is clicked
    def on_button_quit_clicked(self, widget, data=None):
        gtk.main_quit()

    # What to do when Salix Installer logo is clicked
    def on_about_link_clicked(self, widget, data=None):
        self.AboutDialog.show()

    # What to do when the about dialog quit button is clicked
    def on_about_dialog_close(self, widget, data=None):
        self.AboutDialog.hide()
        return True

# LISTS ROWS ###

    # What to do when a keymap list row is added
    def on_keymap_list_store_row_inserted(self, widget, value, treeiter):
        # Check if it is the path of the used keymap to set the cursor on it
        if keyb_item == UsedKeyMap:
            global UsedKeybRow
            UsedKeybRow = value

    # What to do when a locale list row is added
    def on_locale_list_store_row_inserted(self, widget, value, treeiter):
        # Check if it is the path of the used locale to set the cursor on it
        if UsedLocale in locale_set:
            global UsedLocaleRow
            UsedLocaleRow = value

### CHECKBUTTONS ###

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

    # What to do when the NTP checkbutton is toggled
    def on_ntp_checkbutton_toggled(self, widget, data=None):
        global set_ntp
        if self.NTPCheckButton.get_active() == True:
            self.ManualTimeBox.set_sensitive(False)
            set_ntp = 'yes'
        else:
            self.ManualTimeBox.set_sensitive(True)
            set_ntp = 'no'

    # What to do when the numlock checkbutton is toggled
    def on_numlock_checkbutton_toggled(self, widget, data=None):
        global set_numlock
        if self.NumLockCheckButton.get_active() == True :
            set_numlock = 'on'
        else :
            set_numlock = 'off'

    # What to do when the SCIM checkbutton is toggled
    def on_scim_checkbutton_toggled(self, widget, data=None):
        global set_scim
        if self.ScimCheckButton.get_active() == True :
            set_scim = 'on'
        else :
            set_scim = 'off'

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
    def	on_external_device_checkbutton_toggled (self, widget, data=None):
        global show_external_device
        if self.ExternalDeviceCheckButton.get_active() == True :
            show_external_device = 'yes'
        else :
            show_external_device = 'no'
        partition_list_initialization ()
			
### COMBOBOX LINES ###

    # What to do when a combo line is changed in continent zone
    def on_continent_zone_combobox_changed(self, widget, data=None):
        global continent_current_zone
        continent_current_zone = self.ContinentZoneCombobox.get_active_text()
        set_country_zone ()

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

    # What to do when the time selection button is clicked
    def on_time_apply_clicked(self, widget, data=None):
        global ConfigurationSet, set_ntp, months, set_zone
        continent_zone = self.ContinentZoneCombobox.get_active_text()
        country_zone = self.CountryZoneCombobox.get_active_text()
        if continent_zone == None:
            error_dialog("\n" + _("The time zone has not been set") + ". " + _("Please verify and correct") + "! \n")
        elif country_zone == None:
            error_dialog("\n" + _("The time zone has not been set") + ". " + _("Please verify and correct") + "! \n")
        else:
            set_zone = "/usr/share/zoneinfo/" + continent_zone + "/" + country_zone
            self.TimeCheck.show()
            self.TimeCheckMarker.hide()
            self.TimeApplyButton.set_sensitive(False)
            self.ManualTimeBox.set_sensitive(False)
            self.NTPCheckButton.set_sensitive(False)
            self.TimeZoneBox.set_sensitive(False)
            ConfigurationSet[6] = 'yes'
            subprocess.call('ln -sf ' + set_zone + ' /etc/localtime-copied-from', shell=True)
            subprocess.call('rm -f /etc/localtime', shell=True)
            subprocess.call('cp /etc/localtime-copied-from /etc/localtime', shell=True)
            if set_ntp == 'yes':
                subprocess.call('chmod +x /etc/rc.d/rc.ntpd', shell=True)
                subprocess.call("/etc/rc.d/rc.ntpd sync 2>/dev/null", shell=True)
            if set_ntp == 'no':
                subprocess.call("/etc/rc.d/rc.ntpd stop 2>/dev/null", shell=True)
                subprocess.call('chmod -x /etc/rc.d/rc.ntpd', shell=True)
                set_hour = str(int(self.HourSpinButton.get_value()))
                set_minute = str(int(self.MinuteSpinButton.get_value()))
                set_second = str(int(self.SecondSpinButton.get_value()))
                set_year = str(2000 + int(self.YearCombobox.get_active()))
                set_month = str(1 + int(self.MonthCombobox.get_active()))
                set_day = str(self.DayCombobox.get_active())
                subprocess.call('date -s "' + set_month + "/" + set_day + "/" + set_year +
                " " + set_hour + ":" + set_minute + ":" + set_second +'"', shell=True)
                subprocess.call('hwclock --systohc', shell=True)
            if 'no' not in ConfigurationSet:
                self.InstallButton.set_sensitive(True)

    # What to do when the keyboard selection button is clicked
    def on_keyboard_apply_clicked(self, widget, data=None):		
        # Retrieve the selected keyboard map row iter
        keybselection = self.KeyboardList.get_selection()
        self.KeyboardListStore, iter = keybselection.get_selected()
        # Retrieve the selected keyboard map row value from the first column (0)
        global Selected_Keyboard
        Selected_Keyboard = self.KeyboardListStore.get_value(iter, 0)
        # Display the selected keyboard map
        self.KeyboardSelection.set_text(Selected_Keyboard)
        # Display the 'Done' check
        self.KeyboardCheck.show()
        self.KeyboardCheckMarker.hide()
        self.KeyboardList.set_sensitive(False)
        self.KeyboardApplyButton.set_sensitive(False)
        self.NumLockCheckButton.set_sensitive(False)
        self.ScimCheckButton.set_sensitive(False)
        global ConfigurationSet
        ConfigurationSet[0] = 'yes'
        if 'no' not in ConfigurationSet :
            self.InstallButton.set_sensitive(True)

    # What to do when the language selection button is clicked
    def on_locale_apply_clicked(self, widget, data=None):
        # Retrieve the selected language row iter
        localeselection = self.LocaleList.get_selection()
        self.LocaleListStore, iter = localeselection.get_selected()
        # Retrieve the selected language row value from the first column (0)
        global Selected_Locale
        Selected_Locale = self.LocaleListStore.get_value(iter, 0)
        # Display the selected language map
        self.LocaleSelection.set_text(Selected_Locale)
        # Display the 'Done' check
        self.LocaleCheck.show()
        self.LocaleCheckMarker.hide()
        self.LocaleList.set_sensitive(False)
        self.LocaleApplyButton.set_sensitive(False)
        global ConfigurationSet
        ConfigurationSet[1] = 'yes'
        if 'no' not in ConfigurationSet :
            self.InstallButton.set_sensitive(True)

    # What to do when the main partition selection button is clicked
    def on_main_partition_apply_clicked(self, widget, data=None):
        # Initialize other partitions variables
        global LinFullSets
        LinFullSets = [] # These partitions will be formatted -and- mounted (the 'full' treatment)
        global LinFormatSets
        LinFormatSets = [] # These partitions only get formatted
        global LinMountSets
        LinMountSets = [] # These partitions only get mounted
        global WinMountSets
        WinMountSets = [] # We probably want Windows partitions to get mounted without any tempering
        # Tell the confirmation dialog what it is dealing with
        global MainPartitionConfirmation
        MainPartitionConfirmation = True
        global LinuxPartitionConfirmation
        LinuxPartitionConfirmation = False
        global WindowsPartitionConfirmation
        WindowsPartitionConfirmation = False
        global InstallButtonConfirmation
        InstallButtonConfirmation = False

        # Retrieve the selected main partition row iter
        mainpartitionselection = self.MainPartitionList.get_selection()
        self.MainPartitionListStore, iter = mainpartitionselection.get_selected()
        # Retrieve the selected main partition row value from the second column (1)
        global Selected_Main_Partition
        Selected_Main_Partition = self.MainPartitionListStore.get_value(iter, 1)
        # Retrieve the format selection
        global Selected_Main_Format
        Selected_Main_Format = self.MainFormatCombobox.get_active_text()
        # Ask the user to confirm or undo his choice
        global MainPartConfirmLabel
        MainPartConfirmLabel = Selected_Main_Partition + " " + _("will be formatted with") + " " \
        + Selected_Main_Format + " " + _("and will be mounted as") + " /. \n"
        self.YesNoLabel.set_text(MainPartConfirmLabel)
        self.YesNoDialog.show()

    # What to do when the Linux partition Apply settings button is clicked
    def on_linux_partition_apply_clicked(self, widget, data=None):
        # Tell the confirmation dialog what it is dealing with
        global MainPartitionConfirmation
        MainPartitionConfirmation = False
        global WindowsPartitionConfirmation
        WindowsPartitionConfirmation = False
        global LinuxPartitionConfirmation
        LinuxPartitionConfirmation = True
        global InstallButtonConfirmation
        InstallButtonConfirmation = False
        # Retrieve all the Linux partition rows data
        NewLinValues = []
        x = 0
        while x <= 20 :
            try :
                treeiter = self.LinuxPartitionListStore.get_iter(x)
                x += 1
                NewLinValues.append(self.LinuxPartitionListStore.get(treeiter, 1, 4, 5))
            except (ValueError) :
                break
        LinPartitionLabel = []
        UnsetValues = (_("Select..."), 'Select...')
        for set in NewLinValues :
            if set[1] not in UnsetValues :
                if set[2] not in UnsetValues :
                    LinPartitionLabel.append(set[0] + " " + _("will be formatted with") + " " + set[1] +\
                    " " + _("and will be mounted as") + " " + set[2] + ". \n")
                    LinFullSets.append(set)
                else :
                    LinPartitionLabel.append(set[0] + " " + _("will be formatted with") + " " + set[1] +\
                    " " + _("and will not be mounted") + ". \n")
                    LinFormatSets.append(set)
            else :
                if set[2] not in UnsetValues :
                    LinPartitionLabel.append(set[0] + " " + _("will not be formatted") + " " +\
                    _("and will be mounted as") + " " + set[2] + ". \n")
                    LinMountSets.append(set)
                else :
                    LinPartitionLabel.append(set[0] + " " + _("will not be formatted") +\
                    " " + _("and will not be mounted") + ". \n")
        FullConfirmationText = ''
        for i in LinPartitionLabel:
            FullConfirmationText += i
        global LinPartConfirmLabel
        LinPartConfirmLabel = FullConfirmationText
        self.YesNoLabel.set_text(FullConfirmationText)
        self.YesNoDialog.show()
        self.YesNoDialog.resize(1, 1)

    # What to do when the Windows partition Apply settings button is clicked
    def on_windows_partition_apply_clicked(self, widget, data=None):
        # Tell the confirmation dialog what it is dealing with
        global MainPartitionConfirmation
        MainPartitionConfirmation = False
        global LinuxPartitionConfirmation
        LinuxPartitionConfirmation = False
        global WindowsPartitionConfirmation
        WindowsPartitionConfirmation = True
        global InstallButtonConfirmation
        InstallButtonConfirmation = False
        # Retrieve all the Windows partition rows data
        NewWinValues = []
        x = 0
        while x <= 20 :
            try :
                treeiter = self.WindowsPartitionListStore.get_iter(x)
                x += 1
                NewWinValues.append(self.WindowsPartitionListStore.get(treeiter, 1, 4))
            except (ValueError) :
                break
        WinPartitionLabel = []
        UnsetValues = (_("Select..."), 'Select...')
        for set in NewWinValues :
            if set[1] in UnsetValues :
                WinPartitionLabel.append(set[0] + " " + _("will not be formatted") +\
                " " + _("and will not be mounted") + ". \n")

            else :
                WinPartitionLabel.append(set[0] + " " + _("will not be formatted") +\
                " " + _("and will be mounted as") + " " + set[1] + ". \n")
                WinMountSets.append(set)
        FullConfirmationText = ''
        for i in WinPartitionLabel:
            FullConfirmationText += i
        global WinPartConfirmLabel
        WinPartConfirmLabel = FullConfirmationText
        self.YesNoLabel.set_text(FullConfirmationText)
        self.YesNoDialog.show()
        self.YesNoDialog.resize(1, 1)

    # What to do when the clone login apply button is clicked
    def on_clone_login_apply_clicked(self, widget, data=None):
        global login_transfer
        login_transfer = True
        # Detect existing regular users
        passwd_list = commands.getoutput("cat /etc/passwd | grep /bin/bash | grep /home/").splitlines()
        global liveclone_users
        for i in passwd_list :
            liveclone_users.append(i.split(":")[0])
        global ConfigurationSet
        ConfigurationSet[3] = 'yes'
        ConfigurationSet[4] = 'yes'
        self.UsersCheck.show()
        self.UsersCheckMarker.hide()
        if 'no' not in ConfigurationSet :
            self.InstallButton.set_sensitive(True)
        self.CloneLoginApply.set_sensitive(False)
        self.CloneLoginCheckbutton.set_sensitive(False)

    # What to do when the user's settings apply button is clicked
    def on_users_apply_clicked(self, widget, data=None):
        # Pass some basic sanity checks
        # To do => prevent the use of caps for login
        if self.UserLoginEntry.get_text() == '' :
            error_dialog("\n" + _("Your login name is empty") + ". " + _("Please verify and correct") + "! \n")
        elif self.UserLoginEntry.get_text().replace(' ', '').isalnum() == False :
            error_dialog("\n" + _("Your login name should only contain alphanumeric characters") + ". "\
            + _("Please verify and correct") + "! \n")
        elif ' ' in self.UserLoginEntry.get_text() :
            error_dialog("\n" + _("Your login name should not contain any space") + ". "\
            + _("Please verify and correct") + "! \n")
        elif self.UserLoginEntry.get_text().islower() != True :
            error_dialog("\n" + _("Your login name should not contain any upper case letter") + ". "\
            + _("Please verify and correct") + "! \n")
        elif self.UserPass1Entry.get_text() == '' :
            error_dialog("\n" + _("Your password entry is empty") + ". " + _("Please verify and correct") + "! \n")
        elif len(self.UserPass1Entry.get_text()) < 5 :
            error_dialog("\n" + _("Your password is too short. It should have at least 5 characters") + ". "
            + _("Please verify and correct") + "! \n")
        elif self.UserPass1Entry.get_text() != self.UserPass2Entry.get_text() :
            error_dialog("\n" + _("Your 2 password entries do not match") + ". " + _("Please verify and correct") + "! \n")
        else :
            global NewUser
            NewUser = self.UserLoginEntry.get_text()
            global NewUserPW
            NewUserPW = self.UserPass1Entry.get_text()
            self.NewUserLogin.set_text(NewUser)
            if self.RootPassCreated.get_text() != _("None") :
                self.UsersCheck.show()
                self.UsersCheckMarker.hide()
            global ConfigurationSet
            ConfigurationSet[3] = 'yes'
            if 'no' not in ConfigurationSet :
                self.InstallButton.set_sensitive(True)
            self.UserLoginEntry.set_sensitive(False)
            self.UserPass1Entry.set_sensitive(False)
            self.UserPass2Entry.set_sensitive(False)
            self.UserVisibleCheckButton.set_active(False)
            self.UserVisibleCheckButton.set_sensitive(False)
            self.UserPass1Entry.set_visibility(False)
            self.UserPass2Entry.set_visibility(False)
            self.UsersApplyButton.set_sensitive(False)

    # What to do when the root password settings apply button is clicked
    def on_rootpass_apply_clicked(self, widget, data=None):
        if self.RootPass1Entry.get_text() == '' :
            error_dialog("\n" + _("Your password entry is empty") + ". " + _("Please verify and correct") + "! \n")
        elif len(self.RootPass1Entry.get_text()) < 5 :
            error_dialog("\n" + _("Your password is too short. It should have at least 5 characters") + ". "\
            + _("Please verify and correct") + "! \n")
        elif self.RootPass1Entry.get_text() != self.RootPass2Entry.get_text() :
            error_dialog("\n" + _("Your 2 password entries do not match") + ". " + _("Please verify and correct") + "! \n")
        else:
            self.RootPassCreated.set_text(_('Yes'))
            if self.NewUserLogin.get_text() != _("None") :
                self.UsersCheck.show()
                self.UsersCheckMarker.hide()
            global ConfigurationSet
            ConfigurationSet[4] = 'yes'
            global NewRootPW
            NewRootPW = self.RootPass1Entry.get_text()
            if 'no' not in ConfigurationSet :
                self.InstallButton.set_sensitive(True)
            self.RootPass1Entry.set_sensitive(False)
            self.RootPass2Entry.set_sensitive(False)
            self.RootVisibleCheckButton.set_active(False)
            self.RootVisibleCheckButton.set_sensitive(False)
            self.RootPass1Entry.set_visibility(False)
            self.RootPass2Entry.set_visibility(False)
            self.RootPassApplyButton.set_sensitive(False)

    # What to do when the package selection apply button is clicked
    def on_packages_apply_clicked(self, widget, data=None):
        global Selected_Install_Mode
        if self.CoreRadioButton.get_active() == True :
            Selected_Install_Mode = _('core')
        elif self.BasicRadioButton.get_active() == True :
            Selected_Install_Mode = _('basic')
        elif self.FullRadioButton.get_active() == True :
            Selected_Install_Mode = _('full')
        self.CoreRadioButton.set_sensitive(False)
        self.BasicRadioButton.set_sensitive(False)
        self.FullRadioButton.set_sensitive(False)
        self.PackagesCheck.show()
        self.PackagesCheckMarker.hide()
        self.PackagesApplyButton.set_sensitive(False)
        global ConfigurationSet
        ConfigurationSet[5] = 'yes'
        if 'no' not in ConfigurationSet :
            self.InstallButton.set_sensitive(True)

    # What to do when the Install Salix button is clicked
    def on_install_button_clicked(self, widget, data=None):
        # Tell the confirmation dialog what it is dealing with
        global MainPartitionConfirmation
        MainPartitionConfirmation = False
        global LinuxPartitionConfirmation
        LinuxPartitionConfirmation = False
        global WindowsPartitionConfirmation
        WindowsPartitionConfirmation = False
        global InstallButtonConfirmation
        InstallButtonConfirmation = True
        # Prepare the install recap text
        LastRecapFullText = ''
        LastRecapFullText += "\n<b>" + _("You are about to install Salix with the following settings") + ":</b> \n"
        LastRecapFullText += "\n<b>" + _("Time zone") + ":</b> \n" + set_zone.replace('/usr/share/zoneinfo/', '') + "\n"
        LastRecapFullText += "\n<b>" + _("Keyboard layout") + ":</b> \n" + Selected_Keyboard + "\n"
        LastRecapFullText += "\n<b>" + _("System language") + ":</b> \n" + Selected_Locale + "\n"
        LastRecapFullText += "\n<b>" + _("Partitions") + ":</b> \n"
        LastRecapFullText += Selected_Main_Partition + " " + _("will be formatted with") + \
        " " + Selected_Main_Format + " " + _("and will be mounted as") + " / \n"
        if LinFullSets != [] :
            for i in LinFullSets :
                LastRecapFullText += i[0] + " " + _("will be formatted with") + " " + i[1] + \
                " " + _("and will be mounted as") + " " + i[2] + "\n"
        if LinFormatSets != [] :
            for i in LinFormatSets :
                LastRecapFullText += i[0] + " " + _("will be formatted with") + " " + i[1] + \
                " " + _("but will not be mounted") +".\n"
        if LinMountSets != [] :
            for i in LinMountSets :
                LastRecapFullText += i[0] + " " + _("will not be formatted") + \
                " " + _("and will be mounted as") + " " + i[2] + "\n"
        if WinMountSets != [] :
            for i in WinMountSets :
                LastRecapFullText += i[0] + " " + _("will not be formatted") + \
                " " + _("and will be mounted as") + " " + i[1] + "\n"
        try:
            for i in Swap_Partition:
                LastRecapFullText += i + " " + _("will not be formatted") + \
                " " + _("and will mounted as swap") + "\n"
        except:
            info_dialog(_("Salix Live Installer was not able to detect a valid \
Swap partition on your system."))
        if login_transfer == True :
            LastRecapFullText += "\n<b>" + _("Standard User") + ":</b> \n" + _("Using LiveClone login. ")  + "\n"
        elif login_transfer == False :
            LastRecapFullText += "\n<b>" + _("Standard User") + ":</b> \n" + NewUser + "\n"
        LastRecapFullText += "\n<b>" + _("Packages") + ":</b> \n"
        # TRANSLATORS: Please just reposition the '%(mode)' variable as required by your grammar.
        LastRecapFullText += _("You have chosen the %(mode)s installation mode.\n")\
        % {'mode': Selected_Install_Mode}
        self.YesNoLabel.set_markup(LastRecapFullText)
        self.YesNoDialog.show()
        self.YesNoDialog.resize(1, 1)

### CONFIGURATION UNDO BUTTONS ###

    # What to do when the time undo button is clicked
    def on_time_undo_clicked(self, widget, data=None):
        # Remove the 'Done' check
        self.TimeCheck.hide()
        self.TimeCheckMarker.show()
        self.TimeApplyButton.set_sensitive(True)
        self.NTPCheckButton.set_active(True)
        self.NTPCheckButton.set_sensitive(True)
        self.TimeZoneBox.set_sensitive(True)
        global ConfigurationSet
        ConfigurationSet[6] = 'no'
        self.InstallButton.set_sensitive(False)

    # What to do when the keyboard undo button is clicked
    def on_keyboard_undo_clicked(self, widget, data=None):
        # Remove the 'Done' check
        self.KeyboardCheck.hide()
        self.KeyboardCheckMarker.show()
        # Reset the selection to none
        self.KeyboardSelection.set_text(_('None'))
        self.KeyboardList.set_sensitive(True)
        self.KeyboardApplyButton.set_sensitive(True)
        self.NumLockCheckButton.set_sensitive(True)
        self.ScimCheckButton.set_sensitive(True)
        global ConfigurationSet
        ConfigurationSet[0] = 'no'
        self.InstallButton.set_sensitive(False)

    # What to do when the language undo button is clicked
    def on_locale_undo_clicked(self, widget, data=None):
        # Remove the 'Done' check
        self.LocaleCheck.hide()
        self.LocaleCheckMarker.show()
        # Reset the selection to none
        self.LocaleSelection.set_text(_('None'))
        self.LocaleList.set_sensitive(True)
        self.LocaleApplyButton.set_sensitive(True)
        global ConfigurationSet
        ConfigurationSet[1] = 'no'
        self.InstallButton.set_sensitive(False)

    # What to do when the partition recap undo button is clicked
    def on_partition_recap_undo_clicked(self, widget, data=None):
        # Blank Recap box + 'Done' Check & displays the main partition configuration box
        global partition_done_lock
        partition_done_lock = ''
        partition_list_initialization()
        self.PartitionCheck.hide()
        self.PartitionCheckMarker.show()
        self.MainPartitionBox.show()
        self.RecapPartitionBox.hide()
        global ConfigurationSet
        ConfigurationSet[2] = 'no'
        self.InstallButton.set_sensitive(False)

    # What to do when the clone login undo button is clicked
    def on_clone_login_undo_clicked(self, widget, data=None):
        global login_transfer
        login_transfer = False
        global ConfigurationSet
        ConfigurationSet[3] = 'no'
        ConfigurationSet[4] = 'no'
        self.UsersCheck.hide()
        self.UsersCheckMarker.show()
        self.InstallButton.set_sensitive(False)
        self.CloneLoginApply.set_sensitive(True)
        self.CloneLoginCheckbutton.set_sensitive(True)

    # What to do when the user's settings undo button is clicked
    global users_undo
    def users_undo(self):
        self.UsersCheck.hide()
        self.UsersCheckMarker.show()
        self.UserLoginEntry.set_sensitive(True)
        self.UserLoginEntry.set_text('')
        self.UserPass1Entry.set_sensitive(True)
        self.UserPass1Entry.set_text('')
        self.UserPass2Entry.set_sensitive(True)
        self.UserPass2Entry.set_text('')
        self.UsersApplyButton.set_sensitive(True)
        self.UserVisibleCheckButton.set_sensitive(True)
        self.NewUserLogin.set_text(_('None'))
        global ConfigurationSet
        ConfigurationSet[3] = 'no'
        self.InstallButton.set_sensitive(False)
    def on_users_undo_clicked(self, widget, data=None):
        users_undo(self)

    # What to do when the root password settings undo button is clicked
    global rootpass_undo
    def rootpass_undo(self):
        self.UsersCheck.hide()
        self.UsersCheckMarker.show()
        self.RootPass1Entry.set_sensitive(True)
        self.RootPass1Entry.set_text('')
        self.RootPass2Entry.set_sensitive(True)
        self.RootPass2Entry.set_text('')
        self.RootVisibleCheckButton.set_sensitive(True)
        self.RootPassApplyButton.set_sensitive(True)
        self.RootPassCreated.set_text(_('None'))
        global ConfigurationSet
        ConfigurationSet[4] = 'no'
        self.InstallButton.set_sensitive(False)
    def on_rootpass_undo_clicked(self, widget, data=None):
        rootpass_undo(self)

    # What to do when the package selection undo button is clicked
    def on_packages_undo_clicked(self, widget, data=None):
        self.CoreRadioButton.set_sensitive(True)
        self.BasicRadioButton.set_sensitive(True)
        self.FullRadioButton.set_sensitive(True)
        self.PackagesCheck.hide()
        self.PackagesCheckMarker.show()
        self.PackagesApplyButton.set_sensitive(True)
        global ConfigurationSet
        ConfigurationSet[5] = 'no'
        self.InstallButton.set_sensitive(False)

### YESNO CONFIRMATION NEEDED DIALOG ###

    # What to do when the yes button of the YesNo Confirmation Needed dialog is clicked
    def on_confirm_button_clicked(self, widget, data=None):
        global partition_done_lock
        partition_done_lock = ''
        # Check what is being confirmed & act accordingly
        if MainPartitionConfirmation == True :
            # Prevent tab switching until all partitions settings are complete
            global switch_tab_lock
            switch_tab_lock = 'on'
            # Tell the installer if there are extra partitions to set:
            global extra_part_toset
            extra_part_toset = []
            # Initialize the Linux partitions list
            self.LinuxPartitionListStore.clear()
            for set in part_feedline_list :
                if Selected_Main_Partition not in set :
                    # Use non-localized environment to avoid problems
                    os.environ['LANG'] = 'en_US'
                    # Parse fdisk -l output (This will not work with raid disks)
                    fdisk_shell_output = "fdisk -l | grep -w " + set[1]
                    stripped_fdisk_output = commands.getoutput(fdisk_shell_output)
                    if "Linux" in stripped_fdisk_output :
                        # Let the installer know about it:
                        extra_part_toset.append('linux')
                        # Insert editable combobox in appropriate list cells for new formatting configuration
                        self.LinuxNewSysComboCell.set_property("model", self.LinuxFormatListStore)
                        self.LinuxNewSysComboCell.set_property('text-column', 0)
                        self.LinuxNewSysComboCell.set_property('editable', True)
                        self.LinuxNewSysComboCell.set_property('cell-background', '#CCCCCC')
                        self.LinuxNewSysColumn.set_attributes(self.LinuxNewSysComboCell, text = 4)
                        set.append(_("Select..."))
                        # Insert editable combobox in appropriate list cells for new mounting configuration
                        self.LinuxNewMountComboCell.set_property("model", self.LinuxMountListStore)
                        self.LinuxNewMountComboCell.set_property('text-column', 0)
                        self.LinuxNewMountComboCell.set_property('editable', True)
                        self.LinuxNewMountComboCell.set_property('cell-background', '#CCCCCC')
                        self.LinuxNewMountColumn.set_attributes(self.LinuxNewMountComboCell, text = 5)
                        set.append(_("Select..."))
                        set.append("gtk-edit")
                        set.append("gtk-edit")
                        # Add the partition's data row to the list view
                        self.LinuxPartitionListStore.append(set)
                        # Set the cursor on the first row
                        self.LinuxPartitionList.set_cursor(0)

            # Initialize the Windows partitions list
            self.WindowsPartitionListStore.clear()
            for set in part_feedline_list :
                if Selected_Main_Partition not in set :
                    # Use non-localized environment to avoid problems
                    os.environ['LANG'] = 'en_US'
                    # Parse fdisk -l output (This will not work for raid disks)
                    fdisk_shell_output = "fdisk -l | grep -w " + set[1]
                    stripped_fdisk_output = commands.getoutput(fdisk_shell_output)
                    winsys = ('NTFS', 'FAT32')
                    for i in winsys :
                        if i in stripped_fdisk_output :
                            # Let the installer know about it:
                            extra_part_toset.append('windows')
                            # Insert editable combobox in appropriate list cells for new mounting configuration
                            self.WinMountComboCell.set_property("model", self.WinMountListStore)
                            self.WinMountComboCell.set_property('text-column', 0)
                            self.WinMountComboCell.set_property('editable', True)
                            self.WinMountComboCell.set_property('cell-background', '#CCCCCC')
                            self.WinMountColumn.set_attributes(self.WinMountComboCell, text = 4)
                            set.append(_("Select..."))
                            set.append("gtk-edit")
                            # Add the partition's data row to the list view
                            self.WindowsPartitionListStore.append(set)
                            # Set the cursor on the first row
                            self.WindowsPartitionList.set_cursor(0)

            # Display the extra Linux partitions configuration if appropriate
            if 'linux' in extra_part_toset :
                self.YesNoDialog.hide()
                self.MainPartitionBox.hide()
                self.LinuxPartitionBox.show()
            # Else display the Windows partitions configuration if appropriate
            elif 'windows' in extra_part_toset :
                self.YesNoDialog.hide()
                self.MainPartitionBox.hide()
                self.WindowsPartitionBox.show()
            else :
                # Set all infos on the recap box, display it, unlock tabs & display partition check
                partition_done_lock = 'on'
                switch_tab_lock = ''
                self.MainPartRecapLabel.set_text(MainPartConfirmLabel)
                try:
                    for i in Swap_Partition:
                        self.SwapPartRecapLabel.set_text( i + "\n")
                except:
                    self.SwapPartRecapLabel.set_text(_('None') + ' \n')
                self.LinPartRecapLabel.set_text(_('None') + ' \n')
                self.WinPartRecapLabel.set_text(_('None') + ' \n')
                self.YesNoDialog.hide()
                self.MainPartitionBox.hide()
                self.RecapPartitionBox.show()
                self.PartitionCheck.show()
                self.PartitionCheckMarker.hide()
                global ConfigurationSet
                ConfigurationSet[2] = 'yes'
                if 'no' not in ConfigurationSet :
                    self.InstallButton.set_sensitive(True)

        if LinuxPartitionConfirmation == True :
            # Display Windows partitions configuration if appropriate
            if 'windows' in extra_part_toset :
                self.YesNoDialog.hide()
                self.LinuxPartitionBox.hide()
                self.WindowsPartitionBox.show()
            else :
                # Set all infos on the recap box, display it, unlock tabs & display partition check
                partition_done_lock = 'on'
                switch_tab_lock = ''
                self.MainPartRecapLabel.set_text(MainPartConfirmLabel)
                self.LinPartRecapLabel.set_text(LinPartConfirmLabel)
                try:
                    for i in Swap_Partition:
                        self.SwapPartRecapLabel.set_text( i + "\n")
                except:
                    self.SwapPartRecapLabel.set_text(_('None') + ' \n')
                self.WinPartRecapLabel.set_text(_('None') + ' \n')
                self.YesNoDialog.hide()
                self.LinuxPartitionBox.hide()
                self.RecapPartitionBox.show()
                self.PartitionCheck.show()
                self.PartitionCheckMarker.hide()
                ConfigurationSet[2] = 'yes'
                if 'no' not in ConfigurationSet :
                    self.InstallButton.set_sensitive(True)

        if WindowsPartitionConfirmation == True :
            # Set all infos on the recap box, display it, unlock tabs & display partition check
            partition_done_lock = 'on'
            switch_tab_lock = ''
            self.MainPartRecapLabel.set_text(MainPartConfirmLabel)
            if LinPartConfirmLabel != '' :
                self.LinPartRecapLabel.set_text(LinPartConfirmLabel)
            else :
                self.LinPartRecapLabel.set_text(_('None') + ' \n')
            if WinPartConfirmLabel != '' :
                self.WinPartRecapLabel.set_text(WinPartConfirmLabel)
            else :
                self.WinPartRecapLabel.set_text(_('None') + ' \n')
            try:
                for i in Swap_Partition:
                    self.SwapPartRecapLabel.set_text( i + "\n")
            except:
                self.SwapPartRecapLabel.set_text(_('None') + ' \n')

            self.YesNoDialog.hide()
            self.WindowsPartitionBox.hide()
            self.RecapPartitionBox.show()
            self.PartitionCheck.show()
            self.PartitionCheckMarker.hide()
            ConfigurationSet[2] = 'yes'
            if 'no' not in ConfigurationSet :
                self.InstallButton.set_sensitive(True)

        if LaunchLiloSetup == True :
            try :
                subprocess.check_call('lilosetup.py', shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to launch LiloSetup, you must set LILO 'manually'. "))
                gtk.main_quit()
            gtk.main_quit()

    # What to do when the yes button of the YesNo Confirmation Needed dialog is 'released'
    def on_confirm_button_released(self, widget, data=None):
            if InstallButtonConfirmation == True :
                # Verify we are in a LiveCD environment
                if os.path.exists("/mnt/live/memory/images") == False :
                    self.YesNoDialog.hide()
                    error_dialog(_("""<b>Sorry!</b>
\nSalix Live Installer is only meant to be used in a LiveCD environment. 
\nYou cannot proceed any further! """))
                elif os.path.exists("/mnt/live/memory/changes") == False :
                    self.YesNoDialog.hide()
                    error_dialog(_("""<b>Sorry!</b>
\nSalix Live Installer is only meant to be used in a LiveCD environment. 
\nYou cannot proceed any further! """))
                else :
                    task = self.salix_install_process()
                    gobject.idle_add(task.next)

    # Install process
    def salix_install_process(self):
        # first we hide unecessary windows & bring on the progress bar with some info
        self.YesNoDialog.hide()
        self.Window.hide()
        self.InstallProgressBar.set_text(_("Starting installation process..."))
        self.InstallProgressBar.set_fraction(0.03)
        self.ProgressWindow.show()
        self.ProgressWindow.set_keep_above(True)
        # there's more work, yield True to prevent the progress bar from looking inactive
        yield True
        # format and remount the main partition
        global Main_MountPoint
        Main_MountPoint = Selected_Main_Partition.replace('dev', 'mnt')
        # if necessary, create the mountpoint first
        if os.path.exists(Main_MountPoint) == False :
            os.mkdir(Main_MountPoint)
        subprocess.call("umount -l " + Selected_Main_Partition, shell=True)
        self.InstallProgressBar.set_text(_("Formatting the main partition..."))
        self.InstallProgressBar.set_fraction(0.06)
        # there's more work, yield True to prevent the progress bar from looking inactive
        yield True
        # adjust the format command to the selected formatting type
        if 'ext' in Selected_Main_Format :
            subprocess.call("mkfs -t " + Selected_Main_Format + " " + Selected_Main_Partition, shell=True)
        else :
            subprocess.call("mkfs -t " + Selected_Main_Format + " -f " + Selected_Main_Partition, shell=True)
        # the main partition has to be mounted so we can copy the OS files to it
        subprocess.call("mount -t " + Selected_Main_Format + " " + Selected_Main_Partition + " " + Main_MountPoint , shell=True)
        # format and/or remount the eventual other Linux partitions
        # (existing Windows partitions will be managed later while generating /etc/fstab)
        if LinFullSets != [] : # Here we will format -and- mount
            self.InstallProgressBar.set_text(_("Formatting and mounting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.09)
            # there's more work, yield True to prevent the progress bar from looking inactive
            yield True
            for i in LinFullSets :
                # first we create the mountpoint on the target
                os.makedirs(Main_MountPoint + i[2])
                # we ensure that the partition is unmounted before formatting
                subprocess.call("umount -l " + i[0], shell=True)
                # we adapt our formatting command to the chosen formatting type
                if 'ext' in i[1] :
                    subprocess.call("mkfs -t " + i[1] + " " + i[0], shell=True)
                else :
                    subprocess.call("mkfs -t " + i[1] + " -f " + i[0], shell=True)
                # finally we mount the device on the target
                subprocess.call("mount -t " + i[1] + " " + i[0] + " " + Main_MountPoint + i[2], shell=True)
        if LinFormatSets != [] : # Here we will only format the partition (no mounting)
            self.InstallProgressBar.set_text(_("Formatting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.12)
            # there's more work, yield True to prevent the progress bar from looking inactive
            yield True
            for i in LinFormatSets :
                # we ensure that the device is unmounted before formatting
                subprocess.call("umount -l " + i[0], shell=True)
                # we adapt our formatting command to the chosen formatting type
                if 'ext' in i[1] :
                    subprocess.call("mkfs -t " + i[1] + " " + i[0], shell=True)
                else :
                    subprocess.call("mkfs -t " + i[1] + " -f " + i[0], shell=True)
        if LinMountSets != [] : # Here we will only mount the partition (no formatting)
            self.InstallProgressBar.set_text(_("Mounting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.15)
            # there's more work, yield True
            yield True
            for i in LinMountSets :
                # first we create the mountpoint on the target
                os.makedirs(Main_MountPoint + i[2])
                # then we mount the device on the target
                subprocess.call("mount " + i[0] + " " + Main_MountPoint + i[2], shell=True)
        # Now we are ready to copy the new OS on the adequate target partition. Normally we should
        # simply unsquashfs the live modules, but since unsquashfs can be buggy & can stall, it is safer
        # to first mount the squashfs module to a temporary mountpoint & copy its content instead.
        # So first we create the temporary mountpoint
        Temp_Mount = Main_MountPoint + "/temp_mount"
        os.mkdir(Temp_Mount)
        if liveclone_install == True : # We are in a LiveClone generated LiveCD
                self.InstallProgressBar.set_text(_("Installing your LiveClone system..."))
                self.InstallProgressBar.set_fraction(0.50)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # we install the one & only clone module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/01-clone.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                os.rmdir(Temp_Mount)
                # We add missing items, restore some non-live stock files, remove some specific live stuff
                os.makedirs(Main_MountPoint + "/media")
                os.makedirs(Main_MountPoint + "/opt")
                os.makedirs(Main_MountPoint + "/proc")
                os.makedirs(Main_MountPoint + "/sys")
                os.makedirs(Main_MountPoint + "/tmp")
                shutil.copytree("/usr/share/liveclone/stockskel/boot", Main_MountPoint + "/boot", symlinks=False)
                shutil.copy("/boot/vmlinuz", Main_MountPoint + "/boot")
                shutil.copy("/usr/share/liveclone/stockskel/etc/rc.d/rc.6", Main_MountPoint + "/etc/rc.d")
                shutil.copy("/usr/share/liveclone/stockskel/etc/rc.d/rc.M", Main_MountPoint + "/etc/rc.d")
                shutil.copy("/usr/share/liveclone/stockskel/etc/rc.d/rc.S", Main_MountPoint + "/etc/rc.d")
                shutil.copy("/usr/share/liveclone/stockskel/etc/rc.d/rc.alsa", Main_MountPoint + "/etc/rc.d")
                shutil.copy("/usr/share/liveclone/stockskel/etc/rc.d/rc.services", Main_MountPoint + "/etc/rc.d")
                subprocess.call("cp --preserve -rf /dev " + Main_MountPoint, shell=True)
                subprocess.call("mount -t proc proc " + Main_MountPoint + "/proc", shell=True)
                subprocess.call("mount --bind /dev " + Main_MountPoint + "/dev", shell=True)
                subprocess.call("spkg -d liveclone --root=" + Main_MountPoint, shell=True)
                subprocess.call("spkg -d salix-live-installer --root=" + Main_MountPoint, shell=True)
                subprocess.call("spkg -d linux-live --root=" + Main_MountPoint, shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/etc/ssh/ssh_host_*", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/home/one/Desktop/*startup-guide*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/user/share/applications/*startup-guide*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/home/one/Desktop/persistence*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/user/share/applications/persistence*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/home/one/Desktop/salix-live*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/home/one/Desktop/liveclone*desktop", shell=True)
                subprocess.call("rm -f " + Main_MountPoint + "/home/one/Desktop/gparted*desktop", shell=True)
                os.remove(Main_MountPoint + "/etc/rc.d/rc.live")

        elif liveclone_install == False : # We are in a regular Salix LiveCD

            if Selected_Install_Mode == _('core') :
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
                self.InstallProgressBar.set_fraction(0.40)
                # there's more work, yield True
                yield True
                # first we install the core module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                self.InstallProgressBar.set_text(_("Installing the common packages..."))
                self.InstallProgressBar.set_fraction(0.50)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # finally we install all the packages that are common to any installation mode
                # this would be the kernel related packages, etc...
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
            elif Selected_Install_Mode == _('basic') :
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('core')})
                self.InstallProgressBar.set_fraction(0.25)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # first we install the core module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
                self.InstallProgressBar.set_fraction(0.50)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # then we install the basic module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*basic.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                self.InstallProgressBar.set_text(_("Installing the common packages..."))
                self.InstallProgressBar.set_fraction(0.60)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # finally we install all the packages that are common to any installation mode
                # this would be the kernel related packages, etc...
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
            elif Selected_Install_Mode == _('full') :
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('core')})
                self.InstallProgressBar.set_fraction(0.20)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # first we install the core module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('basic')})
                self.InstallProgressBar.set_fraction(0.35)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # then we install the basic module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*basic.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
                self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
                self.InstallProgressBar.set_fraction(0.50)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # then we install the full module
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*full.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
                self.InstallProgressBar.set_text(_("Installing the common packages..."))
                self.InstallProgressBar.set_fraction(0.60)
                # there's more work, yield True to prevent the progress bar from looking inactive
                yield True
                # finally we install all the packages that are common to any installation mode
                # those are the kernel related packages, etc...
                subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
                subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
                subprocess.call("umount " + Temp_Mount, shell=True)
            self.InstallProgressBar.set_text(_("Installing the kernel..."))
            self.InstallProgressBar.set_fraction(0.70)
            # there's more work, yield True to prevent the progress bar from looking inactive
            yield True
            subprocess.call("spkg --root=" + Main_MountPoint + " /mnt/*/packages/std-kernel/*", shell=True)
            os.rmdir(Temp_Mount)

        # Create /etc/fstab
        self.InstallProgressBar.set_text(_("Creating /etc/fstab..."))
        self.InstallProgressBar.set_fraction(0.80)
        # there's more work, yield True to prevent the progress bar from looking inactive
        yield True
        Fstab_File = open(Main_MountPoint + '/etc/fstab', 'w')
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('devpts', '/dev/pts', 'devpts', 'gid=5,mode=620', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('proc', '/proc', 'proc', 'defaults', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('tmpfs', '/dev/shm', 'tmpfs', 'defaults', '0', '0'))
        for i in Swap_Partition:
            Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i, 'swap', 'swap', 'defaults', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (Selected_Main_Partition, '/', Selected_Main_Format, 'noatime,defaults', '1', '1'))
        LinSets = LinFullSets + LinFormatSets
        if LinSets != [] :
            for i in LinSets : # i[0] is the partition, i[1] is the format type, i[2] is the mountpoint.
                Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[2], i[1] , 'noatime,defaults', '1', '2'))
        if LinMountSets != [] :
            for i in LinMountSets : # Here, i[1] value will be 'Select...'
                # so we have to detect the linux partition formating type -> Lin_Filesys
                lshal_fstype_output = "lshal | grep -A50 " + i[0] + " | grep -m 1 'volume.fstype =' "
                Lin_Filesys_String = commands.getoutput(lshal_fstype_output)
                Lin_Filesys = Lin_Filesys_String.split("'")[1]
                Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[2], Lin_Filesys , 'noatime,defaults', '1', '2'))
        if WinMountSets != [] :
            os.environ['LANG'] = 'en_US'
            for i in WinMountSets : # Here i[0] is the partition while i[1] is the mountpoint.
                # so we also have to detect the format type
                fdisk_win_output = 'fdisk -l | grep ' + i[0]
                Win_Filesys = commands.getoutput(fdisk_win_output)
                os.makedirs(Main_MountPoint + i[1])
                if 'NTFS' in Win_Filesys :
                    Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[1], 'ntfs-3g' , 'umask=000', '1', '0'))
                if 'FAT32' in Win_Filesys :
                    Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[1], 'vfat' , 'defaults,utf8,umask=0,shortname=mixed', '1', '0'))
        Fstab_File.close()


        # Set Time, Keyboard, locale, login, etc...
        self.InstallProgressBar.set_text(_("Time, keyboard, locale, login and other system configuration..."))
        self.InstallProgressBar.set_fraction(0.90)
        # there's more work, yield True
        yield True
        global set_ntp, set_zone
        if set_ntp == 'yes':
            subprocess.call('chmod +x ' + Main_MountPoint + '/etc/rc.d/rc.ntpd', shell=True)
        if set_ntp == 'no':
            subprocess.call('chmod -x ' + Main_MountPoint + '/etc/rc.d/rc.ntpd', shell=True)
        subprocess.call('ln -sf ' + Main_MountPoint + set_zone + ' ' + Main_MountPoint + '/etc/localtime-copied-from', shell=True)
        subprocess.call('rm -f ' + Main_MountPoint + '/etc/localtime', shell=True)
        subprocess.call('cp ' + Main_MountPoint + '/etc/localtime-copied-from ' + Main_MountPoint + '/etc/localtime', shell=True)

        # Create /etc/rc.d/rc.font
        RCfont_File = open(Main_MountPoint + '/etc/rc.d/rc.font', 'w')
        RCfont_File.write("#!/bin/sh\n\
#\n\
#This selects your default screen font from among the ones in\n\
# /usr/share/kbd/consolefonts.\n\
#\n\
#setfont -v ter-v16n\n\
unicode_start ter-v16n")
        RCfont_File.close()

        # Create /etc/rc.d/rc.keymap
        RCkeymap_File = open(Main_MountPoint + '/etc/rc.d/rc.keymap', 'w')
        RCkeymap_File.write("#!/bin/sh\n\
#\n\
# Load the keyboard map.  More maps are in /usr/share/kbd/keymaps.\n\
if [ -x /usr/bin/loadkeys ]; then\n\
/usr/bin/loadkeys -u " + Selected_Keyboard + ".map\n\
fi")
        RCkeymap_File.close()
        subprocess.call('chmod +x ' + Main_MountPoint + '/etc/rc.d/rc.keymap', shell=True)
        subprocess.call('chmod +x ' + Main_MountPoint + '/etc/rc.d/rc.font', shell=True)
        subprocess.call('chmod +x ' + Main_MountPoint + '/etc/rc.d/rc.cups', shell=True)
        subprocess.call('chmod -x ' + Main_MountPoint + '/etc/rc.d/rc.pcmcia', shell=True)
        subprocess.call('chmod -x ' + Main_MountPoint + '/etc/rc.d/rc.sshd', shell=True)
        subprocess.call('chmod +x ' + Main_MountPoint + '/var/log/setup/setup.07.update-desktop-database', shell=True)
        subprocess.call('chmod +x ' + Main_MountPoint + '/var/log/setup/setup.htmlview', shell=True)
        subprocess.call('chmod +x ' + Main_MountPoint + '/var/log/setup/setup.services', shell=True)
        # Refresh the progress bar before creating the fork
        self.InstallProgressBar.set_text(_("Time, keyboard, locale, login and other system configuration..."))
        self.InstallProgressBar.set_fraction(0.91)
        # there's more work, yield True
        yield True
        # Create a fork to not get stuck in the chroot
        NewPid = os.fork()
        if NewPid == 0 :
            self.chroot_settings()
        else :
            os.waitpid(NewPid, 0) # make sure the child process gets cleaned up
            self.InstallProgressBar.set_text(_("Installation process completed successfully ..."))
            self.InstallProgressBar.set_fraction(0.98)
            # there's more work, yield True
            yield True

            self.InstallProgressBar.set_text(_("Installation process completed successfully ..."))
            self.InstallProgressBar.set_fraction(1.0)
            # there's more work, yield True
            yield True

            # Close install confirmation + progress dialog
            self.ProgressWindow.hide()
            # Call Success dialog & offer to launch LiloSetup
            self.YesNoLabel.set_markup(_("""<b>Salix installation was executed with success!</b>
\nLiloSetup will now be launched to enable you to add Salix to your bootloader.
(If you prefer to use another bootloader utility, click on the No button and
use the application of your choice before rebooting your machine.)\n"""))
            # Set localized environment back so that lilosetup comes up in the local language
            os.environ['LANG'] = Selected_Locale
            global LaunchLiloSetup
            LaunchLiloSetup = True
            self.YesNoDialog.show()
            self.YesNoDialog.resize(1, 1)
            # there's no more work, yield False
            yield False

    # Set up keyboard, locale, users, etc...
    def chroot_settings(self) :
        os.listdir(Main_MountPoint)
        os.chroot(Main_MountPoint)
        subprocess.call('/var/log/setup/setup.07.update-desktop-database', shell=True)
        subprocess.call('/var/log/setup/setup.htmlview', shell=True)
        subprocess.call('/var/log/setup/setup.services', shell=True)
        subprocess.call('/etc/cron.daily/housekeeping', shell=True)
        try :
            subprocess.check_call('/usr/sbin/keyboardsetup -k ' + Selected_Keyboard + ' -n ' + set_numlock + ' -s ' + set_scim + ' -z', shell=True)
        except :
            error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new keyboard selection on the installation target. "))
        try :
            subprocess.check_call('/usr/sbin/localesetup ' + Selected_Locale, shell=True)
        except :
            error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new language selection on the installation target. "))

        if login_transfer == False : # We must first delete eventual regular users' login accounts in the chrooted target
            for i in liveclone_users :
                subprocess.call(" /usr/sbin/userdel -r " + i + " 2>/dev/null", shell=True)
            try :
                subprocess.check_call('/usr/sbin/useradd -m -s /bin/bash -G lp,floppy,audio,video,cdrom,plugdev,power,netdev,scanner ' + NewUser, shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to create the new user on the installation target. "))
            try :
                subprocess.check_call('echo "' + NewUser + ':' + NewUserPW + '" | /usr/sbin/chpasswd', shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new user's password on the installation target. "))
            try :
                subprocess.check_call('echo "root:' + NewRootPW + '" | /usr/sbin/chpasswd', shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to set root's password on the installation target. "))
        # Exit child process
        sys.exit(0)
        
    # What to do when the no button of the YesNo dialog is clicked
    def on_do_not_confirm_button_clicked(self, widget, data=None):
        # Check what is being cancelled & act accordingly if necessary
        if MainPartitionConfirmation == True :
            global Selected_Main_Partition
            Selected_Main_Partition = ''
        if LinuxPartitionConfirmation == True :
            global LinFullSets
            LinFullSets = []
            global LinFormatSets
            LinFormatSets = []
            global LinMountSets
            LinMountSets = []
        if WindowsPartitionConfirmation == True :
            global WinMountSets
            WinMountSets = []
        self.YesNoDialog.hide()
        if LaunchLiloSetup == True :
            info_dialog(_("""Installation process is fully completed but you have chosen not to install LILO.
\nBefore rebooting your machine, you must now use another bootloader manager to setup Salix new system or it will not be operational."""))
            gtk.main_quit()

### CONFIGURATION TABS ###

    # What to do when the time tab is clicked
    def on_time_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            # Show the keyboard setting area & hide all the others
            time_settings_initialization()
            self.IntroBox.hide()
            self.KeyboardBox.hide()
            self.LocaleBox.hide()
            self.MainPartitionBox.hide()
            self.RecapPartitionBox.hide()
            self.UsersBox.hide()
            self.PackagesBox.hide()
            self.TimeBox.show()
            # Set the combo cursors on current values 
            self.YearCombobox.set_active(current_year_index)
            self.MonthCombobox.set_active(current_month_index)
            self.DayCombobox.set_active(current_day_index)
            self.HourSpinButton.set_value(current_hour)
            self.MinuteSpinButton.set_value(current_minute)
            self.SecondSpinButton.set_value(current_second)
            try:
                self.ContinentZoneCombobox.set_active(continent_current_zone_index)
                self.CountryZoneCombobox.set_active(country_current_zone_index)
            except NameError:
                pass
            self.TimeTab.set_relief(gtk.RELIEF_HALF)
            self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
            self.LocaleTab.set_relief(gtk.RELIEF_NONE)
            self.PartitionTab.set_relief(gtk.RELIEF_NONE)
            self.UsersTab.set_relief(gtk.RELIEF_NONE)
            self.PackagesTab.set_relief(gtk.RELIEF_NONE)

    # What to do when the keyboard tab is clicked
    def on_keyboard_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            # Show the keyboard setting area & hide all the others
            self.IntroBox.hide()
            self.TimeBox.hide()
            self.LocaleBox.hide()
            self.MainPartitionBox.hide()
            self.RecapPartitionBox.hide()
            self.UsersBox.hide()
            self.PackagesBox.hide()
            self.KeyboardBox.show()
            try :
                self.KeyboardList.set_cursor(UsedKeybRow)
            except :
                pass
            self.TimeTab.set_relief(gtk.RELIEF_NONE)
            self.KeyboardTab.set_relief(gtk.RELIEF_HALF)
            self.LocaleTab.set_relief(gtk.RELIEF_NONE)
            self.PartitionTab.set_relief(gtk.RELIEF_NONE)
            self.UsersTab.set_relief(gtk.RELIEF_NONE)
            self.PackagesTab.set_relief(gtk.RELIEF_NONE)

    # What to do when the language tab is clicked
    def on_locale_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            self.IntroBox.hide()
            self.TimeBox.hide()
            self.KeyboardBox.hide()
            self.MainPartitionBox.hide()
            self.RecapPartitionBox.hide()
            self.UsersBox.hide()
            self.PackagesBox.hide()
            self.LocaleBox.show()
            try :
                self.LocaleList.set_cursor(UsedLocaleRow)
            except :
                pass
            self.TimeTab.set_relief(gtk.RELIEF_NONE)
            self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
            self.LocaleTab.set_relief(gtk.RELIEF_HALF)
            self.PartitionTab.set_relief(gtk.RELIEF_NONE)
            self.UsersTab.set_relief(gtk.RELIEF_NONE)
            self.PackagesTab.set_relief(gtk.RELIEF_NONE)

    # What to do when the partitions tab is clicked
    def on_partition_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            self.IntroBox.hide()
            self.TimeBox.hide()
            self.KeyboardBox.hide()
            self.LocaleBox.hide()
            self.UsersBox.hide()
            self.PackagesBox.hide()
            if partition_done_lock == 'on' :
                self.RecapPartitionBox.show()
                self.MainPartitionBox.hide()
            else :
                partition_list_initialization()
                self.RecapPartitionBox.hide()
                self.MainPartitionBox.show()
                # Detect swap & other partitions
                if part_feedline_list == [] :
                    info_dialog(_("Salix Live Installer was not able to detect a \
valid partition on your system. You should exit Salix Live Installer now and use \
Gparted, or any other partitioning tool of your choice, to first create valid \
partitions on your system before resuming with Salix Live Installer process."))
                else :
                    global Swap_Partition
                    fdisk_swap_output = 'fdisk -l | grep -i swap | cut -f1 -d " "'
                    Swap_Partition = commands.getoutput(fdisk_swap_output).splitlines()
                    SwapText = "\n<b>" + _("Detected Swap partition(s)") + ":</b> \n"
                    if commands.getoutput(fdisk_swap_output) == '' :
                        info_dialog(_("Salix Live Installer was not able to detect a valid \
Swap partition on your system. \nA Swap partition could improve overall performances. \
You may want to exit Salix Live Installer now and use Gparted, or any other partitioning \
tool of your choice, to first create a Swap partition before resuming with Salix Live \
Installer process."))
                    else :
                        for i in Swap_Partition:
                            if "doesn't contain a valid partition table" not in i :
                                SwapText += _("Salix Live Installer has detected a Swap \
partition on " + i +" and will automatically add it to your configuration.\n")
                            else :
                                SwapText = _("Salix Live Installer was not able to detect \
a valid partition on your system. You should exit Salix Live Installer now and use Gparted, \
or any other partitioning tool of your choice, to first create valid partitions before resuming with Salix Live \
Installer process.")
                        info_dialog(SwapText)

            self.TimeTab.set_relief(gtk.RELIEF_NONE)
            self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
            self.LocaleTab.set_relief(gtk.RELIEF_NONE)
            self.PartitionTab.set_relief(gtk.RELIEF_HALF)
            self.UsersTab.set_relief(gtk.RELIEF_NONE)
            self.PackagesTab.set_relief(gtk.RELIEF_NONE)

    # What to do when the users tab is clicked
    def on_users_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            self.IntroBox.hide()
            self.TimeBox.hide()
            self.KeyboardBox.hide()
            self.LocaleBox.hide()
            self.MainPartitionBox.hide()
            self.RecapPartitionBox.hide()
            self.UsersBox.show()
            self.PackagesBox.hide()
            self.TimeTab.set_relief(gtk.RELIEF_NONE)
            self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
            self.LocaleTab.set_relief(gtk.RELIEF_NONE)
            self.PartitionTab.set_relief(gtk.RELIEF_NONE)
            self.UsersTab.set_relief(gtk.RELIEF_HALF)
            self.PackagesTab.set_relief(gtk.RELIEF_NONE)

    # What to do when the packages tab is clicked
    def on_packages_tab_clicked(self, widget, data=None):
        if switch_tab_lock == 'on' :
            pass
        else :
            self.IntroBox.hide()
            self.TimeBox.hide()
            self.KeyboardBox.hide()
            self.LocaleBox.hide()
            self.MainPartitionBox.hide()
            self.RecapPartitionBox.hide()
            self.UsersBox.hide()
            self.PackagesBox.show()
            self.TimeTab.set_relief(gtk.RELIEF_NONE)
            self.KeyboardTab.set_relief(gtk.RELIEF_NONE)
            self.LocaleTab.set_relief(gtk.RELIEF_NONE)
            self.PartitionTab.set_relief(gtk.RELIEF_NONE)
            self.UsersTab.set_relief(gtk.RELIEF_NONE)
            self.PackagesTab.set_relief(gtk.RELIEF_HALF)

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
    # If no root privilege, displays error message & exit
    if os.getuid() != 0:
        error_dialog(_("<b>Sorry!</b> \n\nRoot privileges are required to run this program. "))
        sys.exit(1)
    # If root privilege, show the gui & wait for signals
    SalixLiveInstaller()
    gtk.main()
