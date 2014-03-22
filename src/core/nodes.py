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
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import clientFromString, serverFromString
from twisted.application.service import Application
from twisted.application.internet import StreamServerEndpointService
from twisted.protocols.amp import AMP, Integer, Float, String, Unicode, Command


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

NODE_CLIENT = 'tcp:host=192.168.1.36:port=8581'
NODE_SERVER = 'tcp:port=8581'


class NodeUnavailable(Exception):
    pass


class RegisterCommand(Command):
    """
    """
    arguments = [('Command', Integer()),
                 ('NodeName', Unicode()),
                 ('NodeType', Integer()),
                 ('IPv4', String()),
                 ('IPv6', String())
                 ]
    response = [('Ack', Integer())]


class RegisterNode(AMP):

    def register(self, p_name, p_type, p_v4, p_v6):
        l_ack = 1
        return {'Ack': l_ack}

    RegisterCommand.responder(register)


class Divide(Command):
    arguments = [('numerator', Integer()),
                 ('denominator', Integer())]
    response = [('result', Float())]
    errors = {ZeroDivisionError: 'ZERO_DIVISION'}


class NodeClientProtocol(AMP):

    def dataReceived(self, p_data):
        # IrDispatch(p_data)
        pass

    def connectionMade(self):
        g_logger.debug('Client connection made.')


class NodeClientFactory(Factory):

    def startedConnecting(self, p_connector):
        pass

    def buildProtocol(self, _addr):
        return NodeClientProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('NodeClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('NodeClientFactory - Connection failed {0:}'.format(p_reason))


class NodeClient(object):

    def connect(self):
        l_endpoint = clientFromString(reactor, NODE_CLIENT)
        print('Nodes.Endpoint:', l_endpoint)
        l_factory = NodeClientFactory()
        l_defer = l_endpoint.connect(l_factory)
        print("Client started.", l_defer)
        g_logger.info("Client started.")
        return l_defer


class NodeServerProtocol(AMP):

    def dataReceived(self, p_data):
        g_logger.debug('Server data rxed {0:}'.format(p_data))

    def connectionMade(self):
        g_logger.debug('Server connection Made')

    def connectionLost(self, p_reason):
        g_logger.debug('Server connection lost {0:}'.format(p_reason))


class NodeServerFactory(Factory):

    def buildProtocol(self, p_addr):
        return NodeServerProtocol()


class NodeServer(object):

    def server(self):
        l_application = Application('NodeCommunicationService')
        l_endpoint = serverFromString(reactor, NODE_SERVER)
        l_factory = NodeServerFactory()
        # l_factory.protocol = NodeServerProtocol
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(l_application)
        l_ret = l_endpoint.listen(NodeServerFactory())
        g_logger.info("Server started.")
        return l_ret


class Utility(object):

    def StartServer(self, _p_pyhouses_obj):
        _l_server = NodeServer().server()

    def StartClient(self, _p_pyhouses_obj):
        def eb_err():
            pass
        def cb_ok():
            pass
        l_defer = NodeClient().connect()
        l_defer.addErrback(eb_err, "Connection failed.")

    def print_interfaces(self, p_pyhouses_obj):
        for l_interface in p_pyhouses_obj.Nodes.itervalues():
            g_logger.debug('Client Node Interface {0:} {1:} {2:}'.format(l_interface.Name, l_interface.V4Address, l_interface.V6Address))


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.print_interfaces(p_pyhouses_obj)
        self.StartServer(p_pyhouses_obj)
        self.StartClient(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
