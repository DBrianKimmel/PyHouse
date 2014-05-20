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

What I want to happen on startup:
    Start an instance of an AMP server
    When the server is started and listening:
        Start a client for each node that we discovered (it's domain server should be running).
        Send a NodeInformation box using the client to the server at the connected address.
        Receive a response box back.

"""

# Import system type stuff
import pprint
from twisted.internet.endpoints import serverFromString, TCP4ClientEndpoint, connectProtocol
from twisted.internet.protocol import ServerFactory, ClientFactory
from twisted.protocols.amp import AMP, Integer, String, AmpList, Command, CommandLocator
from twisted.internet.defer import Deferred
from twisted.application.internet import StreamServerEndpointService

# Import PyMh files and modules.
from Modules.utils import pyh_log

g_debug = 5
LOG = pyh_log.getLogger('PyHouse.NodeDomain  ')
PP = pprint.PrettyPrinter

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
 Commands
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





class DomainBoxDispatcher(AMP):

    m_amp = None

    def __init__(self):
        """
        @param p_address: is a 3-tupple (AddressFamily, IPv4Addr, Port)
        """
        self.m_locator = LocatorClass()
        super(DomainBoxDispatcher, self).__init__(self.m_locator)
        self.m_amp = self
        if g_debug >= 1:
            LOG.debug('Dispatch DomainBoxDispatcher()  (DBD-1  088)')
            # LOG.debug('      Self: {0:}'.format(vars(self)))


    def makeConnection(self, p_transport):
        """Called from twisted.internet.endpoints
        Required to be here - passes back the transport apparently.
        """
        self.m_transport = p_transport
        if g_debug >= 2:
            LOG.debug('Dispatch - makeConnection  (DBD-2  098)')
            LOG.debug('      Transport:{0:}'.format(p_transport))


    def connectionMade(self):
        """Somebody connected to us...
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            LOG.debug('Dispatch - connectionMade  (DBD-3  110)')
        pass



    def startReceivingBoxes(self, p_boxSender):
        if g_debug >= 1:
            LOG.debug('Dispatch - Start Receiving boxes  (DBD-4  117)')
            LOG.debug('      Sender:{0:}'.format(p_boxSender))
        self.boxSender = p_boxSender


    def ampBoxReceived(self, p_box):
        if g_debug >= 1:
            LOG.debug(' Dispatch - Received box  (DBD-5  124)')
            LOG.debug('      Box:{0:}'.format(p_box))
        self.boxSender.sendBox(p_box)


    def stopReceivingBoxes(self, p_reason):
        if g_debug >= 1:
            LOG.debug(' Dispatch - Stop Receiving boxes  (DBD-6  131)')
            LOG.debug('      Reason: {0:}'.format(p_reason))
        self.boxSender = None


    def send_NodeInformation_1(self, p_node):
        """For some reason, this gives a error 'NoneType' object has no attribute 'sendBox'
        The information is sent somehow.
        """
        l_protocol = self
        if g_debug >= 1:
            LOG.debug('Dispatch - send_NodeInformation_1  (DBD-7  143)')
            LOG.debug('     l_protocol: {0:}'.format(l_protocol))
        try:
            l_defer = self.callRemote(NodeInformationCommand,
                        Name = p_node.Name, Active = str(p_node.Active), Address = p_node.ConnectionAddr_IPv4,
                        Role = int(p_node.Role), UUID = "1122")
            if g_debug >= 1:
                # LOG.debug(' Dispatch - send_NodeInformation_1  - SENT to {0:} (236)'.format(self.m_address))
                pass
        except AttributeError as l_error:
            LOG.error('Dispatch - send_NodeInformation_1  (152)')
            LOG.error('     ERROR: {0:}\n'.format(l_error))
            l_defer = Deferred()
        return l_defer


    def receive_NodeInformation(self, Name = None, Active = None, Address = None, Role = None, UUID = None):
        if g_debug >= 1:
            LOG.debug('Dispatch - receive_NodeInformation - RECEIVED  (DBD-8  160)')
        l_ret = dict(Name = Name, Answer = 'Got it ok')
        return l_ret
    NodeInformationCommand.responder(receive_NodeInformation)


    def update_NodeInformation(self, _p_box):
        if g_debug >= 1:
            LOG.debug('Dispatch - update_NodeInformation  (DBD-9  168)')
        pass




class AmpServerFactory(ServerFactory):
    """
    """

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj

    def buildProtocol(self, _p_address_tupple):
        l_protocol = NodeDomainServerProtocol(self.m_pyhouses_obj)
        if g_debug >= 4:
            LOG.debug('AmpServerFactory.buildProtocol()  (184)')
        return l_protocol





class NodeDomainServerProtocol(DomainBoxDispatcher):
    """
    Implement dataReceived(data) to handle both event-based and synchronous input.
    output can be sent through the 'transport' attribute.

    When BinaryBoxProtocol is connected to a transport, it calls startReceivingBoxes on its IBoxReceiver
    with itself as the IBoxSender parameter.
    """
    def __init__(self, p_pyhouses_obj):
        LOG.debug('NodeDomainServerProtocol()  (NDSP-1  200)')
        self.m_pyhouses_obj = p_pyhouses_obj
        self.m_disp = DomainBoxDispatcher()
        # AMP.__init__(AMP(), boxReceiver = l_disp)
        # super(NodeDomainServerProtocol, self).__init__()
        if g_debug >= 1:
            LOG.debug('ServerProtocol() initialized  (NDSP-1a  206)')
            # LOG.debug('      Proto:{0:}'.format(l_disp))
            LOG.debug('      Dispatch:{0:}'.format(self.m_disp))
            # LOG.debug('      Self: {0:}'.format(vars(self)))
        self.locate_responder('NodeInformationCommand')
        self.connectionMade()



    def dataReceived(self, p_data):
        if g_debug >= 1:
            LOG.debug('ServerProtocol - data rxed  (NDSP-2  217)')
            LOG.debug('       Data rxed: {0:}'.format(PrintBox(p_data)))



    def cb_got_result12(self, p_result):
        if g_debug >= 1:
            LOG.debug('ServerProtocol - ConnectionMade cb_got_result  (NDSP-3  224)')
            LOG.debug('     Client Addr:{0:}'.format(self.m_address))
            LOG.debug('     Result:{0:}'.format(p_result))
            LOG.debug('     Transport{0:}'.format(self.transport))
            LocatorClass().NodeInformationResponse('test dbk')


    def eb_err12(self, p_ConnectionDone):
        LOG.error('ServerProtocol - ConnectionMade  (232)')
        LOG.error('     Address: {0:}'.format(self.m_address))
        LOG.error('     ERROR: {0:}\n'.format(p_ConnectionDone))


    def connectionMade(self):
        """Some client connected to this server.
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established.
        For servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        if g_debug >= 1:
            LOG.debug('ServerProtocol - ConnectionMade  (NDSP-5  245)')
            # LOG.debug('    self = {0:}\n'.format(vars(self)))
        # l_defer12 = self.send_NodeInformation_1(self.m_pyhouses_obj.Nodes[0])
        # l_defer12.addCallback(self.cb_got_result12)
        # l_defer12.addErrback(self.eb_err12)


    def connectionLost(self, p_reason):
        """Clean up the connection.
        """
        if g_debug >= 1:
            LOG.debug('ServerProtocol - connectionLost  (NDSP-6  256)')
            LOG.debug('       Reason: {0:}'.format(p_reason))


    def locate_responder(self, p_name):
        if g_debug >= 1:
            LOG.debug('ServerProtocol - locate_responder  (NDSP-7  262)')
            LOG.debug('        Name: {0:}'.format(p_name))





""" ------------------------------------------------------------------
 Command exceptions
"""
class NodeInformationError(Exception): pass
class UsernameUnavailable(Exception): pass
class IrPacketError(Exception): pass


class GetNodeList(Command):
    """ Get a list of all the nodes.
    """
    commandName = 'getNodelist'
    arguments = [('length', Integer())]
    response = [('Nodes', AmpList([('x', String())]))]




class LocatorClass(CommandLocator):
    """
    """





class AmpClient(object):

    def cb_sendInfo(self, p_ampProto):
        l_node = self.m_pyhouses_obj.Nodes[0]
        if g_debug >= 4:
            LOG.debug('Client - sending info to remote server.  (300)')
            LOG.debug('      Address: {0:}'.format(l_node.ConnectionAddr_IPv4))
        l_ret = p_ampProto.callRemote(NodeInformationCommand,
                        Name = l_node.Name, Active = str(l_node.Active), Address = l_node.ConnectionAddr_IPv4,
                        Role = int(l_node.Role), UUID = "1122")
        return l_ret


    def create_one_client(self, p_pyhouses_obj, p_address):
        """
        Create a client to talk to some node's servers.

        @param p_address: is the address of the server we are connecting to.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        self.m_address = p_address
        l_endpoint = TCP4ClientEndpoint(p_pyhouses_obj.Reactor, p_address, AMP_PORT)
        l_defer = l_endpoint.connect(ClientFactory.forProtocol(AMP))
        l_defer.addCallback(self.cb_sendInfo)
        if g_debug >= 8:
            LOG.debug('Client create_one_client  (320)')
            LOG.debug('     Server Address: {0:}'.format(p_address))



class Utility(AmpClient):
    m_pyhouses_obj = None

    def cb_start_all_clients(self, _ignore):
        """
        Loop thru all the nodes we know about.  Start a client for each node except ourself (Nodes[0]).

        @param _ignore: node_domain.AmpSe rverFactory on 8581
        @type _ignore: class 'twisted.internet.tcp.Port'
        """
        l_nodes = self.m_pyhouses_obj.Nodes
        for l_key, l_node in l_nodes.iteritems():
            if l_key > -9:  # Skip ourself
                self.create_one_client(self.m_pyhouses_obj, l_node.ConnectionAddr_IPv4)

    def eb_start_clients_loop(self, p_reason):
        LOG.error('Utility.eb_start_clients_loop().  (341)')
        LOG.error('     ERROR Creating client - {0:}.\n'.format(p_reason))

    def start_amp_services(self):
        """
        Start the domain server to listen for all incoming requests.

        For all the nodes we know about, create a client and send a message with our info.
        """
        l_endpoint = serverFromString(self.m_pyhouses_obj.Reactor, NODE_SERVER)
        l_factory = AmpServerFactory(self.m_pyhouses_obj)
        self.m_pyhouses_obj.CoreServicesData.DomainService = StreamServerEndpointService(l_endpoint, l_factory)
        self.m_pyhouses_obj.CoreServicesData.DomainService.setServiceParent(self.m_pyhouses_obj.Application)
        l_defer = l_endpoint.listen(AmpServerFactory(self.m_pyhouses_obj))
        l_defer.addCallback(self.cb_start_all_clients)
        l_defer.addErrback(self.eb_start_clients_loop)

class API(Utility):

    def __init__(self):
        pass

    def Start(self, p_pyhouses_obj):
        """
        Try to avoid missing events due to congestion when a power failure has all nodes rebooting at nearly the same time.
        This delay should help ensure that the nodes are all up and functioning before starting AMP.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.Reactor.callLater(15, self.start_amp_services)

    def Stop(self, _p_xml):
        pass

# ## END DBK
