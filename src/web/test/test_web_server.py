'''
Created on Apr 8, 2013

@author: briank
'''

from twisted.trial import unittest
from twisted.test import proto_helpers

from src.web import web_server

class Test(unittest.TestCase):

    def setUp(self):
        self.web_server = web_server.API()
        factory = RemoteCalculationFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def tearDown(self):
        pass

    def test_start(self):
        self.web_server.Start()

    def test_root_page(self):
        pass

# ## END DBK
