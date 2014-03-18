'''
Created on Jul 12, 2013

@author: briank
'''

# from twisted.trial import unittest
from nevow import loaders, tags
from nevow.livetrial import testcase


# This is the hook for nit to catch on to your test.   nit will render OurFirstTest as a LiveFragment and bind it to an instance of Foo.Tests.OurFirstTest.
class OurFirstTest(testcase.TestCase):
    # jsClass = u'Foo.Tests.OurFirstTest'
    jsClass = u'PyHouse.Tests.OurFirstTest'
    docFactory = loaders.stan(tags.div(render = tags.directive('liveTest'))['OurFirstTest'])


# ## END DBK
