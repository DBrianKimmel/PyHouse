"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_schedules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 23, 2016
@summary:   Test

"""

__updated__ = '2017-01-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Housing.test.xml_housing import TESTING_HOUSE_NAME, TESTING_HOUSE_ACTIVE, TESTING_HOUSE_KEY, TESTING_HOUSE_UUID
# from Modules.Utilities.debug_tools import PrettyFormatAny


JSON = '{ Active : false, \
DOW : 127, \
Key : 5, \
Level : 50, \
LightName : "MBR Rope", \
LightUUID : "1efbce9e-4618-11e6-89e7-74da3859e09a", \
Name :"Evening-05". \
Rate : 0, \
RoomName : "Master Bed", \
RoomUUID : "1efc19d0-4618-11e6-89e7-74da3859e09a", \
ScheduleMode : "Home", \
ScheduleType : "Lighting", \
Time : "sunset + 00:15", \
UUID : null, \
_AddFlag : false, \
_DeleteFlag : false \
}'
JSON2 = {"Add":"false",
         "Delete":"false",
         "Name":"Schedule 0",
         "Key":"0",
         "Active":"true",
         "ScheduleType":"Lighting",
         "Time":"13:34",
         "DOW":"127",
         "ScheduleMode":"Home",
         "Level":"100",
         "Rate":"0",
         "RoomName":"Master Bath",
         "LightName":"Light, Insteon (xml_lights)"}

class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class SmartDummyRequest(DummyRequest):

    def __init__(self, method, url, args=None, headers=None):
        DummyRequest.__init__(self, url.split('/'))
        self.method = method
        self.headers.update(headers or {})

        # set args
        args = args or {}
        for k, v in args.items():
            self.addArg(k, v)

    def value(self):
        return "".join(self.written)


class DummySite(server.Site):
    def get(self, url, args=None, headers=None):
        return self._request("GET", url, args, headers)

    def post(self, url, args=None, headers=None):
        return self._request("POST", url, args, headers)

    def _request(self, method, url, args, headers):
        request = SmartDummyRequest(method, url, args, headers)
        resource = self.getResourceFor(request)
        result = resource.render(request)
        return self._resolveResult(request, result)

    def _resolveResult(self, request, result):
        if isinstance(result, str):
            request.write(result)
            request.finish()
            return succeed(request)
        elif result is server.NOT_DONE_YET:
            if request.finished:
                return succeed(request)
            else:
                return request.notifyFinish().addCallback(lambda _: request)
        else:
            raise ValueError("Unexpected return value: %r" % (result,))


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_schedules')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')
        # print(PrettyFormatAny.form(self.m_xml.web_sect, 'XML'))


class A2_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDiv(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)


class B01_JSON(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_xxx(self):
        l_dev = 1


class C02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')

    def test_11_ReadXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Logs = l_web
        self.assertEqual(l_web.WebPort, 8580)

    def test_21_WriteXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)

# ## END DBK
