"""
@name: PyHouse/src/core/node_discovery.py

# -*- test-case-name: PyHouse.src.core.test.test_node_discovery -*-

Created on Apr 5, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for discovering all the PyHouse nodes in a domain.

"""

# Import system type stuff
import logging

from twisted.internet.protocol import DatagramProtocol, ConnectedDatagramProtocol


g_debug = 0
g_logger = logging.getLogger('PyHouse.NodeDiscovry')

PYHOUSE_MULTICAST = '234.35.36.37'
AMP_PORT = 8581
PYHOUSE_DISCOVERY_PORT = 8582
WHOS_THERE = "Who's There?"
I_AM = "I am."


class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


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
        l_msg = "Server Discovery Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address))
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])
            g_logger.info("{0:} - {1:}".format(l_msg, self.m_address_list))
            # self.send_node(p_address[0])
        if p_datagram == WHOS_THERE:
            # Rather than replying to the group multicast address, we send the reply directly (unicast) to the originating port:
            self.transport.write(I_AM, p_address)
            # self.save_node_info()

    def save_node_info(self):
        l_count = 0
        for l_node in self.m_pyhouses_obj.CoreData.Nodes.itervalues():
            l_count += 1
        self.m_pyhouses_obj.CoreData.Nodes[l_count] = l_node


class MulticastDiscoveryClientProtocol(ConnectedDatagramProtocol):
    """Find other PyHouse nodes within range."""

    def startProtocol(self):
        """
        Called when the protocol starts up.

        All listeners on the multicast address (including us) will receive this message.
        """
        self.transport.setTTL(2)
        _l_defer = self.transport.joinGroup(PYHOUSE_MULTICAST)
        self.transport.write(WHOS_THERE, (PYHOUSE_MULTICAST, PYHOUSE_DISCOVERY_PORT))

    def datagramReceived(self, p_datagram, p_address):
        l_msg = "Client Discovery Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address))
        g_logger.info(l_msg)


class Utility(object):

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


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.start_node_discovery(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
