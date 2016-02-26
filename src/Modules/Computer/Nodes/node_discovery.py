"""
-*- test-case-name: PyHouse.src.Modules.Computer/Nodes.test.test_node_discovery -*-

@name:      PyHouse/src/Modules/Computer/Nodes/node_discovery.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 5, 2014
@summary:   Provide a service for discovering all the PyHouse nodes in a domain, and in related domains.

This service runs periodically to find any new nodes and any dropped nodes.

This service is implemented using twisted.
It seems that twisted does not support endpoints for multicast and UDP protocols, so we shall have to build our own.
As I write this, I have not found where IPV6 is yet supported for multicast, so again, we shall ha e to do it ourselves.


This Module:
    Uses IPv4 multicast to discover the other PyHouse nodes in the local network
    Uses IPv6 multicast to discover nodes and overrides IPv4 contact info.
    Uses neighbor discovery to find other potential devices that may play a part in home automation.

TODO: Mark Inactive nodes that have gone away.
      Check for new nodes periodically.
      Inform domain module that something happened.
"""

#  Import system type stuff
from twisted.application import service
from twisted.internet.protocol import DatagramProtocol, ConnectedDatagramProtocol

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.NodeDiscovery  ')



"""
IPv6 first 16bit meaning:
FF01::        Interface-local scope
FF02::        Link-Local scope
FF03::        Realm-Local scope
FF04::        Admin-Local scope
FF05::        Site-Local scope
FF08::        Organization-Local scope
FF0E::        Global scope
"""
PYHOUSE_MULTICAST_IP_V4 = '234.35.36.37'
PYHOUSE_MULTICAST_IP_V6 = 'ff05::35:3637'

PYHOUSE_DISCOVERY_PORT = 8582
WHOS_THERE = "Who's There?"  #  Query
I_AM = "I am."  #  Response
MAX_TTL = 4  #  keep mostly local



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
            #  LOG.info("Update our node (slot 0) address to {}".format(p_address[0]))

    def _create_node(self, p_datagram, p_address, p_pyhouse_obj):
        l_node = NodeUtil().initialize_node(p_address[0], None)
        l_node.Name = p_datagram.split(' ')[-1]
        l_node.Active = True
        l_node.UUID = ''
        self._save_node_info(l_node, p_pyhouse_obj)

    def _append_address(self, p_address):
        if p_address[0] not in self.m_address_list:
            self.m_address_list.append(p_address[0])

    def send_query(self, p_transport, p_address):
        """
        Client will send out a "WHOS_THERE" query.
        This will find out all nodes that are subscribed to the PyHouse discovery multicast address.
        """
        LOG.info("Sent WHOS_THERE to {}".format(p_address[0]))
        p_transport.write(WHOS_THERE, (p_address, PYHOUSE_DISCOVERY_PORT))

    def send_response(self, p_transport, p_address, p_pyhouse_obj):
        """
        Server will send a message out in response to a "WHOS_THERE" query.
        """
        LOG.info('Send I_AM Response to {}'.format(p_transport.getHost()))
        self.set_node_0_addr(p_address, p_pyhouse_obj)
        l_str = I_AM + ' ' + p_pyhouse_obj.Computer.Name
        p_transport.write(l_str, p_address)

    def setup_multicast(self, p_transport, p_address):
        p_transport.setTTL(MAX_TTL)
        p_transport.joinGroup(p_address)
        l_interface = p_transport.getOutgoingInterface()
        return l_interface



class ServerProtocolV4(DatagramProtocol):
    """
    Listen for PyHouse nodes and respond to them.
    We should get a packet from ourself and also packets from other nodes that are running.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def startProtocol(self):
        """Called after protocol has started listening."""
        self.m_interface = DGramUtil().setup_multicast(self.transport, PYHOUSE_MULTICAST_IP_V4)
        LOG.info('Discovery Server Protocol started. {}'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        """
        @type  p_datagram: C{str}
        @param p_datagram: is the contents of the datagram.

        @type  p_address: C{tupple) (IpAddr, port)
        @param p_address: is the (IpAddr, Port) of the sender of this datagram (reply to address).
        """
        LOG.info("Discovery Server rxed: {0:} from: {1:}".format(repr(p_datagram), p_address[0]))
        DGramUtil()._append_address(p_address)
        if p_datagram.startswith(WHOS_THERE):
            DGramUtil().send_response(self.transport, p_address, self.m_pyhouse_obj)
        elif p_datagram.startswith(I_AM):
            DGramUtil()._create_node(p_datagram, p_address, self.m_pyhouse_obj)



class ClientProtocolV4(ConnectedDatagramProtocol):
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
        self.m_interface = DGramUtil().setup_multicast(self.transport, PYHOUSE_MULTICAST_IP_V4)
        DGramUtil().send_query(self.transport, PYHOUSE_MULTICAST_IP_V4)
        LOG.info('Discovery Client Protocol started  {}.'.format(self.m_interface))

    def datagramReceived(self, p_datagram, p_address):
        """
        The client only rxes WHOS_THERE
        """
        NodeUtil().initialize_node(p_address[0], None)
        LOG.info('Discovery Client rxed: {0:} From: {1:}'.format(p_datagram, p_address[0]))
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
        l_port = p_pyhouse_obj.Twisted.Reactor.listenMulticast(
                    PYHOUSE_DISCOVERY_PORT,
                    ServerProtocolV4(p_pyhouse_obj),
                    listenMultiple = True)
        LOG.info('Started Server {}'.format(l_port))
        return l_port

    def _start_discovery_client(self, p_pyhouse_obj):
        l_port = p_pyhouse_obj.Twisted.Reactor.listenMulticast(
                    PYHOUSE_DISCOVERY_PORT,
                    ClientProtocolV4(p_pyhouse_obj),
                    listenMultiple = True)
        LOG.info('Started Client {}'.format(l_port))
        return l_port

    def start_node_discovery_service(self, p_pyhouse_obj):
        p_pyhouse_obj.Services.NodeDiscoveryService.startService()
        self._start_discovery_server(p_pyhouse_obj)
        self._start_discovery_client(p_pyhouse_obj)

    def stop_node_discovery_service(self, p_pyhouse_obj):
        p_pyhouse_obj.Services.NodeDiscoveryService.stopService()

    def create_discovery_service(self, p_pyhouse_obj):
        """
        """
        LOG.info('Create Discovery Service')
        try:
            p_pyhouse_obj.Services.NodeDiscoveryService = service.Service()
            p_pyhouse_obj.Services.NodeDiscoveryService.setName('NodeDiscovery')
            p_pyhouse_obj.Services.NodeDiscoveryService.setServiceParent(p_pyhouse_obj.Twisted.Application)
        except RuntimeError:
            LOG.info('Service already installed.')
        self.m_service_installed = True



class API(Utility):
    """
    Initiate and stop this service
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        self.m_pyhouse_obj = self.m_pyhouse_obj
        self.create_discovery_service(self.m_pyhouse_obj)
        self.start_node_discovery_service(self.m_pyhouse_obj)

    def Stop(self):
        self.stop_node_discovery_service(self.m_pyhouse_obj)

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml

__all__ = [
           'API']

#  ## END DBK
