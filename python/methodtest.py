#!/usr/bin/env python
# The python method test

"""The python method test
"""

class Wrapper(object):
    """A wrapper
    """
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        """Get
        """
        print 'GET', instance, owner
        return self.method

class Tester(object):
    """The test class
    """
    def __init__(self):
        self.amethod = Wrapper(None)

    def amethod(self):
        """A method
        """
        pass

    print 'RAW >', id(amethod)
    amethod = Wrapper(amethod)
    print 'WRAPPER >', id(amethod)

print 'From class >'
print id(Tester.amethod)
print 'New class'
tester = Tester()
print 'From object >'
print id(tester.amethod)

def xmethod((a, b), c):
    pass

