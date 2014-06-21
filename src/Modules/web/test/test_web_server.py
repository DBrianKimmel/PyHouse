"""
@name: PyHouse/src/Modules/web/test/test_web_server.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 8, 2013
@license: MIT License
@summary: This module is for AMP request/response protocol

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet.defer import succeed
from twisted.web import server
from twisted.web.test.test_web import DummyRequest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, ComputerData
from Modules.web import web_server
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data


class SmartDummyRequest(DummyRequest):
    def __init__(self, method, url, args = None, headers = None):
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
    def get(self, url, args = None, headers = None):
        return self._request("GET", url, args, headers)


    def post(self, url, args = None, headers = None):
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


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_api = web_server.API()

        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.Computer = ComputerData()
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml

        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_web_xml = self.m_root_xml.find('Web')
        self.m_web_port_xml = self.m_web_xml.findtext('WebPort')


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_web_xml.tag, 'Web', 'XML - No Web section')

    def test_0211_ReadXML(self):
        l_web = self.m_api.read_web_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Logs = l_web
        PrettyPrintAny(l_web, 'Web Data')
        self.assertEqual(l_web.WebPort, 8580, 'Bad WebPort')

    def test_0221_WriteXML(self):
        l_web = self.m_api.read_web_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_web_xml(l_web)
        PrettyPrintAny(l_xml)

# ## END DBK
