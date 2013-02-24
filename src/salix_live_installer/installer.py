#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
ThreadInstaller is a class to install Salix in a separated thread, with the use of ThreadTask class.
"""
__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'

import gettext
import threading
from time import sleep

class ThreadTask:
  """
  Handles starting a thread that will call a function.
  At the end, a callback may be called on completion.
  """
  def __init__(self, fct, complete_callback=None):
    self._fct = fct
    self._complete_callback = complete_callback
  def _start(self, *args, **kwargs):
    self._stopped = False
    self._fct(*args, **kwargs)
    if not self._stopped:
      if self._complete_callback:
        self._complete_callback()
  def start(self, *args, **kwargs):
    t = threading.Thread(target=self._start, args=args, kwargs=kwargs)
    t.start()
    return t
  def stop(self):
    self._stopped = True



class ThreadInstaller:
  """
  Starts a thread to install Salix from SalixLive.
  """
  def __init__(self, config, gather_gui):
    """
    'gather_gui' must have the following methods:
      - process_gui_events() to process waiting gui events.
      - update_gui_async(fct, *args, **kwargs) which will process the following function and arguments in the GUI thread.
      - install_set_main_window_visibility(is_shown)
      - install_set_progress_bar_text(text)
      - install_set_progress_bar_fraction(fraction)
      - install_set_cancel_button_sensitive(is_sensitive)
      - install_set_progress_window_visibility(is_shown)
      - install_set_progress_window_above(is_above)
    """
    self._cfg = config
    self._gui = gather_gui
  def install(self):
    self._installation = None
    self._gui.install_set_main_window_visibility(False)
    self._gui.install_set_progress_bar_text(_("Starting installation process..."))
    self._gui.install_set_progress_bar_fraction(0)
    self._gui.install_set_cancel_button_sensitive(True)
    self._gui.install_set_progress_window_visibility(True)
    self._gui.install_set_progress_window_above(True)
    t = ThreadTask(self._thread_install_salix, self._thread_install_completed).start()
    while t.is_alive():
      self._gui.process_gui_events()
    self._gui.process_gui_events()
    return self._installation
  def cancel(self):
    print "Installation cancelled."
    self._installation = 'cancelled'
    self._gui.install_set_cancel_button_sensitive(False)
    self._gui_update_progressbar(_("Cancelling installation..."), 1.0)
  def _update_gui(self, fct, *args, **kwargs):
    self._gui.update_gui_async(fct, *args, **kwargs)
  def _thread_install_salix(self):
    """
    Thread to install Salix.
    This works like a generator.
    It should yield fraction of the completion
    """
    print "Installing…"
    # format main partition (and mount it)
    # format linux partitions (and mount them)
    # copying modules (one step per module, so we need to count them before starting the installation)
    # create fstab
    # set date and time
    # set keyboard
    # set locale
    # set users
    # set services
    # update system things:
    # - pango, gtk, fonts, …
    # - adjusting configuration for liveclone
    if self._cfg.is_test:
      if self._cfg.is_test_clone:
        modules = ('01-clone',)
      else:
        modules = ('01-core', '02-basic', '03-full', '04-common', '05-kernel', '06-live')
    else:
      modules = sltl.listSaLTModules()
    if self._cfg.is_liveclone:
      install_modules = modules
    else:
      install_modules = []
      for m in modules:
        if 'core' in m:
          install_modules.append(m)
        elif 'basic' in m:
          if self._cfg.install_mode in ('basic', 'full'):
            install_modules.append(m)
        elif 'full' in m:
          if self._cfg.install_mode == 'full':
            install_modules.append(m)
        elif not 'live' in m:
          install_modules.append(m)
    if self._cfg.linux_partitions == None:
      self._cfg.linux_partitions = []
    if self._cfg.win_partitions == None:
      self._cfg.win_partitions = []
    weight_partition = 3
    if self._cfg.is_liveclone:
      weight_module = 15
    else:
      weight_module = 5
    weights = {
        'checks': 1,
        'main_partition': weight_partition,
        'linux_partitions': dict([(p[0], weight_partition) for p in self._cfg.linux_partitions]),
        'modules': dict([(m, weight_module) for m in install_modules]),
        'fstab': 1,
        'datetime': 1,
        'keyboard': 1,
        'locale': 1,
        'users': 1,
        'services': 1,
        'system_config': 1
        }
    steps = 0
    for w in weights.values():
      if isinstance(w, dict):
        for w2 in w.values():
          steps += w2
      else:
        steps += w
    step = 0
    self._installation = 'installing'
    def installion_cancelled():
      return self._installation == 'cancelled'
    # sanity checks
    modules_size = {}
    if self._cfg.is_test:
      for m in install_modules:
        modules_size[m] = 1
    else:
      main_sizes = sltl.getSizes("/dev/{0}".format(self._cfg.main_partition))
      main_size = main_sizes['size']
      main_block_size = sltl.getBlockSize("/dev/{0}".format(self._cfg.main_partition))
      module_total_size = 0
      for m in install_modules:
        size = sltl.getUsedSize("/mnt/salt/mnt/modules/{0}".format(m), main_block_size, False)['size']
        modules_size[m] = size
        module_total_size += size
      minimum_free_size = 50 * 1024 * 1024 # 50 M
      if module_total_size + minimum_free_size > main_size:
        self._gui.install_set_progress_window_above(False)
        error_dialog(_("Cannot install!\nNot enougth space on main partition ({size} needed)").format(size = sltl.getHumanSize(module_total_size + minimum_free_size)))
        self._installation = 'error'
        return
      sltl.execCall(['rm', '-r', sltl.getTempMountDir()])
    if installion_cancelled(): return
    step += weights['checks']
    msg = _("Formatting and mounting the main partition...")
    self._update_progressbar(msg, step, steps)
    self._install_main_partition()
    if installion_cancelled(): return
    step += weights['main_partition']
    msg = _("Formatting and mounting the Linux partitions...")
    self._update_progressbar(msg, step, steps)
    step = self._install_linux_partitions(msg, step, steps, weights['linux_partitions'])
    if installion_cancelled(): return
    msg = _("Installing the {mode} mode packages...").format(mode = _(self._cfg.install_mode))
    self._update_progressbar(msg, step, steps)
    step = self._install_modules(install_modules, modules_size, msg, step, steps, weights['modules'])
    if installion_cancelled(): return
    msg = _("Creating /etc/fstab...")
    self._update_progressbar(msg, step, steps)
    self._install_fstab()
    if installion_cancelled(): return
    step += weights['fstab']
    msg = _("Date and time configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_datetime()
    if installion_cancelled(): return
    step += weights['datetime']
    msg = _("Keyboard configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_keyboard()
    if installion_cancelled(): return
    step += weights['keyboard']
    msg = _("Locale configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_locale()
    if installion_cancelled(): return
    step += weights['locale']
    msg = _("Users configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_users()
    if installion_cancelled(): return
    step += weights['users']
    msg = _("Services configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_services()
    if installion_cancelled(): return
    step += weights['services']
    msg = _("System configuration...")
    self._update_progressbar(msg, step, steps)
    self._install_config()
    if installion_cancelled(): return
    step += weights['system_config']
    self._update_progressbar(None, step, steps)
  def _update_progressbar(self, msg, step, steps):
    fraction = float(step) / steps
    if msg:
      print "\n{1:3.0%} {0}".format(msg, fraction)
    else:
      print "\n{0:3.0%}".format(fraction)
    self._update_gui(self._gui_update_progressbar, msg, fraction)
  def _gui_update_progressbar(self, msg, fraction):
    if msg:
      self._gui.install_set_progress_bar_text(msg)
    self._gui.install_set_progress_bar_fraction(fraction)
  def _install_main_partition(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      d = "/dev/{0}".format(self._cfg.main_partition)
      sltl.umountDevice(d, deleteMountPoint = False)
      if self._cfg.main_format != 'none':
        label = sltl.getFsLabel(d)
        if not label:
          label = 'Salix'
        sltl.makeFs(self._cfg.main_partition, self._cfg.main_format, label = label)
      sltl.mountDevice(d, fsType = self._cfg.main_format)
  def _install_linux_partitions(self, msg, step, steps, weights):
    if self._cfg.is_test:
      for p in self._cfg.linux_partitions:
        if self._installation == 'cancelled': return step
        d = p[0]
        self._update_progressbar(msg + "\n - {0}".format(d), step, steps)
        w = weights[d]
        sleep(w)
        step += w
      return step
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      for p in self._cfg.linux_partitions:
        if self._installation == 'cancelled': return step
        d = p[0]
        self._update_progressbar(msg + "\n - {0}".format(d), step, steps)
        full_dev = "/dev/{0}".format(d)
        fs = p[1]
        mp = p[2]
        sltl.umountDevice(full_dev, deleteMountPoint = False)
        if fs != 'none':
          label = sltl.getFsLabel(full_dev)
          if not label:
            label = os.path.basename(p[2])
            if len(label) > 12:
              label = None # for not having problems
          sltl.makeFs(d, fs, label)
        sltl.mountDevice(full_dev, mountPoint = "{root}/{mp}".format(root = rootmp, mp = mp))
        step += weights[d]
      return step
  def _install_modules(self, modules, modules_size, msg, step, steps, weight):
    if self._cfg.is_test:
      for m in modules:
        if self._installation == 'cancelled': return step
        self._update_progressbar(msg + "\n - " + _("Installing the {module} module...").format(module = m), step, steps)
        w = weight[m]
        sleep(w)
        step += w
      return step
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self.main_partition))
      for m in modules:
        if self._installation == 'cancelled': return step
        self._update_progressbar(msg + "\n - " + _("Installing the {module} module...").format(module = m), step, steps)
        size = modules_size[m]
        w = weight[m]
        sltl.installSaLTModule(m, size, rootmp, self._install_module_callback, (step, steps, w))
        step += w
      return step
  def _install_module_callback(self, pourcent, step, steps, weight):
    new_step = step + float(pourcent) * weight
    self._update_gui(self._update_progressbar, None, new_step, steps)
  def _install_fstab(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      sltl.createFsTab(rootmp)
      sltl.addFsTabEntry(rootmp, 'proc', '/proc', 'proc')
      sltl.addFsTabEntry(rootmp, 'devpts', '/dev/pts', 'devpts')
      sltl.addFsTabEntry(rootmp, 'tmpfs', '/dev/shm', 'tmpfs')
      for d in self._cfg.swap_partitions:
        sltl.addFsTabEntry(rootmp, "/dev/" + d, 'none', 'swap')
      sltl.addFsTabEntry(rootmp, "/dev/" + self._cfg.main_partition, '/', self._cfg.main_format, dumpFlag = 1, fsckOrder = 1)
      for l in (self._cfg.linux_partitions, self._cfg.win_partitions):
        if l:
          for p in l:
            d = p[0]
            fs = p[1]
            if fs == 'none': # tell to not format, so...
              fs = None # ...come back to autodetection
            mp = p[2]
            try:
              os.makedirs(rootmp + mp)
            except os.error:
              pass # directory exists
            sltl.addFsTabEntry(rootmp, "/dev/" + d, mp, fs)
  def _install_datetime(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      tz = self._cfg.cur_tz_continent + '/' + self._cfg.cur_tz_city
      sltl.setDefaultTimeZone(tz, rootmp)
      sltl.setNTPDefault(self._cfg.cur_use_ntp, rootmp)
      if not self._cfg.cur_use_ntp:
        # we need to update the locale date and time.
        dt = (datetime.now() + self._cfg.cur_time_delta).strftime("%Y-%m-%d %H:%M:%S")
        execCall(['/usr/bin/date', '-s', dt], shell=False)
        execCall(['/sbin/hwclock', '--systohc'], shell=False)
  def _install_keyboard(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      sltl.setDefaultKeymap(self._cfg.cur_km, rootmp)
      sltl.setNumLockDefault(self._cfg.cur_use_numlock, rootmp)
      sltl.setIbusDefault(self._cfg.cur_use_ibus, rootmp)
  def _install_locale(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      sltl.setDefaultLocale(self._cfg.cur_locale, rootmp)
  def _install_users(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      if not self._cfg.keep_live_logins:
        rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
        sltl.createSystemUser(self._cfg.new_login, password = self._cfg.new_password, mountPoint = rootmp)
        sltl.changePasswordSystemUser('root', password = self._cfg.new_root_password, mountPoint = rootmp)
  def _install_services(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      f = 'var/log/setup/setup.services'
      p = "{0}/{1}".format(rootmp, f)
      if os.path.exists(p):
        os.chmod(p, 0755)
        sltl.execCall("{0}/{1} {0}".format(rootmp, f))
  def _install_config(self):
    if self._cfg.is_test:
      sleep(1)
    else:
      rootmp = sltl.getMountPoint("/dev/{0}".format(self._cfg.main_partition))
      rcfont_file = open('{0}/etc/rc.d/rc.font'.format(rootmp), 'w')
      rcfont_file.write("""
#!/bin/sh
#
#This selects your default screen font from among the ones in
# /usr/share/kbd/consolefonts.
#
#setfont -v ter-v16n
unicode_start ter-v16n""")
      rcfont_file.close()
      os.chmod('{0}/etc/rc.d/rc.font'.format(rootmp), 0755)
      for f in ('var/log/setup/setup.04.mkfontdir', 'var/log/setup/setup.07.update-desktop-database', 'var/log/setup/setup.07.update-mime-database', 'var/log/setup/setup.08.gtk-update-icon-cache', 'var/log/setup/setup.htmlview'):
        p = "{0}/{1}".format(rootmp, f)
        if os.path.exists(p):
          os.chmod(p, 0755)
          sltl.execCall("cd {0}; ./{1}".format(rootmp, f))
      for f in ('/usr/bin/update-gtk-immodules', '/usr/bin/update-gdk-pixbuf-loaders', '/usr/bin/update-pango-querymodules'):
        p = "{0}/{1}".format(rootmp, f)
        if os.path.exists(p):
          sltl.execChroot(rootmp, f)
      if self._cfg.is_liveclone:
        # Remove some specific live stuff
        sltl.execCall("spkg -d liveclone --root={0}".format(rootmp))
        sltl.execCall("spkg -d salix-live-installer --root={0}".format(rootmp))
        sltl.execCall("spkg -d salix-persistence-wizard --root={0}".format(rootmp))
        sltl.execCall("rm -f {0}/etc/ssh/ssh_host_*".format(rootmp))
        sltl.execCall("rm -f {0}/home/*/Desktop/*startup-guide*desktop".format(rootmp))
        sltl.execCall("rm -f {0}/user/share/applications/*startup-guide*desktop".format(rootmp))
        os.remove("{0}/hooks.salt".format(rootmp))
  def _thread_install_completed(self):
    if self._installation == 'installing':
      self._installation = 'done'
      self._update_gui(self._gui_install_completed)
    else:
      self._update_gui(self._gui_install_failed)
    print "End of installation thread"
  def _gui_install_failed(self):
    if self._installation == 'error':
      print "Installation in error."
    elif self._installation == 'cancelled':
      print "Installation cancelled."
    self._gui.install_set_progress_window_above(False)
    self._gui.install_set_progress_window_visibility(False)
    self._gui.install_set_main_window_visibility(True)
  def _gui_install_completed(self):
    print "Installation completed."
    self._gui.install_set_progress_window_above(False)
    self._gui.install_set_progress_window_visibility(False)
