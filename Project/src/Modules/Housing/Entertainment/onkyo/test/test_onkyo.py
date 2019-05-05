"""
@name:      PyHouse/src/Modules/Housing/Entertainment/test/test_onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

Run 'PyHouse/src/test/test_xml_data.py' if XML is corrupted.

Passed all 8 tests - DBK - 2018-11-03

"""
from Modules.Core.Utilities.xml_tools import XmlConfigTools

__updated__ = '2019-05-04'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.internet.protocol import ClientCreator

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData, EntertainmentPluginData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Housing.Entertainment.onkyo.onkyo import \
        SECTION, \
        OnkyoClient, \
        OnkyoFactory, MqttActions
from Modules.Housing.Entertainment.test.xml_entertainment import \
        TESTING_ENTERTAINMENT_SECTION
from Modules.Housing.Entertainment.onkyo.test.xml_onkyo import \
        TESTING_ONKYO_DEVICE_KEY_0, \
        TESTING_ONKYO_DEVICE_NAME_0, \
        TESTING_ONKYO_DEVICE_ACTIVE_0, \
        TESTING_ONKYO_SECTION, \
        TESTING_ONKYO_DEVICE_NAME_1, \
        TESTING_ONKYO_DEVICE_KEY_1, \
        TESTING_ONKYO_DEVICE_ACTIVE_1, \
        XML_ONKYO_SECTION
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

MSG_01 = """
{
    'Sender': 'pi-01-pp',
    'DateTime': '2019-05-03 23:27:13.713069',
    'Power': 'On',
    'Zone': '1'
}
"""


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
        l_onkyo_xml = self.m_xml.entertainment_sect.find(TESTING_ONKYO_SECTION)
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.entertainment_sect.tag, 'EntertainmentSection')
        self.assertEqual(l_onkyo_xml.tag, 'OnkyoSection')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_ONKYO_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[1:len(TESTING_ONKYO_SECTION) + 1], TESTING_ONKYO_SECTION)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_ONKYO_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_ONKYO_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
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
        print(PrettyFormatAny.form(l_ret, 'A2-01-B - XML'))
        self.assertEqual(l_ret.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_Onkyo(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.entertainment_sect.find('OnkyoSection')
        print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.tag, TESTING_ONKYO_SECTION)

    def test_03_Device0(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect.findall('Device')[0]
        print(PrettyFormatAny.form(l_xml, 'A2-03-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect.findall('Device')[1]
        print(PrettyFormatAny.form(l_xml, 'A2-04-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)


class B1_Data(SetupMixin, unittest.TestCase):
    """
    Test that the Onkyo XML is correct.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        self.m_xml_onkyo_sect = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')

    def test_00_setup(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-00-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B1-00-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'B1-00-C - Entertainment'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'B1-00-D - Plugins'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'], 'B1-00-E - Onkyo'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices, 'B1-00-F - Devices'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0], 'B1-00-G - Devices'))
        self.assertEqual(self.m_pyhouse_obj.House.Entertainment.PluginCount, 5)

    def test_01_Onkyo(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo']
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.DeviceCount, 2)
        self.assertEqual(l_obj.Name, 'onkyo')

    def test_02_Device0(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0]
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_0)

    def test_03_Device1(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[1]
        print(PrettyFormatAny.form(l_obj, 'B1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_1)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_1)


class B2_Message(SetupMixin, unittest.TestCase):
    """
    This section tests
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        # self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor

    def test_01_Zone(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_msg = MqttActions(self.m_pyhouse_obj)._get_zone(MSG_01)
        # print(PrettyFormatAny.form(l_msg, 'B2-01-A - Zone', 190))
        self.assertEqual(l_msg, 1)


class D1_Protocol(SetupMixin, unittest.TestCase):
    """
    This section tests
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor

    def tearDown(self):
        if self.m_client is not None:
            self.m_client.transport.looseConnection()
        return self.m_port.stopListening()
        pass

    def _test(self, p_operation, a, b, p_expected):
        self.proto.dataReceived('%s %d %d\r\n' % (p_operation, a, b))
        self.assertEqual(int(self.tr.value()), p_expected)

    def test_01_Factory(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_creator = ClientCreator(self.m_reactor, OnkyoClient)
        l_expected = None
        a = b = None

        def cb(p_client):
            self.m_client = p_client
            l_ret = getattr(self.m_client, p_operation)(a, b).addCallback(self.assertEqual, l_expected)
            return  l_ret

        return l_creator.connectTCP('127.0.0.1', self.m_port.getHost().port).addCallback(cb)

    def test_02_Protocol(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_creator = ClientCreator(self.m_reactor, OnkyoClient)
        l_expected = None
        a = b = None

        def cb(p_client):
            self.m_client = p_client
            l_ret = getattr(self.m_client, op)(a, b).addCallback(self.assertEqual, l_expected)
            return l_ret

        return l_creator.connectTCP('127.0.0.1', self.m_port.getHost().port).addCallback(cb)

    def test_03_Transport(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_creator = ClientCreator(self.m_reactor, OnkyoClient)
        l_expected = None
        a = b = None

        def cb(p_client):
            self.m_client = p_client
            return getattr(self.m_client, op)(a, b).addCallback(self.assertEqual, l_expected)

        return l_creator.connectTCP('127.0.0.1', self.m_port.getHost().port).addCallback(cb)

    def test_04_Connection(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_creator = ClientCreator(self.m_reactor, OnkyoClient)
        l_expected = None
        a = b = None

        def cb(p_client):
            self.m_client = p_client
            return getattr(self.m_client, op)(a, b).addCallback(self.assertEqual, l_expected)

        return l_creator.connectTCP('127.0.0.1', self.m_port.getHost().port).addCallback(cb)

# ## END DBK
