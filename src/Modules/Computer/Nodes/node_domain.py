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
from twisted.protocols.amp import AMP, Command, CommandLocator, Integer, String, AmpList
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 5
LOG = Logger.getLogger('PyHouse.NodeDomain  ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581

def PrintBox(p_arg):
    l_ret = ''
    l_arg = p_arg
    while len(l_arg) > 2:
        l_len = ord(l_arg[0]) * 256 + ord(l_arg[1])
        l_ret += "({0:}){1:}, ".format(l_len, l_arg[2:l_len + 2])
        l_arg = l_arg[l_len + 2:]
    return l_ret


""" ------------------------------------------------------------------
 Command exceptions
"""
class NodeInformationError(Exception): pass
class UsernameUnavailable(Exception): pass
class IrPacketError(Exception): pass

""" ------------------------------------------------------------------
 Commands and Responders
"""

class NodeInformationCommand(Command):
    commandName = 'NodeInformationCommand'
    arguments = [('Name', String()),
                 ('Active', String(optional = True)),
                 ('Address', String(optional = True)),
                 ('NodeRole', Integer(optional = True)),
                 ('UUID', String(optional = True))
                 ]
    response = [('Name', String()),
                ('Answer', String(optional = True))
                ]
    errors = {NodeInformationError: 'Name error'}


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


class MessageProcessing(AMP):
    """
    Process message we receive from different nodes.
    """

    def process_node_info(self, p_box, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        l_ret = None
        if p_box['_command'] == 'NodeInformationCommand':
            l_ret = self.update_NodeInformation(p_box)
        else:
            LOG.error('ERROR - Invalid box received - {0:}'.format(p_box))
        return l_ret

    def update_NodeInformation(self, p_box):
        """
        """
        for _k_key, l_node in self.m_pyhouse_obj.Computer.Nodes.iteritems():
            if l_node.Name == p_box['Name']:
                l_node.Role = p_box['NodeRole']
                l_node.UUID = p_box['UUID']
                l_node.Active = p_box['Active']
                LOG.info('Node {0:} updated'.format(l_node.Key))
        l_ret = dict(Name = 'abc', Answer = 'Yes')
        return l_ret


class AmpLocator(CommandLocator):
    """
    """

    @NodeInformationCommand.responder
    def receive_NodeInformation(self, p_box):
        """
        The responder expects to be called with a serialized box.
        It will then
            deserialize it,
            dispatch the objects to application code,
            take the object the application code returns,
            serialize it,
            and then return that serialized form.
        """
        if g_debug >= 1:
            LOG.debug('Dispatch - receive_NodeInformation() - RECEIVED  Name=:{0:}'.format(p_box))
        l_ret = dict(Name = 'AAA', Answer = 'Got it ok')
        return l_ret


class AmpBoxReceiver(AMP):
    """
    """


class DomainAmp(AMP):
    """
    Protocol

    AMP is a subclass of (BinaryBoxProtocol, BoxDispatcher, CommandLocator, SimpleStringLocator)
    """
    locator = AmpLocator()
    boxReceiver = AmpBoxReceiver()

    def __init__(self, p_pyhouse_obj):
        """ Override
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        super(DomainAmp, self).__init__()
        self.m_transport = None

    def makeConnection(self, p_transport):
        """ Override
        315
        Emit a helpful log message when the connection is made.
        Required to be here - passes back the transport.
        """
        self.m_transport = p_transport
        return AMP.makeConnection(self, p_transport)

    def connectionLost(self, p_reason):
        """ Override
        320
        Clean up the connection.
        """
        LOG.debug('==320== Connection Lost - Reason: {0:}'.format(p_reason))
        self.m_transport = None

    def dataReceived(self, data):
        """ Override
        325
        Either parse incoming data as AmpBoxes or relay it to our nested protocol.
        """
        return AMP.dataReceived(self, data)

    def connectionMade(self):
        """
        330
        Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        l_host = self.transport.getPeer().host
        LOG.info('Server received a connection from {0:}'.format(l_host))

    def startReceivingBoxes(self, p_boxSender):
        """ Override
        335
        The given boxSender is going to start calling boxReceived on this BoxDispatcher.

        @param boxSender: The L{IBoxSender} to send command responses to.
        """
        self.boxSender = p_boxSender

    def ampBoxReceived(self, p_box):
        """ Override
        An AmpBox was received, representing a command, or an answer to a previously issued command (either successful or erroneous).
        Respond to it according to its contents.

        _ask #      : Initial box
        _error #    : error response
        """
        if g_debug >= 1:
            LOG.debug('Dispatch - BoxReceived(Box)\n\t{0:}'.format(p_box))
        l_ret = MessageProcessing().process_node_info(p_box, self.m_pyhouse_obj)
        return l_ret

    def stopReceivingBoxes(self, p_reason):
        """ Override
        No further boxes will be received here. Terminate all currently oustanding command deferreds with the given reason.
        """
        if g_debug >= 1:
            LOG.debug('Dispatch - StopReceivingBoxes(Reason)')
            LOG.debug('        Reason: {0:}'.format(p_reason))
        self.boxSender = None

    def response_NodeOnfo(self):
        """
        """
        LOG.debug('Dispatch - received  remote server.')
        l_ret = dict(Name = 'abc', Answer = 'Yes')
        return l_ret

    def sendBox(self, p_box):
        """ Override
        """
        LOG.info('SendBox {0:}'.format(p_box))
        AMP.sendBox(self, p_box)


class AmpServerFactory(ServerFactory):
    """
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj

    def buildProtocol(self, _p_address_tupple):
        l_protocol = DomainAmp(self.m_pyhouse_obj)
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

    def _send_NodeInfo_box(self, p_node, p_protocol):
        """
        Take the node information about this node - build a box and send it.
        Wait for Success or Failure.
        """
        LOG.info('Composing node info box.')
        l_defer = p_protocol.callRemote(
                    NodeInformationCommand,
                    Name = p_node.Name,
                    Active = str(p_node.Active),
                    Address = p_node.ConnectionAddr_IPv4,
                    NodeRole = int(p_node.NodeRole),
                    UUID = "01234567-1234-2345-3456-01234567890ab"
                    )
        return l_defer

    def send_node_information(self, p_protocol):
        """
        Send our local node information to another node in our node list.

        @param p_protocol: is an AMP instance
        """

        def cb_send_node_information(p_arg):
            LOG.info('Sent node info OK - {0:}<<'.format(p_arg))
            return p_arg

        def eb_send_node_information(p_reason):
            LOG.error('ERROR - Send_node_information failed - {0:}'.format(p_reason))

        pass
        l_host = p_protocol.transport.getPeer().host
        LOG.info('send_node_info to {0:}'.format(l_host))
        l_defer = self._send_NodeInfo_box(self.m_pyhouse_obj.Computer.Nodes[0], p_protocol)
        l_defer.addCallback(cb_send_node_information)
        l_defer.addErrback(eb_send_node_information)

    def create_one_client(self, p_pyhouses_obj, p_address):
        """
        Create a client to talk to some node's servers.
        @param p_address: is the address of the server we are connecting to.
        """
        def cb_create_one_client(p_protocol):
            # l_peer = p_protocol.transport.getPeer()
            # LOG.info('Sending Node information to {0:}'.format(self._print_peer_ip_address(l_peer)))
            l_ret = self.send_node_information(p_protocol)
            return l_ret

        def eb_create_one_client(p_reason):
            LOG.error('ERROR - Failed to create a client to send to another node.  {0:}'.format(p_reason))

        self.m_pyhouse_obj = p_pyhouses_obj
        self.m_address = p_address
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Twisted.Reactor, p_address, AMP_PORT)
        l_defer = l_endpoint.connect(ClientFactory.forProtocol(AMP))
        # LOG.info('CreateOneClient starting - Defer {0:}'.format(l_defer))
        l_defer.addCallback(cb_create_one_client)
        l_defer.addErrback(eb_create_one_client)

    def start_sending_to_all_clients(self, _ignore):
        """
        This runs every 2 hours.
        Loop thru all the nodes we know about.  Start a client for each node except ourself (Nodes[0]).
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(2 * 60 * 60, self.start_sending_to_all_clients, None)
        for l_key, l_node in self.m_pyhouse_obj.Computer.Nodes.iteritems():
            if l_key > -1:  # Skip ourself
                self.create_one_client(self.m_pyhouse_obj, l_node.ConnectionAddr_IPv4)


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
            LOG.info('Domain Server is now Listening.')
            self.m_pyhouse_obj.Twisted.Reactor.callLater(5, self.start_sending_to_all_clients, None)

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
    class 700
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, run_delay = 15):
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
