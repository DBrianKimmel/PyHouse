"""
@name: PyHouse/src/core/node_domain.py

Created on Apr 3, 2014

# -*- test-case-name: PyHouse.src.core.test.test_node_domain -*-

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is for AMP request/response protocol

"""

# Import system type stuff
import logging
from twisted.application import service
from twisted.application.internet import StreamServerEndpointService
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint
from twisted.internet.protocol import Factory
from twisted.protocols.amp import AMP, Integer, String, Command

# from src.core.nodes import NodeData
from src.utils.tools import PrintBytes

g_debug = 1
g_logger = logging.getLogger('PyHouse.NodeDomain  ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581


class NodeInfoError(Exception): pass


class ReqNodeInfo(Command):
    """Ask a node for its node information.
    """
    requiresAnswer = True
    arguments = [('Command', Integer()),
                 ('Address', String())]
    response = [('Name', String()),
                ('Active', String()),
                ('Address', String()),
                ('Role', Integer())]
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

class NodeData(object):

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.HostName = ''
        self.ConnectionAddr = None
        self.Role = 0
        self.Interfaces = {}


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
        def cb_show_result(p_dict):
            g_logger.debug("Domain Client - Got result {0:}".format(p_dict))
        def cb_send_register_node(p_protocol):
            g_logger.debug('Domain Client - Sending registration to address {0:}'.format(p_address))
            l_defer2 = p_protocol.callRemote(
                RegisterNode,
                Command = 1,
                NodeName = p_pyhouses_obj.CoreData.Nodes[0].Name,
                NodeType = p_pyhouses_obj.CoreData.Nodes[0].Role,
                IPv4 = '3.5.7.9',
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

    def respond_register_node(self):
        g_logger.debug("respond_register_node")
        l_hostname = 'xxxx'
        l_addr = '44.55.66.77'
        l_role = 0x1234
        return {'Hostname': l_hostname, 'Address': l_addr, 'Role': l_role}
    # RegisterNode.responder(respond_register_node)

    def do_RegisterNode(self, p_command, p_node, p_type, p_v4, p_v6):
        l_hostname = 'wxyz'
        l_addr = '1.22.3.44'
        l_role = 0xfedc
        g_logger.debug("do_RegisterNode {0:}, {1:}, {2:}, {3:}, {4:}".format(p_command, p_node, p_type, p_v4, p_v6))
        return {'Hostname': l_hostname, 'Address': l_addr, 'Role': l_role}
    RegisterNode.responder(do_RegisterNode)


class AmpServerFactory(Factory):

    def buildProtocol(self, _p_addr):
        g_logger.debug('BuildProtocol')
        return AmpServerProtocol()


class AmpServer(object):
    """Sit and listen for amp commands from other nodes.
    """

    def server(self, p_pyhouses_obj):
        p_pyhouses_obj.CoreData.DomainService = service.Service()
        p_pyhouses_obj.CoreData.DomainService.setName('Domain')
        p_pyhouses_obj.CoreData.DomainService.setServiceParent(p_pyhouses_obj.Application)
        #
        l_endpoint = serverFromString(p_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory()
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)
        l_defer = l_endpoint.listen(AmpServerFactory())
        g_logger.info("Domain Server started.")
        return l_defer


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
                g_logger.debug("skip ourself Key:{0:} at addr:{1:}".format(l_key, l_node.ConnectionAddr))
                continue
            g_logger.debug("Client Contacting node {0:} - {1:}".format(l_key, l_node.ConnectionAddr))
            _l_defer = self.connect(self.m_pyhouses_obj, l_node.ConnectionAddr)

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
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.start_amp(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
