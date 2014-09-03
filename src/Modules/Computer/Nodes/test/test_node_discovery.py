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
from Modules.Utilities.tools import PrettyPrintAny


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


class TestServerV4(Mixin, node_discovery.ServerProtocolV4):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        super(TestServerV4, self).datagramReceived(p_data, p_addr)
        self.m_packets.append((p_data, p_addr))
        print("TestServer V4 packet {0:} - Addr:{1:}".format(p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class TestServerV6(Mixin, node_discovery.ServerProtocolV6):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        super(TestServerV6, self).datagramReceived(p_data, p_addr)
        self.m_packets.append((p_data, p_addr))
        print("TestServer V6 packet {0:} - Addr:{1:}".format(p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class TestClientV4(Mixin, node_discovery.ClientProtocolV4):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        super(TestClientV6, self).datagramReceived(p_data)
        self.m_packets.append(p_data)
        print("TestClient V4 packet {0:}".format(p_data))
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


class TestClientV6(Mixin, node_discovery.ClientProtocolV6):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        super(TestClientV6, self).datagramReceived(p_data)
        self.m_packets.append(p_data)
        print("TestClient V6 packet {0:}".format(p_data))
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


class Test_01(SetupMixin, unittest.TestCase):
    """
    Test creating test clients and servers
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor
        self.m_api = node_discovery.API()

    def test_0101_V4(self):
        l_server_v4 = TestServerV4()
        PrettyPrintAny(l_server_v4, 'Server V4')

    def test_0102_V6(self):
        l_server_v6 = TestServerV6()
        PrettyPrintAny(l_server_v6, 'Server V6')

    def test_0103_V4(self):
        l_client_v4 = TestClientV4()
        PrettyPrintAny(l_client_v4, 'Client V4')

    def test_0104_V6(self):
        l_client_v6 = TestClientV6()
        PrettyPrintAny(l_client_v6, 'Client V6')


class Test_04_V4(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor
        self.m_api = node_discovery.API()
        self.m_serverV4 = TestServerV4()
        self.m_clientV4 = TestClientV4()

    def XtearDown(self):
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])

    def test_0401_Ports(self):
        self.m_serverV4 = TestServerV4()
        self.m_port1 = self.m_reactor.listenMulticast(0, self.m_serverV4)
        self.m_port2 = self.m_reactor.listenMulticast(0, self.m_clientV4)
        PrettyPrintAny(self.m_port1, 'Port 1 V4')
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])


class Test_07_V6(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_reactor = self.m_pyhouse_obj.Twisted.Reactor
        self.m_api = node_discovery.API()
        self.m_serverV6 = TestServerV6()
        self.m_clientV6 = TestClientV6()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_serverV6)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_clientV6)
        self.m_clientV6.transport.connect("::1", self.m_serverV6.transport.getHost().port)

    def tearDown(self):
        return gatherResults([
                maybeDeferred(self.m_port1.stopListening),
                maybeDeferred(self.m_port2.stopListening)
                ])

    def test_0701(self):
        self.m_serverV6 = TestServerV6()
        self.m_port1 = self.m_reactor.listenMulticast(0, self.m_serverV6)
        self.m_port2 = self.m_reactor.listenMulticast(0, self.m_clientV6)
        PrettyPrintAny(self.m_port1, 'Port 1 V6')


class Test_15_V4(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_discovery.API()
        print("setUp V4")
        self.m_serverV4 = TestServerV4()
        self.m_clientV4 = TestClientV4()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_serverV4)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_clientV4)
        self.m_clientV4.transport.connect("127.0.0.1", self.m_serverV4.transport.getHost().port)

    def tearDown(self):
        return gatherResults([maybeDeferred(self.m_port1.stopListening), maybeDeferred(self.m_port2.stopListening)])


    def test_1501_TTL(self):
        for l_obj in self.m_clientV4, self.m_serverV4:
            PrettyPrintAny(l_obj, 'V4 Obj')
            self.assertEqual(l_obj.transport.getTTL(), 1)
            l_obj.transport.setTTL(2)
            self.assertEqual(l_obj.transport.getTTL(), 2)

    def test_1502_loopback(self):
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



    def test_1503_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        def cb_interfaces(_ignored):
            self.assertEqual(self.m_clientV4.transport.getOutgoingInterface(), "127.0.0.1")
            self.assertEqual(self.m_serverV4.transport.getOutgoingInterface(), "127.0.0.1")

        self.assertEqual(self.m_clientV4.transport.getOutgoingInterface(), "0.0.0.0")
        self.assertEqual(self.m_serverV4.transport.getOutgoingInterface(), "0.0.0.0")
        d1 = self.m_clientV4.transport.setOutgoingInterface("127.0.0.1")
        d2 = self.m_serverV4.transport.setOutgoingInterface("127.0.0.1")
        l_result_defer = gatherResults([d1, d2])
        l_result_defer.addCallback(cb_interfaces)
        return l_result_defer

    def test_1504_joinLeave(self):
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

    def test_1505_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        return self.assertFailure(self.m_clientV4.transport.joinGroup("127.0.0.1"), error.MulticastJoinError)

    def test_1506_multicast(self):
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

        c = TestServerV4()
        p = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, c)
        addr = self.m_serverV4.transport.getHost()
        joined = self.m_serverV4.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V4)
        joined.addCallback(cb_joined)
        joined.addCallback(cb_packet)
        joined.addCallback(cb_cleanup)
        return joined

    def test_1507_multiListen(self):
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

        firstClient = TestServerV4()
        firstPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, firstClient, listenMultiple = True)
        portno = firstPort.getHost().port
        secondClient = TestServerV4()
        secondPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(portno, secondClient, listenMultiple = True)
        theGroup = node_discovery.PYHOUSE_MULTICAST_IP_V4
        l_joined_defer = gatherResults([self.m_serverV4.transport.joinGroup(theGroup), firstPort.joinGroup(theGroup), secondPort.joinGroup(theGroup)])
        l_joined_defer.addCallback(cb_serverJoined)
        l_joined_defer.addCallback(cb_gotPackets)
        l_joined_defer.addBoth(bb_cleanup)
        return l_joined_defer



class Test_25_V6(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = node_discovery.API()
        print("setUp V6")
        self.m_serverV6 = TestServerV6()

        self.m_clientV6 = TestClientV6()
        self.m_port1 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_serverV6)
        self.m_port2 = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, self.m_clientV6)
        # self.m_clientV6.transport.connect("::1", self.m_serverV6.transport.getHost().port)

    def tearDown(self):
        return gatherResults([maybeDeferred(self.m_port1.stopListening), maybeDeferred(self.m_port2.stopListening)])


    def test_2501_TTL(self):
        for l_obj in self.m_clientV6, self.m_serverV6:
            PrettyPrintAny(l_obj, 'V6 obj')
            self.assertEqual(l_obj.transport.getTTL(), 1)
            l_obj.transport.setTTL(2)
            self.assertEqual(l_obj.transport.getTTL(), 2)

    def test_2502_loopback(self):
        """
        Test that after loopback mode has been set, multicast packets are delivered to their sender.
        """
        def cb_joined(_ignored):
            l_defer = self.m_serverV6.m_packetReceived = Deferred()
            self.m_serverV6.transport.write("Test_002 - A", (node_discovery.PYHOUSE_MULTICAST_IP_V6, l_addr.port))
            return l_defer

        def cb_packet(_ignored):
            self.assertEqual(len(self.m_serverV6.m_packets), 1)
            self.m_serverV6.transport.setLoopbackMode(0)
            self.assertEqual(self.m_serverV6.transport.getLoopbackMode(), 0)
            self.m_serverV6.transport.write("Test_002 - B", (node_discovery.PYHOUSE_MULTICAST_IP_V6, l_addr.port))
            l_defer = Deferred()
            self.m_pyhouse_obj.Twisted.Reactor.callLater(0, l_defer.callback, None)
            return l_defer

        def cb_no_packet(_ignored):
            self.assertEqual(len(self.m_serverV6.m_packets), 1)

        self.assertEqual(self.m_serverV6.transport.getLoopbackMode(), 1)
        l_addr = self.m_serverV6.transport.getHost()
        l_joined_defer = self.m_serverV6.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)
        l_joined_defer.addCallback(cb_joined)
        l_joined_defer.addCallback(cb_packet)
        l_joined_defer.addCallback(cb_no_packet)
        return l_joined_defer



    def test_2503_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        def cb_interfaces(_ignored):
            self.assertEqual(self.m_clientV6.transport.getOutgoingInterface(), "::1")
            self.assertEqual(self.m_serverV6.transport.getOutgoingInterface(), "::1")

        self.assertEqual(self.m_clientV6.transport.getOutgoingInterface(), "::")
        self.assertEqual(self.m_serverV6.transport.getOutgoingInterface(), "::")
        d1 = self.m_clientV6.transport.setOutgoingInterface("::1")
        d2 = self.m_serverV6.transport.setOutgoingInterface("::1")
        l_result_defer = gatherResults([d1, d2])
        l_result_defer.addCallback(cb_interfaces)
        return l_result_defer

    def test_2504_joinLeave(self):
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

    def test_2505_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        return self.assertFailure(self.m_clientV6.transport.joinGroup("::1"), error.MulticastJoinError)

    def test_2506_multicast(self):
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

        c = TestServerV6()
        p = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, c)
        addr = self.m_serverV6.transport.getHost()
        joined = self.m_serverV6.transport.joinGroup(node_discovery.PYHOUSE_MULTICAST_IP_V6)
        joined.addCallback(cb_joined)
        joined.addCallback(cb_packet)
        joined.addCallback(cb_cleanup)
        return joined

    def test_2507_multiListen(self):
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

        firstClient = TestServerV6()
        firstPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(0, firstClient, listenMultiple = True, interface = '::')
        portno = firstPort.getHost().port
        secondClient = TestServerV6()
        secondPort = self.m_pyhouse_obj.Twisted.Reactor.listenMulticast(portno, secondClient, listenMultiple = True, interface = '::')
        theGroup = node_discovery.PYHOUSE_MULTICAST_IP_V6
        l_joined_defer = gatherResults([self.m_serverV6.transport.joinGroup(theGroup), firstPort.joinGroup(theGroup), secondPort.joinGroup(theGroup)])
        l_joined_defer.addCallback(cb_serverJoined)
        l_joined_defer.addCallback(cb_gotPackets)
        l_joined_defer.addBoth(bb_cleanup)
        return l_joined_defer

# ## END DBK
