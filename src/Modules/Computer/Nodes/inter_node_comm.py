"""
@name:      PyHouse/src/Modules/Computer/Nodes/inter_node_comm.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 20, 2014
@Summary:   Internode communications subsystem.

This is the communication system that allows nodes to share information/
Things like configuration information, Node lists and role information are passed around using this module.
Events such as IR signals received are passed.

Each node starts a server nad listens for incoming AMP boxes.
  An ACK type response is sent back to the originator for the AMP message received.
  The information on the local node is updated.

"""

# Import system type stuff
from twisted.protocols import amp
from twisted.protocols.amp import AMP, Command, Integer, String, Boolean, AmpList
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, RoomData
from Modules.Computer import logging_pyh as Logger


LOG = Logger.getLogger('PyHouse.Inter-NodeComm ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581
INITIAL_DELAY = 10
REPEAT_DELAY = 2 * 60 * 60


""" ------------------------------------------------------------------
 Command exceptions
"""

class NodeInfoError(Exception): pass
class UsernameUnavailable(Exception): pass
class IrPacketError(Exception): pass

""" ------------------------------------------------------------------
 Commands
"""

class NodeInfo(Command):
    arguments = [
        ('Name', String()),
        ('Active', String(optional = True)),
        ('AddressV4', String(optional = True)),
        ('AddressV6', String(optional = True)),
        ('NodeRole', Integer(optional = True)),
        ('UUID', String(optional = True))
        ]
    response = [
        ('AckId', String()),
        ('Name', String()),
        ('From', String(optional = True)),
        ('NodeId', Integer(optional = True))
        ]
    errors = {NodeInfoError: 'Node Info error'}


class GetNodeList(Command):
    """ Get a list of all the nodes.
    """
    arguments = [('length', Integer())]
    response = [('Nodes', AmpList([('x', String())]))]


class SendNodeList(Command):
    """ Send a list of all the nodes.
    """
    arguments = [
        ('length', Integer()),
        ('Nodes', AmpList([('x', String())]))
        ]
    response = [('Length', Integer())]



class HouseInfo(Command):
    """ Send the house specific information.
    """
    arguments = [
        ('Name', String()),
        ('Street', String()),
        ('City', String()),
        ('State', String()),
        ('ZipCode', String()),
        ('Phone', String()),
        ('Latitude', String()),
        ('Longitude', String()),
        ('TimeZoneName', String()),

        ('DomainID', String())
        ]


class RoomInfo(Command):
    """ Send all the info for one room.
    """
    arguments = [
        ('Name' , String()),
        ('Active', Boolean()),
        ('UUID', String()),
        ('Comment', String()),
        ('Corner', String()),
        ('Floor', Integer()),
        ('Size', String()),
        ('RoomType', String())
        ]
    response = [
        ('Ack', Integer())
        ]


# ================== Server =======================

class InterNodeProtocol(amp.AMP):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


    @NodeInfo.responder
    def receive_NodeInfo(self, Name, Active, AddressV4, AddressV6, NodeRole, UUID):
        """ Receive an AMP box from some other node and create the response to the command.
        Put the info we just got into our PyHouse Obj.
        """
        l_node = self.create_node_from_response(Name, Active, AddressV4, AddressV6, NodeRole, UUID)
        l_key = self.insert_node(l_node)
        l_response = self.create_NodeInfo_response(l_node, l_key)
        LOG.info('from  address=:{}  Response = {}'.format(AddressV4, l_response))
        return l_response

    def create_node_from_response(self, Name, Active, AddressV4, AddressV6, NodeRole, UUID):
        """Create a filled in node obj.
        Interfaces don't mtter at this point since they are internal to the remote node.
        """
        l_node = NodeData()
        l_node.Name = Name
        l_node.Active = Active
        l_node.ConnectionAddr_IPv4 = AddressV4
        l_node.ConnectionAddr_IPv6 = AddressV6
        l_node.NodeRole = NodeRole
        l_node.UUID = UUID
        return l_node

    def create_room_from_response(self):
        l_room = RoomData
        return l_room

    def insert_node(self, p_node):
        l_len = len(self.m_pyhouse_obj.Computer.Nodes)
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervalues():
            if p_node.Name == l_node.Name:
                l_node.Active = p_node.Active
                l_node.ConnectionAddr_IPv4 = p_node.ConnectionAddr_IPv4
                l_node.ConnectionAddr_IPv6 = p_node.ConnectionAddr_IPv6
                l_node.NodeRole = p_node.NodeRole
                l_node.UUID = p_node.UUID
                return l_node.Key
        p_node.Key = l_len
        self.m_pyhouse_obj.Computer.Nodes[l_len] = p_node
        return l_len


    def create_NodeInfo_response(self, p_node, p_key):
        """
        Create a response we can pass back to the NodeInfo sender.
        """
        l_response = {
            'AckId' : 'NodeInfo',
            'Name' : p_node.Name,
            'From' : self.m_pyhouse_obj.Computer.Nodes[0].Name,
            'NodeId' : p_key}
        return l_response



class AmpServerFactory(ServerFactory):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


    def buildProtocol(self, _p_address_tupple):
        # LOG.info('Server Factory is now building an InterNodeProtocol protocol - Addr: {}'.format(_p_address_tupple))
        l_protocol = InterNodeProtocol(self.m_pyhouse_obj)
        self.protocol = l_protocol
        return l_protocol



class Utility(object):

    def _build_NodeInfo_box(self, p_node, p_protocol):
        """
        Take the node information about this node - build a box and send it.
        """
        l_defer = p_protocol.callRemote(
            NodeInfo,
            Name = p_node.Name,
            Active = str(p_node.Active),
            AddressV4 = p_node.ConnectionAddr_IPv4,
            AddressV6 = p_node.ConnectionAddr_IPv6,
            NodeRole = int(p_node.NodeRole),
            UUID = "01234567-1234-2345-3456-01234567890ab"
            # UUID = "309"
            )
        return l_defer

    def _build_RoomInfo_box(self, p_room, p_protocol):
        l_defer = p_protocol.callRemote(
            RoomInfo,
            Name = p_room.Name,
            Active = p_room.Active,
            UUID = p_room.UUID,
            Comment = p_room.Comment,
            Corner = p_room.Cornar,
            Floor = p_room.Floor,
            Size = p_room.Size,
            RoomType = p_room.RoomType
            )
        return l_defer


    def send_NodeInfo_to_node(self, p_pyhouse_obj, p_address):
        """ Send
        """
        def cb_send_our_info(p_amp_protocol):
            l_defer = self._build_NodeInfo_box(self.m_node, p_amp_protocol)
            LOG.info('Send NodeInfo')
            return l_defer
        def cb_get_info_response(p_result):
            LOG.info('NodeInfo Response {}'.format(p_result))
        def eb_send_our_info(p_message):
            LOG.info('ERROR sending NodeInfo - {}'.format(p_message))
        self.m_node = p_pyhouse_obj.Computer.Nodes[0]
        LOG.info('Sending our NodeInfo to {}'.format(p_address))
        destination = TCP4ClientEndpoint(reactor, p_address, AMP_PORT)
        l_defer = connectProtocol(destination, AMP())
        l_defer.addCallback(cb_send_our_info)
        l_defer.addCallback(cb_get_info_response)
        l_defer.addErrback(eb_send_our_info)


    def _send_NodeInfo_to_all(self, p_pyhouse_obj):
        """
        Loop thru all the nodes we know about (from node_discovery) and send them our node info
        """
        for l_node in p_pyhouse_obj.Computer.Nodes.itervalues():
            self.send_NodeInfo_to_node(p_pyhouse_obj, l_node.ConnectionAddr_IPv4)


    def _send_periodically(self, p_pyhouse_obj):
        """ Periodically, refresh other nodes with our information.
        """
        p_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._send_periodically, p_pyhouse_obj)
        self._send_NodeInfo_to_all(p_pyhouse_obj)


    def _start_amp_server(self, p_pyhouse_obj):
        """
        Start the Internode communivation server to listen for all incoming requests.

        The server stays running for the duration of the PyHouse daemon.
        """
        def cb_start_server(p_port):
            LOG.info('Server listening on port {}.'.format(p_port.getHost()))
        def eb_start_server(p_reason):
            LOG.error('ERROR in starting Server; {}.\n'.format(p_reason))
        self.m_pyhouse_obj = p_pyhouse_obj
        l_endpoint = TCP4ServerEndpoint(p_pyhouse_obj.Twisted.Reactor, AMP_PORT)
        l_defer = l_endpoint.listen(AmpServerFactory(p_pyhouse_obj))
        l_defer.addCallback(cb_start_server)
        l_defer.addErrback(eb_start_server)



class API(Utility):
    """
    Items that are called by other modules
    """

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._start_amp_server(p_pyhouse_obj)
        p_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._send_periodically, p_pyhouse_obj)


    def Stop(self):
        pass

    def SendUpdate(self, p_obj):
        pass

# ## END DBK
