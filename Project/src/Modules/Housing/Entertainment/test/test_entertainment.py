"""
@name:      PyHouse/src/Modules/Entertainment/test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 11 tests - DBK - 2018-08-17


<EntertainmentSection>
    <OnkyoSection Active="True">
        <Type>Component</Type>
        <Device Active="True" Key="0" Name="L/R Receiver TX-555">
            <UUID>Onkyo...-0000-0000-0000-0123456789ab</UUID>
            <Comment>Tx-555 Receiver</Comment>
            <IPv4>192.168.1.138</IPv4>
            <Port>60128</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>Receiver</Type>
        </Device>
        <Device Active="False" Key="1" Name="Receiver T2 = X-555">
            <UUID>Onkyo...-0000-0001-0001-0123456789ab</UUID>
            <Comment>Tx-555 Receiver_2</Comment>
            <IPv4>192.168.1.139</IPv4>
            <Port>60128</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>Receiver</Type>
        </Device>
    </OnkyoSection>
    <PanasonicSection Active="False">
    </PanasonicSection>
    <PandoraSection Active="True">
        <Type>Service</Type>
        <Device Active="True" Key="0" Name="On pi-06-ct ">
            <Comment>Living Room</Comment>
            <Host>192.168.9.16</Host>
            <Type>Service</Type>
            <ConnectionName>Pioneer</ConnectionName>
            <InputName>CD</InputName>
            <InputCode>01FN</InputCode>
            <Volume>47</Volume>
        </Device>
    </PandoraSection>
    <PioneerSection Active="True">
        <Device Active="True" Key="0" Name="L/R Receiver VSX-822-K">
            <UUID>Pioneer.-0000-0000-0000-0123456789ab</UUID>
            <Comment>VSX-822-K Receiver</Comment>
            <CommandSet>2015</CommandSet>
            <IPv4>192.168.9.121</IPv4>
            <Port>8102</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Status>On</Status>
            <Type>Receiver</Type>
            <Volume>75</Volume>
        </Device>
        <Device Active="True" Key="0" Name="Missing Device">
            <UUID>Pioneer.-0001-0000-0000-0123456789ab</UUID>
            <CommandSet>2015</CommandSet>
            <Comment>VSX-822-K Bogus</Comment>
            <IPv4>192.168.1.122</IPv4>
            <Port>8102</Port>
            <RoomName>Master Bedroom</RoomName>
            <RoomUUID>Room....-0001-0000-0000-0123456789ab</RoomUUID>
            <Type>Fake Receiver</Type>
        </Device>
    </PioneerSection>
    <SamsungSection Active="True">
        <Device Active="True" Key="0" Name="ct - L/R - TV 48abc1234">
            <UUID>Samsung.-0000-0000-0000-0123456789ab</UUID>
            <Comment>48in Smart-Tv  </Comment>
            <Installed>2016-07-29</Installed>
            <IPv4>192.168.9.118</IPv4>
            <Model>UN48J5201AFXZA</Model>
            <Port>55000</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>TV</Type>
        </Device>
    </SamsungSection>
</EntertainmentSection>

"""

__updated__ = '2018-10-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData
from Modules.Housing.Entertainment.onkyo.test.xml_onkyo import \
        TESTING_ONKYO_DEVICE_NAME_0
from Modules.Housing.test.xml_housing import \
        TESTING_HOUSE_DIVISION, \
        TESTING_HOUSE_NAME, \
        TESTING_HOUSE_ACTIVE, \
        TESTING_HOUSE_KEY, \
        TESTING_HOUSE_UUID
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION, \
        XML_ENTERTAINMENT, \
        L_ENTERTAINMENT_SECTION_START
from Modules.Housing.Entertainment.pandora.test.xml_pandora import \
        TESTING_PANDORA_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = entertainmentAPI(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_entertainment')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.entertainment_sect.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertEqual(self.m_xml.pandora_sect.tag, TESTING_PANDORA_SECTION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_ENTERTAINMENT
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:22], L_ENTERTAINMENT_SECTION_START)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_ENTERTAINMENT)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouseXML(self):
        """ Test to see if the house XML is built correctly
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml.XmlRoot, 'PyHouse'))
        pass

    def test_02_HouseDivXml(self):
        """ Test to see if the house XML is built correctly
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A3-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_03_EntertainmentXml(self):
        """ Test to see if the Entertainment XML is built properly
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A3-02-A - Entertainment'))
        # print(PrettyFormatAny.form(l_xml[1][0], 'A3-02-B - Entertainment'))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        self.assertGreater(len(l_xml), 2)


class C1_Load(SetupMixin, unittest.TestCase):
    """ This will test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')

    def test_01_Create(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-01-B - Entertainment'))

    def test_02_CrMod(self):
        """ Test that _create_module_refs is functional
        """
        for l_section in self.m_xml:
            # print(PrettyFormatAny.form(l_section, 'C1-02-A - Section'))
            l_plug = self.m_api._create_module_refs(l_section)
            # print(PrettyFormatAny.form(l_plug, 'C1-02-B - One Plugin'))
            self.m_pyhouse_obj.House.Entertainment.Plugins[l_plug.Name] = l_plug
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'C1-02-C - Plugins'))
        self.assertEqual(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Device[0].Name, TESTING_ONKYO_DEVICE_NAME_0)

    def test_03_XML(self):
        """ Test
        """
        self.m_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        l_ret = self.m_api.LoadXml(self.m_pyhouse_obj)
        l_entertain = self.m_pyhouse_obj.House.Entertainment
        print(PrettyFormatAny.form(l_entertain, 'C1-01-A - Entertainment'))
        print(PrettyFormatAny.form(l_entertain.Plugins, 'C1-01-B- Plugins'))
        print(PrettyFormatAny.form(l_entertain.Plugins['onkyo'], 'C1-01-C - Plugins["onkyo"]'))
        print(PrettyFormatAny.form(l_entertain.Plugins['panasonic'], 'C1-01-D - Plugins["panasonic"]'))
        print(PrettyFormatAny.form(l_entertain.Plugins['pandora'], 'C1-01-E - Plugins["pandora"]'))
        print(PrettyFormatAny.form(l_entertain.Plugins['pioneer'], 'C1-01-F - Plugins["pioneer"]'))
        print(PrettyFormatAny.form(l_entertain.Plugins['samsung'], 'C1-01-G - Plugins["samsung"]'))


class D1_Save(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_XML(self):
        """ Test
        """
        l_ret = entertainmentAPI(self.m_pyhouse_obj).LoadXml(self.m_pyhouse_obj)
        l_xml = ET.Element('HouseDivision')
        l_xml1 = entertainmentAPI(self.m_pyhouse_obj).SaveXml(l_xml)

        l_ent = self.m_pyhouse_obj.House.Entertainment
        print(PrettyFormatAny.form(l_ret, 'D1-01-A - Ret'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B1-01-B - HouseInformation()'))
        print(PrettyFormatAny.form(l_ent, 'B1-01-C - Entertainment'))
        print(PrettyFormatAny.form(l_ent.Plugins, 'B1-01-D- Plugins'))
        print(PrettyFormatAny.form(l_ent.Plugins['pandora'], 'B1-01-E - Plugins["pandora"]'))
        print(PrettyFormatAny.form(l_ent.Plugins['pioneer'], 'B1-01-F - Plugins["pioneer"]'))
        print(PrettyFormatAny.form(l_ent.Plugins['onkyo'], 'B1-01-G - Plugins["onkyo"]'))
        print(PrettyFormatAny.form(l_ent.Plugins['pandora'].API, 'B1-01-H - Plugins["pandora"].API'))

# ## END DBK
