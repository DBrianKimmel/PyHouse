"""
@name: PyHouse/src/Modules/Families/test/test_family_utils.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 15, 2014
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Families import family
from Modules.Families.family_utils import FamUtil
from Modules.Families.Insteon import Insteon_xml, Insteon_device
from Modules.Lighting import lighting_core
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device_obj = LightData()



class C01_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))


    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'OBJs', 115)
        PrettyPrintAny(self.m_xml, 'XML')
        PrettyPrintAny(self.m_device_obj, 'Device')



class C02_Utils(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_device_obj.ControllerFamily = 'Insteon'

    def test_01_GetFamily(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_family = FamUtil.get_family(self.m_device_obj)
        print('Testing - Family: "{}"'.format(l_family))
        self.assertEqual(l_family, 'Insteon')

    def test_02_GetApi(self):
        l_api = FamUtil.get_family_api(self.m_pyhouse_obj, self.m_device_obj)
        PrettyPrintAny(l_api, 'API')
        self.assertIsInstance(l_api, Insteon_device.API)



class C03_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_device_obj.ControllerFamily = 'Insteon'
        self.m_api = FamUtil.get_family_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Components(self):
        PrettyPrintAny(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.House)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs.FamilyData['Insteon'])
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs.FamilyData['Insteon'].FamilyModuleAPI)

    def test_02_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = lighting_core.ReadWriteConfigXml().read_base_lighting_xml(l_device, l_xml)
        PrettyPrintAny(l_light, 'Light 1')
        FamUtil().read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        PrettyPrintAny(l_light, 'Light 2')
        self.assertEqual(l_light.Name, 'outside_front')
        self.assertEqual(l_light.ControllerFamily, 'Insteon')
        self.assertEqual(l_light.InsteonAddress, 1466925)

class C04_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_device_obj.ControllerFamily = 'Insteon'
        self.m_api = FamUtil.get_family_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_02_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_in_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = lighting_core.ReadWriteConfigXml().read_base_lighting_xml(l_device, l_in_xml)
        FamUtil().read_family_data(self.m_pyhouse_obj, l_light, l_in_xml)
        PrettyPrintAny(l_light, 'Light 1')

        l_out_xml = lighting_core.ReadWriteConfigXml().write_base_lighting_xml(l_light)
        PrettyPrintAny(l_out_xml, 'xml 1')
        FamUtil().write_family_data(self.m_pyhouse_obj, l_out_xml, l_light)
        PrettyPrintAny(l_out_xml, 'xml 2')

        self.assertEqual(l_light.Name, 'outside_front')
        self.assertEqual(l_light.ControllerFamily, 'Insteon')
        self.assertEqual(l_light.InsteonAddress, 1466925)

# ## END DBK
