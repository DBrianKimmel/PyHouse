"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_server -*-

@name:      PyHouse/src/Modules/Web/web_server.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2012-2015 by D. Brian Kimmel
@note:      Created on Apr 3, 2012
@license:   MIT License
@summary:   This module provides the web server service of PyHouse.

This is a Main Module - always present.

Open a port (8580 default) that will allow web browsers to control the
PyHouse system.  This will be an AJAX/COMET system using Nevow Athena.

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
# from twisted.application import service
from nevow import appserver
# from twisted.internet import ssl
from twisted.internet import protocol, defer
from twisted.internet import task
from twisted.python.modules import getModule

# Import PyMh files and modules.
from Modules.Core.data_objects import WebData
from Modules.Web.web_xml import Xml as webXml
from Modules.Web import web_utils
from Modules.Web import web_mainpage
from Modules.Computer import logging_pyh as Logger

ENDPOINT_WEB_SERVER = 'tcp:port=8580'

LOG = Logger.getLogger('PyHouse.WebServer      ')



class ClientConnections(object):
    """This class keeps track of all the connected browsers.
    We can update the browser via COMET when a controlled device changes.
    (Light On/Off, Pool water low, Garage Door open/Close ...)
    """
    def __init__(self):
        self.ConnectedBrowsers = []

    def add_browser(self, p_login):
        self.ConnectedBrowsers.append(p_login)


class Utility(ClientConnections):

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Web = WebData()

    def start_webserver(self, p_pyhouse_obj):
        # try:
        #    p_pyhouse_obj.Services.WebServerService = service.Service()
        #    p_pyhouse_obj.Services.WebServerService.setName('WebServer')
        #    p_pyhouse_obj.Services.WebServerService.setServiceParent(p_pyhouse_obj.Twisted.Application)
        # except RuntimeError:  # The service is already installed
        #    LOG.info('Service already installed.')
        #
        l_site_dir = None
        l_site = appserver.NevowSite(web_mainpage.TheRoot(l_site_dir, p_pyhouse_obj))
        l_port = p_pyhouse_obj.Computer.Web.WebPort
        p_pyhouse_obj.Twisted.Reactor.listenTCP(l_port, l_site)
        l_msg = "Port:{}, Path:{}".format(p_pyhouse_obj.Computer.Web.WebPort, l_site_dir)
        LOG.info("Started - {}".format(l_msg))

    def start_non_tls(self, p_pyhouse_obj, p_site, p_port):
        p_pyhouse_obj.Twisted.Reactor.listenTCP(p_port, p_site)

    def start_tls(self, p_pyhouse_obj):
        l_certData = getModule(__name__).filePath.sibling('server.pem').getContent()
        l_certificate = ssl.PrivateCertificate.loadPEM(l_certData)
        l_factory = protocol.Factory.forProtocol(echoserv.Echo)
        p_pyhouse_obj.Twisted.Reactor.listenSSL(8000, l_factory, l_certificate.options())
        return defer.Deferred()


class API(Utility, ClientConnections):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.State = web_utils.WS_IDLE
        self.m_web_running = False

    def Start(self):
        self.update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Web = self.LoadXml(self.m_pyhouse_obj)
        self.start_webserver(self.m_pyhouse_obj)

    def Stop(self):
        self.m_pyhouse_obj.Services.WebServerService.stopService()

    def LoadXml(self, p_pyhouse_obj):
        l_ret = webXml.read_web_xml(p_pyhouse_obj)
        return l_ret

    def SaveXml(self, p_xml):
        p_xml.append(webXml.write_web_xml(self.m_pyhouse_obj.Computer.Web))
        LOG.info("Saved WebServer XML.")

# ## END DBK
