"""
PyHouse/src/core/nodes.py

Created on Mar 6, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for inter_node communication.
"""

# Import system type stuff
import logging

# from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.internet.endpoints import clientFromString, serverFromString
from twisted.application.internet import StreamServerEndpointService
from twisted.protocols.amp import AMP, Integer, Float, String, Unicode, Command


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

NODE_CLIENT = 'tcp:host=192.168.1.36:port=8581'
NODE_SERVER = 'tcp:port=8581'
PYHOUSE_MULTICAST = '234.35.36.37'
PYHOUSE_PORT = 8581


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

    def register(self, _p_name, _p_type, _p_v4, _p_v6):
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

    def connect(self, p_pyhouses_obj):
        l_endpoint = clientFromString(p_pyhouses_obj.Reactor, NODE_CLIENT)
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

    def buildProtocol(self, _p_addr):
        return NodeServerProtocol()


class NodeServer(object):

    def server(self, p_pyhouses_obj):
        l_endpoint = serverFromString(p_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = NodeServerFactory()
        # l_factory.protocol = NodeServerProtocol
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)
        l_ret = l_endpoint.listen(NodeServerFactory())
        g_logger.info("Server started.")
        return l_ret


class MulticastDiscoveryServerProtocol(DatagramProtocol):
    """Listen for PyHouse nodes and respond to them.
    """
    m_addresses = []

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        self.transport.setTTL(2)
        self.transport.joinGroup(PYHOUSE_MULTICAST)

    def datagramReceived(self, p_datagram, p_address):
        l_msg = "Server Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address))
        g_logger.info(l_msg)
        self.m_addresses.append(p_address)
        if p_datagram == "Client: Ping":
            # Rather than replying to the group multicast address, we send the reply directly (unicast) to the originating port:
            self.transport.write("Server: Pong", p_address)


class MulticastDiscoveryClientProtocol(DatagramProtocol):
    """Try to find other PyHouse nodes within range.
    """

    def startProtocol(self):
        self.transport.joinGroup(PYHOUSE_MULTICAST)
        # all listeners on the multicast address (including us) will receive this message.
        self.transport.write('Client: Ping', (PYHOUSE_MULTICAST, PYHOUSE_PORT))

    def datagramReceived(self, datagram, address):
        l_msg = "Client Datagram {0:} received from {1:}".format(repr(datagram), repr(address))
        g_logger.info(l_msg)


class Utility(object):

    def StartServer(self, p_pyhouses_obj):
        # _l_server = NodeServer().server(p_pyhouses_obj)
        # We use listenMultiple=True so that we can run MulticastServer.py and MulticastClient.py on same machine:
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_PORT, MulticastDiscoveryServerProtocol(), listenMultiple = True)

    def StartClient(self, p_pyhouses_obj):
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_PORT, MulticastDiscoveryClientProtocol(), listenMultiple = True)


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.StartServer(p_pyhouses_obj)
        self.StartClient(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
