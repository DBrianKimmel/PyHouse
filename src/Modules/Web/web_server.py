"""
-*- test-case-name: PyHouse.Modules.web.test.test_web_server -*-

@name: PyHouse/src/Modules/web/web_server.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@note: Created on Apr 3, 2012
@license: MIT License
@summary: This module provides the web server service of PyHouse.

This is a Main Module - always present.

Open a port (8580 default) that will allow web browsers to control the
PyHouse system.  This will be an AJAX/COMET system using nevow athena.

On initial startup allow a house to be created
    then rooms
    then light controllers
        and lights
        and buttons
        and scenes
    then schedules

Do not require reloads, auto change PyHouse on the fly.
"""

# Import system type stuff
from twisted.application import service
from nevow import appserver
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import WebData
from Modules.Web import web_utils
from Modules.Web import web_mainpage
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities import xml_tools
# from Modules.Utilities.tools import PrettyPrintAny

ENDPOINT_WEB_SERVER = 'tcp:port=8580'

g_debug = 9
LOG = Logger.getLogger('PyHouse.WebServer   ')


class ClientConnections(object):
    """This class keeps track of all the connected browsers.
    We can update the browser via COMET when a controlled device changes.
    (Light On/Off, Pool water low, Garage Door open/Close ...)
    """
    def __init__(self):
        self.ConnectedBrowsers = []

    def add_browser(self, p_login):
        self.ConnectedBrowsers.append(p_login)


class ReadWriteConfigXml(xml_tools.PutGetXML):
    """
    """

    def read_web_xml(self, p_pyhouses_obj):
        l_ret = WebData()
        try:
            l_sect = p_pyhouses_obj.XmlRoot.find('WebSection')
            l_ret.WebPort = self.get_int_from_xml(l_sect, 'WebPort')
        except AttributeError:
            l_ret.WebPort = 8580
        return l_ret

    def write_web_xml(self, p_web_obj):
        l_web_xml = ET.Element("WebSection")
        self.put_int_element(l_web_xml, 'WebPort', p_web_obj.WebPort)
        return l_web_xml


class Utility(ReadWriteConfigXml):

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Web = WebData()

    def start_webserver(self, p_pyhouses_obj):
        try:
            p_pyhouses_obj.Services.WebServerService = service.Service()
            p_pyhouses_obj.Services.WebServerService.setName('WebServer')
            p_pyhouses_obj.Services.WebServerService.setServiceParent(p_pyhouses_obj.Twisted.Application)
        except RuntimeError:  # The service is already installed
            pass
        #
        l_site_dir = None
        l_site = appserver.NevowSite(web_mainpage.TheRoot(l_site_dir, p_pyhouses_obj))
        p_pyhouses_obj.Twisted.Reactor.listenTCP(p_pyhouses_obj.Computer.Web.WebPort, l_site)
        l_msg = "Port:{0:}, Path:{1:}".format(p_pyhouses_obj.Computer.Web.WebPort, l_site_dir)
        LOG.info("Started - {0:}".format(l_msg))


class API(Utility, ClientConnections):

    def __init__(self):
        self.State = web_utils.WS_IDLE
        LOG.info("Initialized.\n")
        self.m_web_running = False

    def Start(self, p_pyhouse_obj):
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Computer.Web = self.read_web_xml(p_pyhouse_obj)
        self.start_webserver(p_pyhouse_obj)

    def Stop(self):
        self.m_pyhouse_obj.Services.WebServerService.stopService()

    def SaveXml(self, p_xml):
        p_xml.append(self.write_web_xml(self.m_pyhouse_obj.Computer.Web))
        LOG.info("Saved XML.")

# ## END DBK
