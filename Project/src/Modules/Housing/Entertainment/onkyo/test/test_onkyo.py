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

__updated__ = '2019-06-07'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
# from twisted.test import proto_helpers
from twisted.internet.protocol import ClientCreator

# Import PyMh files
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.onkyo.onkyo import \
        SECTION, \
        OnkyoClient, \
        MqttActions, \
        OnkyoQueueData, \
        API as onkyoAPI, \
        OnkyoDeviceInformation
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
        XML_ONKYO_SECTION, TESTING_ONKYO_DEVICE_MODEL_0
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
        l_xml = self.m_xml.onkyo_sect.findall('Device')[0]
        # print(PrettyFormatAny.form(l_xml, 'A2-03-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_0)

    def test_04_Device1(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.onkyo_sect.findall('Device')[1]
        # print(PrettyFormatAny.form(l_xml, 'A2-04-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ONKYO_DEVICE_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ONKYO_DEVICE_ACTIVE_1)


class A4_YAML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by Onkyo.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)

    def test_01_Read(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_device = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        # print('A4-01-A - Device\n{}'.format(PrettyFormatAny.form(l_device, 'Device')))
        l_yaml = onkyoAPI(self.m_pyhouse_obj)._read_yaml(l_device)
        # print('A4-01-A - Yaml\n{}'.format(PrettyFormatAny.form(l_yaml, 'Yaml')))
        self.assertEqual(l_yaml['UnitType'], 1)


class B1_Data(SetupMixin, unittest.TestCase):
    """
    Test that the Onkyo XML is correct.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
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
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.DeviceCount, 2)
        self.assertEqual(l_obj.Name, 'onkyo')

    def test_02_Device0(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0]
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_0)
        self.assertEqual(l_obj.Model, TESTING_ONKYO_DEVICE_MODEL_0)

    def test_03_Device1(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[1]
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_1)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_1)


class B2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests that the XML will work for the rest of the tests
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)

    def test_01_Device0(self):
        """ Be sure that
        """
        l_onk = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # print(PrettyFormatAny.form(l_onk, 'B2-01-A - Onkyo', 190))
        l_dev = l_onk.Devices[0]
        # print(PrettyFormatAny.form(l_dev, 'B2-01-B - Zone', 190))
        self.assertEqual(l_dev.Model, TESTING_ONKYO_DEVICE_MODEL_0)


class B3_Yaml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading of the YAML file for each of the Onkyo devices.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        l_device = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        self.m_yaml = onkyoAPI(self.m_pyhouse_obj)._read_yaml(l_device)

    def test_00_Yaml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml, 'B3-01-A - Yaml', 190))
        self.assertGreater(len(self.m_yaml), 4)

    def test_01_Unit(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print('B3-01-A - Unit type: {}'.format(self.m_yaml['UnitType']))
        self.assertEqual(self.m_yaml['UnitType'], 1)

    def test_02_Cmds(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['ControlCommands'], 'B3-02-A - Yaml', 190))
        self.assertEqual(self.m_yaml['ControlCommands']['Power'][0], 'PWR')
        self.assertEqual(self.m_yaml['ControlCommands']['Power'][1], 'PWZ')
        self.assertEqual(self.m_yaml['ControlCommands']['Volume'][0], 'MVL')
        self.assertEqual(self.m_yaml['ControlCommands']['Volume'][1], 'ZVL')
        self.assertEqual(self.m_yaml['ControlCommands']['Mute'][0], 'AMT')
        self.assertEqual(self.m_yaml['ControlCommands']['Mute'][1], 'ZMT')
        self.assertEqual(self.m_yaml['ControlCommands']['InputSelect'][0], 'SLI')
        self.assertEqual(self.m_yaml['ControlCommands']['InputSelect'][1], 'SLZ')

    def test_03_Args(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['Arguments'], 'B3-03-A - Yaml', 190))
        # print(PrettyFormatAny.form(self.m_yaml['Arguments']['Power'], 'B3-03-B - Yaml', 190))
        self.assertEqual(self.m_yaml['Arguments']['Power']['Off'], '00')
        self.assertEqual(self.m_yaml['Arguments']['Power']['On'], '01')
        self.assertEqual(self.m_yaml['Arguments']['Power']['?'], 'QSTN')

    def test_04_Input(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_yaml['InputSelect'], 'B3-04-A - Yaml', 190))
        self.assertEqual(self.m_yaml['InputSelect']['Cbl/Sat'], '01')
        self.assertEqual(self.m_yaml['InputSelect']['Game'], '02')
        self.assertEqual(self.m_yaml['InputSelect']['Aux'], '03')


class C3_Command(SetupMixin, unittest.TestCase):
    """
    This section tests building commands to the onkyo device
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        l_device = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        l_yaml = onkyoAPI(self.m_pyhouse_obj)._read_yaml(l_device)
        l_device._Yaml = l_yaml

    def test_01_Zone1(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_device_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        # print(PrettyFormatAny.form(l_device_obj, 'C3-01-A - Device', 190))
        l_queue = OnkyoQueueData()
        l_queue.Zone = 0
        l_queue.Command = 'Power'
        l_queue.Args = 'On'
        # print(PrettyFormatAny.form(l_queue, 'C3-01-B - Queue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(l_queue, l_device_obj)
        # print(PrettyFormatAny.form(l_msg, 'C3-01-C - Zone', 190))
        self.assertEqual(l_msg, b'!1PWR01')

    def test_02_Zone2(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_device_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        # print(PrettyFormatAny.form(l_device_obj, 'C3-02-A - Device', 190))
        l_queue = OnkyoQueueData()
        l_queue.Zone = 1
        l_queue.Command = 'Power'
        l_queue.Args = 'Off'
        # print(PrettyFormatAny.form(l_queue, 'C3-02-B - Queue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(l_queue, l_device_obj)
        # print(PrettyFormatAny.form(l_msg, 'C3-02-C - Zone', 190))
        self.assertEqual(l_msg, b'!1PWZ00')

    def test_03_VolZ1(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_device_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        # print(PrettyFormatAny.form(l_device_obj, 'C3-03-A - Device', 190))
        l_queue = OnkyoQueueData()
        l_queue.Zone = 0
        l_queue.Command = 'Volume'
        l_queue.Args = 2
        # print(PrettyFormatAny.form(l_queue, 'C3-03-B - Queue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(l_queue, l_device_obj)
        # print(PrettyFormatAny.form(l_msg, 'C3-03-C - Zone', 190))
        self.assertEqual(l_msg, b'!1MVL02')

    def test_04_VolZ2(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_device_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        # print(PrettyFormatAny.form(l_device_obj, 'C3-04-A - Device', 190))
        l_queue = OnkyoQueueData()
        l_queue.Zone = 1
        l_queue.Command = 'Volume'
        l_queue.Args = 44
        # print(PrettyFormatAny.form(l_queue, 'C3-04-B - Queue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(l_queue, l_device_obj)
        # print(PrettyFormatAny.form(l_msg, 'C3-04-C - Zone', 190))
        self.assertEqual(l_msg, b'!1ZVL2C')


class D1_Protocol(SetupMixin, unittest.TestCase):
    """
    This section tests
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
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

        return l_creator.connectTCP('127.0.0.1', 12345).addCallback(cb, None)

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


class E1_Data(SetupMixin, unittest.TestCase):
    """
    Test that the Onkyo XML is correct.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # l_ret = entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        self.m_xml_onkyo_sect = XmlConfigTools.find_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')

    def test_00_setup(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'E1-00-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'E1-00-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'E1-00-C - Entertainment'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'E1-00-D - Plugins'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'], 'E1-00-E - Onkyo'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices, 'E1-00-F - Devices'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0], 'E1-00-G - Devices'))
        self.assertEqual(self.m_pyhouse_obj.House.Entertainment.PluginCount, 5)

    def test_01_Onkyo(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo']
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.DeviceCount, 2)
        self.assertEqual(l_obj.Name, 'onkyo')

    def test_02_Device0(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[0]
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_0)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_0)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_0)

    def test_03_Device1(self):
        l_obj = self.m_pyhouse_obj.House.Entertainment.Plugins['onkyo'].Devices[1]
        print(PrettyFormatAny.form(l_obj, 'E1-01-A - PyHouse', 190))
        self.assertEqual(l_obj.Name, TESTING_ONKYO_DEVICE_NAME_1)
        self.assertEqual(str(l_obj.Active), TESTING_ONKYO_DEVICE_ACTIVE_1)
        self.assertEqual(str(l_obj.Key), TESTING_ONKYO_DEVICE_KEY_1)


class E2_Message(SetupMixin, unittest.TestCase):
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
        # print(PrettyFormatAny.form(l_msg, 'E2-01-A - Zone', 190))
        self.assertEqual(l_msg, 1)


class F3_Yaml(SetupMixin, unittest.TestCase):
    """
    This section tests building commands to the onkyo device
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        entertainmentXML().read_entertainment_all(self.m_pyhouse_obj)
        self.m_device = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices[0]
        self.m_yaml = onkyoAPI(self.m_pyhouse_obj)._read_yaml(self.m_device)
        self.m_queue = OnkyoQueueData()
        self.m_queue.Zone = 1
        self.m_queue.Command = 'Power'
        self.m_queue.Args = 'On'

    def test_01_Power(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_queue, 'F3-01-A - ZoneQueue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(self.m_queue, self.m_device)
        # print('F3-01-B - {}'.format(l_msg))
        # self.assertEqual(l_msg, b'!1PWR01')
        #
        self.m_queue.Args = '?'
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_comand(self.m_queue, self.m_device)
        # print('F3-01-C - {}'.format(l_msg))
        self.assertEqual(l_msg, b'!1PWRQSTN')

    def test_02_Vol(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_queue.Command = 'Volume'
        self.m_queue.Args = 27
        # print(PrettyFormatAny.form(self.m_queue, 'F3-01-A - ZoneQueue', 190))
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_volume(self.m_yaml, self.m_queue)
        # print('F3-01-B - {}'.format(l_msg))
        self.assertEqual(l_msg, b'!1MVL27')
        #
        self.m_queue.Args = 61
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_volume(self.m_yaml, self.m_queue)
        # print('F3-01-C - {}'.format(l_msg))
        self.assertEqual(l_msg, b'!1MVL61')
        #
        self.m_queue.Args = 3
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_volume(self.m_yaml, self.m_queue)
        # print('F3-01-C - {}'.format(l_msg))
        self.assertEqual(l_msg, b'!1MVL03')
        #
        self.m_queue.Zone = 0
        self.m_queue.Args = 3
        l_msg = OnkyoClient(self.m_pyhouse_obj)._build_volume(self.m_yaml, self.m_queue)
        # print('F3-01-C - {}'.format(l_msg))
        self.assertEqual(l_msg, b'!1MVL03')

# ## END DBK
