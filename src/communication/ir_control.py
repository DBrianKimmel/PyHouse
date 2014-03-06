"""
Created on Jan 26, 2014

Name: ir_control.py
@author: briank

Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.

"""

# Import system type stuff
import logging

from twisted.application.internet import StreamServerEndpointService
from twisted.application.service import Application
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint, UNIXClientEndpoint, clientFromString
from twisted.protocols.amp import AMP


g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


LIRC_SOCKET = 'unix:path=/var/run/lirc/lircd'

class LircProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        print 'Lirc data =', p_data


class LircClientFactory(ClientFactory):

    def startedConnecting(self, p_connector):
        print "LircClientFactory - Started to connect."

    def buildProtocol(self, addr):
        print "LircClientFactory - connected"
        return LircProtocol()

    def clientConnectionLost(self, connector, p_reason):
        print 'LircClientFactory - lost connection ', p_reason

    def clientConnectionFailed(self, connector, p_reason):
        print 'LircClientFactory - Connection failed ', p_reason


class LircFactory(Factory):

    def buildProtocol(self, addr):
        print "LircFactory - connected"
        return LircProtocol()


class IrDispatch(object):
    """
    """

class API(object):

    def __init__(self):
        print "ir_control.API()"
        l_endpoint = clientFromString(reactor, LIRC_SOCKET)
        l_factory = LircClientFactory()
        l_endpoint.connect(l_factory)

    def Start(self, _p_pyhouses_obj):
        print 'ir_control.API.Start()'
        l_application = Application('IR Control Server')
        l_endpoint = TCP4ServerEndpoint
        l_factory = Factory()
        l_factory.protocol = AMP
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(l_application)

    def Stop(self):
        pass

# ## END DBK
