"""
@name:      PyHouse/src/Modules/irrigation/_test/test_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2018 by briank
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

Passed all 6 tests - DBK - 2017-01-18

"""

__updated__ = '2018-02-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import TESTING_PYHOUSE, XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Irrigation.irrigation_data import IrrigationData
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION
from Modules.Housing.Irrigation.test.xml_irrigation import \
    XML_IRRIGATION, \
    TESTING_IRRIGATION_SECTION, \
    TESTING_IRRIGATION_SYSTEM, \
    TESTING_IRRIGATION_ZONE


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_irrigation_obj = IrrigationData()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_irrigation')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.irrigation_sect.tag, TESTING_IRRIGATION_SECTION)
        self.assertEqual(self.m_xml.irrigation_system.tag, TESTING_IRRIGATION_SYSTEM)
        self.assertEqual(self.m_xml.irrigation_zone.tag, TESTING_IRRIGATION_ZONE)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_xml = XML_IRRIGATION
        # print(l_xml)
        self.assertEqual(l_xml[:19], '<IrrigationSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_IRRIGATION)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_IRRIGATION_SECTION)


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass

# ## END DBK
