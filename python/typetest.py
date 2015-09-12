#!/usr/bin/env python
# encoding=utf8
# The python type test

import sys
import types
import inspect

for name in dir(types):
    value = getattr(types, name)
    if isinstance(value, type):
        print 'Type: types.%s:' % name, value

def method(): pass

class TestClass(object):
    """A test class
    """
    def __call__(self):
        """The callable method
        """

    def instanceMethod(self):
        """The instance method
        """
        pass

    @classmethod
    def classMethod(cls):
        """The class method
        """
        pass

    @staticmethod
    def staticMethod():
        """The staticmethod
        """

print 'Normal.Method:', type(method)
print 'Class.BeforeInstant.InstanceMethod', type(TestClass.instanceMethod), \
        'UnboundMethodType:%s' % isinstance(TestClass.instanceMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(TestClass.instanceMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(TestClass.instanceMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(TestClass.instanceMethod)
print 'Class.BeforeInstant.ClassMethod', type(TestClass.classMethod), \
        'UnboundMethodType:%s' % isinstance(TestClass.classMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(TestClass.classMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(TestClass.classMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(TestClass.classMethod)
print 'Class.BeforeInstant.StaticMethod', type(TestClass.staticMethod), \
        'UnboundMethodType:%s' % isinstance(TestClass.staticMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(TestClass.staticMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(TestClass.staticMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(TestClass.staticMethod)
testClass = TestClass()
print 'Class.AfterInstant.InstanceMethod', type(testClass.instanceMethod), \
        'UnboundMethodType:%s' % isinstance(testClass.instanceMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(testClass.instanceMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(testClass.instanceMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(testClass.instanceMethod)
print 'Class.AfterInstant.ClassMethod', type(testClass.classMethod), \
        'UnboundMethodType:%s' % isinstance(testClass.classMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(testClass.classMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(testClass.classMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(testClass.classMethod)
print 'Class.AfterInstant.StaticMethod', type(testClass.staticMethod), \
        'UnboundMethodType:%s' % isinstance(testClass.staticMethod, types.UnboundMethodType), \
        'MethodType:%s' % isinstance(testClass.staticMethod, types.MethodType), \
        'inspect.ismethod:%s' % inspect.ismethod(testClass.staticMethod), \
        'inspect.isfunction:%s' % inspect.isfunction(testClass.staticMethod)
print 'Class.Class', type(TestClass), 'ClassType:%s' % isinstance(TestClass, types.ClassType), 'InstanceType:%s' % isinstance(TestClass, types.InstanceType), 'inspect.isclass:%s' % inspect.isclass(TestClass)
print 'Class.Object', type(testClass),'ClassType:%s' % isinstance(testClass, types.ClassType), 'InstanceType:%s' % isinstance(testClass, types.InstanceType), 'inspect.isclass:%s' % inspect.isclass(testClass)

def amethod(a, b = None, *args, **kwargs):
    pass

print inspect.getargspec(amethod)

