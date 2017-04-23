"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Web/websocket_server.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Web/websocket_server.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Apr 17, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-04-17'

#  Import system type stuff
# import ssl
import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
# from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Core.data_objects import WebData
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Computer.Web import web_utils
# from Modules.Computer.Web import web_mainpage
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

ENDPOINT_WEBSOCKET_SERVER = 'tcp:port=8581'

LOG = Logger.getLogger('PyHouse.WebServer      ')


from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class SomeServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("some request connected {}".format(request))

    def onMessage(self, payload, isBinary):
        self.sendMessage("message received")







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

    def start_tls(self, p_pyhouse_obj):
        # l_certData = getModule(__name__).filePath.sibling('server.pem').getContent()
        # l_certificate = ssl.PrivateCertificate.loadPEM(l_certData)
        # l_factory = protocol.Factory.forProtocol(echoserv.Echo)
        # p_pyhouse_obj.Twisted.Reactor.listenSSL(8581, l_factory, l_certificate.options())
        # return defer.Deferred()
        pass


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized.')

    def LoadXml(self, p_pyhouse_obj):
        pass

    def Start(self):
        LOG.info('Starting websocket server.')


        # static file server seving index.html as root
        root = File(".")

        factory = WebSocketServerFactory(u"ws://127.0.0.1:8581")
        factory.protocol = SomeServerProtocol
        resource = WebSocketResource(factory)
        # websockets resource on "/ws" path
        root.putChild(u"ws", resource)

        site = Site(root)
        self.m_pyhouse_obj.Twisted.Reactor.listenTCP(8581, site)




        # self.start_webserver(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        pass

    def Stop(self):
        LOG.info('Stopped.')




if __name__ == "__main__":
    log.startLogging(sys.stdout)


# ## END DBK
