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
from twisted.protocols.amp import AMP, Command, Integer, String, Float, AmpList
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import ServerFactory
# from twisted.internet.protocol import ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.Core.data_objects import NodeData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.tools import PrettyPrintAny


LOG = Logger.getLogger('PyHouse.InterNodeCom')

NODE_SERVER = 'tcp:port=8581'
AMP_PORT = 8581
INITIAL_DELAY = 10
REPEAT_DELAY = 2 * 60 * 60
CLIENT_DELAY = 3


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

class Sum(Command):
    arguments = [('a', Integer()),
                 ('b', Integer())]
    response = [('total', Integer())]

class Divide(Command):
    arguments = [('numerator', Integer()),
                 ('denominator', Integer())]
    response = [('result', Float())]
    errors = {ZeroDivisionError: 'ZERO_DIVISION'}

# ================== Server =======================

class InterNodeProtocol(amp.AMP):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    @NodeInfo.responder
    def receive_NodeInfo(self, Name, Active, AddressV4, NodeRole, UUID):
        l_response = self.update_NodeInfo(Name, Active, AddressV4, NodeRole, UUID)
        LOG.info('receive_NodeInfo() - from  address=:{}\n\tResponse = {}'.format(AddressV4, l_response))
        return l_response


    @Sum.responder
    def sum(self, a, b):
        l_total = a + b
        print('Server - Did a sum: {} + {} = {}'.format(a, b, l_total))
        return {'total': l_total}


    @Divide.responder
    def divide(self, numerator, denominator):
        l_result = float(numerator) / denominator
        print 'Server - Divided: %d / %d = %f' % (numerator, denominator, l_result)
        return {'result': l_result}

    def update_NodeInfo(self, Name, Active, AddressV4, NodeRole, UUID):
        """
        Update our PyHouse Nodes information with the data we just got.
        Create a response we can pass back to the sender
        """
        l_key = -1
        for l_node in self.m_pyhouse_obj.Computer.Nodes.itervalues():
            if l_node.Name == Name:
                l_node.Active = Active
                l_node.AddressV4 = AddressV4
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

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def buildProtocol(self, _p_address_tupple):
        # LOG.info('Server Factory is now building an InterNodeProtocol protocol - Addr: {}'.format(_p_address_tupple))
        l_protocol = InterNodeProtocol(self.m_pyhouse_obj)
        self.protocol = l_protocol
        return l_protocol


# ================== Client =======================

class MathClient(object):
    """
    """

    def doMath(self):
        destination = TCP4ClientEndpoint(reactor, '127.0.0.1', AMP_PORT)

        def connected_sum(ampProto):
            l_ret = ampProto.callRemote(Sum, a = 13, b = 81)
            PrettyPrintAny(l_ret, 'call remote result')
            return l_ret

        def summed(result):
            l_ret = result['total']
            PrettyPrintAny(result, 'Result')
            PrettyPrintAny(l_ret, 'xxx')
            return l_ret
        sumDeferred = connectProtocol(destination, AMP())
        sumDeferred.addCallback(connected_sum)
        sumDeferred.addCallback(summed)

        def connected_divide(ampProto):
            return ampProto.callRemote(Divide, numerator = 1234, denominator = 3)
        def trapZero(result):
            result.trap(ZeroDivisionError)
            print "Client - Divided by zero: returning INF"
            return 1e1000
        divideDeferred = connectProtocol(destination, AMP())
        divideDeferred.addCallback(connected_divide)
        divideDeferred.addErrback(trapZero)


        def math_done(result):
            print 'Client - Done with math:', result
        l_defer = defer.DeferredList([sumDeferred, divideDeferred])
        l_defer.addCallback(math_done)



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
            LOG.info('Server listening on port {}.'.format(p_port.getHost()))
            self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._send_node_info_to_all, self.m_pyhouse_obj)

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



class API(Utility):
    """
    """

    def _send_node_info_to_all(self, p_pyhouse_obj):
        """
        Loop thru all the nodes we know about (from node_discovery) and send them our node info
        """
        for l_node in p_pyhouse_obj.Computer.Nodes.itervalues():
            self.send_our_info_to_node(p_pyhouse_obj, l_node.ConnectionAddr_IPv4)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._send_node_info_to_all, self.m_pyhouse_obj)


    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        l_endpoint = self._create_amp_service(p_pyhouse_obj)
        self._start_amp_server(p_pyhouse_obj, l_endpoint)


    def Stop(self):
        pass

# ## END DBK
