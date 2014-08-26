"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_node_discovery -*-

@name: PyHouse/src/Modules/Core/node_discovery.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 5, 2014
@summary: This module is for discovering all the PyHouse nodes in a domain.

This Module:
    Uses IPv4 multicast to discover the other PyHouse nodes in the local network
    Uses IPv6 multicast to discover nodes and overrides IPv4 contact info.
    Uses neighbor discovery to find other potential devices that may play a part in home automation.

TODO: Delete nodes that have gone away.
      Check for new nodes periodically.
      Inform domain module that something happened.
"""

# Import system type stuff
from twisted.application import service
from twisted.internet.protocol import DatagramProtocol, ConnectedDatagramProtocol

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 9
LOG = Logger.getLogger('PyHouse.NodeDiscovry')


__all__ = [
           'API']

PYHOUSE_MULTICAST_IP_V4 = '234.35.36.37'
PYHOUSE_MULTICAST_IP_V6 = 'ff05::35:3637'

PYHOUSE_DISCOVERY_PORT = 8582
WHOS_THERE = "Who's There?"
I_AM = "I am."
MAX_TTL = 4


class NodeUtil(object):
    """
    """

    def initialize_node(self, p_addr_v4, p_addr_v6):
        l_node = NodeData()
        l_node.ConnectionAddr_IPv4 = p_addr_v4
        l_node.ConnectionAddr_IPv6 = p_addr_v6
        return l_node


class DGramUtil(object):
    m_address_list = []
    m_interface = ''

    def _save_node_info(self, p_node, p_pyhouse_obj):
        l_count = 0
        for l_node in p_pyhouse_obj.Computer.Nodes.itervalues():
            l_count += 1
            if p_node.ConnectionAddr_IPv4 == l_node.ConnectionAddr_IPv4:
                return
        p_node.Key = l_count
        p_pyhouse_obj.Computer.Nodes[l_count] = p_node
        LOG.info("Added node # {0:} - From Addr: {1:}, Named: {2:}".format(l_count, p_node.ConnectionAddr_IPv4, p_node.Name))

    def set_node_0_addr(self, p_address, p_pyhouse_obj):
        if p_pyhouse_obj.Computer.Nodes[0].ConnectionAddr_IPv4 == None:
            p_pyhouse_obj.Computer.Nodes[0].ConnectionAddr_IPv4 = p_address[0]
            LOG.info("Update our node (slot 0) address to {0:}".format(p_address[0]))

    def _create_node(self, p_datagram, p_address, p_pyhouse_obj):
        l_node = NodeUtil().initialize_node(p_address[0], None)
        l_node.Name = p_datagram.split(' ')[-1]
        l_node.Active = True
        l_node.UUID = ''
        self._save_node_info(l_node, p_pyhouse_obj)

    def _append_address(self, p_address):
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])

    def _send_query(self, p_transport):
        """
        Send out a "WHOS_THERE" query to find out everyone out there that is subscribed to our discovery multicast address.
        """
        p_transport.write(WHOS_THERE, (PYHOUSE_MULTICAST_IP_V4, PYHOUSE_DISCOVERY_PORT))

    def _send_response(self, p_address, p_pyhouse_obj, p_transport):
        """
        Send a message out in response to a "WHOS_THERE" query.
        """
        self.set_node_0_addr(p_address, p_pyhouse_obj)
        l_str = I_AM + ' ' + p_pyhouse_obj.Computer.Nodes[0].Name
        p_transport.write(l_str, p_address)

    def setup_multicast(self, p_transport):
        p_transport.setTTL(MAX_TTL)
        p_transport.joinGroup(PYHOUSE_MULTICAST_IP_V4)
        l_interface = p_transport.getOutgoingInterface()
        return l_interface


class ServerProtocol(DatagramProtocol):
    """Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def startProtocol(self):
        """
        Called after protocol has started listening.
        Set the TTL>1 so multicast will cross router hops:
        Join a specific multicast group:
        """
        self.m_interface = DGramUtil().setup_multicast(self.transport)
        if g_debug >= 1:
            LOG.debug('Discovery Server Protocol started. {0:}'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        """
        @type  p_datagram: C{str}
        @param p_datagram: is the contents of the datagram.

        @type  p_address: C{tupple) (IpAddr, port)
        @param p_address: is the (IpAddr, Port) of the sender of this datagram (reply to address).
        """
        if g_debug >= 1:
            LOG.debug("Discovery Server rxed: {0:} from: {1:}".format(repr(p_datagram), p_address[0]))
        DGramUtil()._append_address(p_address)
        if p_datagram.startswith(WHOS_THERE):
            DGramUtil()._send_response(p_address, self.m_pyhouse_obj, self.transport)
        elif p_datagram.startswith(I_AM):
            DGramUtil()._create_node(p_datagram, p_address, self.m_pyhouse_obj)


class ClientProtocol(ConnectedDatagramProtocol):
    """
    Find other PyHouse nodes within range.
    """
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def startProtocol(self):
        """
        Called when the protocol starts up.
        All listeners on the Multicast address (including us) will receive the "Who's There?" message.
        """
        self.m_interface = DGramUtil().setup_multicast(self.transport)
        DGramUtil()._send_query(self.transport)
        if g_debug >= 1:
            LOG.debug('Discovery Client Protocol started  {0:}.'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        """
        The client only rxes WHOS_THERE
        """
        NodeUtil().initialize_node(p_address[0], None)
        if g_debug >= 1:
            LOG.debug('Discovery Client rxed: {0:} From: {1:}'.format(p_datagram, p_address[0]))
        if p_datagram.startswith(WHOS_THERE):
            DGramUtil().set_node_0_addr(p_address, self.m_pyhouse_obj)


class Utility(object):
    """
    Use UDP multicast to discover the other PyHouse nodes that are local.
    Use listenMultiple=True so that we can run a server and a client on same node.
    """
    m_pyhouse_obj = None
    m_service_installed = False

    def _start_discovery_server(self, p_pyhouse_obj):
        p_pyhouse_obj.Twisted.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, ServerProtocol(p_pyhouse_obj), listenMultiple = True)

    def _start_discovery_client(self, p_pyhouse_obj):
        p_pyhouse_obj.Twisted.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, ClientProtocol(p_pyhouse_obj), listenMultiple = True)

    def start_node_discovery(self, p_pyhouse_obj):
        try:
            p_pyhouse_obj.Services.NodeDiscoveryService = service.Service()
            p_pyhouse_obj.Services.NodeDiscoveryService.setName('NodeDiscovery')
            p_pyhouse_obj.Services.NodeDiscoveryService.setServiceParent(p_pyhouse_obj.Twisted.Application)
            self._start_discovery_server(p_pyhouse_obj)
            self._start_discovery_client(p_pyhouse_obj)
        except RuntimeError:  # The service is already installed
            pass
        self.m_service_installed = True


class API(Utility):

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.start_node_discovery(p_pyhouse_obj)

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        return p_xml

# ## END DBK
