"""
nodes.py

Created on Mar 6, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module if for inter_node communication.
"""


# Import system type stuff
import logging

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import clientFromString, serverFromString
from twisted.application.service import Application
from twisted.application.internet import StreamServerEndpointService
from twisted.protocols.amp import AMP, Integer, Float, String, Unicode, Command


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

NODE_PORT = 'tcp:port=8581'


class NodeUnavailable(Exception):
    pass


class RegisterNode(Command):
    """
    """
    arguments = [('NodeName', Unicode()),
                 ('IPv6', String())
                 ]
    response = [('total', Integer())]


class Sum(Command):
    """
    """
    arguments = [('a', Integer()),
                 ('b', Integer())
                 ]
    response = [('total', Integer())]


class JustSum(AMP):
    def sum(self, a, b):
        total = a + b
        return {'total': total}
    Sum.responder(sum)

class Divide(Command):
    arguments = [('numerator', Integer()),
                 ('denominator', Integer())]
    response = [('result', Float())]
    errors = {ZeroDivisionError: 'ZERO_DIVISION'}


class NodeClientProtocol(Protocol):

    def dataReceived(self, p_data):
        # IrDispatch(p_data)
        pass


class NodeClientFactory(Factory):

    def startedConnecting(self, p_connector):
        pass

    def buildProtocol(self, addr):
        return NodeClientProtocol()

    def clientConnectionLost(self, connector, p_reason):
        g_logger.error('NodeClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, connector, p_reason):
        g_logger.error('NodeClientFactory - Connection failed {0:}'.format(p_reason))


class NodeClient(object):

    def connect(self):
        l_endpoint = clientFromString(reactor, NODE_PORT)
        l_factory = NodeClientFactory()
        l_endpoint.connect(l_factory)


class NodeServerProtocol(Protocol):
    pass


class NodeServer(object):

    def server(self):
        l_application = Application('NodeCommunicationService')
        l_endpoint = serverFromString(reactor, NODE_PORT)
        l_factory = Factory()
        l_factory.protocol = NodeServerProtocol
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(l_application)
        g_logger.info("Server started.")


class Utility(object):

    def StartServer(self, p_pyhouses_obj):
        _l_server = NodeServer().server()

    def StartClient(self, p_pyhouses_obj):
        _l_client = NodeClient().connect()


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        for l_interface in p_pyhouses_obj.Nodes.itervalues():
            g_logger.debug('Client Node Interface {0:} {1:} {2:}'.format(l_interface.Name, l_interface.V4Address, l_interface.V6Address))
        self.StartServer(p_pyhouses_obj)
        self.StartClient(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
