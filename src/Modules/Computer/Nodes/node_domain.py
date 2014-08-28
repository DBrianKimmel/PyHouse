"""
-*- test-case-name: PyHouse.src.Modules.Computer.Nodes.test.test_node_domain -*-

@name: PyHouse/src/Modules/Computer/Nodes/node_domain.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Apr 3, 2014
@license: MIT License
@summary: This module is for AMP request/response protocol

This Module is the hub of a domain communication system.
Each node will have a server listening for AMP boxes on the AMP_PORT.
It starts a server and uses the AMP protocol to communicate with all the known nodes.

There is no central node so each node needs to talk with all other nodes.

What I want to happen on startup:
    Start an instance of an AMP server
    When the server is started and listening:
        Start a client for each node that we discovered (it's domain server should be running).
        Send a NodeInformation box using the client to the server at the connected address.
        Receive a response box back.

"""

# Import system type stuff
from twisted.internet.endpoints import TCP4ClientEndpoint, TCP4ServerEndpoint
from twisted.internet.protocol import ServerFactory, ClientFactory
from twisted.protocols.amp import AMP, Command, Integer, String, AmpList
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

LOG = Logger.getLogger('PyHouse.NodeDomain  ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581


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
    commandName = 'NodeInfo'
    arguments = [('Name', String()),
                 ('Active', String(optional = True)),
                 ('Address', String(optional = True)),
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
    commandName = 'getNodelist'
    arguments = [('length', Integer())]
    response = [('Nodes', AmpList([('x', String())]))]


class SendNodeList(Command):
    """ Send a list of all the nodes.
    """
    commandName = 'getNodelist'
    arguments = [('length', Integer()),
                 ('Nodes', AmpList([('x', String())]))
                 ]
    response = [('Length', Integer())]


class DomainProtocol(AMP):
    """
    AMP is a subclass of (BinaryBoxProtocol, BoxDispatcher, CommandLocator, SimpleStringLocator)
    """
    m_peer_address = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        """ Override
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        super(DomainProtocol, self).__init__()
        self.m_transport = None

    def startReceivingBoxes(self, p_boxSender):
        """ Override
        The given boxSender is going to start calling boxReceived on this BoxDispatcher.

        @param boxSender: The L{IBoxSender} to send command responses to.
        """
        # LOG.info('Start\n')
        self.boxSender = p_boxSender

    def makeConnection(self, p_transport):
        """ Required Override
        Emit a helpful log message when the connection is made.
        Required to be here - passes back the transport.
        """
        self.m_transport = p_transport
        self.m_peer_address = p_transport.getPeer()
        return super(DomainProtocol, self).makeConnection(p_transport)

    def dataReceived(self, data):
        """ Override
        Either parse incoming data as AmpBoxes or relay it to our nested (switched-to) protocol.
        """
        l_box = super(DomainProtocol, self).dataReceived(data)
        if l_box == None:
            return
        LOG.info('Data arrived AmpBox {0:} \n'.format(l_box))
        self.ampBoxReceived(l_box)

    def ampBoxReceived(self, p_box):
        """ Override
        An AmpBox was received, representing a command, or an answer to a previously issued command (either successful or erroneous).
        Respond to it according to its contents.

        _ask #      : Initial box
        _answer #   : Response box
        _error #    : error response
        """
        LOG.info('AmpBox Received from {0:}\n\t{1:}'.format(self.m_peer_address.host, p_box))
        if p_box == None:
            LOG.error('We got a None instead of a box ???')
            return None
        return super(DomainProtocol, self).ampBoxReceived(p_box)

    def connectionLost(self, p_reason):
        """ Override
        Clean up the connection.
        """
        LOG.debug('Connection Lost - Reason: {0:}'.format(p_reason))
        self.m_transport = None

    def stopReceivingBoxes(self, p_reason):
        """ Override
        No further boxes will be received here. Terminate all currently oustanding command deferreds with the given reason.
        """
        LOG.debug('Dispatch - StopReceivingBoxes(Reason)')
        LOG.debug('        Reason: {0:}'.format(p_reason))
        self.boxSender = None

    @NodeInfo.responder
    def receive_NodeInfo(self, Name, Active, Address, NodeRole, UUID):
        """
        """
        l_response = MessageProcessing(self.m_pyhouse_obj).update_NodeInfo(Name, Active, Address, NodeRole, UUID)
        LOG.debug('receive_NodeInfo() - from  address=:{0:}\n\tResponse = {1:}'.format(Address, l_response))
        return l_response


class MessageProcessing(object):
    """
    Process message we receive from different nodes.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def update_NodeInfo(self, Name, Active, Address, NodeRole, UUID):
        """
        Update our PyHouse Nodes information with the data we just got.
        Create a response we can pass back to the sender
        """
        l_key = -1
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervalues():
            if l_node.Name == Name:
                l_node.Active = Active
                l_node.Address = Address
                l_node.Role = NodeRole
                l_node.UUID = UUID
                l_key = int(l_node.Key)
                # LOG.info('Node {0:} updated'.format(l_node.Key))
        l_response = {'Name' : Name,
                      'From' : self.m_pyhouse_obj.Computer.Nodes[0].Name,
                      'NodeId' : l_key}
        # LOG.info('Return response {0:}'.format(l_response))
        return l_response


class AmpServerFactory(ServerFactory):
    """
    Listen for connections.
    When one is made, build a protocol for using that connection.
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj

    def buildProtocol(self, _p_address_tupple):
        # LOG.info('Server Factory is now building a DomainProtocol protocol - Addr: {0:}'.format(_p_address_tupple))
        l_protocol = DomainProtocol(self.m_pyhouse_obj)
        self.protocol = l_protocol
        return l_protocol


class AmpClient(object):
    """
    """

    def _print_peer_ip_address(self, p_address):
        """
        Takes a twisted address structure and returns the IP address portion.
        IPv4Address   .type   .host   .port
        """
        return p_address.host

    def send_NodeInfo_box(self, p_node, p_protocol):
        """
        Take the node information about this node - build a box and send it.
        """
        # l_peer = p_protocol.transport.getPeer().host
        # LOG.info('Composing node info box for {0:} to {1:}.'.format(p_node.Name, l_peer))
        l_defer = p_protocol.callRemote(
                    NodeInfo,
                    Name = p_node.Name,
                    Active = str(p_node.Active),
                    Address = p_node.ConnectionAddr_IPv4,
                    NodeRole = int(p_node.NodeRole),
                    # UUID = "01234567-1234-2345-3456-01234567890ab"
                    UUID = "309"
                    )
        return l_defer

    def send_node_information(self, p_protocol):
        """
        Send our local node information to another node in our node list.

        @param p_protocol: is an AMP instance

        Either the CB or EB will fire !
        """

        def cb_send_node_information(p_arg):
            # LOG.info('Sent node info OK - {0:} \n'.format(p_arg))
            return p_arg

        def eb_send_node_information(p_reason):
            LOG.error('ERROR - Send_node_information failed\n\t{0:}\n'.format(p_reason))

        def bb_send_node_info(_ignore):
            LOG.info('Done sending node info - stop client.')

        l_defer = self.send_NodeInfo_box(self.m_pyhouse_obj.Computer.Nodes[0], p_protocol)
        l_defer.addCallback(cb_send_node_information)
        l_defer.addErrback(eb_send_node_information)
        l_defer.addBoth(bb_send_node_info)

    def update_client_node(self, p_pyhouses_obj, p_address):
        """
        Create a client to talk to some node's servers.
        Send node info
        Close the client
        """
        def cb_update_client_node(p_protocol):
            return self.send_node_information(p_protocol)

        def eb_update_client_node(p_reason):
            LOG.error('ERROR - Failed to create a client to update node \n {0:}'.format(p_reason))

        def bb_close_connection(_ignore):
            # LOG.info('Closing connection to node {0:} - Arg: {1:}'.format(p_address, p_arg))
            pass

        self.m_pyhouse_obj = p_pyhouses_obj
        self.m_address = p_address
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Twisted.Reactor, p_address, AMP_PORT)
        l_defer = l_endpoint.connect(ClientFactory.forProtocol(AMP))
        l_defer.addCallback(cb_update_client_node)
        l_defer.addErrback(eb_update_client_node)
        l_defer.addBoth(bb_close_connection)

    def start_sending_to_all_clients(self, _ignore):
        """
        This runs every 2 hours.
        Loop thru all the nodes we know about.  Start a client for each node except ourself (Nodes[0]).
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(2 * 60 * 60, self.start_sending_to_all_clients, None)
        for l_key, l_node in self.m_pyhouse_obj.Computer.Nodes.iteritems():
            if l_key > -1:  # Skip ourself
                self.update_client_node(self.m_pyhouse_obj, l_node.ConnectionAddr_IPv4)


class Utility(AmpClient):
    """
    """
    m_pyhouse_obj = None

    def start_amp_server(self, p_pyhouse_obj, p_endpoint):
        """
        Start the domain server to listen for all incoming requests.
        Then, for all the nodes we know about, create a client and send a message with our info.
        """
        def cb_start_all_clients(_p_port):
            """
            @param p_port: Modules.Computer.Nodes.node_domain.AmpServerFactory on 8581
            @type p_port: class 'twisted.internet.tcp.Port'
            """
            # LOG.info('Domain Server is now Listening.')
            self.m_pyhouse_obj.Twisted.Reactor.callLater(3, self.start_sending_to_all_clients, None)

        def eb_start_clients_loop(p_reason):
            LOG.error('ERROR in starting Domain Server (NOT Listening) - {0:}.\n'.format(p_reason))

        l_defer = p_endpoint.listen(AmpServerFactory(p_pyhouse_obj))
        l_defer.addCallback(cb_start_all_clients)
        l_defer.addErrback(eb_start_clients_loop)

    def create_amp_service(self, _ignore):
        """
        Create a Message Exchange service that we can stop and restart
        """
        l_endpoint = TCP4ServerEndpoint(self.m_pyhouse_obj.Twisted.Reactor, AMP_PORT)
        l_factory = AmpServerFactory(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Services.NodeDomainService = StreamServerEndpointService(l_endpoint, l_factory)
        self.m_pyhouse_obj.Services.NodeDomainService.setName('NodeDomain')
        self.m_pyhouse_obj.Services.NodeDomainService.setServiceParent(self.m_pyhouse_obj.Twisted.Application)
        self.start_amp_server(self.m_pyhouse_obj, l_endpoint)


class API(Utility):
    """
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, run_delay = 10):
        """
        Try to avoid missing events due to congestion when a power failure has all nodes rebooting at nearly the same time.
        This delay should help ensure that the nodes are all up and functioning before starting AMP.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Twisted.Reactor.callLater(run_delay, self.create_amp_service, None)

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        return p_xml

    def SendMessage(self, p_box, p_node):
        """
        """
        pass

# ## END DBK
