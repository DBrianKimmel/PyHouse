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
"""

# Import system type stuff
import logging
from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint
from twisted.internet.protocol import Factory, ClientCreator
from twisted.protocols.amp import AMP, Integer, Unicode, String, Command, IBoxReceiver, CommandLocator
from twisted.python.dist import twisted_subprojects
from twisted.python.filepath import FilePath
from zope.interface import implements

from src.utils.tools import PrintBytes

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
class NodeInfoError(Exception): pass


""" ------------------------------------------------------------------
 Commands
"""
class TestNameError(Exception): pass

class TestNameCommand(Command):
    arguments = [('Name', String()),
                 ('Active', String()),
                 ('Address', String()),
                 ('Role', Integer())
                 ]
    response = [('Answer', String())
                ]
    errors = {TestNameError: 'Name error'}


class TestNameResponse(CommandLocator):
    @TestNameCommand.responder
    def NameResponse(self, p_name):
        g_logger.debug('Test name response {0:}'.format(p_name))
        l_answer = p_name + '_answer'
        return {'Answer': l_answer}


#-----------------------------------------------------------
class UsernameUnavailable(Exception): pass

class RegisterUser(Command):
    arguments = [('username', Unicode()),
                  ('publickey', String())]
    response = [('uid', Integer())]
    errors = {UsernameUnavailable: 'username-unavailable'}


class UserRegistration(CommandLocator):
    uidCounter = 0
    @RegisterUser.responder
    def register(self, username, publickey):
        path = FilePath(username)
        if path.exists():
            raise UsernameUnavailable()
        self.uidCounter += 1
        path.setContent('%d %s\n' % (self.uidCounter, publickey))
        return self.uidCounter


### -----------------------------------------------------------------
# Boxes

class BoxReflector(object):
    implements (IBoxReceiver)

    def startReceivingBoxes(self, p_boxSender):
        g_logger.debug('Start Receiving boxes - Sender:{0:}'.format(p_boxSender))
        self.boxSender = p_boxSender

    def ampBoxReceived(self, p_box):
        g_logger.debug('Receivied box - Box:{0:}'.format(p_box))
        self.boxSender.sendBox(p_box)

    def stopReceivingBoxes(self, p_reason):
        g_logger.debug('Stop Receiving boxes - {0:}'.format(p_reason))
        self.boxSender = None


class LocatorClass(UserRegistration, TestNameResponse):
    pass

### -----------------------------------------------------------------

class AmpClientProtocol(AMP):

    def __init__(self):
        AMP.__init__(self, boxReceiver = BoxReflector(), locator = LocatorClass())
        g_logger.debug('AmpClientProtocol() initialized..')

    def dataReceived(self, p_data):
        l_msg = 'Domain Client - Received {0:}'.format(PrintBytes(p_data))
        g_logger.debug(l_msg)

    def connectionMade(self):
        g_logger.debug('Domain Client - Outgoing connection made.')


class AmpClientFactory(Factory):

    def startedConnecting(self, p_connector):
        g_logger.info("Domain Client - startedConnecting {0:}".format(p_connector))

    def buildProtocol(self, _addr):
        return AmpClientProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('DomainClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('DomainClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def connect(self, p_pyhouses_obj, p_address):
        """Connect to a server.

        @rtype: is a deferred
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory()
        l_defer1 = l_endpoint.connect(l_factory)
        g_logger.info("Domain Client connecting to address {0:}".format(p_address))
        return l_defer1

    def create_client(self, p_pyhouses_obj, p_address):
        def cb_connected(p_protocol):
            def cb_got_result(p_result):
                g_logger.debug('cb_got_result Client Addr:{0:} - Result:{1:}'.format(p_address, p_result))
                TestNameResponse().NameResponse('test dbk')

            def eb_err2(p_ConnectionDone):
                g_logger.error('eb_err2 - Addr:{0:} - arg:{1:}'.format(p_address, p_ConnectionDone))
            l_defer1 = p_protocol.callRemote(
                    TestNameCommand,
                    Name = p_pyhouses_obj.CoreData.Nodes[0].Name,
                    Active = str(p_pyhouses_obj.CoreData.Nodes[0].Active),
                    Address = p_pyhouses_obj.CoreData.Nodes[0].ConnectionAddr,
                    Role = p_pyhouses_obj.CoreData.Nodes[0].Role
                    )
            g_logger.debug('cb_connected To Client at addr {0:} - Sending - {1:}'.format(p_address, l_defer1))
            l_defer1.addCallback(cb_got_result)
            l_defer1.addErrback(eb_err2)

        def cb_result(p_result):
            g_logger.debug('cb_result Addr:{0:}, Result:{1:}'.format(p_address, p_result))
        def eb_create(p_result):
            p_result.trap(TestNameError)
            g_logger.error('Got test error Addr:{0:}, Result:{1:}'.format(p_address, p_result))
        l_defer = ClientCreator(p_pyhouses_obj.Reactor, AMP).connectTCP(p_address, AMP_PORT)
        l_defer.addCallback(cb_connected)
        l_defer.addCallback(cb_result)
        l_defer.addErrback(eb_create)


class AmpServerProtocol(AMP):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.
    """
    def __init__(self):
        AMP.__init__(self, boxReceiver = BoxReflector(), locator = LocatorClass())
        g_logger.debug('AmpServerProtocol() initialized..')

    def dataReceived(self, p_data):
        """
        """
        g_logger.debug('Domain Server data rxed {0:}'.format(PrintBox(p_data)))

    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established;
        for servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        g_logger.debug('Domain Server inbound connection Made.')

    def connectionLost(self, p_reason):
        g_logger.debug('Domain Server connection lost {0:}'.format(p_reason))


class AmpServerFactory(Factory):
    protocol = AmpServerProtocol()

    def buildProtocol(self, _p_addr):
        g_logger.debug('BuildProtocol Amp Server')
        return AmpServerProtocol()


class AmpServer(object):
    """Sit and listen for amp messages from other nodes.
    """

    def create_domain_server(self, p_pyhouses_obj, p_endpoint):
        p_pyhouses_obj.CoreData.DomainService.setName('Domain')
        p_pyhouses_obj.CoreData.DomainService.setServiceParent(p_pyhouses_obj.Application)
        l_listen_defer = p_endpoint.listen(AmpServerFactory())
        g_logger.info("Domain Server started.")
        return l_listen_defer


class Utility(AmpServer, AmpClient):
    m_pyhouses_obj = None

    def start_amp(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.Reactor.callLater(15, self.start_amp_server)

    def start_amp_server(self):
        """Start the domain server to listen for all incoming requests.
        For all the nodes we know about, send a message with our info and expect nodes info as a response.
        If the request times out, mark the node as non active.
        """
        def cb_client_loop(_p_protocol):
            l_nodes = self.m_pyhouses_obj.CoreData.Nodes
            for l_key, l_node in l_nodes.iteritems():
                if l_key == 0:
                    # g_logger.debug("cb_client_loop skip ourself Key:{0:} at addr:{1:}".format(l_key, l_node.ConnectionAddr))
                    continue
                # g_logger.debug("Client Contacting node {0:} - {1:}".format(l_key, l_node.ConnectionAddr))
                # _l_defer = self.connect(self.m_pyhouses_obj, l_node.ConnectionAddr)
                self.create_client(self.m_pyhouses_obj, l_node.ConnectionAddr)

        g_logger.debug('Domain server is now starting.')
        l_endpoint = serverFromString(self.m_pyhouses_obj.Reactor, NODE_SERVER)
        # l_factory = Factory()
        l_factory = AmpServerFactory()
        l_factory.protocol = AmpServerProtocol
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        self.m_pyhouses_obj.CoreData.DomainService = l_service
        l_defer1 = self.create_domain_server(self.m_pyhouses_obj, l_endpoint)
        l_defer1.addCallback(cb_client_loop)

    def start_amp_client(self):
        """We need one of these for every node in the domain.
        """
        def cb_send_node_info(p_protocol):
            g_logger.debug('Domain client cb_send_node_info - {0:}.'.format(p_protocol))
            _l_defer = self.send_register_node(AmpClientProtocol)
        l_defer = self.connect(self.m_pyhouses_obj)
        l_defer.addCallback(cb_send_node_info)


class API(Utility):

    def __init__(self):
        # g_logger.info("Initialized.")
        pass

    def Start(self, p_pyhouses_obj):
        self.start_amp(p_pyhouses_obj)
        # g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
