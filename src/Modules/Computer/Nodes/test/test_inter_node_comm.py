"""
@name:      PyHouse/src/Modules/Computer/Nodes/test/test-inter-node-comm.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 20, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.trial.runner import TestLoader
from twisted.internet.base import DelayedCall

# Import PyMh files and modules.
from Modules.Computer.Nodes import inter_node_comm
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        DelayedCall.debug = True



class C01_Start(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = inter_node_comm.API()

    def tearDown(self):
        pass


    def test_01_Setup(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        PrettyPrintAny(self.m_pyhouse_obj.Twisted, 'PyHouse.Twisted')

    def test_02_StartServer(self):
        l_defer = self.m_api._start_amp_server(self.m_pyhouse_obj)
        PrettyPrintAny(l_defer, 'Defer')
        return l_defer

    def test_04_StartModule(self):
        self.m_api.Start(self.m_pyhouse_obj)



class C02_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = inter_node_comm.InterNodeProtocol(self.m_pyhouse_obj)

    def test_01_Response(self):
        Name = 'Node Name 1'
        Active = True
        AddressV4 = '192.168.1.2'
        AddressV6 = '1234:5678:'
        NodeRole = 123
        UUID = '1-2-3-4 '
        l_node = self.m_api.create_node_from_response(Name, Active, AddressV4, AddressV6, NodeRole, UUID)
        PrettyPrintAny(l_node, 'Node')


def TestSuite():
    suite = TestLoader().loadTestsFromTestCase(C01_Start)
    return suite

# ## END DBK
