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
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.NodeDiscovry')


__all__ = [
           'API']

PYHOUSE_MULTICAST_IP_V4 = '234.35.36.37'
PYHOUSE_DISCOVERY_PORT = 8582
WHOS_THERE = "Who's There?"
I_AM = "I am."


class DGramUtil(object):
    m_address_list = []
    m_pyhouse_obj = None
    m_interface = ''

    def _save_node_info(self, p_node):
        l_count = 0
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervalues():
            l_count += 1
            if p_node.ConnectionAddr_IPv4 == l_node.ConnectionAddr_IPv4:
                return
        p_node.Key = l_count
        self.m_pyhouse_obj.Computer.Nodes[l_count] = p_node
        LOG.info("Added node # {0:} - From Addr: {1:}, Named: {2:}".format(l_count, p_node.ConnectionAddr_IPv4, p_node.Name))

    def set_node_0_addr(self, p_address):
        if self.m_pyhouse_obj.Computer.Nodes[0].ConnectionAddr_IPv4 == None:
            self.m_pyhouse_obj.Computer.Nodes[0].ConnectionAddr_IPv4 = p_address[0]
            LOG.info("Update our node (slot 0) address to {0:}".format(p_address[0]))


class MulticastDiscoveryServerProtocol(DatagramProtocol, DGramUtil):
    """Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj

    def startProtocol(self):
        """
        Called after protocol has started listening.
        Set the TTL>1 so multicast will cross router hops:
        Join a specific multicast group:
        """
        self.transport.setTTL(4)
        self.transport.joinGroup(PYHOUSE_MULTICAST_IP_V4)
        self.m_interface = self.transport.getOutgoingInterface()
        if g_debug >= 1:
            LOG.debug('Discovery Server Protocol started. {0:}'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        """
        @type  p_datagram: C{str}
        @param p_datagram: is the contents of the datagram.

        @type  p_address: C{tupple) (IpAddr, port)
        @param p_address: is the (IpAddr, Port) of the sender of this datagram (reply to address).
        """
        l_node = NodeData()
        l_node.ConnectionAddr_IPv4 = p_address[0]
        if g_debug >= 1:
            LOG.debug("Server Discovery Datagram {0:} received from {1:}".format(repr(p_datagram), repr(p_address)))
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])
        if p_datagram.startswith(WHOS_THERE):
            self.set_node_0_addr(p_address)
            l_str = I_AM + ' ' + self.m_pyhouse_obj.Computer.Nodes[0].Name
            self.transport.write(l_str, p_address)
        elif p_datagram.startswith(I_AM):
            l_node.Name = p_datagram.split(' ')[-1]
            l_node.Active = True
            l_node.UUID = '247'
            self._save_node_info(l_node)


class MulticastDiscoveryClientProtocol(ConnectedDatagramProtocol, DGramUtil):
    """Find other PyHouse nodes within range."""
    m_pyhouse_obj = None

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj

    def startProtocol(self):
        """
        Called when the protocol starts up.
        All listeners on the Multicast address (including us) will receive the "Who's There?" message.
        """
        self.transport.setTTL(4)
        self.transport.joinGroup(PYHOUSE_MULTICAST_IP_V4)
        self.m_interface = self.transport.getOutgoingInterface()
        self.transport.write(WHOS_THERE, (PYHOUSE_MULTICAST_IP_V4, PYHOUSE_DISCOVERY_PORT))
        if g_debug >= 1:
            LOG.debug('Discovery Client Protocol started  {0:}.'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        l_node = NodeData()
        l_node.ConnectionAddr_IPv4 = p_address[0]
        if g_debug >= 1:
            LOG.debug('Discovery Client rxed:{0:} From:{1:}'.format(p_datagram, p_address[0]))
        if p_datagram.startswith(WHOS_THERE):
            self.set_node_0_addr(p_address)
        elif p_datagram.startswith(I_AM):
            l_node.Name = p_datagram.split(' ')[-1]
            l_node.Active = True
            l_node.UUID = '4352'
            self._save_node_info(l_node)


class Utility(object):
    """
    Use UDP multicast to discover the other PyHouse nodes that are local.
    Use listenMultiple=True so that we can run a server and a client on same node.
    """

    m_service_installed = False

    def start_node_discovery(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj
        LOG.info('NodeDiscovery - StartNodeDiscovery - Service:{0:}'.format(self.m_service_installed))
        try:
            p_pyhouses_obj.Services.NodeDiscoveryService = service.Service()
            p_pyhouses_obj.Services.NodeDiscoveryService.setName('NodeDiscovery')
            p_pyhouses_obj.Services.NodeDiscoveryService.setServiceParent(p_pyhouses_obj.Twisted.Application)
            self._start_discovery_server(p_pyhouses_obj)
            self._start_discovery_client(p_pyhouses_obj)
            # PrettyPrintAny(p_pyhouses_obj.Services, 'NodeDiscovery - StartService - PyHouse.Services')
        except RuntimeError:  # The service is already installed
            pass
        self.m_service_installed = True

    def stop_node_discovery(self):
        pass

    def _start_discovery_server(self, p_pyhouses_obj):
        p_pyhouses_obj.Twisted.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryServerProtocol(p_pyhouses_obj), listenMultiple = True)

    def _start_discovery_client(self, p_pyhouses_obj):
        p_pyhouses_obj.Twisted.Reactor.listenMulticast(PYHOUSE_DISCOVERY_PORT, MulticastDiscoveryClientProtocol(p_pyhouses_obj), listenMultiple = True)


class API(Utility):

    def __init__(self):
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        self.start_node_discovery(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        self.stop_node_discovery()
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        LOG.info('Saved XML')
        return p_xml

# ## END DBK
