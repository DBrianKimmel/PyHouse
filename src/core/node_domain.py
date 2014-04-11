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
from twisted.protocols.amp import AMP, Integer, String, Command, IBoxReceiver
from zope.interface import implements

from src.utils.tools import PrintBytes

g_debug = 1
g_logger = logging.getLogger('PyHouse.NodeDomain  ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581


""" ------------------------------------------------------------------
 Command exceptions
"""
class NodeInfoError(Exception): pass


""" ------------------------------------------------------------------
 Commands
"""
class ReqNodeInfo(Command):
    """Ask a node for its node information.
    """
    requiresAnswer = True
    arguments = [('Command1', Integer()),
                 ('Name1', String()),
                 ('Address1', String()),
                 ('Role1', Integer())
                 ]
    response = [('Name2', String()),
                ('Active2', String()),
                ('Address2', String()),
                ('Role2', Integer())
                ]
    errors = {NodeInfoError: 'Node information unavailable.'}


class NodeInfoResponse(AMP):
    def NodeInfo(self, p_name, p_active, p_address, p_role):
        g_logger.debug("NodeInfoResponse")
        Name = p_name
        Active = p_active
        Address = p_address
        Role = p_role
        return {'Name': Name,
                'Active': Active,
                'Address': Address,
                'Role': Role}

    ReqNodeInfo.responder(NodeInfo)

class RegisterNodeError(Exception):
    pass


class RegisterNode(Command):
    """
    """
    requiresAnswer = True
    arguments = [('Command', Integer()),
                 ('NodeName', String()),
                 ('NodeType', Integer()),
                 ('IPv4', String()),
                 ('IPv6', String())]
    response = [('Hostname', String()),
                ('Address', String()),
                ('Role', Integer())]
    errors = {RegisterNodeError: 'Node Information unavailable.'}


class BoxReflector(object):
    implements (IBoxReceiver)

    def startReceivingBoxes(self, p_boxSender):
        self.boxSender = p_boxSender

    def ampBoxReceived(self, p_box):
        self.boxSender.sendBox(p_box)

    def stopReceivingBoxes(self, _p_reason):
        self.boxSender = None

class AmpClientProtocol(AMP):

    def dataReceived(self, p_data):
        l_msg = 'Domain Client - Received {0:}'.format(PrintBytes(p_data))
        g_logger.debug(l_msg)

    def connectionMade(self):
        """We connected to some server.
        Send them our node info
        Ask for their Node info.
        """
        g_logger.debug('Domain Client - connection made.')

    def do_RegisterNode2(self, p_command, p_node, p_type, p_v4, p_v6):
        l_hostname = 'wxyz'
        l_addr = '1.22.3.44'
        l_role = 0xfedc
        g_logger.debug("do_RegisterNode {0:}, {1:}, {2:}, {3:}, {4:}".format(p_command, p_node, p_type, p_v4, p_v6))
        return {'Hostname': l_hostname, 'Address': l_addr, 'Role': l_role}
    RegisterNode.responder(do_RegisterNode2)


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
        def cb_show_result(p_dict):
            g_logger.debug("Domain Client - Got result {0:}".format(p_dict))
        def cb_send_register_node(p_protocol):
            g_logger.debug('Domain Client - Sending registration to address {0:}'.format(p_address))
            l_node = self.m_pyhouses_obj.CoreData.Nodes[0]
            l_defer2 = p_protocol.callRemote(
                RegisterNode,
                Command = 1,
                NodeName = l_node.Name,
                NodeType = l_node.Role,
                IPv4 = l_node.ConnectionAddr,
                IPv6 = 'ff00::'
                )
            l_defer2.addCallback(cb_show_result)
        def cb_registered(p_result):
            g_logger.debug('Domain Client - Registration result:{0:}'.format(p_result))
        def eb_error(p_error):
            g_logger.debug('Domain Client - Registration error:{0:}'.format(p_error))
        def cb_done(p_done):
            g_logger.debug('Domain Client - Registration done:{0:}'.format(p_done))

        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory()
        l_defer1 = l_endpoint.connect(l_factory)
        g_logger.info("Domain Client connecting to address {0:}".format(p_address))
        #
        l_defer1.addCallback(cb_send_register_node)
        l_defer1.addCallback(cb_registered)
        l_defer1.addErrback(eb_error)
        l_defer1.addCallback(cb_done)
        return l_defer1

    def create_client(self, p_pyhouses_obj, p_address):
        def cb_got_result(p_result):
            g_logger.debug('cb_got_result {0:}'.format(p_result))
            pass
        def cb_connected(p_protocol):
            g_logger.debug('cb_connected')
            l_defer1 = p_protocol.callRemote(ReqNodeInfo, Command1 = 42, Name1 = 'n1', Address1 = 'A1', Role1 = 53)
            l_defer1.addCallback(cb_got_result)
            return l_defer1

        def eb_error(p_reason):
            g_logger.error('en_error - {0:}'.format(p_reason))

        g_logger.debug('Create Client {0:}'.format(p_address))
        l_defer2 = ClientCreator(p_pyhouses_obj.Reactor, AMP).connectTCP(p_address, AMP_PORT)
        l_defer2.addCallback(cb_connected)
        l_defer2.addErrback(eb_error)


class AmpServerProtocol(AMP):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.
    """

    def dataReceived(self, p_data):
        """
        """
        g_logger.debug('Domain Server data rxed {0:}'.format(PrintBytes(p_data)))

    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established;
        for servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        g_logger.debug('Domain Server inbound connection Made')

    def connectionLost(self, p_reason):
        g_logger.debug('Domain Server connection lost {0:}'.format(p_reason))

    @ReqNodeInfo.responder
    def do_RegisterNode(self, p_command, p_node, p_type, p_v4, p_v6):
        l_hostname = 'wxyz'
        l_active = True
        l_addr = '1.22.3.44'
        l_role = 0xfedc
        g_logger.debug("do_RegisterNode {0:}, {1:}, {2:}, {3:}, {4:}".format(p_command, p_node, p_type, p_v4, p_v6))
        return {'Name2': l_hostname, 'Active2': l_active, 'Address2': l_addr, 'Role2': l_role}
    # RegisterNode.responder(do_RegisterNode)


class AmpServerFactory(Factory):

    def buildProtocol(self, _p_addr):
        g_logger.debug('BuildProtocol')
        return AmpServerProtocol()


class AmpServer(object):
    """Sit and listen for amp messages from other nodes.
    """

    def server(self, p_pyhouses_obj):
        l_endpoint = serverFromString(p_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory()
        l_service = StreamServerEndpointService(l_endpoint, l_factory)

        p_pyhouses_obj.CoreData.DomainService = l_service
        p_pyhouses_obj.CoreData.DomainService.setName('Domain')
        p_pyhouses_obj.CoreData.DomainService.setServiceParent(p_pyhouses_obj.Application)
        #
        l_listen_defer = l_endpoint.listen(AmpServerFactory())
        g_logger.info("Domain Server started.")
        return l_listen_defer


class Utility(AmpServer, AmpClient):

    def start_amp(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.Reactor.callLater(15, self.start_amp_server)

    def cb_send_node_info(self, p_protocol):
        g_logger.debug('Domain client cb_send_node_info - {0:}.'.format(p_protocol))
        _l_defer = self.send_register_node(AmpClientProtocol)

    def cb_client_loop(self, _p_protocol):
        l_nodes = self.m_pyhouses_obj.CoreData.Nodes
        for l_key, l_node in l_nodes.iteritems():
            if l_key == 0:
                g_logger.debug("cb_client_loop skip ourself Key:{0:} at addr:{1:}".format(l_key, l_node.ConnectionAddr))
                continue
            g_logger.debug("Client Contacting node {0:} - {1:}".format(l_key, l_node.ConnectionAddr))
            # _l_defer = self.connect(self.m_pyhouses_obj, l_node.ConnectionAddr)
            self.create_client(self.m_pyhouses_obj, l_node.ConnectionAddr)

    def start_amp_server(self):
        """Start the domain server to listen for all incoming requests.
        For all the nodes we know about, send a message with our info and expect nodes info as a response.
        If the request times out, mark the node as non active.
        """
        l_defer = self.server(self.m_pyhouses_obj)
        l_defer.addCallback(self.cb_client_loop)

    def _start_amp_client(self):
        """We need one of these for every node in the domain.
        """
        l_defer = self.connect(self.m_pyhouses_obj)
        l_defer.addCallback(self.cb_send_node_info)


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
