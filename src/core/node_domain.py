"""
@name: PyHouse/src/core/node_domain.py

Created on Apr 3, 2014

# -*- test-case-name: PyHouse.src.core.test.test_node_domain -*-

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is for AMP request/response protocol

This Module is the hub of a domain communication system.
Each node will have a server listening for AMP boxes on the AMP_PORT.
It starts a server and uses the AMP protocol to communicate with all the known nodes.

There is no central node so each node needs to talk with all other nodes.
"""

# Import system type stuff
import logging
from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint
from twisted.internet.protocol import ClientCreator, ClientFactory, ServerFactory
from twisted.protocols.amp import AMP, Integer, Unicode, String, Command, IBoxReceiver, CommandLocator, BinaryBoxProtocol, BoxDispatcher
from twisted.python.filepath import FilePath
from zope.interface import implements
from twisted.internet.defer import Deferred

g_debug = 1
g_logger = logging.getLogger('PyHouse.NodeDomain  ')

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
class NodeInformationCommand(Command):
    arguments = [('Name', String()),
                 ('Active', String()),
                 ('Address', String()),
                 ('Role', Integer())
                 ]
    response = [('Answer', String())
                ]
    errors = {NodeInformationError: 'Name error'}


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

    @NodeInformationCommand.responder
    def NodeInformationResponse(self, Name, _Active, _Address, _Role):
        if g_debug >= 1:
            g_logger.debug('NodeInformationResponse:{0:}'.format(Name))
        l_answer = Name + '_answer'
        return {'Answer': l_answer}

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
    implements (IBoxReceiver)

    def __init__(self, p_pyhouses_obj, p_address):
        """
        @param p_address: is a 3-tupple (AddressFamily, IPv4Addr, Port)
        """
        self.m_address = p_address
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 1:
            g_logger.debug(' Dispatch - initialized (123)')

    def startReceivingBoxes(self, p_boxSender):
        if g_debug >= 1:
            g_logger.debug(' Dispatch - Start Receiving boxes - Sender:{0:}'.format(p_boxSender))
        self.boxSender = p_boxSender

    def ampBoxReceived(self, p_box):
        if g_debug >= 1:
            g_logger.debug(' Dispatch - Received box - Box:{0:}'.format(p_box))
        self.boxSender.sendBox(p_box)

    def stopReceivingBoxes(self, p_reason):
        if g_debug >= 1:
            g_logger.debug(' Dispatch - Stop Receiving boxes - {0:}'.format(p_reason))
        self.boxSender = None

    def send_NodeInformation(self, p_node):
        if g_debug >= 1:
            g_logger.debug(' Dispatch - SendNodeInformation  Self = {0:} (142)'.format(self))
        try:
            l_defer = self.callRemote(NodeInformationCommand,
                    Name = p_node.Name,
                    Active = str(p_node.Active),
                    Address = p_node.ConnectionAddr,
                    Role = int(p_node.Role))
        except AttributeError as l_error:
            g_logger.error(' Dispatch - SendNodeInfo - Attribute error - {0:}'.format(l_error))
            l_defer = Deferred()
        return l_defer

    @NodeInformationCommand.responder
    def abd(self): pass

### -----------------------------------------------------------------

class AmpClientProtocol(DomainBoxDispatcher):

    def __init__(self, p_address, p_pyhouses_obj):
        self.m_address = p_address
        self.m_pyhouses_obj = p_pyhouses_obj
        AMP.__init__(self, boxReceiver = DomainBoxDispatcher(p_pyhouses_obj, p_address), locator = LocatorClass())
        if g_debug >= 2:
            g_logger.debug('ClientProtocol - initialized. {0:} (161)'.format(p_address))
        pass

    def dataReceived(self, p_data):
        if g_debug >= 1:
            g_logger.debug('ClientProtocol - DataReceived {0:} (166)'.format(PrintBox(p_data)))
        pass

    def connectionMade(self):
        def cb_got_result12(p_result):
            if g_debug >= 1:
                g_logger.debug('ClientProtocol - ConnectionMade - cb_got_result Client Addr:{0:} - Result:{1:}'.format(self.m_address, p_result))
            LocatorClass().NodeInformationResponse('test dbk')
        def eb_err12(p_ConnectionDone):
            g_logger.error('ClientProtocol - ConnectionMade - eb_err2 - Addr:{0:} - arg:{1:}'.format(self.m_address, p_ConnectionDone))

        if g_debug >= 1:
            g_logger.debug('ClientProtocol - ConnectionMade to:{0:} (178)'.format(self.m_address))
        l_defer12 = self.send_NodeInformation(self.m_pyhouses_obj.CoreData.Nodes[0])
        l_defer12.addCallback(cb_got_result12)
        l_defer12.addErrback(eb_err12)

    def connectionLost(self, p_reason):
        g_logger.error('ClientProtocol - ConnectionLost {0:} (184)'.format(p_reason))


class AmpClientFactory(ClientFactory):
    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 3:
            g_logger.debug('AmpClientFactory() __init__ (202).')

    def startedConnecting(self, p_connector):
        if g_debug >= 1:
            g_logger.debug("DomainClientFactory - StartedConnecting {0:}".format(p_connector))

    def buildProtocol(self, p_address):
        if g_debug >= 1:
            g_logger.debug("DomainClientFactory - BuildProtocol {0:}".format(p_address))
        return AmpClientProtocol(p_address, self.m_pyhouses_obj)

    def clientConnectionLost(self, _p_connector, p_reason):
        g_logger.error('DomainClientFactory - Lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _p_connector, p_reason):
        g_logger.error('DomainClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def client_connect(self, p_pyhouses_obj, p_address):
        """Connect to a server.

        @rtype: is a deferred
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory(p_pyhouses_obj)
        if g_debug >= 3:
            g_logger.debug('Created {0:}, {1:}'.format(l_endpoint, l_factory))
        l_connect_defer = l_endpoint.connect(l_factory)
        if g_debug >= 1:
            g_logger.debug("Domain Client connecting to server at address {0:} - Defer:{1:} (234).".format(p_address, l_connect_defer))
        return l_connect_defer

    def create_client(self, p_pyhouses_obj, p_address):
        def cb_connected_l1(p_protocol):
            def cb_got_result_l2(p_result):
                g_logger.debug('cb_got_result Client Addr:{0:} - Result:{1:} (240).'.format(p_address, p_result))
                LocatorClass().NodeInformationResponse('test dbk')

            def eb_err_l2(p_ConnectionDone):
                g_logger.error('eb_err_l2 - Addr:{0:} - arg:{1:} (244).'.format(p_address, p_ConnectionDone))

            if g_debug >= 2:
                g_logger.debug('cb_connected_l1 - Protocol:{0:} (251).'.format(p_protocol))
            l_defer1 = p_protocol.callRemote(
                    NodeInformationCommand,
                    Name = p_pyhouses_obj.CoreData.Nodes[0].Name,
                    Active = str(p_pyhouses_obj.CoreData.Nodes[0].Active),
                    Address = p_pyhouses_obj.CoreData.Nodes[0].ConnectionAddr,
                    Role = p_pyhouses_obj.CoreData.Nodes[0].Role
                    )
            if g_debug >= 1:
                g_logger.debug('Domain Client has connected to Server at addr {0:} - Sending Node Information (255).'.format(p_address))
            l_defer1.addCallback(cb_got_result_l2)
            l_defer1.addErrback(eb_err_l2)

        def cb_result_l1(p_result):
            l_result = p_pyhouses_obj.CoreData.Nodes[0].Name
            if g_debug >= 1:
                g_logger.debug('cb_result_l1 - Client returning result from Server at Addr:{0:}, Result:{1:} (262).'.format(p_address, p_result))
            LocatorClass().NodeInformationResponse(l_result)

        def eb_create_l1(p_result):
            p_result.trap(NodeInformationError)
            g_logger.error('eb_create_l1 - Client got error Addr:{0:}, Result:{1:} (265).'.format(p_address, p_result))

        if g_debug >= 2:
            g_logger.debug('Create_Client to Addr:{0:} (270).'.format(p_address))
        l_defer_l0 = self.client_connect(p_pyhouses_obj, p_address)
        if g_debug >= 2:
            g_logger.debug('CreateClient - Defer: {0:} (273).'.format(l_defer_l0))
        l_defer_l0.addCallback(cb_connected_l1)
        l_defer_l0.addCallback(cb_result_l1)
        l_defer_l0.addErrback(eb_create_l1)


class AmpServerProtocol(DomainBoxDispatcher):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.
    """
    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        AMP.__init__(self)
        l_disp = DomainBoxDispatcher(p_pyhouses_obj, None)
        if g_debug >= 1:
            g_logger.debug('  ServerProtocol() initialized. (279)')
        self.locateResponder(NodeInformationCommand)

    def dataReceived(self, p_data):
        if g_debug >= 1:
            g_logger.debug('  ServerProtocol data rxed {0:} (284)'.format(PrintBox(p_data)))

    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            g_logger.debug('  ServerProtocol inbound connection Made. (294)')
        self.send_NodeInformation(self.m_pyhouses_obj.CoreData.Nodes[0])

    def connectionLost(self, p_reason):
        if g_debug >= 1:
            g_logger.debug('  ServerProtocol connection lost {0:}'.format(p_reason))

    def locateResponder(self, p_name):
        if g_debug >= 2:
            g_logger.debug('  ServerProtocol locateResponder = {0:} (303)'.format(p_name))


class AmpServerFactory(ServerFactory):

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 3:
            g_logger.debug('  ServerFactory() __init__ (311).')


    def buildProtocol(self, p_address_tupple):
        if g_debug >= 1:
            g_logger.debug('  ServerFactory - BuildProtocol from {0:}'.format(p_address_tupple))
        return AmpServerProtocol(self.m_pyhouses_obj)


class AmpServer(object):
    """Sit and listen for amp messages from other nodes.
    """

    def create_domain_server(self, p_endpoint, p_pyhouses_obj):
        l_listen_defer = p_endpoint.listen(AmpServerFactory(p_pyhouses_obj))
        if g_debug >= 2:
            g_logger.info("  Server started (327).")
        return l_listen_defer


class Utility(AmpServer, AmpClient):
    m_pyhouses_obj = None

    def create_domain_service(self, p_pyhouses_obj, p_service):
        p_pyhouses_obj.CoreData.DomainService = p_service
        p_pyhouses_obj.CoreData.DomainService.setName('Domain')
        p_pyhouses_obj.CoreData.DomainService.setServiceParent(p_pyhouses_obj.Application)

    def start_amp(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.Reactor.callLater(15, self.start_amp_server)

    def start_amp_server(self):
        """Start the domain server to listen for all incoming requests.
        For all the nodes we know about, send a message with our info and expect nodes info as a response.
        If the request times out, mark the node as non active.
        """
        def cb_client_loop(_ignore):
            l_nodes = self.m_pyhouses_obj.CoreData.Nodes
            for l_key, l_node in l_nodes.iteritems():
                if l_key == 0:
                    if g_debug >= 1:
                        g_logger.debug("cb_client_loop skip ourself Key:{0:} at addr:{1:}".format(l_key, l_node.ConnectionAddr))
                    # continue
                if g_debug >= 2:
                    g_logger.debug("Client Contacting node {0:} server at {1:} (367).".format(l_key, l_node.ConnectionAddr))
                self.create_client(self.m_pyhouses_obj, l_node.ConnectionAddr)
        def eb_client_loop(p_reason):
            g_logger.error('Creating client - {0:} (370).'.format(p_reason))

        if g_debug >= 2:
            g_logger.debug('Domain server is now starting (373).')
        l_endpoint = serverFromString(self.m_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory(self.m_pyhouses_obj)
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        self.create_domain_service(self.m_pyhouses_obj, l_service)
        l_defer1 = self.create_domain_server(l_endpoint, self.m_pyhouses_obj)
        l_defer1.addCallback(cb_client_loop)
        l_defer1.addErrback(eb_client_loop)
        if g_debug >= 2:
            g_logger.debug('  Server has started (371).\n')


class API(Utility):

    def __init__(self):
        if g_debug >= 2:
            g_logger.info("Initialized.")
        pass

    def Start(self, p_pyhouses_obj):
        self.start_amp(p_pyhouses_obj)
        if g_debug >= 2:
            g_logger.info("Started.")

    def Stop(self):
        if g_debug >= 2:
            g_logger.info("Stopped.")

# ## END DBK
