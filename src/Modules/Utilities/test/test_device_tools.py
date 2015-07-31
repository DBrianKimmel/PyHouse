"""
@name:      PyHouse/src/Modules/Utilities/test/test_device_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 26, 2015
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
from xml.etree import ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData, ButtonData, ControllerData
from Modules.Core.test.xml_device import TESTING_DEVICE_COMMENT, TESTING_DEVICE_FAMILY, \
            TESTING_DEVICE_ROOM_NAME, TESTING_DEVICE_ROOM_X
from Modules.Utilities.device_tools import XML
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = XML
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerData()
        self.m_light_obj = LightData()


class A1_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Find(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        pass

    def test_02_Find(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml, 'XML', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses section')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controller section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection', 'XML - No Buttons section')
        self.assertEqual(self.m_xml.button.tag, 'Button', 'XML - No Button')

    def test_03_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml.light, 'Light XML')
        pass


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the device info
        """
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.light)
        # PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'Insteon Light')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))

    def test_02_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.controller)
        # PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'Insteon Serial Controller', 'Bad Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, True, 'Bad Active')
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_03_ReadBaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.button)
        # PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'Insteon Button')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)



class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.light)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # PrettyPrintAny(l_xml, 'Lighting Core')
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_02_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.controller)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # PrettyPrintAny(l_xml, 'Lighting Core')
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Serial Controller')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_03_BaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.button)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # PrettyPrintAny(l_xml, 'Lighting Core')
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Button')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')



class C2_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML before anything has been defined.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        # PrettyPrintAny(self.m_xml, 'XML', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')



class C3_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_02_ReadBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_base_device_object_xml(self.m_xml.light)
        # PrettyPrintAny(l_base, 'ReadBaseLighting', 120)
        self.assertEqual(l_base.Name, 'Missing Name')
        self.assertEqual(l_base.Key, 0, 'Bad Key')
        self.assertEqual(l_base.Active, False, 'Bad Active')
        # self.assertEqual(l_base.Comment, 'None', 'Bad Comments')
        self.assertEqual(l_base.RoomCoords.X_Easting, 0.0)
        self.assertEqual(l_base.DeviceFamily, 'None')
        self.assertEqual(l_base.RoomName, 'None')



class C6_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_WriteBaseXml(self):
        """ Read in the xml file and fill in the lights
        """
        # l_xml = ET.Element('Lights')
        l_xml = self.m_api.write_base_device_object_xml('Light', self.m_light_obj)
        # PrettyPrintAny(l_xml, 'Lighting Core')

# ## END DBK
