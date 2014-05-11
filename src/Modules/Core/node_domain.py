"""
-*- test-case-name: PyHouse.Modules.Core.test.test_node_domain -*-

@name: PyHouse/Modules/Core/node_domain.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Apr 3, 2014
@license: MIT License
@summary: This module is for AMP request/response protocol

This Module is the hub of a domain communication system.
Each node will have a server listening for AMP boxes on the AMP_PORT.
It starts a server and uses the AMP protocol to communicate with all the known nodes.

There is no central node so each node needs to talk with all other nodes.
"""

# Import system type stuff
from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.protocols.amp import AMP, Integer, Unicode, String, Command, CommandLocator, BinaryBoxProtocol  # , BoxDispatcher
# from twisted.protocols.amp import IBoxReceiver
from twisted.python.filepath import FilePath
# from zope.interface import implements
from twisted.internet.defer import Deferred

# Import PyMh files and modules.
from Modules.utils import pyh_log

g_debug = 0
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
 Command exceptions
"""
class NodeInformationError(Exception): pass
class UsernameUnavailable(Exception): pass
class IrPacketError(Exception): pass


""" ------------------------------------------------------------------
 Commands
"""
class InvalidCommand(Command):
    """
    An example of an invalid command.  everything is massing.
    """


class NodeInformationCommand(Command):
    commandName = 'NodeInformationCommand'
    arguments = [('Name', String()),
                 ('Active', String(optional = True)),
                 ('Address', String(optional = True)),
                 ('Role', Integer(optional = True)),
                 ('UUID', String(optional = True))
                 ]
    response = [('Name', String()),
                ('Answer', String(optional = True))
                ]
    # errors = {NodeInformationError: 'Name error'}


class IrPacketCommand(Command):
    arguments = [('Key', String()),
                 ('Module', String()),
                 ('Command', String())
                 ]
    response = [('Answer', String())
                ]
    errors = {IrPacketError: 'Ir Packet error.'}


class RegisterUser(Command):
    arguments = [('username', Unicode()),
                  ('publickey', String())]
    response = [('uid', Integer())]
    errors = {UsernameUnavailable: 'username-unavailable'}


### -----------------------------------------------------------------

class LocatorClass(CommandLocator):

    uidCounter = 0
    @RegisterUser.responder
    def register(self, username, publickey):
        path = FilePath(username)
        if path.exists():
            raise UsernameUnavailable()
        self.uidCounter += 1
        path.setContent('%d %s\n' % (self.uidCounter, publickey))
        return self.uidCounter

    @IrPacketCommand.responder
    def ir_packet_response(self, _Key, _Module, _Command):
        return {'Answer': 'Ir packet dbk'}

### -----------------------------------------------------------------
# Boxes

class DomainBoxDispatcher(AMP):
    # implements (IBoxReceiver)

    def __init__(self, p_pyhouses_obj):
        """
        @param p_address: is a 3-tupple (AddressFamily, IPv4Addr, Port)
        """
        AMP.__init__(self)
        self.m_pyhouses_obj = p_pyhouses_obj
        self.m_amp = self
        if g_debug >= 1:
            LOG.debug(' Dispatch - initialized. (127)')

    def makeConnection(self, p_transport):
        if g_debug >= 1:
            LOG.debug(' Dispatch - makeConnection - transport:{0:} (131)'.format(p_transport))
        AMP.makeConnection(self, p_transport)

    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            LOG.debug(' Dispatch - connectionMade (142)')
        pass

    def startReceivingBoxes(self, p_boxSender):
        if g_debug >= 1:
            LOG.debug(' Dispatch - Start Receiving boxes - Sender:{0:} (147)'.format(p_boxSender))
        self.boxSender = p_boxSender

    def ampBoxReceived(self, p_box):
        if g_debug >= 1:
            LOG.debug(' Dispatch - Received box - Box:{0:} (152)'.format(p_box))
        self.boxSender.sendBox(p_box)

    def stopReceivingBoxes(self, p_reason):
        if g_debug >= 1:
            LOG.debug(' Dispatch - Stop Receiving boxes - {0:} (157)'.format(p_reason))
        self.boxSender = None

    def send_NodeInformation(self, p_node):
        """For some reason, this gives a error 'NoneType' object has no attribute 'sendBox'
        The information is sent somehow.
        """
        l_call = self.boxReceiver
        if g_debug >= 1:
            LOG.debug(' Dispatch - send_NodeInformation  l_call = {0:} (167)'.format(l_call))
            LOG.debug('    self = {0:}\n'.format(vars(self)))
        try:
            l_defer = l_call.callRemote(NodeInformationCommand, Name = p_node.Name, Active = str(p_node.Active),
                    Address = p_node.ConnectionAddr_IPv4, Role = int(p_node.Role))
            if g_debug >= 1:
                # LOG.debug(' Dispatch - send_NodeInformation  - SENT to {0:} (171)'.format(self.m_address))
                pass
        except AttributeError as l_error:
            LOG.error(' Dispatch - send_NodeInformation - Attribute error:"{0:}" (173)'.format(l_error))
            l_defer = Deferred()
        return l_defer

    def receive_NodeInformation(self, NodeInformationCommand, Name = None, Active = None, Address = None, Role = None):
        if g_debug >= 1:
            LOG.debug(' Dispatch - receive_NodeInformation  - RECEIVED (179)')
        for l_node in self.m_pyhouses_obj.Nodes.itervalues():
            if l_node.Name == Name:
                pass
        _l_result = dict(Name = Name, Active = Active, Address = Address, Role = Role)
        l_ret = dict(Name = Name, Answer = 'Got it ok')
        return l_ret
    NodeInformationCommand.responder(receive_NodeInformation)

    def update_NodeInformation(self, _p_box):
        if g_debug >= 1:
            LOG.debug(' Dispatch - update_NodeInformation (190)')
        pass

### -----------------------------------------------------------------

class AmpClientProtocol(DomainBoxDispatcher):

    def __init__(self, p_address, p_pyhouses_obj):
        # AMP.__init__(self, boxReceiver = DomainBoxDispatcher(p_pyhouses_obj, p_address), locator = LocatorClass())
        self.m_address = p_address
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            LOG.debug('ClientProtocol - initialized. {0:} (182)'.format(p_address))
        pass


    def makeConnection(self, transport):
        '''placed here to kill strange error messages - twisted swallowing traces AGAIN ???
        '''
        if g_debug >= 2:
            LOG.debug('ClientProtocol - makeConnection - ???? transport:{0:}'.format(transport))
        pass

    def dataReceived(self, p_data):
        """Somehow, encoded data is arriving here.
        """
        if g_debug >= 1:
            LOG.debug('ClientProtocol - DataReceived {0:} (196)'.format(PrintBox(p_data)))
        # self.parseResponse()

    def connectionMade(self):

        def cb_got_result12(p_result):
            if g_debug >= 2:
                LOG.debug('ClientProtocol - ConnectionMade - cb_got_result Client Addr:{0:} - Result:{1:}  transport{2:} (203)'.format(self.m_address, p_result, self.transport))
            LocatorClass().NodeInformationResponse('test dbk')

        def eb_err12(p_ConnectionDone):
            LOG.error('ClientProtocol - ConnectionMade - eb_err2 - Addr:{0:} - arg:{1:}'.format(self.m_address, p_ConnectionDone))

        if g_debug >= 1:
            LOG.debug('ClientProtocol - ConnectionMade to:{0:}, transp:{1:} (219)'.format(self.m_address, self.transport))
        l_defer12 = self.send_NodeInformation(self.m_pyhouses_obj.Nodes[0], self.protocol)
        l_defer12.addCallback(cb_got_result12)
        l_defer12.addErrback(eb_err12)

    def connectionLost(self, p_reason):
        LOG.error('ClientProtocol - ConnectionLost {0:} (216)'.format(p_reason))


class AmpClientFactory(ClientFactory):
    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 3:
            LOG.debug('AmpClientFactory() __init__ (223).')

    def startedConnecting(self, p_connector):
        if g_debug >= 2:
            LOG.debug("DomainClientFactory - StartedConnecting {0:}".format(p_connector))

    def buildProtocol(self, p_address):
        if g_debug >= 2:
            LOG.debug("DomainClientFactory - BuildProtocol {0:}".format(p_address))
        return AmpClientProtocol(p_address, self.m_pyhouses_obj)

    def clientConnectionLost(self, _p_connector, p_reason):
        LOG.error('DomainClientFactory - Lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _p_connector, p_reason):
        LOG.error('DomainClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def client_connect(self, p_pyhouses_obj, p_address):
        """Connect to a server.

        @return: A deferred fired when the connection is complete.
        @rtype: deferred
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory(p_pyhouses_obj)
        l_connect_defer = l_endpoint.connect(l_factory)
        if g_debug >= 2:
            LOG.debug("Domain Client connecting to server at address {0:} - Defer:{1:} (253).".format(p_address, l_connect_defer))
        return l_connect_defer

    def create_client(self, p_pyhouses_obj, p_address):
        """
        Create a client to talk to other node's servers.
        """
        def cb_connected_l1(p_protocol):

            def cb_got_result_l2(p_result):
                LOG.debug('cb_got_result Client Addr:{0:} - Result:{1:} (272).'.format(p_address, p_result))
                LocatorClass().NodeInformationResponse('test dbk')

            def eb_err_l2(p_ConnectionDone):
                LOG.error('eb_err_l2 - Addr:{0:} - arg:{1:} (276).'.format(p_address, p_ConnectionDone))

            def eb_timeout(_p_reason):
                LOG.error('eb_timeout (292)')

            if g_debug >= 1:
                LOG.debug('Client - cb_connected_l1 - Protocol:{0:} (296).'.format(p_protocol))
            l_nodes = self.m_pyhouses_obj.Nodes[0]
            l_defer12 = self.send_NodeInformation(l_nodes)
            l_defer12.setTimeout(30, eb_timeout)
            print('300')
            if g_debug >= 1:
                LOG.debug('Domain Client has connected to Server at addr {0:} - Sending Node Information (302).'.format(p_address))
            l_defer12.addCallback(cb_got_result_l2)
            l_defer12.addErrback(eb_err_l2)

        def cb_result_l1(p_result):
            """
            p_result is always none here.  The next message I get is ClientProtocol - DataReceived
            """
            l_result = p_pyhouses_obj.Nodes[0].Name
            if g_debug >= 1:
                LOG.debug('cb_result_l1 - Client returning result from Server at Addr:{0:}, Result:{1:} (292).'.format(p_address, p_result))
            LocatorClass().NodeInformationResponse(l_result)

        def eb_create_l1(p_result):
            p_result.trap(NodeInformationError)
            LOG.error('eb_create_l1 - Client got error Addr:{0:}, Result:{1:} (297).'.format(p_address, p_result))

        l_defer_l0 = self.client_connect(p_pyhouses_obj, p_address)
        if g_debug >= 2:
            LOG.debug('CreateClient (322).')
        l_defer_l0.addCallback(cb_connected_l1)
        l_defer_l0.addCallback(cb_result_l1)
        l_defer_l0.addErrback(eb_create_l1)


class AmpServerProtocol(DomainBoxDispatcher):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.

    When BinaryBoxProtocol is connected to a transport, it calls startReceivingBoxes on its IBoxReceiver with itself
         as the IBoxSender parameter.
    """
    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        l_disp = DomainBoxDispatcher(p_pyhouses_obj)
        AMP.__init__(self, boxReceiver = l_disp)
        l_proto = BinaryBoxProtocol(self)
        if g_debug >= 1:
            LOG.debug('  ServerProtocol() initialized (341)')
            LOG.debug('      Proto:{0:}'.format(l_disp))
            LOG.debug('      Dispatch:{0:}'.format(l_disp))
        self.locate_responder(NodeInformationCommand)

    def dataReceived(self, p_data):
        if g_debug >= 1:
            LOG.debug('  ServerProtocol data rxed {0:} (348)'.format(PrintBox(p_data)))

    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        def cb_got_result12(p_result):
            if g_debug >= 1:
                LOG.debug('ServerProtocol - ConnectionMade - cb_got_result Client Addr:{0:} - Result:{1:}  transport{2:}'.format(self.m_address, p_result, self.transport))
                ().NodeInformationResponse('test dbk')

        def eb_err12(p_ConnectionDone):
            LOG.error('ServerProtocol - ConnectionMade - eb_err2 - Addr:{0:} - arg:{1:}'.format(self.m_address, p_ConnectionDone))

        if g_debug >= 1:
            LOG.debug('ServerProtocol - ConnectionMade (368)')
            # LOG.debug('    self = {0:}\n'.format(vars(self)))
        l_defer12 = self.locator.send_NodeInformation(self.m_pyhouses_obj.Nodes[0])
        l_defer12.addCallback(cb_got_result12)
        l_defer12.addErrback(eb_err12)

    def connectionLost(self, p_reason):
        if g_debug >= 1:
            LOG.debug('  ServerProtocol connection lost {0:}'.format(p_reason))

    def locate_responder(self, p_name):
        if g_debug >= 2:
            LOG.debug('  ServerProtocol locate_responder = {0:} (344)'.format(p_name))


class AmpServerFactory(ServerFactory):
    """
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 3:
            LOG.debug('  ServerFactory() __init__.')

    def buildProtocol(self, p_address_tupple):
        if g_debug >= 2:
            LOG.debug('  ServerFactory - BuildProtocol from {0:}'.format(p_address_tupple))
        return AmpServerProtocol(self.m_pyhouses_obj)


class AmpServer(object):
    """Sit and listen for amp messages from other nodes.
    """

    def create_domain_server(self, p_endpoint, p_pyhouses_obj):
        l_listen_defer = p_endpoint.listen(AmpServerFactory(p_pyhouses_obj))
        if g_debug >= 2:
            LOG.info("  Server started (352).")
        return l_listen_defer


class Utility(AmpServer, AmpClient):
    m_pyhouses_obj = None

    def create_domain_service(self, p_pyhouses_obj, p_service):
        p_pyhouses_obj.CoreServicesData.DomainService = p_service
        p_pyhouses_obj.CoreServicesData.DomainService.setName('Domain')
        p_pyhouses_obj.CoreServicesData.DomainService.setServiceParent(p_pyhouses_obj.Application)

    def start_amp(self, p_pyhouses_obj):
        """
        Try to avoid missing events due to congestion when a power outage has all nodes rebooting at nearly the same timer.
        This delay should help ensure that the nodes are all up and functioning before starting AMP.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.Reactor.callLater(15, self.start_amp_server)

    def stop_amp(self):
        pass

    def start_amp_server(self):
        """Start the domain server to listen for all incoming requests.
        For all the nodes we know about, create a client and send a message with our info.
        If the request times out, mark the node as non active.
        """
        def cb_client_loop(_ignore):
            """
            @param _ignore: node_domain.AmpServerFactory on 8581
            @type _ignore: class 'twisted.internet.tcp.Port'
            """
            l_nodes = self.m_pyhouses_obj.Nodes
            for l_key, l_node in l_nodes.iteritems():
                if l_key > -99:  # Skip ourself
                    self.create_client(self.m_pyhouses_obj, l_node.ConnectionAddr_IPv4)

        def eb_client_loop(p_reason):
            LOG.error('Creating client - {0:}.'.format(p_reason))

        l_endpoint = serverFromString(self.m_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory(self.m_pyhouses_obj)
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        self.create_domain_service(self.m_pyhouses_obj, l_service)
        #
        l_defer1 = self.create_domain_server(l_endpoint, self.m_pyhouses_obj)
        l_defer1.addCallback(cb_client_loop)
        l_defer1.addErrback(eb_client_loop)
        if g_debug >= 1:
            LOG.debug('  Server has started. (433)\n')


class API(Utility):

    def __init__(self):
        if g_debug >= 2:
            LOG.info("Initialized.")
        pass

    def Start(self, p_pyhouses_obj):
        self.start_amp(p_pyhouses_obj)
        if g_debug >= 0:
            LOG.info("Started.")

    def Stop(self, _p_xml):
        if g_debug >= 2:
            LOG.info("Stopped.")
        self.stop_amp()

# ## END DBK
