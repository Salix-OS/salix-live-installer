#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Salix Live Installer helps installing Salix on you computer.
This is the launcher.
"""
__app__ = 'salix-live-installer'
__copyright__ = 'Copyright 2011-2013, Salix OS'
__author__ = 'Pierrick Le Brun <akuna~at~salixos~dot~org> and Cyrille Pontvieux <jrd~at~enialis~dot~net>'
__credits__ = ['Pierrick Le Brun', 'Cyrille Pontvieux']
__maintainer__ = 'Cyrille Pontvieux'
__email__ = 'jrd~at~enialis~dot~net'
__license__ = 'GPL2+'
__version__ = '0.4'
__min_salt_version__ = '0.2.1'

import os
import sys

def usage():
  print """Salix Live Installer v{ver}
{copyright}
{license}
{author}

  launcher.py [--help] [--version] [--test [--clone] [--data]]

Parameters:
  --help: Show this help message
  --version: Show the Salix Live Installer version
  --test: Run it in test mode
    --clone: Run it simulating a LiveClone environment
    --data: Run itwith some pre-filled data
""".format(ver = __version__, copyright = __copyright__, license = __license__, author = __author__)

if __name__ == '__main__':
  os.chdir(os.path.dirname(__file__))
  is_graphic = bool(os.environ.get('DISPLAY'))
  is_test = False
  is_clone = False
  use_test_data = False
  for arg in sys.argv[1:]: # argv[0] = own name
    if arg == '--help':
      usage()
      sys.exit(0)
    elif arg == '--version':
      print __version__
      sys.exit(0)
    elif arg == '--test':
      is_test = True
      print "*** Testing mode ***"
    elif is_test and arg == '--clone':
      is_clone = True
      print "*** Clone mode ***"
    elif is_test and arg == '--data':
      use_test_data = True
      print "*** Test data mode ***"
    else:
      sys.stderr.write("Unrecognized parameter '{0}'.\n".format(arg))
      sys.exit(1)
  locale_dir = '/usr/share/locale'
  if is_test:
    locale_dir = '../data/locale'
  print 'Salix Live Installer v' + __version__
  if is_graphic:
    from salix_live_installer.installer_gtk import *
  else:
    from salix_live_installer.installer_curses import *
  run_install(__app__, locale_dir, __version__, __min_salt_version__, is_test, is_clone, use_test_data)
