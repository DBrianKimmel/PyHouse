"""
@name: PyHouse/src/Modules/lights/test/test_lighting.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 9, 2013
@license: MIT License
@summary: Handle the home lighting system automation.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseObjs, BaseLightingData
from Modules.lights import lighting
from src.test import xml_data
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_api = lighting.API()

        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseObjs = HouseObjs()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml

        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')

        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')  # First one
        # print('SetupMixin setUp ran')


class Test_02_ReadXMLLong(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.HouseObjs.Lights, {}, 'No Lights{}')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_lights_xml.tag, 'Lights', 'XML - No Lights section')

    def test_0211_read_lighting(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)

    def test_0212_write_lighting(self):
        pass


# class Test_03_ReadXMLEmpty(SetupMixin, unittest.TestCase):
#    """ This section tests the reading and writing of XML used by node_local.
#    """

    # def XsetUp(self):
    #    self.m_root_xml = ET.fromstring(xml_data.XML_EMPTY)
    #    SetupMixin.setUp(self)

    # def Xtest_0301_read_lighting(self):
    #    pass

    # def Xtest_0302_write_lighting(self):
    #    pass

# ## END DBK
