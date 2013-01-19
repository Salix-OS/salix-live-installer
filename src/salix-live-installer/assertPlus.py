#!/bin/evn python
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
assert functions:
 - assertTrue(expression)
 - assertFalse(expression)
 - assertEquals(expected, expression)
 - assertNotEquals(expected, expression)
 - assertException(exceptionType, function)
 - assertNoException(function)

to pass a function, you can use lambda expression like:
  assertException(lambda: myfunction())
"""
def assertTrue(expression):
  "Expect the expression to be true"
  assert expression, "'%s' was expected to be true" % expression
def assertFalse(expression):
  "Expect the expression to be false"
  assert (not expression), "'%s' was expected to be false" % expression
def assertEquals(expected, expression):
  "Expect that the expression equals to the expected value"
  assert expression == expected, "'%s' expected, got '%s'" % (expected, expression)
def assertNotEquals(expected, expression):
  "Expect that the expression does not equals to the expected value"
  assert expression != expected, "'%s' not expected, got '%s'" % (expected, expression)
def assertException(exceptionType, function):
  "Expect that the function trigger an exception of type exceptionType"
  triggered = False
  try:
    function()
  except BaseException as e:
    if isinstance(e, exceptionType):
      triggered = True
  assert triggered, "Exception '%s' expected with '%s'" % (exceptionType, function.__doc__)
def assertNoException(function):
  "Expect that the function does not trigger any exception"
  triggered = False
  unExpectedE = None
  try:
    function()
  except BaseException as e:
    unExpectedE = e
    triggered = True
  assert (not triggered), "Exception '%s' was not expected with '%s'" % (unExpected, function.__doc__)

# Unit test
if __name__ == '__main__':
  assertTrue(True)
  assertFalse(False)
  assertEquals(0, 2 - 2)
  assertNotEquals(1, 2 - 2)
  assertException(ZeroDivisionError, lambda: 1 / 0)
  assertNoException(lambda: 1)
