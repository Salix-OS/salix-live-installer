#!/bin/evn python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
assert functions:
 - assertTrue(expression)
 - assertFalse(expression)
 - assertEquals(expected, value)
 - assertNotEquals(expected, value)
 - assertException(exceptionType, function)
 - assertNoException(function)
"""
def assertTrue(expression):
  assert expression, "'%s' was expected to be true" % expression
def assertFalse(expression):
  assert (not expression), "'%s' was expected to be false" % expression
def assertEquals(expected, value):
  assert expected == value, "'%s' expected, got '%s'" % (expected, value)
def assertNotEquals(expected, value):
  assert expected != value, "'%s' not expected, got '%s'" % (expected, value)
def assertException(exceptionType, function):
  triggered = False
  try:
    function()
  except BaseException as e:
    if isinstance(e, exceptionType):
      triggered = True
  assert triggered, "Exception '%s' expected with '%s'" % (exceptionType, function.__doc__)
def assertNoException(function):
  triggered = False
  unExpectedE = None
  try:
    function()
  except BaseException as e:
    unExpectedE = e
    triggered = True
  assert (not triggered), "Exception '%s' was not expected with '%s'" % (unExpected, function.__doc__)
