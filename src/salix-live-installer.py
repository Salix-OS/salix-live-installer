#!/usr/bin/env python

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#                                                                             #
# Salix installer will install Salix on your computer from the comfort of     #
# SalixLive's graphic environment.                                            #
#                                                                             #
# Copyright Pierrick Le Brun <akuna~at~free~dot~fr>.                          #
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

# version = '0.1' - 201002021400 build -  First version

import commands
import subprocess
import os
import gtk
import sys
import gobject
import glob

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

# To do => Add time zone settings
# To do => Install log
# To do => More Error checking with subprocess.check_call() and try/except

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
        self.WinMountComboCell = builder.get_object("win_newmount_renderer_combo")
        self.WinMountColumn = builder.get_object("win_newmount_column")
        self.WinMountListStore = builder.get_object("win_mountpoint_list_store")
        self.MainPartRecapLabel = builder.get_object("main_part_recap_label")
        self.LinPartRecapLabel = builder.get_object("lin_part_recap_label")
        self.WinPartRecapLabel = builder.get_object("win_part_recap_label")
        self.LiveKernelRadioButton = builder.get_object("live_kernel_radiobutton")
        self.SalixKernelRadioButton = builder.get_object("salix_kernel_radiobutton")
        self.CoreRadioButton = builder.get_object("core_radiobutton")
        self.BasicRadioButton = builder.get_object("basic_radiobutton")
        self.FullRadioButton = builder.get_object("full_radiobutton")
        self.PackagesApplyButton = builder.get_object("packages_apply")
        self.TimeApplyButton = builder.get_object("time_apply")
        self.KeyboardApplyButton = builder.get_object("keyboard_apply")
        self.LocaleApplyButton = builder.get_object("locale_apply")
        self.RootPass1Entry = builder.get_object("root_pass1_entry")
        self.RootPass2Entry = builder.get_object("root_pass2_entry")
        self.UserPass1Entry = builder.get_object("user_pass1_entry")
        self.UserPass2Entry = builder.get_object("user_pass2_entry")
        self.UserLoginEntry = builder.get_object("user_login_entry")
        self.UserVisibleCheckButton = builder.get_object("user_visible_checkbutton")
        self.RootVisibleCheckButton = builder.get_object("root_visible_checkbutton")
        self.ExternalDeviceCheckButton = builder.get_object("external_device_checkbutton")
        self.NumLockCheckButton = builder.get_object("numlock_checkbutton")
        self.RootPassCreated = builder.get_object("root_pass_created")
        self.NewUserLogin = builder.get_object("new_user_login")
        self.UsersApplyButton = builder.get_object("users_apply")
        self.RootPassApplyButton = builder.get_object("rootpass_apply")
        self.InstallButton = builder.get_object("install_button")
        self.YearCombobox = builder.get_object("year_combobox")
        self.MonthCombobox = builder.get_object("month_combobox")
        self.DayCombobox = builder.get_object("day_combobox")
        self.ZoneCombobox = builder.get_object("zone_combobox")
        self.YearListStore = builder.get_object("year_list_store")
        self.MonthListStore = builder.get_object("month_list_store")
        self.DayListStore = builder.get_object("day_list_store")
        self.ZoneListStore = builder.get_object("zone_list_store")
        self.NTPCheckButton = builder.get_object("ntp_checkbutton")
        self.ManualTimeBox = builder.get_object("manual_time_box")
        self.HourSpinButton = builder.get_object("hour_spinbutton")
        self.MinuteSpinButton = builder.get_object("minute_spinbutton")
        self.SecondSpinButton = builder.get_object("second_spinbutton")
        self.TimeZoneBox = builder.get_object("time_zone_box")

        # Connect signals
        builder.connect_signals(self)

### INITIALIZATION ###

        ### Initialise some global variables ###
        # Prevent switching to another tab until the current configuration is completed or cancelled
        global switch_tab_lock
        switch_tab_lock = ''
        # Control which partition box is shown depending if the configuration is set or not
        global partition_done_lock
        partition_done_lock = ''
        # The other partition lists needs to know what has been chosen as the main partition
        global Selected_Main_Partition
        Selected_Main_Partition = ''
        # Initialize the lock system preventing the Install button to be activated prematurely
        global ConfigurationSet
        ConfigurationSet = ['no'] * 7
        # Initialise the external device checkbutton value
        global show_external_device
        show_external_device = 'no'
        global LaunchLiloSetup
        LaunchLiloSetup = False
        global LinPartConfirmLabel
        LinPartConfirmLabel = ''
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
                # set the status of the numlock checkbutton
                global set_numlock
                if self.NumLockCheckButton.get_active() == True :
                    set_numlock = 'yes'
                else :
                    set_numlock = 'no'
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
#        os.environ['LANG'] = 'en_US'
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

            self.ZoneListStore.clear()
            global zonelist
            zonelist = sorted(glob.glob("/usr/share/zoneinfo/*/*"))
            current_zone = commands.getoutput("ls -l /etc/localtime-copied-from").split()[-1].replace('/usr/share/zoneinfo/', '')
            global current_zone_index
            zone_index = 0
            for i in zonelist:
                zone_info = i.replace('/usr/share/zoneinfo/', '')
                self.ZoneListStore.append([zone_info])
                if current_zone == zone_info:
                    current_zone_index = zone_index
                zone_index += 1

        # Initialize the main partitions list.
        global partition_list_initialization
        def partition_list_initialization() :
            global part_feedline_list
            part_feedline_list = []
            self.MainPartitionListStore.clear()
            # Use non-localized environment to avoid problems
            os.environ['LANG'] = 'en_US'
            # Detect all partitions except swap and extended
            strip_swap_extended = 'parted -sl | grep -v swap | grep -v extended'
            global parted_output
            parted_output = commands.getoutput(strip_swap_extended).splitlines()
            # Initialize the different variables
            disk_name = ''
            disk_size = ''
            disk_device = ''
            part_name = ''
            part_size = ''
            part_system = ''
            part_feedline = ''
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
                # Get the device reference & size of the disk
                elif 'Disk' in line:
                    disk_device = line.split()[1]
                    disk_size = line.split()[2]
                # Get the size & filesystem for each partition of the disk
                elif line.startswith(' '):
                    part_name = disk_device.replace(':', '') + line.split() [0]
                    part_size = line.split() [3]
                    try :
                        part_system = line.split() [5]
                        if 'ext3' in part_system:
                            part_system = 'ext3/ext4'
                    except :
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
                        if usb_dev != '' :
                            pass
                        elif firewire_dev != '' :
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

### Callback signals waiting in a constant loop: ###

### WINDOWS MAIN SIGNALS ###	
	
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


    # What to do when the NTP checkbutton is toggled
    def on_ntp_checkbutton_toggled(self, widget, data=None):
        global set_ntp
        if self.NTPCheckButton.get_active() == True:
            self.ManualTimeBox.set_sensitive(False)
            set_ntp = 'yes'
        else:
            self.ManualTimeBox.set_sensitive(True)
            set_ntp = 'no'

    # What to do when the user's password visible checkbutton is toggled
    def on_numlock_checkbutton_toggled(self, widget, data=None):
        global set_numlock
        if self.NumLockCheckButton.get_active() == True :
            set_numlock = 'yes'
        else :
            set_numlock = 'no'
						
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

    # What to do when a combo line is edited in the Linux New system column
    def on_linux_newsys_renderer_combo_edited(self, widget, row_number, new_text):
        # Retrieve the selected Linux partition row iter
        linuxnewsyschoice = self.LinuxPartitionList.get_selection()
        self.LinuxPartitionListStore, iter = linuxnewsyschoice.get_selected()
        # Set the new partition row value on the fifth column (4)
        if new_text in ('ext2', 'ext3', 'ext4', 'reiserfs', 'xfs', 'jfs', 'Select...' ):
            self.LinuxPartitionListStore.set_value(iter, 4, new_text)

    # What to do when a combo line is edited in the Linux mountpoint column
    def on_linux_newmount_renderer_combo_edited(self, widget, row_number, new_text):
        # Retrieve the selected Linux partition row iter
        linuxnewmountchoice = self.LinuxPartitionList.get_selection()
        self.LinuxPartitionListStore, iter = linuxnewmountchoice.get_selected()
        # Set the new partition row value on the sixth column (5)
        self.LinuxPartitionListStore.set_value(iter, 5, new_text)
				
    # What to do when a combo line is edited in the Windows mountpoint column
    def on_win_newmount_renderer_combo_edited(self, widget, row_number, new_text,):
        # Retrieve the selected Windows partition row iter
        windowsnewmountchoice = self.WindowsPartitionList.get_selection()
        self.WindowsPartitionListStore, iter = windowsnewmountchoice.get_selected()
        # Set the new mountpoint row value on the fifth column (4)
        self.WindowsPartitionListStore.set_value(iter, 4, new_text)

# CONFIGURATION APPLY BUTTONS ###

    # What to do when the time selection button is clicked
    def on_time_apply_clicked(self, widget, data=None):
        # Display the 'Done' check
        self.TimeCheck.show()
        self.TimeCheckMarker.hide()
        self.TimeApplyButton.set_sensitive(False)
        self.ManualTimeBox.set_sensitive(False)
        self.NTPCheckButton.set_sensitive(False)
        self.TimeZoneBox.set_sensitive(False)
        global ConfigurationSet, set_ntp, months, zonelist, set_zone
        ConfigurationSet[6] = 'yes'
        set_zone = zonelist[self.ZoneCombobox.get_active()]
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
        LinFullSets = []
        global LinFormatSets
        LinFormatSets = []
        global LinMountSets
        LinMountSets = []
        global WinMountSets
        WinMountSets = []
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

    # What to do when the user's settings apply button is clicked
    def on_users_apply_clicked(self, widget, data=None):
        # Pass some basic sanity checks
        # To do => prevent the use of caps for login
        if self.UserLoginEntry.get_text() == '' :
            error_dialog("\n" + _("Your user's name is empty") + ". " + _("Please verify and correct") + "! \n")
        elif self.UserLoginEntry.get_text().replace(' ', '').isalnum() == False :
            error_dialog("\n" + _("Your user's name should only contain alphanumeric characters") + ". "\
            + _("Please verify and correct") + "! \n")
        elif ' ' in self.UserLoginEntry.get_text() :
            error_dialog("\n" + _("Your user's name should not contain any space") + ". "\
            + _("Please verify and correct") + "! \n")
        elif self.UserLoginEntry.get_text().islower() != True :
            error_dialog("\n" + _("Your user's name should not contain any upper case letter") + ". "\
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
        global Selected_Kernel
        if self.SalixKernelRadioButton.get_active() == True :
            Selected_Kernel = _('standard')
        elif self.LiveKernelRadioButton.get_active() == True :
            Selected_Kernel = _('live')
        self.CoreRadioButton.set_sensitive(False)
        self.BasicRadioButton.set_sensitive(False)
        self.FullRadioButton.set_sensitive(False)
        self.SalixKernelRadioButton.set_sensitive(False)
        self.LiveKernelRadioButton.set_sensitive(False)
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
        LastRecapFullText += "\n<b>" + _("Standard User") + ":</b> \n" + NewUser + "\n"
        LastRecapFullText += "\n<b>" + _("Packages") + ":</b> \n"
        # TRANSLATORS: Please just reposition the 2 '%(...)s' variables as required by your grammar.
        LastRecapFullText += _("You have chosen the %(mode)s installation mode with the %(type)s kernel.\n")\
        % {'mode': Selected_Install_Mode, 'type': Selected_Kernel}
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

    # What to do when the user's settings undo button is clicked
    def on_users_undo_clicked(self, widget, data=None):
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

    # What to do when the root password settings undo button is clicked
    def on_rootpass_undo_clicked(self, widget, data=None):
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

    # What to do when the package selection undo button is clicked
    def on_packages_undo_clicked(self, widget, data=None):
        self.CoreRadioButton.set_sensitive(True)
        self.BasicRadioButton.set_sensitive(True)
        self.FullRadioButton.set_sensitive(True)
        self.SalixKernelRadioButton.set_sensitive(True)
        self.LiveKernelRadioButton.set_sensitive(True)
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
                    fdisk_shell_output = "fdisk -l | grep " + set[1]
                    stripped_fdisk_output = commands.getoutput(fdisk_shell_output)
                    if "Linux" in stripped_fdisk_output :
                        # Let the installer know about it:
                        extra_part_toset.append('linux')
                        # Insert editable combobox in appropriate list cells for new formatting configuration
                        self.LinuxNewSysComboCell.set_property("model", self.LinuxFormatListStore)
                        self.LinuxNewSysComboCell.set_property('text-column', 0)
                        self.LinuxNewSysComboCell.set_property('editable', True)
                        self.LinuxNewSysColumn.set_attributes(self.LinuxNewSysComboCell, text = 4)
                        set.append(_("Select..."))
                        # Insert editable combobox in appropriate list cells for new mounting configuration
                        self.LinuxNewMountComboCell.set_property("model", self.LinuxMountListStore)
                        self.LinuxNewMountComboCell.set_property('text-column', 0)
                        self.LinuxNewMountComboCell.set_property('editable', True)
                        self.LinuxNewMountColumn.set_attributes(self.LinuxNewMountComboCell, text = 5)
                        set.append(_("Select..."))
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
                    fdisk_shell_output = "fdisk -l | grep " + set[1]
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
                            self.WinMountColumn.set_attributes(self.WinMountComboCell, text = 4)
                            set.append(_("Select..."))
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
            self.WinPartRecapLabel.set_text(WinPartConfirmLabel)
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
                if os.path.exists("/mnt/live/memory/images/01-core.lzm") == False :
                    self.YesNoDialog.hide()
                    error_dialog(_("""<b>Sorry!</b>
\nSalix Live Installer is only meant to be used in a LiveCD environment. 
\nYou cannot proceed any further! """))
                elif os.path.exists("/mnt/live/memory/changes/home/one") == False :
                    self.YesNoDialog.hide()
                    error_dialog(_("""<b>Sorry!</b>
\nSalix Live Installer is only meant to be used in a LiveCD environment. 
\nYou cannot proceed any further! """))
                else :
                    task = self.salix_install_process()
                    gobject.idle_add(task.next)

    # Install process
    def salix_install_process(self):
        self.YesNoDialog.hide()
        self.Window.hide()
        self.InstallProgressBar.set_text(_("Starting installation process..."))
        self.InstallProgressBar.set_fraction(0.03)
        self.ProgressWindow.show()
        self.ProgressWindow.set_keep_above(True)
        # there's more work, yield True
        yield True
        # Format and remount the main partition
        global Main_MountPoint
        Main_MountPoint = Selected_Main_Partition.replace('dev', 'mnt')
        if os.path.exists(Main_MountPoint) == False :
            os.mkdir(Main_MountPoint)
        subprocess.call("umount -l " + Selected_Main_Partition, shell=True)

        self.InstallProgressBar.set_text(_("Formatting the main partition..."))
        self.InstallProgressBar.set_fraction(0.06)
        # there's more work, yield True
        yield True
        if 'ext' in Selected_Main_Format :
            subprocess.call("mkfs -t " + Selected_Main_Format + " " + Selected_Main_Partition, shell=True)
        else :
            subprocess.call("mkfs -t " + Selected_Main_Format + " -f " + Selected_Main_Partition, shell=True)
        subprocess.call("mount -t " + Selected_Main_Format + " " + Selected_Main_Partition + " " + Main_MountPoint , shell=True)
        # Format and/or remount the other Linux partitions (Windows partitions will be managed later while generating /etc/fstab)
        if LinFullSets != [] :
            self.InstallProgressBar.set_text(_("Formatting and mounting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.09)
            # there's more work, yield True
            yield True
            for i in LinFullSets :
                os.makedirs(Main_MountPoint + i[2])
                subprocess.call("umount -l " + i[0], shell=True)
                if 'ext' in i[1] :
                    subprocess.call("mkfs -t " + i[1] + " " + i[0], shell=True)
                else :
                    subprocess.call("mkfs -t " + i[1] + " -f " + i[0], shell=True)
                subprocess.call("mount -t " + i[1] + " " + i[0] + " " + Main_MountPoint + i[2], shell=True)
        if LinFormatSets != [] :
            self.InstallProgressBar.set_text(_("Formatting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.12)
            # there's more work, yield True
            yield True
            for i in LinFormatSets :
                subprocess.call("umount -l " + i[0], shell=True)
                if 'ext' in i[1] :
                    subprocess.call("mkfs -t " + i[1] + " " + i[0], shell=True)
                else :
                    subprocess.call("mkfs -t " + i[1] + " -f " + i[0], shell=True)
        if LinMountSets != [] :
            self.InstallProgressBar.set_text(_("Mounting your Linux partition(s)..."))
            self.InstallProgressBar.set_fraction(0.15)
            # there's more work, yield True
            yield True
            for i in LinMountSets :
                os.makedirs(Main_MountPoint + i[2])
                subprocess.call("mount " + i[0] + " " + Main_MountPoint + i[2], shell=True)
        # Unsquashfs the live modules on the mounted installation partition(s)
        # (Actually since unsquashfs can be buggy & can stall, we will mount + copy instead)
        os.mkdir(Main_MountPoint + "/temp_mount")
        Temp_Mount = Main_MountPoint + "/temp_mount"
        if Selected_Install_Mode == _('core') :
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
            self.InstallProgressBar.set_fraction(0.40)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            self.InstallProgressBar.set_text(_("Installing the common packages..."))
            self.InstallProgressBar.set_fraction(0.50)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
        elif Selected_Install_Mode == _('basic') :
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('core')})
            self.InstallProgressBar.set_fraction(0.25)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
            self.InstallProgressBar.set_fraction(0.50)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*basic.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            self.InstallProgressBar.set_text(_("Installing the common packages..."))
            self.InstallProgressBar.set_fraction(0.60)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
        elif Selected_Install_Mode == _('full') :
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('core')})
            self.InstallProgressBar.set_fraction(0.20)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*core.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': _('basic')})
            self.InstallProgressBar.set_fraction(0.35)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*basic.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            # TRANSLATORS: Simply reposition the '%(mode)s' variable as required by your grammar. The value of '%(mode)s' will be 'core', 'basic' or 'full'.
            self.InstallProgressBar.set_text(_("Installing the %(mode)s mode packages...") % {'mode': Selected_Install_Mode})
            self.InstallProgressBar.set_fraction(0.50)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*full.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            self.InstallProgressBar.set_text(_("Installing the common packages..."))
            self.InstallProgressBar.set_fraction(0.60)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*common.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
        if Selected_Kernel == _('live') :
            # TRANSLATORS: Simply reposition the '%(type)s' variable as required by your grammar. The value of '%(type)s' will be 'standard' or 'live'.
            self.InstallProgressBar.set_text(_("Installing the %(type)s kernel...") % {'type': Selected_Kernel})
            self.InstallProgressBar.set_fraction(0.65)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*kernel.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)
            self.InstallProgressBar.set_text(_("Installing the livetools..."))
            self.InstallProgressBar.set_fraction(0.75)
            # there's more work, yield True
            yield True
            subprocess.call("mount -t squashfs /mnt/*/salixlive/base/*livetools.lzm " + Temp_Mount + " -o loop", shell=True)
            subprocess.call("cp --preserve -rf " + Temp_Mount + "/* " + Main_MountPoint, shell=True)
            subprocess.call("umount " + Temp_Mount, shell=True)

        elif Selected_Kernel == _('standard') :
            # TRANSLATORS: Simply reposition the '%(type)s' variable as required by your grammar. The value of '%(type)s' will be 'standard' or 'live'.
            self.InstallProgressBar.set_text(_("Installing the %(type)s kernel...") % {'type': Selected_Kernel})
            self.InstallProgressBar.set_fraction(0.70)
            # there's more work, yield True
            yield True
            subprocess.call("spkg --root=" + Main_MountPoint + " /mnt/*/packages/std-kernel/*", shell=True)
        os.rmdir(Temp_Mount)

        # Create /etc/fstab
        self.InstallProgressBar.set_text(_("Creating /etc/fstab..."))
        self.InstallProgressBar.set_fraction(0.80)
        # there's more work, yield True
        yield True
        fdisk_swap_output = 'fdisk -l | grep -i swap | cut -f1 -d " "'
        Swap_Partition = commands.getoutput(fdisk_swap_output)
        Fstab_File = open(Main_MountPoint + '/etc/fstab', 'w')
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('devpts', '/dev/pts', 'devpts', 'gid=5,mode=620', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('proc', '/proc', 'proc', 'defaults', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % ('tmpfs', '/dev/shm', 'tmpfs', 'defaults', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (Swap_Partition, 'swap', 'swap', 'defaults', '0', '0'))
        Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (Selected_Main_Partition, '/', Selected_Main_Format, 'noatime,defaults', '1', '1'))
        LinSets = LinFullSets + LinFormatSets
        if LinSets != [] :
            for i in LinSets :
                Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[2], i[1] , 'noatime,defaults', '1', '2'))
        if LinMountSets != [] :
            for i in LinMountSets :
                lshal_fstype_output = "lshal | grep -A10 hda5 | grep 'volume.fstype =' "
                Lin_Filesys_String = commands.getoutput(lshal_fstype_output)
                Lin_Filesys = Lin_Filesys_String.split("'")[1]
                Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[2], Lin_Filesys , 'noatime,defaults', '1', '2'))
        if WinMountSets != [] :
            os.environ['LANG'] = 'en_US'
            for i in WinMountSets :
                fdisk_win_output = 'fdisk -l | grep ' + i[0]
                Win_Filesys = commands.getoutput(fdisk_win_output)
                os.makedirs(Main_MountPoint + i[1])
                if 'NTFS' in Win_Filesys :
                    Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[1], 'ntfs-3g' , 'umask=000', '1', '0'))
                if 'FAT32' in Win_Filesys :
                    Fstab_File.write('%-20s%-20s%-15s%-20s%-10s%s\n' % (i[0], i[1], 'vfat' , 'defaults,utf8,umask=0,shortname=mixed', '1', '0'))
        Fstab_File.close()

        # Create /etc/rc.d/rc.font
        self.InstallProgressBar.set_text(_("Creating /etc/rc.d/rc.font..."))
        self.InstallProgressBar.set_fraction(0.90)
        # there's more work, yield True
        yield True
        RCfont_File = open(Main_MountPoint + '/etc/rc.d/rc.font', 'w')
        RCfont_File.write("#!/bin/sh\n\
#\n\
#This selects your default screen font from among the ones in\n\
# /usr/share/kbd/consolefonts.\n\
#\n\
#setfont -v ter-v16n\n\
unicode_start ter-v16n")
        RCfont_File.close()

        # Set Time, Keyboard, locale, login...
        self.InstallProgressBar.set_text(_("Setting the time, keyboard, locale & login..."))
        self.InstallProgressBar.set_fraction(0.95)
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

        RCkeymap_File = open(Main_MountPoint + '/etc/rc.d/rc.keymap', 'w')
        RCkeymap_File.write("#!/bin/sh\n\
#\n\
# Load the keyboard map.  More maps are in /usr/share/kbd/keymaps.\n\
if [ -x /usr/bin/loadkeys ]; then\n\
/usr/bin/loadkeys -u " + Selected_Keyboard + ".map\n\
fi")
        RCkeymap_File.close()
        subprocess.call('chmod -x ' + Main_MountPoint + '/etc/rc.d/rc.keymap', shell=True)

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
(If you prefer to use another bootloader utility, click on the no button
and use the application of your choice before rebooting your machine.)\n"""))
            # Set localized environment back so that lilosetup comes up in the local language
            os.environ['LANG'] = Selected_Locale
            global LaunchLiloSetup
            LaunchLiloSetup = True
            self.YesNoDialog.show()
            self.YesNoDialog.resize(1, 1)
            # there's no more work, yield False
            yield False

    # Set up keyboard, locale & users
    def chroot_settings(self) :
        os.listdir(Main_MountPoint)
        os.chroot(Main_MountPoint)
        # We have to deactivate some stuff in keyboardsetup first
        subprocess.call('sed -i "s/cd $backtohome/# cd $backtohome/" /usr/sbin/keyboardsetup', shell=True)
        subprocess.call('sed -i "s/\/etc\/rc.d\/rc.hald restart/# \/etc\/rc.d\/rc.hald restart/" /usr/sbin/keyboardsetup', shell=True)
        if set_numlock == 'yes' :
            try :
                subprocess.check_call('keyboardsetup ' + Selected_Keyboard + ' on', shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new keyboard selection on the installation target. "))
        else :
            try :
                subprocess.check_call('keyboardsetup ' + Selected_Keyboard + ' off', shell=True)
            except :
                error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new keyboard selection on the installation target. "))
        subprocess.call('sed -i "s/# cd $backtohome/cd $backtohome/" /usr/sbin/keyboardsetup', shell=True)
        subprocess.call('sed -i "s/# \/etc\/rc.d\/rc.hald restart/\/etc\/rc.d\/rc.hald restart/" /usr/sbin/keyboardsetup', shell=True)
        try :
            subprocess.check_call('localesetup ' + Selected_Locale, shell=True)
        except :
            error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new language selection on the installation target. "))
        try :
            subprocess.check_call('useradd -m -s /bin/bash -G floppy,audio,video,cdrom,plugdev,power,netdev,scanner ' + NewUser, shell=True)
        except :
            error_dialog(_("<b>Sorry!</b> \n\nUnable to create the new user on the installation target. "))
        try :
            subprocess.check_call('echo "' + NewUser + ':' + NewUserPW + '" | chpasswd', shell=True)
        except :
            error_dialog(_("<b>Sorry!</b> \n\nUnable to set the new user's password on the installation target. "))
        try :
            subprocess.check_call('echo "root:' + NewRootPW + '" | chpasswd', shell=True)
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
                self.ZoneCombobox.set_active(current_zone_index)
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

# Error window skeleton:
def error_dialog(message, parent = None):
    """
    Displays an error message.
    """
    dialog = gtk.MessageDialog(parent = parent, type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE, flags = gtk.DIALOG_MODAL)
    dialog.set_markup(message)
    dialog.set_icon_from_file("/usr/share/icons/gnome-colors-common/scalable/actions/gtk-stop.svg")
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
