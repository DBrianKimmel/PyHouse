"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_server -*-

@name:      PyHouse/src/Modules/Web/web_server.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2012-2018 by D. Brian Kimmel
@note:      Created on Apr 3, 2012
@license:   MIT License
@summary:   This module provides the web server service of PyHouse.

This is a Main Module - always present.

Open 2 web browsers.
    open browser on port 8580.
    Secure (TLS) browser on port 8588.

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

__updated__ = '2018-01-27'

#  Import system type stuff
# import ssl
# from nevow import appserver
#  from twisted.internet import ssl
# from twisted.internet import protocol
from twisted.internet import defer
# from twisted.python.modules import getModule

#  Import PyMh files and modules.
# from Modules.Core.data_objects import WebData
# from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.Web import web_utils
# from Modules.Computer.Web import web_mainpage
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

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
        LOG.warn('Connected to: {}'.format(PrettyFormatAny.form(p_login, 'Login')))


class Utility(ClientConnections):

    def start_webserver(self, p_pyhouse_obj):
        l_site_dir = None
        # l_site = appserver.NevowSite(web_mainpage.TheRoot(l_site_dir, p_pyhouse_obj))
        # l_port = p_pyhouse_obj.Computer.Web.WebPort
        # p_pyhouse_obj.Twisted.Reactor.listenTCP(l_port, l_site)
        l_msg = "Port:{}, Path:{}".format(p_pyhouse_obj.Computer.Web.WebPort, l_site_dir)
        LOG.info("Started - {}".format(l_msg))

    def start_non_tls(self, p_pyhouse_obj, p_site, p_port):
        p_pyhouse_obj.Twisted.Reactor.listenTCP(p_port, p_site)

    def start_tls(self, _p_pyhouse_obj):
        # l_certData = getModule(__name__).filePath.sibling('server.pem').getContent()
        # l_certificate = ssl.PrivateCertificate.loadPEM(l_certData)
        # l_factory = protocol.Factory.forProtocol(echoserv.Echo)
        # p_pyhouse_obj.Twisted.Reactor.listenSSL(8000, l_factory, l_certificate.options())
        return defer.Deferred()


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.State = web_utils.WS_IDLE
        self.m_web_running = False
        LOG.info('Initialized.')

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        LOG.info('Starting web server.')
        self.start_webserver(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info('Stopped.')

#  ## END DBK
