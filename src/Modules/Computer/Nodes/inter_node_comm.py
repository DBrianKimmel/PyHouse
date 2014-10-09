"""
@name: PyHouse/src/Modules/Computer/Nodes/inter_node_comm.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 20, 2014
@Summary:

"""

# Import system type stuff
from twisted.protocols import amp
from twisted.protocols.amp import AMP, Command, Integer, String, AmpList
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny


LOG = Logger.getLogger('PyHouse.InterNodeCom')

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
 Commands and Responders
"""

class NodeInfo(Command):
    arguments = [('Name', String()),
                 ('Active', String(optional = True)),
                 ('AddressV4', String(optional = True)),
                 ('AddressV6', String(optional = True)),
                 ('NodeRole', Integer(optional = True)),
                 ('UUID', String(optional = True))
                 ]
    response = [('Name', String()),
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
    arguments = [('length', Integer()),
                 ('Nodes', AmpList([('x', String())]))
                 ]
    response = [('Length', Integer())]


# ================== Server =======================

class InterNodeProtocol(amp.AMP):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    @NodeInfo.responder
    def receive_NodeInfo(self, Name, Active, AddressV4, AddressV6, NodeRole, UUID):
        l_node = self.create_node_from_response(Name, Active, AddressV4, AddressV6, NodeRole, UUID)
        l_key = self.insert_node(l_node)
        l_response = self.create_response(l_node, l_key)
        # LOG.info('receive_NodeInfo() - from  address=:{}\n\tResponse = {}'.format(AddressV4, l_response))
        # self._dump_nodes()
        return l_response

    def _dump_nodes(self):
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervalues():
            LOG.info('Node: {}  {}'.format(l_node.Name, l_node.ConnectionAddr_IPv4))


    def create_node_from_response(self, Name, Active, AddressV4, AddressV6, NodeRole, UUID):
        l_node = NodeData()
        l_node.Name = Name
        l_node.Active = Active
        l_node.ConnectionAddr_IPv4 = AddressV4
        l_node.ConnectionAddr_IPv6 = AddressV6
        l_node.NodeRole = NodeRole
        l_node.UUID = UUID
        return l_node


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


    def create_response(self, p_node, p_key):
        """
        Update our PyHouse Nodes information with the data we just got.
        Create a response we can pass back to the sender
        """
        l_response = {'Name' : p_node.Name,
                      'From' : self.m_pyhouse_obj.Computer.Nodes[0].Name,
                      'NodeId' : p_key}
        # LOG.info('Return response {0:}'.format(l_response))
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
                    # UUID = "01234567-1234-2345-3456-01234567890ab"
                    UUID = "309"
                    )
        return l_defer


    def send_our_info_to_node(self, p_pyhouse_obj, p_address):

        def cb_send_our_info(p_amp_protocol):
            l_defer = self._build_NodeInfo_box(self.m_node, p_amp_protocol)
            return l_defer

        def cb_get_info_response(p_result):
            LOG.info('Response {}'.format(p_result))

        def eb_send_our_info(p_message):
            LOG.info('ERROR sending info - {}'.format(p_message))

        self.m_node = p_pyhouse_obj.Computer.Nodes[0]
        LOG.info('Sending our node info to {}'.format(p_address))
        destination = TCP4ClientEndpoint(reactor, p_address, AMP_PORT)
        l_defer = connectProtocol(destination, AMP())
        l_defer.addCallback(cb_send_our_info)
        l_defer.addCallback(cb_get_info_response)
        l_defer.addErrback(eb_send_our_info)


    def _start_amp_server(self, p_pyhouse_obj, p_endpoint):
        """
        Start the domain server to listen for all incoming requests.

        The server stays running for the duration of the PyHouse daemon.
        """
        def cb_start_server(p_port):
            # LOG.info('Server listening on port {}.'.format(p_port.getHost()))
            self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._info_loop, self.m_pyhouse_obj)

        def eb_start_server(p_reason):
            LOG.error('ERROR in starting Server; {}.\n'.format(p_reason))

        self.m_pyhouse_obj = p_pyhouse_obj
        l_defer = p_endpoint.listen(AmpServerFactory(p_pyhouse_obj))
        l_defer.addCallback(cb_start_server)
        l_defer.addErrback(eb_start_server)
        return l_defer


    def _create_amp_service(self, p_pyhouse_obj):
        """
        Create a Message Exchange service that we can stop and restart
        """
        l_Listen_endpoint = TCP4ServerEndpoint(p_pyhouse_obj.Twisted.Reactor, AMP_PORT)
        l_factory = AmpServerFactory(p_pyhouse_obj)
        p_pyhouse_obj.Services.InterNodeComm = StreamServerEndpointService(l_Listen_endpoint, l_factory)
        p_pyhouse_obj.Services.InterNodeComm.setName('InterNodeComm')
        p_pyhouse_obj.Services.InterNodeComm.setServiceParent(p_pyhouse_obj.Twisted.Application)
        return l_Listen_endpoint


    def _info_loop(self, p_pyhouse_obj):
        self.m_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._info_loop, p_pyhouse_obj)
        self.send_node_info_to_all(p_pyhouse_obj)



class API(Utility):
    """
    Items that are called by other modules
    """

    def send_node_info_to_all(self, p_pyhouse_obj):
        """
        Loop thru all the nodes we know about (from node_discovery) and send them our node info
        """
        for l_node in p_pyhouse_obj.Computer.Nodes.itervalues():
            self.send_our_info_to_node(p_pyhouse_obj, l_node.ConnectionAddr_IPv4)


    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        l_endpoint = self._create_amp_service(p_pyhouse_obj)
        self._start_amp_server(p_pyhouse_obj, l_endpoint)


    def Stop(self):
        pass

# ## END DBK