"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 11, 2013
@summary:   This module is for testing XML tools.

Passed all 59 tests - DBK 2017-03-27
"""

__updated__ = '2017-03-27'

# Import system type stuff
# import copy
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files and modules.
from test.xml_data import \
    XML_LONG, \
    XML_EMPTY
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import CoreLightingData, LocationData
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_UUID_0, \
    TESTING_LIGHT_ACTIVE_0
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_0, \
    TESTING_CONTROLLER_KEY_0, \
    TESTING_CONTROLLER_ACTIVE_0
from Modules.Core.Utilities.xml_tools import XML, PutGetXML, XmlConfigTools, stuff_new_attrs
from Modules.Core.Utilities import convert
from Modules.Core.Utilities.test.xml_xml_tools import \
    TESTING_XML_BOOL_0, \
    XML_TEST, \
    TESTING_XML_INT_0, \
    TESTING_XML_IPV4_0, \
    TESTING_XML_IPV6_0, \
    TESTING_XML_TEXT_0, \
    TESTING_XML_TEXT_1, \
    TESTING_XML_FLOAT_0, \
    TESTING_XML_ROOM_X_0, \
    TESTING_XML_ROOM_Y_0, \
    TESTING_XML_ROOM_Z_0, \
    TESTING_XML_BOOL_1, \
    TESTING_XML_BOOL_2, \
    TESTING_XML_UUID_0, \
    TESTING_XML_YEAR_0, \
    TESTING_XML_MONTH_0, \
    TESTING_XML_DAY_0, \
    TESTING_XML_HOUR_0, \
    TESTING_XML_MINUTE_0, \
    TESTING_XML_SECOND_0, \
    TESTING_XML_TEXT_A0, \
    TESTING_XML_BOOL_A0, \
    TESTING_XML_FLOAT_A0, \
    TESTING_XML_INT_A0, \
    TESTING_XML_DATE_TIME_0, \
    TESTING_XML_ROOM_X_1, \
    TESTING_XML_ROOM_Y_1, \
    TESTING_XML_ROOM_Z_1, \
    TESTING_XML_ROOM_COORDS_1
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = PutGetXML


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_xml_tools')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This tests the setup to see if everything is there.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Setup(self):
        l_xml = self.m_fields
        # print(PrettyFormatAny.form(l_xml, 'Fields A1-1'))
        self.assertEqual(l_xml.find('Int0').text, TESTING_XML_INT_0)
        self.assertEqual(l_xml.find('IpV40').text, TESTING_XML_IPV4_0)


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This texts the XML to see if it is proper.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Setup(self):
        l_xml = self.m_fields
        # print(PrettyFormatAny.form(l_xml, 'Fields A2-1'))
        self.assertEqual(l_xml.find('Int0').text, TESTING_XML_INT_0)
        self.assertEqual(l_xml.find('IpV40').text, TESTING_XML_IPV4_0)


class B1_Element(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_Text(self):
        l_elem = XML.get_element_field(self.m_fields, 'Text0')
        self.assertEqual(l_elem, TESTING_XML_TEXT_0)

    def test_2_Bool(self):
        l_elem = XML.get_element_field(self.m_fields, 'Bool0')
        self.assertEqual(l_elem, TESTING_XML_BOOL_0)

    def test_3_Int(self):
        l_elem = XML.get_element_field(self.m_fields, 'Int0')
        self.assertEqual(l_elem, TESTING_XML_INT_0)

    def test_4_Float(self):
        l_elem = XML.get_element_field(self.m_fields, 'Float0')
        self.assertEqual(l_elem, TESTING_XML_FLOAT_0)


class B2_Attribute(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetAttribute(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'BoolA0')
        self.assertEqual(l_attr, TESTING_XML_BOOL_A0)

    def test_02_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'FloatA0')
        self.assertEqual(l_attr, TESTING_XML_FLOAT_A0)

    def test_03_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'IntA0')
        self.assertEqual(l_attr, TESTING_XML_INT_A0)

    def test_04_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'TextA0')
        self.assertEqual(l_attr, TESTING_XML_TEXT_A0)

    def test_05_GetAttribute_Missing(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'MissingAttribute')
        self.assertEqual(l_attr, None)


class B3_AnyField(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetAnyField_Element(self):
        l_field = XML.get_any_field(self.m_fields, 'Text1')
        self.assertEqual(l_field, TESTING_XML_TEXT_1)

    def test_02_GetAnyField_Attribute(self):
        l_field = XML.get_any_field(self.m_fields, 'TextA0')
        self.assertEqual(l_field, TESTING_XML_TEXT_A0)

    def test_03_GetAnyField_Missing(self):
        l_field = XML.get_any_field(self.m_fields, 'NoSuchField')
        self.assertEqual(l_field, None)


class C1_Boolean(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods for bools.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Element(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool0')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_02_Element(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool1')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_1)

    def test_03_Attribute(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolA1')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_04_Path(self):
        """This should find a path name field
        """
        l_result = (self.m_api.get_bool_from_xml(self.m_fields, './SubTest/BoolA1') == True)
        # print(PrettyFormatAny.form(l_result, 'Fields C1-3'))
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_05_GetFalse(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool2')
        self.assertNotEqual(str(l_result), TESTING_XML_BOOL_2)

    def test_06_FalseDirect(self):
        result = PutGetXML.get_bool_from_xml(self.m_fields, 'Bool2')
        self.assertFalse(result)

    def test_07_GetInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_08_GetMissing(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(l_result)

    def test_09_PutElement(self):
        """ Create this:
        <TestBoolElement_1>
            <Active>True</Active>
        </TestBoolElement_1>
        """
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', True)
        # print(PrettyFormatAny.form(l_element, 'element'))
        self.assertEqual(l_element.find("Active").text, 'True')

    def test_10_PutElement(self):
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', False)
        # print(PrettyFormatAny.form(l_element, 'element'))
        self.assertEqual(l_element.find("Active").text, 'False')

    def test_11_PutAttribute(self):
        """ Create this:
        <TestBoolAttribute_2 Active="True"/>
        """
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', True)
        # print(PrettyFormatAny.form(l_element, 'element'))
        self.assertEqual(l_element.attrib['Active'], 'True')

    def test_12_PutAttribute(self):
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', False)
        self.assertEqual(l_element.attrib['Active'], 'False')


class C2_Integer(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_GetIntElement(self):
        l_result = self.m_api.get_int_from_xml(self.m_fields, 'Int0')
        self.assertEqual(l_result, int(TESTING_XML_INT_0))

    def test_2_GetIntAttribute(self):
        l_result = self.m_api.get_int_from_xml(self.m_fields, 'IntA0')
        # print(PrettyFormatAny.form(l_result, 'Fields C2-2-A Attr'))
        self.assertEqual(l_result, int(TESTING_XML_INT_A0))

    def test_3_PutIntElement(self):
        l_element = ET.Element('TestIntElement_1')
        self.m_api.put_int_element(l_element, 'IntNumber', -57)
        # print(PrettyFormatAny.form(l_element, 'Fields C2-3'))
        self.assertEqual(int(l_element.find('IntNumber').text), -57)

    def test_4_PutIntAttribute(self):
        l_element = ET.Element('TestIntAttribute_2')
        self.m_api.put_int_attribute(l_element, 'IntNumber', 853)
        self.assertEqual(int(l_element.attrib['IntNumber']), 853)


class C3_Text(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetTextElement(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'Text0')
        self.assertEqual(l_text, TESTING_XML_TEXT_0)

    def test_02_GetTextElement(self):
        """
        we seem to not work if the field is the xml passed in.
        """
        l_text = self.m_api.get_text_from_xml(self.m_fields.find('Text0'), 'Text0')
        self.assertEqual(l_text, TESTING_XML_TEXT_0)

    def test_03_GetTextAttribute(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'TextA0')
        self.assertEqual(l_text, TESTING_XML_TEXT_A0)

    def test_04_GetTextInvalid(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField', '0223 No such field')
        self.assertEqual(l_text, '0223 No such field')

    def test_05_GetTextInvalid_NoDefault(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_text, '')

    def test_06_PutTextElement(self):
        l_element = ET.Element('TestTextElement_1')
        self.m_api.put_int_element(l_element, 'Comment', 'Arbitrary Comment')
        self.assertEqual(l_element.find('Comment').text, 'Arbitrary Comment')

    def test_07_PutTextAttribute(self):
        l_element = ET.Element('TestTextAttribute_2')
        self.m_api.put_text_attribute(l_element, 'Name', 'Any old Name')
        self.assertEqual(l_element.attrib['Name'], 'Any old Name')


class C4_Float(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetFloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'Float0')
        self.assertAlmostEqual(result, float(TESTING_XML_FLOAT_0), places=5)

    def test_02_GetFloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatA0')
        self.assertAlmostEqual(result, float(TESTING_XML_FLOAT_A0), places=5, msg='get_float_from_xml failed')


class D1_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetUuidElement(self):
        """UUID elements must be returned intact
        """
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'UUID0')
        self.assertEqual(l_uuid, TESTING_XML_UUID_0)


class D2_IP(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_IPv4(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV40')
        # print(PrettyFormatAny.form(l_ip, 'DateTime D2-01-A'))
        self.assertEqual(l_ip, convert.str_to_long(TESTING_XML_IPV4_0))

    def test_02_IPv6(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV60')
        self.assertEqual(l_ip, convert.str_to_long(TESTING_XML_IPV6_0))

    def test_03_IPv4(self):
        l_element = ET.Element('TestIPv4')
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV40')
        self.m_api.put_ip_element(l_element, 'IPv4', l_ip)
        # print(PrettyFormatAny.form(l_element, 'D2-03-A'))
        self.assertEqual(l_element.find('IPv4').text, TESTING_XML_IPV4_0)

    def test_04_IPv6(self):
        l_element = ET.Element('TestIPv6')
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV60')
        self.m_api.put_ip_element(l_element, 'IPv6', l_ip)
        # print(PrettyFormatAny.form(l_element, 'D2-04-A'))
        self.assertEqual(l_element.find('IPv6').text, TESTING_XML_IPV6_0)



class D3_DateTime(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_Read(self):
        l_answer = datetime.datetime(int(TESTING_XML_YEAR_0), int(TESTING_XML_MONTH_0), int(TESTING_XML_DAY_0),
                                     int(TESTING_XML_HOUR_0), int(TESTING_XML_MINUTE_0), int(TESTING_XML_SECOND_0))
        # print(PrettyFormatAny.form(l_answer, 'DateTime D3-1 A'))
        l_date = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime0')
        self.assertEqual(l_date, l_answer)

    def test_2_Write(self):
        l_date = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime0')
        l_element = ET.Element('TestDateTime')
        self.m_api.put_date_time_element(l_element, 'TestField', l_date)
        # print(PrettyFormatAny.form(l_element, 'DateTime D3-2 A'))
        self.assertEqual(l_element[0].text, TESTING_XML_DATE_TIME_0)


class D4_Coords(SetupMixin, unittest.TestCase):
    """
    This series test reeading and writing of CoOrdinates.
    Since there are various input formats tested and the xml-tools output is always ideal,
    we need to use string literals to test for correctness.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)
        self.m_api = PutGetXML

    def test_01_Read(self):
        # print(PrettyFormatAny.form(self.m_fields, 'Coords D4-1 A'))
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords0')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-1 B'))
        self.assertEqual(l_coords.X_Easting, float(TESTING_XML_ROOM_X_0))
        self.assertEqual(l_coords.Y_Northing, float(TESTING_XML_ROOM_Y_0))
        self.assertEqual(l_coords.Z_Height, float(TESTING_XML_ROOM_Z_0))

    def test_02_Read(self):
        # print(PrettyFormatAny.form(self.m_fields, 'Coords D4-2 A'))
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords1')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-2 B'))
        self.assertEqual(l_coords.X_Easting, float(TESTING_XML_ROOM_X_1))
        self.assertEqual(l_coords.Y_Northing, float(TESTING_XML_ROOM_Y_1))
        self.assertEqual(l_coords.Z_Height, float(TESTING_XML_ROOM_Z_1))

    def test_03_Read(self):
        # print(PrettyFormatAny.form(self.m_fields, 'Coords D4-3 A'))
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords2')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-3 B'))
        self.assertEqual(l_coords.X_Easting, 23.7)
        self.assertEqual(l_coords.Y_Northing, 2.15)
        self.assertEqual(l_coords.Z_Height, 3.33)

    def test_04_Write(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords0')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-4 A'))
        l_element = ET.Element('TestCoords')
        self.m_api.put_coords_element(l_element, 'OutCoords', l_coords)
        # print(PrettyFormatAny.form(l_element, 'Coords D4-4 B'))
        self.assertEqual(l_element[0].text, '[3.4,5.6,1.2]')

    def test_05_Write(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords1')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-5 A'))
        l_element = ET.Element('TestCoords')
        self.m_api.put_coords_element(l_element, 'OutCoords', l_coords)
        # print(PrettyFormatAny.form(l_element, 'Coords D4-5 B'))
        self.assertEqual(l_element[0].text, TESTING_XML_ROOM_COORDS_1)

    def test_06_Write(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords2')
        # print(PrettyFormatAny.form(l_coords, 'Coords D4-6 A'))
        l_element = ET.Element('TestCoords')
        self.m_api.put_coords_element(l_element, 'OutCoords', l_coords)
        # print(PrettyFormatAny.form(l_element, 'Coords D4-6 B'))
        self.assertEqual(l_element[0].text, '[23.7,2.15,3.33]')


class E1_Read(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = XmlConfigTools()

    def test_01_BaseUUIDObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_UUID_object_xml(l_base_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_base_obj, 'E1-01-A - Base Obj'))
        self.assertEqual(l_base_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(str(l_base_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_base_obj.UUID, TESTING_LIGHT_UUID_0)

    def test_02_readBaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_UUID_object_xml(l_base_obj, self.m_xml.controller)
        self.assertEqual(str(l_base_obj.Name), TESTING_CONTROLLER_NAME_0)
        self.assertEqual(str(l_base_obj.Key), TESTING_CONTROLLER_KEY_0)
        self.assertEqual(str(l_base_obj.Active), TESTING_CONTROLLER_ACTIVE_0)


class E2_ReadEmpty(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))
        self.m_api = XmlConfigTools()

    def test_01_BaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_base_obj, 'E2-01-A Base))
        self.assertEqual(l_base_obj.Name, '')
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(l_base_obj.Active, False)


class E3_Write(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseObject(self):
        """Write Base Object XML w/UUID
        """
        l_base_obj = CoreLightingData()
        XmlConfigTools.read_base_UUID_object_xml(l_base_obj, self.m_xml.light)
        l_base_obj.Key = 43
        l_uuid = '12345678-fedc-1111-ffff-aaBBccDDeeFF'
        l_base_obj.UUID = l_uuid
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Light', l_base_obj)
        # print(PrettyFormatAny.form(l_xml, 'E3-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], '43')
        self.assertEqual(l_xml.find('UUID').text, l_uuid)

    def test_02_BaseObject(self):
        """Write Base Object XML w/ NO UUID
        """
        l_base_obj = CoreLightingData()
        XmlConfigTools.read_base_UUID_object_xml(l_base_obj, self.m_xml.light)
        l_base_obj.Key = 44
        l_xml = XmlConfigTools.write_base_object_xml('Light', l_base_obj)
        # print(PrettyFormatAny.form(l_xml, 'E3-02-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], '44')


class Z1_NoClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_StuffAttrs(self):
        l_objA = CoreLightingData()
        l_objA.Name = 'Test 1A'
        # print(PrettyFormatAny.form(l_objA, 'Obj A'))
        l_objB = LocationData()
        l_objB.Street = 'Some road'
        # print(PrettyFormatAny.form(l_objB, 'Obj B', 120))
        #
        stuff_new_attrs(l_objA, l_objB)
        # print(PrettyFormatAny.form(l_objA, 'Result B stuffed into A', 120))
        self.assertEqual(l_objA.Street, 'Some road')

# ## END DBK
