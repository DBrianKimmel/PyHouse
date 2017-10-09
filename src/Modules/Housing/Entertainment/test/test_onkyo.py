"""
@name:      PyHouse/src/Modules/Housing/Entertainment/test/test_onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Run 'PyHouse/src/test/test_xml_data.py' if XML is corrupted.

Passed all 13 tests - DBK - 2017-06-25

"""

__updated__ = '2017-06-25'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Housing.Entertainment.onkyo import XML as onkyoXML
from Modules.Core.Utilities import convert
from Modules.Core.data_objects import EntertainmentData
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ONKYO_DEVICE_UUID_0, \
        TESTING_ONKYO_DEVICE_KEY_0, \
        TESTING_ONKYO_DEVICE_NAME_0, \
        TESTING_ONKYO_DEVICE_ACTIVE_0, \
        TESTING_ONKYO_DEVICE_IPV4_0, \
        TESTING_ONKYO_DEVICE_PORT_0, \
        TESTING_ONKYO_DEVICE_COMMENT_0, \
        TESTING_ONKYO_DEVICE_TYPE_0, \
        TESTING_ENTERTAINMENT_SECTION, \
        TESTING_ONKYO_SECTION, \
        TESTING_ONKYO_DEVICE_NAME_1, \
        TESTING_ONKYO_DEVICE_KEY_1, \
        TESTING_ONKYO_DEVICE_ACTIVE_1
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_onkyo')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_onkyo_xml = self.m_xml.entertainment_sect.find('OnkyoSection')
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(l_onkyo_xml.tag, 'OnkyoSection')


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by Onkyo.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Entertainment(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.house_div
        l_ret = l_xml.find('EntertainmentSection')
        # print(PrettyFormatAny.form(l_ret, 'A2-01-B - XML'))
        self.assertEqual(l_ret.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_Onkyo(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.entertainment_sect.find('OnkyoSection')
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.tag, TESTING_ONKYO_SECTION)

    def test_03_Device0(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'A2-03-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml_onkyo = self.m_xml.entertainment_sect.find('OnkyoSection').find('Device')

    def test_01_base(self):
        l_xml = self.m_xml.entertainment_sect.find('OnkyoSection').find('Device')
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - XML Base Onkyo device.'))
        l_obj = onkyoXML._read_device(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-B - Base Onkyo device.'))
        self.assertEqual(str(l_obj.Name), TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_ONKYO_DEVICE_UUID_0)
        self.assertEqual(str(l_obj.Comment), TESTING_ONKYO_DEVICE_COMMENT_0)
        self.assertEqual(convert.long_to_str(l_obj.IPv4), TESTING_ONKYO_DEVICE_IPV4_0)
        self.assertEqual(str(l_obj.Port), TESTING_ONKYO_DEVICE_PORT_0)
        self.assertEqual(str(l_obj.Type), TESTING_ONKYO_DEVICE_TYPE_0)

    def test_02_One(self):
        l_xml = self.m_xml.entertainment_sect.find('OnkyoSection').find('Device')
        l_obj = onkyoXML._read_one(l_xml)
        # print(PrettyFormatAny.form(l_obj, 'C1-02-A - One Onkyo device.'))
        self.assertEqual(str(l_obj.Name), TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.UUID), TESTING_ONKYO_DEVICE_UUID_0)

    def test_03_All(self):
        l_obj = onkyoXML.read_all(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-A - All Onkyo devices.'))
        self.assertEqual(str(l_obj[0].Name), TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj[1].Name), TESTING_ONKYO_DEVICE_NAME_1)


class D1_Write(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_onkyo = onkyoXML.read_all(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Onkyo = self.m_onkyo

    def test_01_Base(self):
        """Test the write for proper XML elements
        """
        l_xml = onkyoXML._write_device(self.m_onkyo[0])
        print(PrettyFormatAny.form(l_xml, 'D1-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ONKYO_DEVICE_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ONKYO_DEVICE_COMMENT_0)
        self.assertEqual(l_xml.find('IPv4').text, TESTING_ONKYO_DEVICE_IPV4_0)
        self.assertEqual(l_xml.find('Port').text, TESTING_ONKYO_DEVICE_PORT_0)
        self.assertEqual(l_xml.find('Type').text, TESTING_ONKYO_DEVICE_TYPE_0)

    def test_02_One(self):
        """Test the write for proper XML elements
        """
        l_xml = onkyoXML._write_one(self.m_pyhouse_obj, self.m_onkyo[0])
        print(PrettyFormatAny.form(l_xml, 'D1-02-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)

    def test_03_All(self):
        """Test the write for proper XML elements
        """
        l_xml = onkyoXML.write_all(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'D1-03-A - XML'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml[0].attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml[0].attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml[1].attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml[1].attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)


class E1_Start(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_onkyo = onkyoXML.read_all(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Entertainment.Onkyo = self.m_onkyo

    def test_01_Base(self):
        """Test the write for proper XML elements
        """
        l_xml = onkyoXML._write_device(self.m_onkyo[0])

# ## END DBK
