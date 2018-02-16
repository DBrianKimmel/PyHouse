"""
@name: PyHouse/src/Modules/Computer/Web/test/test_web_server.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2018 by D. Brian Kimmel
@note: Created on Apr 8, 2013
@license: MIT License
@summary: This module is for AMP request/response protocol

Passed all 4 tests - DBK - 2018-01-27

"""

__updated__ = '2018-02-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest

# Import PyMh files and modules.
from Modules.Computer.Web.web_xml import Xml as webXml
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Web.test.xml_web import \
        TESTING_WEB_PORT, TESTING_WEB_SECURE_PORT, TESTING_WEB_SOCKET_PORT, TESTING_LOGIN_NAME_0, TESTING_LOGIN_KEY_0, \
    TESTING_LOGIN_ACTIVE_0, TESTING_LOGIN_FULL_NAME_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


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
        print('Id: test_web_server')


class B1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.web_sect.tag, 'WebSection')


class B2_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ReadXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        # print(PrettyFormatAny.form(l_web, 'C02-11-A - Xml'))
        self.assertEqual(str(l_web.WebPort), TESTING_WEB_PORT)
        self.assertEqual(str(l_web.SecurePort), TESTING_WEB_SECURE_PORT)
        self.assertEqual(str(l_web.WebSocketPort), TESTING_WEB_SOCKET_PORT)


class W1_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_WriteXML(self):
        l_web = webXml.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = l_web
        # print(PrettyFormatAny.form(l_web, 'W1-01-A - Web'))
        l_xml = webXml.write_web_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'W1-01-B - Xml'))
        # print(PrettyFormatAny.form(l_xml[3], 'W1-01-B - Xml'))
        self.assertEqual(l_xml[3][0].attrib['Name'], TESTING_LOGIN_NAME_0)
        self.assertEqual(l_xml[3][0].attrib['Key'], TESTING_LOGIN_KEY_0)
        self.assertEqual(l_xml[3][0].attrib['Active'], TESTING_LOGIN_ACTIVE_0)
        self.assertEqual(l_xml[3][0].find('FullName').text, TESTING_LOGIN_FULL_NAME_0)

# ## END DBK
