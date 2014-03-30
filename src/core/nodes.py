"""
@name: PyHouse/src/core/nodes.py

# -*- test-case-name: PyHouse.src.core.test.test_nodes -*-

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
PYHOUSE_DISCOVERY_PORT = 8582


class NodeData(object):

    def __init__(self):
        self.HostName = ''
        self.Key = 0
        self.IpV4Addr = None


class RegisterNodeError(Exception):
    pass


class RegisterNode(Command):
    """
    """
    arguments = [('Command', Integer()),
                 ('NodeName', Unicode()),
                 ('NodeType', Integer()),
                 ('IPv4', String()),
                 ('IPv6', String())
                 ]
    response = [('Ack', Integer())]
    errors = {RegisterNodeError: 'Node Information unavailable.'}


class AmpClientProtocol(AMP):

    def dataReceived(self, p_data):
        l_msg = 'Amp Client Received {0:}'.format(p_data)
        g_logger.debug(l_msg)

    def connectionMade(self):
        g_logger.debug('Amp Client connection made.')


class AmpClientFactory(Factory):

    def startedConnecting(self, p_connector):
        pass

    def buildProtocol(self, _addr):
        return AmpClientProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def connect(self, p_pyhouses_obj):
        l_endpoint = clientFromString(p_pyhouses_obj.Reactor, NODE_CLIENT)
        # print('Amp Client Nodes.Endpoint:', l_endpoint)
        l_factory = AmpClientFactory()
        l_defer = l_endpoint.connect(l_factory)
        # print("Amp Client started.", l_defer)
        g_logger.info("Amp Client started.")
        return l_defer

    def send_register_node(self, p_protocol):
        p_protocol.callRemote(
            RegisterNode,
            Command = 1,
            NodeName = u'briank',
            NodeType = None,
            IPv4 = '1.2.3.4',
            Ipv6 = 'ff00::'
            )


class AmpServerProtocol(AMP):

    def dataReceived(self, p_data):
        g_logger.debug('Amp Server data rxed {0:}'.format(p_data))

    def connectionMade(self):
        g_logger.debug('Amp Server connection Made')

    def connectionLost(self, p_reason):
        g_logger.debug('Amp Server connection lost {0:}'.format(p_reason))


class AmpServerFactory(Factory):

    def buildProtocol(self, _p_addr):
        return AmpServerProtocol()


class AmpServer(object):
    """Sit and listen for amp commands from other nodes.
    """

    def server(self, p_pyhouses_obj):
        l_endpoint = serverFromString(p_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory()
        # l_factory.protocol = AmpServerProtocol
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)
        l_ret = l_endpoint.listen(AmpServerFactory())
        g_logger.info("Amp Server started.")
        return l_ret


class MulticastDiscoveryServerProtocol(DatagramProtocol):
    """Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """
    m_addresses = []
    m_pyhouses_obj = None

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj

    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        self.transport.setTTL(2)
        _l_defer = self.transport.joinGroup(PYHOUSE_MULTICAST)

    def datagramReceived(self, p_datagram, p_address):
        l_node = NodeData()
        l_node.IpV4Addr = p_address
        l_msg = "Server Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address))
        g_logger.info("Addr:{0:} - {1:}".format(l_msg, self.m_addresses))
        self.m_addresses.append(p_address)
        if p_datagram == "Client: Ping":
            # Rather than replying to the group multicast address, we send the reply directly (unicast) to the originating port:
            self.transport.write("Server: Pong", p_address)
        l_count = 0
        for l_node in self.m_pyhouses_obj.Nodes.itervalues():
            l_count += 1
            if l_node.IpV4Addr == p_address:
                return
        self.m_pyhouses_obj.Nodes[l_count] = l_node


class MulticastDiscoveryClientProtocol(DatagramProtocol):
    """Find other PyHouse nodes within range."""

    def startProtocol(self):
        """All listeners on the multicast address (including us) will receive this message."""
        _l_defer = self.transport.joinGroup(PYHOUSE_MULTICAST)
        self.transport.write('Client: Ping', (PYHOUSE_MULTICAST, PYHOUSE_DISCOVERY_PORT))

    def datagramReceived(self, datagram, address):
        l_msg = "Client Datagram {0:} received from {1:}".format(repr(datagram), repr(address))
        g_logger.info(l_msg)


class Utility(AmpServer, AmpClient):

    def start_node_discovery(self, p_pyhouses_obj):
        """Use UDP multicast to discover the other PyHouse nodes that are local.
        Fire the client off again once per hour to re-discover any new nodes
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        self._start_discovery_server(p_pyhouses_obj)
        self._start_discovery_client(p_pyhouses_obj)

    def _start_discovery_server(self, p_pyhouses_obj):
        """Use listenMultiple=True so that we can run a server and a client on same node."""
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryServerProtocol(p_pyhouses_obj), listenMultiple = True)

    def _start_discovery_client(self, p_pyhouses_obj):
        p_pyhouses_obj.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryClientProtocol(), listenMultiple = True)

    def start_amp(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        self.server(p_pyhouses_obj)
        l_defer = self.connect(p_pyhouses_obj)
        l_defer.addCallback(self.send_node_info)
        g_logger.debug('Amp server / client started.')
        p_pyhouses_obj.Reactor.callLater(60, self.send_node_info)

    def send_node_info(self):
        self.m_pyhouses_obj.Reactor.callLater(60 * 60, self.send_node_info)
        _l_defer = self.send_register_node(AmpClientProtocol)


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        if p_pyhouses_obj == None:
            p_pyhouses_obj.Nodes = {}
        self.start_node_discovery(p_pyhouses_obj)
        self.start_amp(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
