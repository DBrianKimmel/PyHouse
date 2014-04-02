"""
@name: PyHouse/src/core/nodes.py

# -*- test-case-name: PyHouse.src.core.test.test_nodes -*-

Created on Mar 6, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for inter_node communication.

Using a Raspberry Pi as a node works fine for about any function, but I expect that it will run out
of capacity if too many services are attempted on one node.

Therefore, a cluster of nodes (a domain), each one running a small number of tasks will probably be the norm.

This design will then need a way for each node to discover all its neighbor nodes and establish a
communication network so we can pass information between nodes.

This module will establish a domain network and use Twisted's AMP protocol to pass messages around.
"""

# Import system type stuff
import logging

# from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.internet.endpoints import clientFromString, serverFromString, TCP4ClientEndpoint
from twisted.application.internet import StreamServerEndpointService
from twisted.protocols.amp import AMP, Integer, String, Unicode, Command


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

NODE_CLIENT = 'tcp:host=192.168.1.36:port=8581'
NODE_SERVER = 'tcp:port=8581'
PYHOUSE_MULTICAST = '234.35.36.37'
AMP_PORT = 8581
PYHOUSE_DISCOVERY_PORT = 8582


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.ConnectionAddr = None
        self.Role = None
        self.Interfaces = {}


class RegisterNodeError(Exception):
    pass


class RegisterNode(Command):
    """
    """
    arguments = [('Command', Integer()),
                 ('NodeName', Unicode()),
                 ('NodeType', Integer()),
                 ('IPv4', String())]
    response = [('Ack', Integer())]
    errors = {RegisterNodeError: 'Node Information unavailable.'}


class AmpClientProtocol(AMP):

    def dataReceived(self, p_data):
        l_msg = 'Amp Client Received {0:}'.format(p_data)
        g_logger.debug(l_msg)

    def connectionMade(self):
        """We connected to some server.
        Send them our node info
        Ask for their Node info.
        """
        g_logger.debug('Amp Client connection made.')



class AmpClientFactory(Factory):

    def startedConnecting(self, p_connector):
        g_logger.info("AMP Client startedConnecting {0:}".format(p_connector))

    def buildProtocol(self, _addr):
        return AmpClientProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def connect(self, p_pyhouses_obj, p_address):
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory()
        l_defer = l_endpoint.connect(l_factory)
        g_logger.info("Amp Client started.")
        def cb_send_register_node(p_protocol):
            g_logger.debug('Sending our local node to a new discovered address {0:}'.format(p_address))
            p_protocol.callRemote(
                RegisterNode,
                Command = 1,
                NodeName = u'briank',
                NodeType = 1,
                IPv4 = '1.2.3.4',
                Ipv6 = 'ff00::'
                )
        l_defer.addCallback(cb_send_register_node)
        def cb_registered(p_result):
            g_logger.debug('Registration result:{0:}'.format(p_result))
        l_defer.addCallback(cb_registered)
        def eb_error(p_error):
            g_logger.debug('Registration error:{0:}'.format(p_error))
        l_defer.addErrback(eb_error, "Failed to register")
        def cb_done(_ignored):
            g_logger.debug('Registration done')
        l_defer.addCallback(cb_done)
        return l_defer

    def XXsend_register_node(self, p_protocol):
        g_logger.debug('Sending our local node to a new discovered address')
        p_protocol.callRemote(
            RegisterNode,
            Command = 1,
            NodeName = u'briank',
            NodeType = 1,
            IPv4 = '1.2.3.4',
            Ipv6 = 'ff00::'
            )


class AmpServerProtocol(AMP):

    def dataReceived(self, p_data):
        g_logger.debug('Amp Server data rxed {0:}'.format(p_data))

    def connectionMade(self):
        """Somebody connected to us...
        """
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
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)
        l_ret = l_endpoint.listen(AmpServerFactory())
        g_logger.info("Amp Server started.")
        return l_ret


class MulticastDiscoveryServerProtocol(DatagramProtocol):
    """Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """
    m_address_list = []
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
        """
        @type p_datagram: C{str}
        @param p_datagram: is the contents of the datagram.

        @type p_address: C{tupple) (ipaddr, port)
        @param p_address: is the (IpAddr, Port) of the sender of this datagram
        """
        l_node = NodeData()
        l_node.ConnectionAddr = p_address
        l_msg = "Server Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address))
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])
            g_logger.info("{0:} - {1:}".format(l_msg, self.m_address_list))
            self.send_node(p_address[0])
        if p_datagram == "Client: Ping":
            # Rather than replying to the group multicast address, we send the reply directly (unicast) to the originating port:
            self.transport.write("Server: Pong", p_address)
        l_count = 0
        for l_node in self.m_pyhouses_obj.Nodes.itervalues():
            l_count += 1
        self.m_pyhouses_obj.Nodes[l_count] = l_node

    def send_node(self, p_address):
        """
        @type p_address: C{str)
        @param p_address: is the IpAddr to send to node info to
        """
        AmpClient().connect(self.m_pyhouses_obj, p_address)
        g_logger.debug('Open AMP client connection to {0:}'.format(p_address))


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
        self._start_amp_server()

    def cb_send_node_info(self, p_protocol):
        g_logger.debug('Amp client cb_send_node_info - {0:}.'.format(p_protocol))
        _l_defer = self.send_register_node(AmpClientProtocol)

    def _start_amp_server(self):
        _l_defer = self.server(self.m_pyhouses_obj)

    def _start_amp_client(self):
        """We need one of these for every node in the domain.
        """
        l_defer = self.connect(self.m_pyhouses_obj)
        l_defer.addCallback(self.cb_send_node_info)


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
