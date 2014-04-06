"""
@name: PyHouse/src/core/nodes.py

# -*- test-case-name: PyHouse.src.core.test.test_nodes -*-

Created on Mar 6, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for inter_node communication.

Using a Raspberry Pi as a node works fine for about any function, but I expect that it will run out
of capacity if too many services are attempted on one node.

Therefore, a cluster of nodes (a domain), each one running a small number of tasks will probably be the norm.

This design will then need a way for each node to discover all its neighbor nodes and establish a
communication network so we can pass information between nodes.

This module will establish a domain network and use Twisted's AMP protocol to pass messages around.
"""

# Import system type stuff
import logging

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint
from twisted.application.internet import StreamServerEndpointService
from twisted.protocols.amp import AMP, Integer, String, Command


g_debug = 0
g_logger = logging.getLogger('PyHouse.Nodes       ')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581


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
    arguments = [('Command', Integer()),
                 ('NodeName', String()),
                 ('NodeType', Integer()),
                 ('IPv4', String()),
                 ('IPv6', String())]
    response = [('Ack', Integer())]
    errors = {RegisterNodeError: 'Node Information unavailable.'}


class AmpClientProtocol(AMP):

    def dataReceived(self, p_data):
        l_msg = 'Amp Client Received {0:}'.format(p_data)
        g_logger.debug(l_msg)

    def connectionMade(self):
        """We connected to some server.
        Send them our node info
        Ask for their Node info.
        """
        g_logger.debug('Amp Client connection made.')


class AmpClientFactory(Factory):

    def startedConnecting(self, p_connector):
        g_logger.info("AMP Client startedConnecting {0:}".format(p_connector))

    def buildProtocol(self, _addr):
        return AmpClientProtocol()

    def clientConnectionLost(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - lost connection {0:}'.format(p_reason))

    def clientConnectionFailed(self, _connector, p_reason):
        g_logger.error('AmpClientFactory - Connection failed {0:}'.format(p_reason))


class AmpClient(object):

    def connect(self, p_pyhouses_obj, p_address):
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_factory = AmpClientFactory()
        l_defer = l_endpoint.connect(l_factory)
        g_logger.info("Amp Client started.")
        def cb_send_register_node(p_protocol):
            g_logger.debug('Sending our local node to a new discovered address {0:}'.format(p_address))
            p_protocol.callRemote(
                RegisterNode,
                Command = 1,
                NodeName = p_pyhouses_obj.Nodes[0].Name,
                NodeType = p_pyhouses_obj.Nodes[0].Role,
                IPv4 = '3.5.7.9',
                IPv6 = 'ff00::'
                )
        l_defer.addCallback(cb_send_register_node)
        def cb_registered(p_result):
            g_logger.debug('Registration result:{0:}'.format(p_result))
        l_defer.addCallback(cb_registered)
        def eb_error(p_error):
            g_logger.debug('Registration error:{0:}'.format(p_error))
        l_defer.addErrback(eb_error)
        def cb_done(_ignored):
            g_logger.debug('Registration done')
        l_defer.addCallback(cb_done)
        return l_defer


class AmpServerProtocol(AMP):

    def dataReceived(self, p_data):
        g_logger.debug('Amp Server data rxed {0:}'.format(p_data))

    def connectionMade(self):
        """Somebody connected to us...
        """
        g_logger.debug('Amp Server connection Made')

    def connectionLost(self, p_reason):
        g_logger.debug('Amp Server connection lost {0:}'.format(p_reason))


class AmpServerFactory(Factory):

    def buildProtocol(self, _p_addr):
        return AmpServerProtocol()


class AmpServer(object):
    """Sit and listen for amp commands from other nodes.
    """

    def server(self, p_pyhouses_obj):
        l_endpoint = serverFromString(p_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory()
        l_service = StreamServerEndpointService(l_endpoint, l_factory)
        l_service.setServiceParent(p_pyhouses_obj.Application)
        l_ret = l_endpoint.listen(AmpServerFactory())
        g_logger.info("Amp Server started.")
        return l_ret


class Utility(AmpServer, AmpClient):

    def start_amp(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        self._start_amp_server()

    def cb_send_node_info(self, p_protocol):
        g_logger.debug('Amp client cb_send_node_info - {0:}.'.format(p_protocol))
        _l_defer = self.send_register_node(AmpClientProtocol)

    def _start_amp_server(self):
        _l_defer = self.server(self.m_pyhouses_obj)

    def _start_amp_client(self):
        """We need one of these for every node in the domain.
        """
        l_defer = self.connect(self.m_pyhouses_obj)
        l_defer.addCallback(self.cb_send_node_info)


class API(Utility):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        if p_pyhouses_obj == None:
            p_pyhouses_obj.Nodes = {}
        self.start_amp(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        g_logger.info("Stopped.")

# ## END DBK
