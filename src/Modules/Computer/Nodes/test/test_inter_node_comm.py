"""
@name: Modules/Computer/Nodes/test/test-inter-node-comm.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 20, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet import protocol
from twisted.internet import defer
from twisted.internet import error
from twisted.internet import reactor
from twisted.trial import unittest

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



class C01_Start(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = inter_node_comm.API()

    def tearDown(self):
        pass


    def test_01_Setup(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        PrettyPrintAny(self.m_pyhouse_obj.Twisted, 'PyHouse.Twisted')

    def test_02_CreateService(self):
        l_endpont = self.m_api._create_amp_service(self.m_pyhouse_obj)
        PrettyPrintAny(l_endpont, 'Endpoint', 240)

    def test_03_start_service(self):
        l_endpont = self.m_api._create_amp_service(self.m_pyhouse_obj)
        l_defer = self.m_api._start_amp_server(self.m_pyhouse_obj, l_endpont)
        PrettyPrintAny(l_defer, 'Defer')
        return l_defer

    def test_04_Start(self):
        self.m_api.Start(self.m_pyhouse_obj)


def TestSuite():
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(C01_Start)
    # print('\nSuite {}'.format(suite))
    return suite

# ## END DBK
