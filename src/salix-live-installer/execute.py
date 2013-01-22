#!/usr/bin/env python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
Module to execute native commands and get their output:
  - execCall
  - execCheck
  - execGetOutput
  - checkRoot
"""
import subprocess
import sys
import os

def execCall(cmd, shell = True, env = {'LANG' : 'en_US'}):
  """
  Execute a command and return the exit code.
  The command is executed by default in a /bin/sh shell and using english locale.
  """
  return subprocess.call(cmd, shell = shell, env = env)

def execCheck(cmd, shell = True, env = {'LANG' : 'en_US'}):
  """
  Execute a command and return 0 if ok or a subprocess.CalledProcessorError exception in case of error.
  The command is executed by default in a /bin/sh shell and using english locale.
  """
  return subprocess.check_call(cmd, shell = shell, env = env)

def execGetOutput(cmd, withError = False, shell = True, env = {'LANG' : 'en_US'}):
  """
  Execute a command and return its output in a list, line by line.
  In case of error, it returns a subprocess.CalledProcessorError exception.
  The command is executed by default in a /bin/sh shell and using english locale.
  """
  stdErr = None
  if withError:
    stdErr = subprocess.STDOUT
  if sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 7): # ver >= 2.7
    return subprocess.check_output(cmd, stderr = stdErr, shell = shell, env = env).splitlines()
  else:
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = stdErr)
    output = p.communicate()[0]
    if p.returncode == 0:
      return output.splitlines()
    else:
      raise subprocess.CalledProcessError(returncode = p.returncode, cmd = cmd)

def checkRoot():
  """
  Raise an Exception if you run this code without root permissions
  """
  if os.getuid() != 0:
    raise Exception('You need root permissions.')

# Unit test
if __name__ == '__main__':
  from assertPlus import *
  assertEquals(0, execCall("ls"))
  assertEquals(0, execCall("ls -lh | grep '[.]'"))
  assertEquals(0, execCall("ls", shell = False))
  assertEquals(127, execCall("xyz"))
  assertException(subprocess.CalledProcessError, lambda: execCheck("xyz"))
  assertEquals(0, execCheck("ls"))
  assertEquals(os.getcwd(), execGetOutput("pwd")[0].strip())
  assertException(Exception, lambda: checkRoot())
