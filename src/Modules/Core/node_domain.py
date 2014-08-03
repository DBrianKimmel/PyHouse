"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_node_domain -*-

@name: PyHouse/src/Modules/Core/node_domain.py
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
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny

g_debug = 5
LOG = pyh_log.getLogger('PyHouse.NodeDomain  ')

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
    # errors = {NodeInformationError: 'Name error'}


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


class DomainAmp(AMP):
    """
    AMP is a subclass of (BinaryBoxProtocol, BoxDispatcher, CommandLocator, SimpleStringLocator)
    """

    m_amp = None


    def __init__(self, p_pyhouse_obj):
        """
        @param p_address: is a 3-tupple (AddressFamily, IPv4Addr, Port)
        """
        super(DomainAmp, self).__init__()
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_transport = None
        self.m_amp = self
        if g_debug >= 1:
            LOG.debug('==106== DomainAmp.__init__()')
            LOG.debug('        Repr: {0:}'.format(repr(self)))



    def makeConnection(self, p_transport):
        """ Override
        Emit a helpful log message when the connection is made.
        Required to be here - passes back the transport.
        """
        self.m_transport = p_transport
        if g_debug >= 2:
            LOG.debug('==118== Dispatcher - makeConnection(Transport) to:{0:}'.format(p_transport.getPeer()))
            LOG.debug('        Transport:{0:}'.format(p_transport))
        return AMP.makeConnection(self, p_transport)



    def connectionLost(self, p_reason):
        """ Override
        Clean up the connection.
        """
        self.m_transport = None
        if g_debug >= 1:
            LOG.debug('==129== Dispatcher - connectionLost(Reason)')
            LOG.debug('        ERROR: {0:}\n'.format(p_reason))



    def dataReceived(self, data):
        """ Override
        Either parse incoming data as AmpBoxes or relay it to our nested protocol.
        """
        LOG.debug('==138== Dispatcher - dataReceived(Data) - {0:}'.format(PrintBox(data)))
        return AMP.dataReceived(self, data)

    def connectionMade(self):
        """
        Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            LOG.debug('==150== Dispatcher - connectionMade()')
        pass



    def startReceivingBoxes(self, p_boxSender):
        """ Override
        The given boxSender is going to start calling boxReceived on this BoxDispatcher.

        @param boxSender: The L{IBoxSender} to send command responses to.
        """
        if g_debug >= 1:
            LOG.debug('==160== Dispatch - StartReceivingBoxes(Sender)')
            LOG.debug('        Sender:{0:}'.format(p_boxSender))
        self.boxSender = p_boxSender



    def ampBoxReceived(self, p_box):
        """ Override
        An AmpBox was received, representing a command, or an answer to a previously issued command (either successful or erroneous).
        Respond to it according to its contents.
        """
        if g_debug >= 1:
            LOG.debug('==169== Dispatch - BoxReceived(Box)')
            LOG.debug('        Box:{0:}'.format(p_box))
        self.sendBox(p_box)
        # self.boxSender.sendBox(p_box)



    def stopReceivingBoxes(self, p_reason):
        """ Override
        No further boxes will be received here. Terminate all currently oustanding command deferreds with the given reason.
        """
        if g_debug >= 1:
            LOG.debug('==179== Dispatch - StopReceivingBoxes(Reason)')
            LOG.debug('        Reason: {0:}'.format(p_reason))
        self.boxSender = None



    @NodeInformationCommand.responder
    def receive_NodeInformation(self, Name = None):
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
            LOG.debug('==197== Dispatch - receive_NodeInformation() - RECEIVED')
        _l_box = NodeInformationCommand.makeArguments({'Name': 'AAA'})
        l_ret = dict(Name = Name, Answer = 'Got it ok')
        return l_ret
    # NodeInformationCommand.responder(receive_NodeInformation)



    def update_NodeInformation(self, p_box):
        if g_debug >= 1:
            LOG.debug('==208== Dispatch - update_NodeInformation(Box)')
            LOG.debug('        Box: {0:}'.format(vars(p_box)))
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervals():
            if l_node.Name == p_box.Name:
                l_node.Role = p_box.Role
                l_node.UUID = p_box.UUID
                l_node.Active = p_box.Active



    # @NodeInformationCommand.responder
    def response_NodeOnfo(self):
        LOG.debug('==219== Dispatch - received  remote server.')
        l_ret = dict(Name = 'abc', Answer = 'Yes')
        return l_ret

    def sendBox(self, box):
        """ Override
        """
        AMP.sendBox(self, box)









class AmpServerFactory(ServerFactory):
    """
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouse_obj = p_pyhouses_obj



    def buildProtocol(self, _p_address_tupple):
        # l_protocol = NodeDomainServerProtocol(self.m_pyhouse_obj)
        l_protocol = DomainAmp(self.m_pyhouse_obj)
        self.protocol = l_protocol
        if g_debug >= 4:
            LOG.debug('==246== AmpServerFactory.buildProtocol()')
        return l_protocol


class NodeDomainServerProtocol(DomainAmp):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.

    When BinaryBoxProtocol is connected to a transport, it calls startReceivingBoxes on its IBoxReceiver
    with itself as the IBoxSender parameter.
    """

    def __init__(self, p_pyhouse_obj):
        LOG.debug('==245== NodeDomainServerProtocol()')
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_disp = DomainAmp(p_pyhouse_obj)
        if g_debug >= 1:
            LOG.debug('==249== ServerProtocol() initialized')
            LOG.debug('        Dispatch:{0:}'.format(self.m_disp))



    def _extract_arg(self, p_msg):
        l_len = ord(p_msg[0]) * 256 + ord(p_msg[1])
        l_arg = p_msg[2:l_len + 2]
        l_rest = p_msg[l_len + 2:]
        return l_arg, l_rest



    def _make_dict_from_message(self, p_msg):
        l_dict = {}
        l_rest = p_msg
        while len(l_rest) > 2:
            l_key, l_rest = self._extract_arg(l_rest)
            l_arg, l_rest = self._extract_arg(l_rest)
            l_dict[l_key] = l_arg
        return l_dict



    def dataReceived(self, p_data):
        if g_debug >= 1:
            LOG.debug('==275== ServerProtocol - dataReceived(Data)')
            LOG.debug('        Data rxed: {0:}'.format(PrintBox(p_data)))
        l_dict = self._make_dict_from_message(p_data)
        PrettyPrintAny(l_dict, 'NodeDomain - DataReceived - Dict', 120)



    def cb_got_result12(self, p_result):
        if g_debug >= 1:
            LOG.debug('==284== ServerProtocol - ConnectionMade cb_got_result(Result)')
            LOG.debug('        Client Addr:{0:}'.format(self.m_address))
            LOG.debug('        Result:{0:}'.format(p_result))
            LOG.debug('        Transport{0:}'.format(self.transport))



    def eb_err12(self, p_ConnectionDone):
        LOG.error('==292== ServerProtocol - ConnectionMade eb_G')
        LOG.error('        Address: {0:}'.format(self.m_address))
        LOG.error('        ERROR: {0:}\n'.format(p_ConnectionDone))



    def connectionMade(self):
        """Some client connected to this server.
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            LOG.debug('==306== ServerProtocol - ConnectionMade')
            # LOG.debug('    self = {0:}\n'.format(vars(self)))



""" ------------------------------------------------------------------
 Command exceptions
"""
class NodeInformationError(Exception): pass
class UsernameUnavailable(Exception): pass
class IrPacketError(Exception): pass


class AmpClient(object):



    def cb_sendInfo(self, p_ampProto):
        l_node = self.m_pyhouse_obj.Computer.Nodes[0]
        if g_debug >= 4:
            LOG.debug('==326== Client - sending our node info to remote server.')
            LOG.debug('        Protocol:{0:}   Addr:{1:}'.format(p_ampProto, self.m_address))
        l_ret = p_ampProto.callRemote(NodeInformationCommand,
                        Name = l_node.Name, Active = str(l_node.Active), Address = l_node.ConnectionAddr_IPv4,
                        NodeRole = int(l_node.NodeRole), UUID = "01234567-1234-2345-3456-01234567890ab")
        return l_ret



    def eb_send_info(self, p_reason):
        LOG.warn('WARNING - Failed to create a client to send to another node.  {0:}'.format(p_reason))

    def create_one_client(self, p_pyhouses_obj, p_address):
        """
        Create a client to talk to some node's servers.
        @param p_address: is the address of the server we are connecting to.
        """
        self.m_pyhouse_obj = p_pyhouses_obj
        self.m_address = p_address
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Twisted.Reactor, p_address, AMP_PORT)
        LOG.debug('==346== About to create client to {0:}'.format(p_address))
        l_defer = l_endpoint.connect(ClientFactory.forProtocol(AMP))
        l_defer.addCallback(self.cb_sendInfo)
        l_defer.addErrback(self.eb_send_info)


class Utility(AmpClient):
    m_pyhouse_obj = None

    def cb_start_all_clients(self, _ignore):
        """
        Loop thru all the nodes we know about.  Start a client for each node except ourself (Nodes[0]).

        @param _ignore: node_domain.AmpSe rverFactory on 8581
        @type _ignore: class 'twisted.internet.tcp.Port'
        """
        l_nodes = self.m_pyhouse_obj.Computer.Nodes
        for l_key, l_node in l_nodes.iteritems():
            if l_key > -1:  # Skip ourself
                self.create_one_client(self.m_pyhouse_obj, l_node.ConnectionAddr_IPv4)

    def eb_start_clients_loop(self, p_reason):
        LOG.error('Utility.eb_start_clients_loop().')
        LOG.error('     ERROR Creating client - {0:}.\n'.format(p_reason))

    def start_amp_server(self, p_pyhouse_obj, p_endpoint):
        """
        Start the domain server to listen for all incoming requests.
        Then, for all the nodes we know about, create a client and send a message with our info.
        """
        l_defer = p_endpoint.listen(AmpServerFactory(p_pyhouse_obj))
        l_defer.addCallback(self.cb_start_all_clients)
        l_defer.addErrback(self.eb_start_clients_loop)

    def start_amp_services(self):
        """
        Create a service that we can stop and restart
        """
        l_endpoint = TCP4ServerEndpoint(self.m_pyhouse_obj.Twisted.Reactor, AMP_PORT)
        l_factory = AmpServerFactory(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Services.NodeDomainService = StreamServerEndpointService(l_endpoint, l_factory)
        self.m_pyhouse_obj.Services.NodeDomainService.setName('NodeDomain')
        self.m_pyhouse_obj.Services.NodeDomainService.setServiceParent(self.m_pyhouse_obj.Twisted.Application)
        self.start_amp_server(self.m_pyhouse_obj, l_endpoint)


class API(Utility):

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj, run_delay = 15):
        """
        Try to avoid missing events due to congestion when a power failure has all nodes rebooting at nearly the same time.
        This delay should help ensure that the nodes are all up and functioning before starting AMP.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Twisted.Reactor.callLater(run_delay, self.start_amp_services)

    def Stop(self):
        pass

    def SaveXml(self, _p_xml):
        pass

# ## END DBK
