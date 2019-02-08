"""
@name:      PyHouse/Project/src/Modules/Housing/Lighting/test/test_lighting_utility.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 20, 2019
@summary:   Test

"""

__updated__ = '2019-02-07'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Lighting.lighting_controllers import XML as controllerXML
from Modules.Housing.Lighting.lighting_lights import XML as lightXML
from Modules.Housing.Lighting.lighting_utility import Utility
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_0
from Modules.Housing.Lighting.test.xml_lights import \
    XML_LIGHT_SECTION, \
    TESTING_LIGHT_SECTION, TESTING_LIGHT_NAME_0, TESTING_LIGHT_UUID_0, TESTING_LIGHT_UUID_1, TESTING_LIGHT_NAME_1, TESTING_LIGHT_NAME_2, \
    TESTING_LIGHT_UUID_2
from Modules.Housing.Lighting.test.xml_lighting import \
    XML_LIGHTING
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting_utility')


class A1_Api(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_DoSchedule(self):
        pass

    def test_02_ChangeLight(self):
        pass


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_xml = XML_LIGHTING
        # print(l_xml)
        self.assertEqual(l_xml[:17], '<LightingSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_LIGHT_SECTION)
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A Parsed'))
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class B1_Lights_by_id(SetupMixin, unittest.TestCase):
    """ This section tests lookup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_lights = lightXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Name(self):
        """ Write out the XML file for the Base controller
        """
        l_obj = self.m_lights[0]
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Light'))
        l_ret = Utility()._test_object_by_id(l_obj, name=TESTING_LIGHT_NAME_0)
        # print(PrettyFormatAny.form(l_ret, 'B1-01-B - Light'))
        self.assertEqual(l_ret.UUID, TESTING_LIGHT_UUID_0)

    def test_02_UUID(self):
        """ Write out the XML file for the Base controller
        """
        l_obj = self.m_lights[1]
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - Light'))
        l_ret = Utility()._test_object_by_id(l_obj, UUID=TESTING_LIGHT_UUID_1)
        # print(PrettyFormatAny.form(l_ret, 'B1-02-B - Light'))
        self.assertEqual(l_ret.Name, TESTING_LIGHT_NAME_1)

    def test_03_Key(self):
        """ Write out the XML file for the Base controller
        """
        l_obj = self.m_lights[2]
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Light'))
        l_ret = Utility()._test_object_by_id(l_obj, key=2)
        # print(PrettyFormatAny.form(l_ret, 'B1-03-B - Light'))
        self.assertEqual(l_ret.Name, TESTING_LIGHT_NAME_2)

    def test_04_None(self):
        """ Write out the XML file for the Base controller
        """
        l_obj = self.m_lights[0]
        # print(PrettyFormatAny.form(l_obj, 'B1-04-A - Light'))
        l_ret = Utility()._test_object_by_id(l_obj, name=None)
        # print(PrettyFormatAny.form(l_ret, 'B1-04-B - Light'))
        self.assertIsNone(l_ret)


class B2_Object_by_id(SetupMixin, unittest.TestCase):
    """ This section tests lookup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_lights = lightXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Name(self):
        """ Write out the XML file for the Base controller
        """
        l_objs = self.m_lights
        # print(PrettyFormatAny.form(l_objs, 'B2-01-A - Lights'))
        l_ret = Utility()._get_object_by_id(l_objs, name=TESTING_LIGHT_NAME_0)
        # print(PrettyFormatAny.form(l_ret, 'B2-01-B - Light'))
        self.assertEqual(l_ret.UUID, TESTING_LIGHT_UUID_0)

    def test_02_UUID(self):
        """ Write out the XML file for the Base controller
        """
        l_objs = self.m_lights
        # print(PrettyFormatAny.form(l_objs, 'B2-02-A - Lights'))
        l_ret = Utility()._get_object_by_id(l_objs, UUID=TESTING_LIGHT_UUID_2)
        # print(PrettyFormatAny.form(l_ret, 'B2-02-B - Light'))
        self.assertEqual(l_ret.Name, TESTING_LIGHT_NAME_2)

    def test_03_None(self):
        """ Write out the XML file for the Base controller
        """
        l_objs = self.m_lights
        # print(PrettyFormatAny.form(l_objs, 'B2-01-A - Lights'))
        l_ret = Utility()._get_object_by_id(l_objs, key=17)
        # print(PrettyFormatAny.form(l_ret, 'B2-01-B - Light'))
        self.assertIsNone(l_ret)


class C1_ByFamuly(SetupMixin, unittest.TestCase):
    """ This section tests lookup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)

    def test_01_Name(self):
        """ Write out the XML file for the Base controller
        """
        l_objs = self.m_controllers
        print(PrettyFormatAny.form(l_objs, 'C1-01-A - Controllers'))
        l_ret = Utility().get_controller_objs_by_family(l_objs, 'Insteon')
        print(PrettyFormatAny.form(l_ret, 'C1-01-B - Controller'))
        # self.assertEqual(l_ret.Name, TESTING_CONTROLLER_NAME_0)

# ## END DBK
