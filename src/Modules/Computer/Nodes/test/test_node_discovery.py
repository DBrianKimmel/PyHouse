"""
@name: PyHouse/src/Modules/Computer/test/test_node_discovery.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 5, 2014
@summary: Test the discovery for the domains nodes.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from twisted.internet.defer import Deferred, gatherResults, maybeDeferred
from twisted.internet import error

# Import PyMh files and modules.
from Modules.Computer.Nodes import node_discovery
from test import xml_data
from Modules.Core.data_objects import PyHouseData
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Mixin(object):
    m_started = 0
    m_stopped = 0
    m_startedDeferred = None
    m_packets = []

    def __init__(self):
        self.m_packets = []

    def startProtocol(self):
        self.m_started = 1
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.callback(None)

    def stopProtocol(self):
        self.m_stopped = 1


class TestServer(Mixin, node_discovery.MulticastDiscoveryServerProtocol):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        super(TestServer, self).datagramReceived(p_data, p_addr)
        self.m_packets.append((p_data, p_addr))
        print("TestServer packet {0:} - Addr:{1:}".format(p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class TestClient(Mixin, node_discovery.MulticastDiscoveryClientProtocol):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        super(TestClient, self).datagramReceived(p_data)
        self.m_packets.append(p_data)
        print("TestClient packet {0:}".format(p_data))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)

    def connectionFailed(self, failure):
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(failure)
        self.failure = failure

    def connectionRefused(self):
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(error.ConnectionRefusedError("yup"))
        self.m_refused = 1


class Test(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_discovery.API()
        print("setUp")
        self.m_api = node_discovery.API()
        self.m_server = TestServer()
        self.m_client = TestClient()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_server)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_client)
        self.m_client.transport.connect("127.0.0.1", self.m_server.transport.getHost().port)

    def tearDown(self):
        return gatherResults([maybeDeferred(self.m_port1.stopListening), maybeDeferred(self.m_port2.stopListening)])


    def test_001_TTL(self):
        for l_obj in self.m_client, self.m_server:
            self.assertEqual(l_obj.transport.getTTL(), 1)
            l_obj.transport.setTTL(2)
            self.assertEqual(l_obj.transport.getTTL(), 2)

    def test_002_loopback(self):
        """
        Test that after loopback mode has been set, multicast packets are delivered to their sender.
        """
        def cb_joined(_ignored):
            l_defer = self.m_server.m_packetReceived = Deferred()
            self.m_server.transport.write("Test_002 A", (node_discovery.PYHOUSE_MULTICAST_IP_V4, l_addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(len(self.m_server.m_packets), 1)
            self.m_server.transport.setLoopbackMode(0)
            self.assertEqual(self.m_server.transport.getLoopbackMode(), 0)
            self.m_server.transport.write("Test_002 B", (node_discovery.PYHOUSE_MULTICAST_IP_V4, l_addr.port))
            l_defer = Deferred()
            self.m_pyhouse_obj.Twisted.Reactor.callLater(0, l_defer.callback, None)
            return l_defer

        def cb_no_packet(_ignored):
            self.assertEqual(len(self.m_server.m_packets), 1)

        self.assertEqual(self.m_server.transport.getLoopbackMode(), 1)
        l_addr = self.m_server.transport.getHost()
        l_joined_defer = self.m_server.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        l_joined_defer.addCallback(cb_joined)
        l_joined_defer.addCallback(cb_packet)
        l_joined_defer.addCallback(cb_no_packet)
        return l_joined_defer

    def test_003_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        def cb_interfaces(_ignored):
            self.assertEqual(self.m_client.transport.getOutgoingInterface(), "127.0.0.1")
            self.assertEqual(self.m_server.transport.getOutgoingInterface(), "127.0.0.1")

        self.assertEqual(self.m_client.transport.getOutgoingInterface(), "0.0.0.0")
        self.assertEqual(self.m_server.transport.getOutgoingInterface(), "0.0.0.0")
        d1 = self.m_client.transport.setOutgoingInterface("127.0.0.1")
        d2 = self.m_server.transport.setOutgoingInterface("127.0.0.1")
        l_result_defer = gatherResults([d1, d2])
        l_result_defer.addCallback(cb_interfaces)
        return l_result_defer

    def test_004_joinLeave(self):
        """
        Test that a multicast group can be joined and left.
        """
        def cb_clientJoined(_ignored):
            return self.m_client.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        def cb_clientLeft(_ignored):
            return self.m_server.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        def cb_serverJoined(_ignored):
            return self.m_server.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        l_defer = self.m_client.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        l_defer.addCallback(cb_clientJoined)
        l_defer.addCallback(cb_clientLeft)
        l_defer.addCallback(cb_serverJoined)
        return l_defer

    def test_005_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        return self.assertFailure(self.m_client.transport.joinGroup("127.0.0.1"), error.MulticastJoinError)

    def test_006_multicast(self):
        """
        Test that a multicast group can be joined and messages sent to and received from it.
        """
        MESSAGE = "Test_006 A"
        def cb_joined(_ignored):
            l_defer = self.m_server.m_packetReceived = Deferred()
            c.transport.write(MESSAGE, (node_discovery.PYHOUSE_MULTICAST_IP_V4, addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(self.m_server.m_packets[0][0], MESSAGE)

        def cb_cleanup(passthrough):
            result = maybeDeferred(p.stopListening)
            result.addCallback(lambda _ign: passthrough)
            return result

        c = TestServer()
        p = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, c)
        addr = self.m_server.transport.getHost()
        joined = self.m_server.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        joined.addCallback(cb_joined)
        joined.addCallback(cb_packet)
        joined.addCallback(cb_cleanup)
        return joined

    def test_007_multiListen(self):
        """
        Test that multiple sockets can listen on the same multicast port and
        that they both receive multicast messages directed to that address.
        """
        MESSAGE = "Test_007 A"
        def cb_serverJoined(_ignored):
            d1 = firstClient.m_packetReceived = Deferred()
            d2 = secondClient.m_packetReceived = Deferred()
            firstClient.transport.write(MESSAGE, (theGroup, portno))
            return gatherResults([d1, d2])

        def cb_gotPackets(_ignored):
            self.assertEqual(firstClient.m_packets[0][0], MESSAGE)
            self.assertEqual(secondClient.m_packets[0][0], MESSAGE)

        def bb_cleanup(passthrough):
            l_result_defer = gatherResults([maybeDeferred(firstPort.stopListening), maybeDeferred(secondPort.stopListening)])
            l_result_defer.addCallback(lambda _ign: passthrough)
            return l_result_defer

        firstClient = TestServer()
        firstPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, firstClient, listenMultiple = True)
        portno = firstPort.getHost().port
        secondClient = TestServer()
        secondPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(portno, secondClient, listenMultiple = True)
        theGroup = node_discovery.PYHOUSE_MULTICAST_IP_V4
        l_joined_defer = gatherResults([self.m_server.transport.joinGroup(theGroup), firstPort.joinGroup(theGroup), secondPort.joinGroup(theGroup)])
        l_joined_defer.addCallback(cb_serverJoined)
        l_joined_defer.addCallback(cb_gotPackets)
        l_joined_defer.addBoth(bb_cleanup)
        return l_joined_defer


    def Xtest_501_server(self):
        l_server = self.m_api._start_discovery_server(self.m_pyhouse_obj)
        # l_defer = l_server.m_startedDeferred = defer.Deferred()
        return l_server

    def Xtest_502_client(self):
        _l_client = self.m_api._start_discovery_client(self.m_pyhouse_obj)
        # l_defer = l_client.m_startedDeferred = defer.Deferred()

# ## END DBK
