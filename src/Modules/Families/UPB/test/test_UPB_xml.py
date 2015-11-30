"""
@name:      PyHouse/src/Modules/Families/UPB/test/test_UPB_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:       Created on Aug 6, 2014
@Summary:

Passed all 2 tests - DBK - 2015-07-29

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from Modules.Families.UPB.UPB_xml import Xml as upbXML
from Modules.Families.UPB.test.xml_upb import TESTING_UPB_ADDRESS, TESTING_UPB_NETWORK, TESTING_UPB_PASSWORD
from Modules.Core.data_objects import ControllerData
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Read(self):
        l_list = list(self.m_xml.controller_sect.iterfind('Controller'))
        l_xml = l_list[1]
        l_dev = ControllerData()
        upbXML.ReadXml(l_dev, l_xml)
        self.assertEqual(l_dev.UPBAddress, int(TESTING_UPB_ADDRESS))
        self.assertEqual(l_dev.UPBNetworkID, int(TESTING_UPB_NETWORK))
        self.assertEqual(l_dev.UPBPassword, int(TESTING_UPB_PASSWORD))

    def test_02_Write(self):
        l_list = list(self.m_xml.controller_sect.iterfind('Controller'))
        l_xml = l_list[1]
        l_dev = ControllerData()
        upbXML.ReadXml(l_dev, l_xml)
        l_out = ET.Element('Testing')
        upbXML.WriteXml(l_out, l_dev)

# ## END DBK
