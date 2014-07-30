"""


"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import InsteonData
from Modules.families.Insteon import Device_Insteon
from Modules.Core import conversions
from Modules.lights import lighting_lights
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_ReadXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = Device_Insteon.API()
        self.m_controller_obj = InsteonData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.thermostat_sect.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_xml.thermostat.tag, 'Thermostat', 'XML - No Thermostat Entry')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Light section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light Entry')

    def test_0203_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj).read_one_light_xml(self.m_xml.light)
        l_insteon_obj = self.m_api.extract_device_xml(l_light, self.m_xml.light)
        PrettyPrintAny(l_insteon_obj, 'Insteon', 120)
        self.assertEqual(l_light.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        # self.assertEqual(l_light.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int('16.62.2D'), 'Bad Address')
        self.assertEqual(l_light.DevCat, conversions.dotted_hex2int('02.0A'), 'Bad DevCat')
        self.assertEqual(l_light.ProductKey, conversions.dotted_hex2int('30.1A.35'), 'Bad ProductKey')

# ## END
