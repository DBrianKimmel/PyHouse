"""
@name:      C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/Nodes/test/test_node_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Computer.Nodes import node_local
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = node_local.API()





class C01_Struct(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_Name(self):
        pass


class C02_Broker(SetupMixin, unittest.TestCase):
    """Test connection to a broker
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_Connect(self):
        pass

# ## END DBK
