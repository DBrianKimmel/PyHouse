"""
@name: PyHouse/src/Modules/utils/test/test_xml_tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 11, 2013
@summary: This module is for testing xml tools.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.utils import xml_tools
from test import xml_data
from Modules.Core.data_objects import PyHouseData, RoomData

XML1 = xml_data.XML_LONG

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text' >
    <BoolField>True</BoolField>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField>Test of text</TextField>
    <UUIDField>ec97a5c3-89c9-11e3-fedc-0123456789ab</UUIDField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text' />
</Test>
"""

class Test_02_PutGet(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML1)
        self.m_fields = ET.fromstring(XML)
        self.api = xml_tools.PutGetXML()

    def test_0201_get_bool_element(self):
        result = self.api.get_bool_from_xml(self.m_fields, 'BoolField')
        self.assertTrue(result)

    def test_0202_get_bool_attribute(self):
        result = self.api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def Xtest_0203_get_bool_compound(self):
        result = self.api.get_bool_from_xml(self.m_fields, 'Part_3/b3')
        self.assertTrue(result)

    def test_0211_get_int_element(self):
        result = self.api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 371)

    def test_0212_get_int_attribute(self):
        result = self.api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)

    def test_0221_get_text_element(self):
        result = self.api.get_text_from_xml(self.m_fields, 'TextField')
        self.assertEqual(result, 'Test of text')

    def test_0222_get_text_attribute(self):
        result = self.api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text')

    def test_0231_get_float_element(self):
        result = self.api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0232_get_float_attribute(self):
        result = self.api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0241_get_uuid_element(self):
        result = self.api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(result, 'ec97a5c3-89c9-11e3-fedc-0123456789ab')

    def Xtest_0242_get_uuid_attribute(self):
        result = self.api.get_uuid_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text')


class Test_03_CommonElement(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML1)
        print('Root', self.m_pyhouses_obj.XmlRoot)
        self.m_houses = self.m_pyhouses_obj.XmlRoot.find('Houses')
        print('Houses', self.m_houses)
        self.m_house = self.m_houses.find('House')
        self.m_rooms = self.m_house.find('Rooms')
        self.m_room = self.m_rooms.find('Room')
        self.api = xml_tools.ConfigTools()


    def test_0301_get_room(self):
        l_room = RoomData()
        self.api.xml_read_common_info(l_room, self.m_room)
        self.assertEqual(l_room.Name, 'Test Living Room')
        self.assertEqual(l_room.Key, 0)
        self.assertEqual(l_room.Active, True)

    def test_0302_put_room(self):
        l_room = RoomData()
        self.api.xml_read_common_info(l_room, self.m_room)
        l_element = self.api.xml_create_common_element('Room', l_room)
        self.assertTrue(self.m_room, l_element)

    def x(self):
        pass

# ## END DBK
