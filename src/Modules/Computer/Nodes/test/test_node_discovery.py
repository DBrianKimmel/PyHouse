"""
@name: PyHouse/src/Modules/Computer/Nodes/test/test_node_discovery.py
@author: D. Brian Kimmel
@contact: d.briankimmel@gmail.com
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

# from twisted.internet import udp

# Import PyMh files and modules.
from Modules.Computer.Nodes import node_discovery
from test import xml_data
# from Modules.Core.data_objects import PyHouseData
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


T_ALL_PORTS = 0


class SetupMixin(object):
    """
    Set up pyhouse_obj and xml element pointers
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class MulticastMixin(object):
    """
    Twisted testing
    """
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


class TestServerV4Protocol(MulticastMixin, node_discovery.ServerProtocolV4):
    """
    a server for testing IPv4 connections
    """
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        super(TestServerV4Protocol, self).datagramReceived(p_data, p_addr)
        self.m_packets.append((p_data, p_addr))
        print("TestServer V4 packet {0:} - Addr:{1:}".format(p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class DummyServerV6(MulticastMixin, node_discovery.ServerProtocolV6):
    """
    A server for testing an IPv6 connections
    """
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        super(DummyServerV6, self).datagramReceived(p_data, p_addr)
        self.m_packets.append((p_data, p_addr))
        print("TestServer V6 packet {0:} - Addr:{1:}".format(p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class TestClientV4(MulticastMixin, node_discovery.ClientProtocolV4):
    """
    A client to talk to the IPv4 server.
    """
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        super(TestClientV4, self).datagramReceived(p_data)
        self.m_packets.append(p_data)
        print("TestClient V4 packet {0:}".format(p_data))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)

    def connectionFailed(self, p_failure):
        print('ClientV4 connection failed {}'.format(p_failure))
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(p_failure)
        self.failure = p_failure

    def connectionRefused(self):
        print('ClientV4 - Connection refused.')
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(error.ConnectionRefusedError("yup"))
        self.m_refused = 1


class DummyClientV6(MulticastMixin, node_discovery.ClientProtocolV6):
    """
    A client to talk to the IPv6 Server.
    """
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        super(DummyClientV6, self).datagramReceived(p_data)
        self.m_packets.append(p_data)
        print("TestClient V6 packet {0:}".format(p_data))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)

    def connectionFailed(self, p_failure):
        print('ClientV6 - Connection Failed.')
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(p_failure)
        self.failure = p_failure

    def connectionRefused(self):
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(error.ConnectionRefusedError("yup"))
        self.m_refused = 1


class Test_01Creation(SetupMixin, unittest.TestCase):
    """
    Test creating test clients and servers
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor
        self.m_api = node_discovery.API()

    def test_01_V4Server(self):
        l_server_v4 = TestServerV4Protocol()
        PrettyPrintAny(l_server_v4, 'Server V4', 250)
        self.assertIsNotNone(l_server_v4, 'V4 Server not created.')

    def test_02_V6Server(self):
        l_server_v6 = DummyServerV6()
        PrettyPrintAny(l_server_v6, 'Server V6')
        self.assertIsNotNone(l_server_v6, 'V6 Server not created.')

    def test_03_V4Client(self):
        l_client_v4 = TestClientV4()
        PrettyPrintAny(l_client_v4, 'Client V4')
        self.assertIsNotNone(l_client_v4, 'V4 Client not created.')

    def test_04_V6Client(self):
        l_client_v6 = DummyClientV6()
        PrettyPrintAny(l_client_v6, 'Client V6')
        self.assertIsNotNone(l_client_v6, 'V6 Client not created.')


class Test_02_V4(SetupMixin, unittest.TestCase):
    """
    Test to see if Client can connect to server.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor

    def tearDown(self):
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])

    def test_01_Ports(self):
        self.m_serverV4 = TestServerV4Protocol()
        PrettyPrintAny(self.m_serverV4, 'Server V4', 250)
        self.m_clientV4 = TestClientV4()
        PrettyPrintAny(self.m_clientV4, 'Client V4', 250)
        # _l_x1 = self.m_serverV4.transport.getHost()
        # self.m_clientV4.transport.connect("127.0.0.1", self.m_serverV4.transport.getHost().port)
        self.m_port1 = self.m_reactor.listenMulticast(T_ALL_PORTS, self.m_serverV4)
        PrettyPrintAny(self.m_port1, 'Server - Port 1 V4', 256)
        self.m_port2 = self.m_reactor.listenMulticast(T_ALL_PORTS, self.m_clientV4)
        PrettyPrintAny(self.m_port2, 'Client - Port 2 V4', 256)
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])


class Test_03_V6(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor

    def tearDown(self):
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])

    def test_01_Ports(self):
        self.m_serverV6 = DummyServerV6()
        PrettyPrintAny(self.m_serverV6, 'Server V6', 250)
        self.m_clientV6 = DummyClientV6()
        self.m_clientV6.transport.connect("::", self.m_serverV6.transport.getHost().port)
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_serverV6, interface = '::')
        PrettyPrintAny(self.m_port1, 'Server Port 1 V6', 250)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_clientV6, interface = '::')
        PrettyPrintAny(self.m_port2, 'Client Port 2 V6', 250)
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])


class Test_04_V4(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_discovery.API()
        print("setUp V4")
        self.m_serverV4 = TestServerV4Protocol()
        self.m_clientV4 = TestClientV4()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_serverV4)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_clientV4)
        self.m_clientV4.transport.connect("127.0.0.1", self.m_serverV4.transport.getHost().port)

    def tearDown(self):
        return gatherResults([maybeDeferred(self.m_port1.stopListening), maybeDeferred(self.m_port2.stopListening)])

    def test_01_TTL(self):
        for l_obj in self.m_clientV4, self.m_serverV4:
            PrettyPrintAny(l_obj, 'V4 Obj', 250)
            self.assertEqual(l_obj.transport.getTTL(), 1)
            l_obj.transport.setTTL(2)
            self.assertEqual(l_obj.transport.getTTL(), 2)

    def test_02_loopback(self):
        """
        Test that after loopback mode has been set, multicast packets are delivered to their sender.
        """
        def cb_joined(_ignored):
            l_defer = self.m_serverV4.m_packetReceived = Deferred()
            self.m_serverV4.transport.write("Test_002 A", (node_discovery.PYHOUSE_MULTICAST_IP_V4, l_addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(len(self.m_serverV4.m_packets), 1)
            self.m_serverV4.transport.setLoopbackMode(0)
            self.assertEqual(self.m_serverV4.transport.getLoopbackMode(), 0)
            self.m_serverV4.transport.write("Test_002 B", (node_discovery.PYHOUSE_MULTICAST_IP_V4, l_addr.port))
            l_defer = Deferred()
            self.m_pyhouse_obj.Twisted.Reactor.callLater(0, l_defer.callback, None)
            return l_defer

        def cb_no_packet(_ignored):
            self.assertEqual(len(self.m_serverV4.m_packets), 1)

        self.assertEqual(self.m_serverV4.transport.getLoopbackMode(), 1)
        l_addr = self.m_serverV4.transport.getHost()
        l_joined_defer = self.m_serverV4.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        l_joined_defer.addCallback(cb_joined)
        l_joined_defer.addCallback(cb_packet)
        l_joined_defer.addCallback(cb_no_packet)
        return l_joined_defer

    def test_03_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        def cb_interfaces(_ignored):
            self.assertEqual(self.m_clientV4.transport.getOutgoingInterface(), "127.0.0.1")
            self.assertEqual(self.m_serverV4.transport.getOutgoingInterface(), "127.0.0.1")

        l_i1 = self.m_clientV4.transport.getOutgoingInterface()
        self.assertEqual(l_i1, "0.0.0.0")
        l_i2 = self.m_serverV4.transport.getOutgoingInterface()
        self.assertEqual(l_i2, "0.0.0.0")
        d1 = self.m_clientV4.transport.setOutgoingInterface("127.0.0.1")
        d2 = self.m_serverV4.transport.setOutgoingInterface("127.0.0.1")
        l_result_defer = gatherResults([d1, d2])
        l_result_defer.addCallback(cb_interfaces)
        return l_result_defer

    def test_04_joinLeave(self):
        """
        Test that a multicast group can be joined and left.
        """
        def cb_clientJoined(_ignored):
            return self.m_clientV4.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        def cb_clientLeft(_ignored):
            return self.m_serverV4.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        def cb_serverJoined(_ignored):
            return self.m_serverV4.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)

        l_defer = self.m_clientV4.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        l_defer.addCallback(cb_clientJoined)
        l_defer.addCallback(cb_clientLeft)
        l_defer.addCallback(cb_serverJoined)
        return l_defer

    def test_05_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        return self.assertFailure(self.m_clientV4.transport.joinGroup("127.0.0.1"), error.MulticastJoinError)

    def test_06_multicast(self):
        """
        Test that a multicast group can be joined and messages sent to and received from it.
        """
        MESSAGE = "Test_006 A"
        def cb_joined(_ignored):
            l_defer = self.m_serverV4.m_packetReceived = Deferred()
            c.transport.write(MESSAGE, (node_discovery.PYHOUSE_MULTICAST_IP_V4, addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(self.m_serverV4.m_packets[0][0], MESSAGE)

        def cb_cleanup(passthrough):
            result = maybeDeferred(p.stopListening)
            result.addCallback(lambda _ign: passthrough)
            return result

        c = TestServerV4Protocol()
        p = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, c)
        addr = self.m_serverV4.transport.getHost()
        joined = self.m_serverV4.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        joined.addCallback(cb_joined)
        joined.addCallback(cb_packet)
        joined.addCallback(cb_cleanup)
        return joined

    def test_07_multiListen(self):
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

        firstClient = TestServerV4Protocol()
        firstPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, firstClient, listenMultiple = True)
        portno = firstPort.getHost().port
        secondClient = TestServerV4Protocol()
        secondPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(portno, secondClient, listenMultiple = True)
        theGroup = node_discovery.PYHOUSE_MULTICAST_IP_V4
        l_joined_defer = gatherResults([self.m_serverV4.transport.joinGroup(theGroup), firstPort.joinGroup(theGroup), secondPort.joinGroup(theGroup)])
        l_joined_defer.addCallback(cb_serverJoined)
        l_joined_defer.addCallback(cb_gotPackets)
        l_joined_defer.addBoth(bb_cleanup)
        return l_joined_defer


class Test_05_V6(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_discovery.API()
        print("setUp V6")
        self.m_serverV6 = DummyServerV6()
        self.m_clientV6 = DummyClientV6()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_serverV6, interface = '::')
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, self.m_clientV6, interface = '::')
        # self.m_clientV6.transport.connect("::1", self.m_serverV6.transport.getHost().port)

    def tearDown(self):
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])

    def test_01_TTL(self):
        for l_obj in self.m_clientV6, self.m_serverV6:
            PrettyPrintAny(l_obj, 'V6 obj', 250)
            self.assertEqual(l_obj.transport.getTTL(), 1)
            l_obj.transport.setTTL(3)
            self.assertEqual(l_obj.transport.getTTL(), 3)

    def test_02_loopback(self):
        """
        Test that after loopback mode has been set, multicast packets are delivered to their sender.
        """
        def cb_joined(_ignored):
            print('Loopback cb_joined')
            l_defer = self.m_serverV6.m_packetReceived = Deferred()
            self.m_serverV6.transport.write("Test_002 - A", (node_discovery.PYHOUSE_MULTICAST_IP_V6, l_addr.port))
            return l_defer

        def cb_packet(_ignored):
            print('Loopback cb_packet')
            self.assertEqual(len(self.m_serverV6.m_packets), 1)
            self.m_serverV6.transport.setLoopbackMode(0)
            self.assertEqual(self.m_serverV6.transport.getLoopbackMode(), 0)
            self.m_serverV6.transport.write("Test_002 - B", (node_discovery.PYHOUSE_MULTICAST_IP_V6, l_addr.port))
            l_defer = Deferred()
            self.m_pyhouse_obj.Twisted.Reactor.callLater(0, l_defer.callback, None)
            return l_defer

        def cb_no_packet(_ignored):
            print('Loopback cb_no_packet')
            self.assertEqual(len(self.m_serverV6.m_packets), 1)

        def eb_no_packet(p_reason):
            print('Loopback eb_no_packet {}'.format(p_reason))

        print('Loopback start')
        self.assertEqual(self.m_serverV6.transport.getLoopbackMode(), 1)
        # l_addr = self.m_serverV6.transport.getHost()
        l_addr = node_discovery.PYHOUSE_MULTICAST_IP_V6
        print('Loopback B')
        l_joined_defer = self.m_serverV6.transport.joinGroup(l_addr)
        print('Loopback D')
        l_joined_defer.addCallback(cb_joined)
        l_joined_defer.addCallback(cb_packet)
        l_joined_defer.addCallback(cb_no_packet)
        l_joined_defer.addErrback(eb_no_packet)
        print('Loopback finished')
        return l_joined_defer

    def test_03_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        def cb_interfaces(_ignored):
            self.assertEqual(self.m_clientV6.transport.getOutgoingInterface(), "::1")
            self.assertEqual(self.m_serverV6.transport.getOutgoingInterface(), "::1")

        # self.assertEqual(self.m_clientV6.transport.getOutgoingInterface(), "::")
        # self.assertEqual(self.m_serverV6.transport.getOutgoingInterface(), "::")
        d1 = self.m_clientV6.transport.setOutgoingInterface("::1")
        PrettyPrintAny(d1, 'd1', 250)
        # d2 = self.m_serverV1transport.setOutgoingInterface("::1")
        # PrettyPrintAny(d2, 'd2', 250)
        l_result_defer = gatherResults([
                d1,
        #        d2
                ])
        l_result_defer.addCallback(cb_interfaces)
        return l_result_defer

    def test_04_joinLeave(self):
        """
        Test that a multicast group can be joined and left.
        """
        def cb_clientJoined(_ignored):
            return self.m_clientV6.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)

        def cb_clientLeft(_ignored):
            return self.m_serverV6.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)

        def cb_serverJoined(_ignored):
            return self.m_serverV6.transport.leaveGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)

        l_defer = self.m_clientV6.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)
        l_defer.addCallback(cb_clientJoined)
        l_defer.addCallback(cb_clientLeft)
        l_defer.addCallback(cb_serverJoined)
        return l_defer

    def test_05_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        return self.assertFailure(self.m_clientV6.transport.joinGroup("::"),
                                  error.MulticastJoinError)

    def test_06_multicast(self):
        """
        Test that a multicast group can be joined and messages sent to and received from it.
        """
        MESSAGE = "Test_006 A"
        def cb_joined(_ignored):
            l_defer = self.m_serverV6.m_packetReceived = Deferred()
            c.transport.write(MESSAGE, (node_discovery.PYHOUSE_MULTICAST_IP_V6, addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(self.m_serverV6.m_packets[0][0], MESSAGE)

        def cb_cleanup(passthrough):
            result = maybeDeferred(p.stopListening)
            result.addCallback(lambda _ign: passthrough)
            return result

        c = DummyServerV6()
        p = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(T_ALL_PORTS, c, interface = '::')
        addr = self.m_serverV6.transport.getHost()
        joined = self.m_serverV6.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)
        joined.addCallback(cb_joined)
        joined.addCallback(cb_packet)
        joined.addCallback(cb_cleanup)
        return joined

    def test_07_multiListen(self):
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
            l_result_defer = gatherResults([
                    maybeDeferred(firstPort.stopListening),
                    maybeDeferred(secondPort.stopListening)])
            l_result_defer.addCallback(lambda _ign: passthrough)
            return l_result_defer

        firstClient = DummyServerV6()
        firstPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(
                    T_ALL_PORTS, firstClient, listenMultiple = True, interface = '::')
        portno = firstPort.getHost().port
        secondClient = DummyServerV6()
        secondPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(
                    portno, secondClient, listenMultiple = True, interface = '::')
        theGroup = node_discovery.PYHOUSE_MULTICAST_IP_V6
        l_joined_defer = gatherResults([
                    self.m_serverV6.transport.joinGroup(theGroup),
                    firstPort.joinGroup(theGroup),
                    secondPort.joinGroup(theGroup)])
        l_joined_defer.addCallback(cb_serverJoined)
        l_joined_defer.addCallback(cb_gotPackets)
        l_joined_defer.addBoth(bb_cleanup)
        return l_joined_defer

# ## END DBK
