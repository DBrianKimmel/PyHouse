"""
PyHouse/src/core/test/test_nodes.py

Created on Mar 20, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for testing inter_node communication.
"""

from src.core import nodes
from src.core.data_objects import PyHouseData

from twisted.trial import unittest
from twisted.internet.defer import Deferred, gatherResults, maybeDeferred
from twisted.internet import protocol, error, defer, udp
from twisted.python import runtime


class Mixin:

    m_started = 0
    m_stopped = 0
    m_startedDeferred = None

    def __init__(self):
        self.packets = []

    def startProtocol(self):
        self.m_started = 1
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.callback(None)

    def stopProtocol(self):
        self.m_stopped = 1


class Server(Mixin, protocol.DatagramProtocol):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data, p_addr):
        self.packets.append((p_data, p_addr))
        if self.m_packetReceived is not None:
            l_defer, self.m_packetReceived = self.m_packetReceived, None
            l_defer.callback(None)


class Client(Mixin, protocol.ConnectedDatagramProtocol):
    m_packetReceived = None
    m_refused = 0

    def datagramReceived(self, p_data):
        self.packets.append(p_data)
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


class GoodClient(Server):

    def connectionRefused(self):
        if self.m_startedDeferred is not None:
            l_defer, self.m_startedDeferred = self.m_startedDeferred, None
            l_defer.errback(error.ConnectionRefusedError("yup"))
        self.m_refused = 1


class BadClientError(Exception):
    """
    Raised by BadClient at the end of every datagramReceived call to try and
    screw stuff up.
    """


class BadClient(protocol.DatagramProtocol):
    """
    A DatagramProtocol which always raises an exception from datagramReceived.
    Used to test error handling behavior in the reactor for that method.
    """
    m_defer = None

    def setDeferred(self, p_defer):
        """
        Set the Deferred which will be called back when datagramReceived is
        called.
        """
        self.m_defer = p_defer

    def datagramReceived(self, _bytes, _addr):
        if self.m_defer is not None:
            l_defer, self.m_defer = self.m_defer, None
            l_defer.callback(bytes)
        raise BadClientError("Application code is very buggy!")


class Test1(unittest.TestCase):

    def setUp(self):
        print("setUp")
        self.m_api = nodes.API()
        self.m_pyhouse_obj = PyHouseData()

    def tearDown(self):
        print("tearDown")

    def test_001_Init(self):
        print("Test 001")
        self.assertIsNotNone(self.m_api)

    def test_002_StartServer(self):
        print("Test 002")
        # self.m_api.StartServer(self.m_pyhouse_obj)
        # server = nodes.API()
        server = Server()
        l_defer = server.m_startedDeferred = defer.Deferred()
        p = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
        def cbStarted(_ignored):
            addr = p.getHost()
            print "addr = {0:}".format(addr)
            self.assertEqual(addr.type, 'UDP')
            return p.stopListening()
        return l_defer.addCallback(cbStarted)

    def test_003_StartClient(self):
        print("Test 003")
        # l_api = nodes.API()
        # l_pyhouse_obj = PyHouseData()
        # self.m_api._start_discovery_client(self.m_pyhouse_obj)

    def test_101_oldAddress(self):
        """
        The C{type} of the host address of a listening L{DatagramProtocol}'s transport is C{"UDP"}.
        """
        server = Server()
        l_defer = server.m_startedDeferred = defer.Deferred()
        p = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
        def cbStarted(_ignored):
            addr = p.getHost()
            self.assertEqual(addr.type, 'UDP')
            return p.stopListening()
        return l_defer.addCallback(cbStarted)

    def test_102_startStop(self):
        """
        The L{DatagramProtocol}'s C{startProtocol} and C{stopProtocol}
        methods are called when its transports starts and stops listening, respectively.
        """
        server = Server()
        l_defer = server.m_startedDeferred = defer.Deferred()
        port1 = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
        def cbStarted(_ignored):
            self.assertEqual(server.m_started, 1)
            self.assertEqual(server.m_stopped, 0)
            return port1.stopListening()
        def cbStopped(_ignored):
            self.assertEqual(server.m_stopped, 1)
        return l_defer.addCallback(cbStarted).addCallback(cbStopped)

    def test_103_rebind(self):
        """
        Re-listening with the same L{DatagramProtocol} re-invokes the C{startProtocol} callback.
        """
        server = Server()
        l_defer = server.m_startedDeferred = defer.Deferred()
        p = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")

        def cbStarted(_ignored, port):
            return port.stopListening()

        def cbStopped(_ignored):
            l_defer = server.m_startedDeferred = defer.Deferred()
            p = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
            return l_defer.addCallback(cbStarted, p)

        return l_defer.addCallback(cbStarted, p)

    def test_104_bindError(self):
        """
        A L{CannotListenError} exception is raised when attempting to bind a second protocol instance to an already bound port
        """
        server = Server()
        l_defer = server.m_startedDeferred = defer.Deferred()
        port = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = '127.0.0.1')

        def cbStarted(_ignored):
            self.assertEqual(port.getHost(), server.transport.getHost())
            server2 = Server()
            self.assertRaises(
                error.CannotListenError,
                self.m_pyhouse_obj.Reactor.listenUDP, port.getHost().port, server2,
                interface = '127.0.0.1')

        l_defer.addCallback(cbStarted)

        def cbFinished(_ignored):
            return port.stopListening()

        l_defer.addCallback(cbFinished)
        return l_defer

    def test_105_sendPackets(self):
        """
        Datagrams can be sent with the transport's C{write} method and received via the C{datagramReceived} callback method.
        """
        server = Server()
        serverStarted = server.m_startedDeferred = defer.Deferred()
        port1 = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
        client = GoodClient()
        clientStarted = client.m_startedDeferred = defer.Deferred()

        def cbServerStarted(_ignored):
            self.port2 = self.m_pyhouse_obj.Reactor.listenUDP(0, client, interface = "127.0.0.1")
            return clientStarted

        l_defer = serverStarted.addCallback(cbServerStarted)

        def cbClientStarted(_ignored):
            client.transport.connect("127.0.0.1", server.transport.getHost().port)
            cAddr = client.transport.getHost()
            sAddr = server.transport.getHost()

            serverSend = client.m_packetReceived = defer.Deferred()
            server.transport.write("hello", (cAddr.host, cAddr.port))

            clientWrites = [
                ("a",),
                ("b", None),
                ("c", (sAddr.host, sAddr.port))]

            def cbClientSend(_ignored):
                if clientWrites:
                    nextClientWrite = server.m_packetReceived = defer.Deferred()
                    nextClientWrite.addCallback(cbClientSend)
                    client.transport.write(*clientWrites.pop(0))
                    return nextClientWrite

            # No one will ever call .errback on either of these Deferreds,
            # but there is a non-trivial amount of test code which might
            # cause them to fail somehow.  So fireOnOneErrback=True.
            return defer.DeferredList([
                cbClientSend(None),
                serverSend],
                fireOnOneErrback = True)

        l_defer.addCallback(cbClientStarted)

        def cbSendsFinished(_ignored):
            cAddr = client.transport.getHost()
            sAddr = server.transport.getHost()
            self.assertEqual(
                client.packets,
                [("hello", (sAddr.host, sAddr.port))])
            clientAddr = (cAddr.host, cAddr.port)
            self.assertEqual(
                server.packets,
                [("a", clientAddr),
                 ("b", clientAddr),
                 ("c", clientAddr)])

        l_defer.addCallback(cbSendsFinished)

        def cbFinished(_ignored):
            return defer.DeferredList([
                defer.maybeDeferred(port1.stopListening),
                defer.maybeDeferred(self.port2.stopListening)],
                fireOnOneErrback = True)

        l_defer.addCallback(cbFinished)
        return l_defer

    def test_106_connectionRefused(self):
        """
        A L{ConnectionRefusedError} exception is raised when a connection attempt is actively refused by the other end.

        Note: This test assumes no one is listening on port 80 UDP.
        """
        client = GoodClient()
        clientStarted = client.m_startedDeferred = defer.Deferred()
        port = self.m_pyhouse_obj.Reactor.listenUDP(0, client, interface = "127.0.0.1")
        server = Server()
        serverStarted = server.m_startedDeferred = defer.Deferred()
        port2 = self.m_pyhouse_obj.Reactor.listenUDP(0, server, interface = "127.0.0.1")
        l_defer = defer.DeferredList([clientStarted, serverStarted], fireOnOneErrback = True)

        def cbStarted(_ignored):
            connectionRefused = client.m_startedDeferred = defer.Deferred()
            client.transport.connect("127.0.0.1", 80)
            for i in range(10):
                client.transport.write(str(i))
                server.transport.write(str(i), ("127.0.0.1", 80))
            return self.assertFailure(connectionRefused, error.ConnectionRefusedError)

        l_defer.addCallback(cbStarted)

        def cbFinished(_ignored):
            return defer.DeferredList([defer.maybeDeferred(port.stopListening), defer.maybeDeferred(port2.stopListening)], fireOnOneErrback = True)

        l_defer.addCallback(cbFinished)
        return l_defer

    def test_107_badConnect(self):
        """
        A call to the transport's connect method fails with a L{ValueError} when a non-IP address is passed as the host value.
        A call to a transport's connect method fails with a L{RuntimeError} when the transport is already connected.
        """
        client = GoodClient()
        port = self.m_pyhouse_obj.Reactor.listenUDP(0, client, interface = "127.0.0.1")
        self.assertRaises(ValueError, client.transport.connect, "localhost", 80)
        client.transport.connect("127.0.0.1", 80)
        self.assertRaises(RuntimeError, client.transport.connect, "127.0.0.1", 80)
        return port.stopListening()

    def test_108_datagramReceivedError(self):
        """
        When datagramReceived raises an exception it is logged but the port is not disconnected.
        """
        finalDeferred = defer.Deferred()

        def cbCompleted(_ign):
            """
            Flush the exceptions which the reactor should have logged and make
            sure they're actually there.
            """
            errs = self.flushLoggedErrors(BadClientError)
            self.assertEqual(len(errs), 2, "Incorrectly found %d errors, expected 2" % (len(errs),))
        finalDeferred.addCallback(cbCompleted)

        client = BadClient()
        port = self.m_pyhouse_obj.Reactor.listenUDP(0, client, interface = '127.0.0.1')

        def cbCleanup(result):
            """
            Disconnect the port we started and pass on whatever was given to us
            in case it was a Failure.
            """
            return defer.maybeDeferred(port.stopListening).addBoth(lambda _ign: result)

        finalDeferred.addBoth(cbCleanup)
        addr = port.getHost()

        # UDP is not reliable.  Try to send as many as 60 packets before giving up.
        # Conceivably, all sixty could be lost, but they probably won't be
        # unless all UDP traffic is being dropped, and then the rest of these
        # UDP tests will likely fail as well.  Ideally, this test (and probably
        # others) wouldn't even use actual UDP traffic: instead, they would
        # stub out the socket with a fake one which could be made to behave in
        # whatever way the test desires.  Unfortunately, this is hard because
        # of differences in various reactor implementations.
        attempts = range(60)
        succeededAttempts = []

        def makeAttempt():
            """
            Send one packet to the listening BadClient.  Set up a 0.1 second
            timeout to do re-transmits in case the packet is dropped.  When two
            packets have been received by the BadClient, stop sending and let
            the finalDeferred's callbacks do some assertions.
            """
            if not attempts:
                try:
                    self.fail("Not enough packets received")
                except:
                    finalDeferred.errback()

            self.failIfIdentical(client.transport, None, "UDP Protocol lost its transport")

            packet = str(attempts.pop(0))
            packetDeferred = defer.Deferred()
            client.setDeferred(packetDeferred)
            client.transport.write(packet, (addr.host, addr.port))

            def cbPacketReceived(packet):
                """
                A packet arrived.  Cancel the timeout for it, record it, and
                maybe finish the test.
                """
                timeoutCall.cancel()
                succeededAttempts.append(packet)
                if len(succeededAttempts) == 2:
                    # The second error has not yet been logged, since the
                    # exception which causes it hasn't even been raised yet.
                    # Give the datagramReceived call a chance to finish, then
                    # let the test finish asserting things.
                    self.m_pyhouse_obj.Reactor.callLater(0, finalDeferred.callback, None)
                else:
                    makeAttempt()

            def ebPacketTimeout(_err):
                """
                The packet wasn't received quickly enough.  Try sending another
                one.  It doesn't matter if the packet for which this was the
                timeout eventually arrives: makeAttempt throws away the
                Deferred on which this function is the errback, so when
                datagramReceived callbacks, so it won't be on this Deferred, so
                it won't raise an AlreadyCalledError.
                """
                makeAttempt()

            packetDeferred.addCallbacks(cbPacketReceived, ebPacketTimeout)
            packetDeferred.addErrback(finalDeferred.errback)

            timeoutCall = self.m_pyhouse_obj.Reactor.callLater(0.1, packetDeferred.errback, error.TimeoutError("Timed out in testDatagramReceivedError"))

        makeAttempt()
        return finalDeferred

    def test_109_portRepr(self):
        """
        The port number being listened on can be found in the string returned from calling repr() on L{twisted.internet.udp.Port}.
        """
        client = GoodClient()
        p = self.m_pyhouse_obj.Reactor.listenUDP(0, client)
        portNo = str(p.getHost().port)
        self.failIf(repr(p).find(portNo) == -1)
        def stoppedListening(_ign):
            self.failIf(repr(p).find(portNo) != -1)
        l_defer = defer.maybeDeferred(p.stopListening)
        l_defer.addCallback(stoppedListening)
        return l_defer

    def test_110_NoWarningOnBroadcast(self):
        """
        C{'<broadcast>'} is an alternative way to say C{'255.255.255.255'}
        ({socket.gethostbyname("<broadcast>")} returns C{'255.255.255.255'}),
        so because it becomes a valid IP address, no deprecation warning about
        passing hostnames to L{twisted.internet.udp.Port.write} needs to be
        emitted by C{write()} in this case.
        """
        class fakeSocket:
            def sendto(self, foo, bar):
                pass

        p = udp.Port(0, Server())
        p.socket = fakeSocket()
        p.write("test", ("<broadcast>", 1234))

        warnings = self.flushWarnings([self.test_110_NoWarningOnBroadcast])
        self.assertEqual(len(warnings), 0)


class Test2ReactorShutdownInteraction(unittest.TestCase):
    """Test reactor shutdown interaction"""

    def setUp(self):
        """Start a UDP port"""
        self.m_pyhouse_obj = PyHouseData()
        self.server = Server()
        self.port = self.m_pyhouse_obj.Reactor.listenUDP(0, self.server, interface = '127.0.0.1')

    def tearDown(self):
        """Stop the UDP port"""
        return self.port.stopListening()

    def test_201_ShutdownFromDatagramReceived(self):
        """Test reactor shutdown while in a recvfrom() loop"""

        # udp.Port's doRead calls recvfrom() in a loop, as an optimization.
        # It is important this loop terminate under various conditions.
        # Previously, if datagramReceived synchronously invoked reactor.stop(),
        # under certain reactors, the Port's socket would synchronously disappear, causing an AttributeError inside that loop.
        # This was mishandled, causing the loop to spin forever.
        # This test is primarily to ensure that the loop never spins forever.

        finished = defer.Deferred()
        pr = self.server.m_packetReceived = defer.Deferred()

        def pktRece(_ignored):
            # Simulate reactor.stop() behavior :(
            self.server.transport.connectionLost()
            # Then delay this Deferred chain until the protocol has been
            # disconnected, as the reactor should do in an error condition
            # such as we are inducing.  This is very much a whitebox test.
            self.m_pyhouse_obj.Reactor.callLater(0, finished.callback, None)
        pr.addCallback(pktRece)

        def flushErrors(_ignored):
            # We are breaking abstraction and calling private APIs, any
            # number of horrible errors might occur.  As long as the reactor
            # doesn't hang, this test is satisfied.  (There may be room for
            # another, stricter test.)
            self.flushLoggedErrors()
        finished.addCallback(flushErrors)
        self.server.transport.write('\0' * 64, ('127.0.0.1', self.server.transport.getHost().port))
        return finished


class Test3MulticastTestCase(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.server = Server()
        self.client = Client()
        # multicast won't work if we listen over loopback, apparently
        self.port1 = self.m_pyhouse_obj.Reactor.listenMulticast(0, self.server)
        self.port2 = self.m_pyhouse_obj.Reactor.listenMulticast(0, self.client)
        self.client.transport.connect("127.0.0.1", self.server.transport.getHost().port)

    def tearDown(self):
        return gatherResults([
            maybeDeferred(self.port1.stopListening),
            maybeDeferred(self.port2.stopListening)])

    def test_301_TTL(self):
        for o in self.client, self.server:
            self.assertEqual(o.transport.getTTL(), 1)
            o.transport.setTTL(2)
            self.assertEqual(o.transport.getTTL(), 2)

    def test_302_loopback(self):
        """
        Test that after loopback mode has been set, multicast packets are delivered to their sender.
        """
        self.assertEqual(self.server.transport.getLoopbackMode(), 1)
        addr = self.server.transport.getHost()
        joined = self.server.transport.joinGroup("225.0.0.250")

        def cbJoined(_ignored):
            l_defer = self.server.m_packetReceived = Deferred()
            self.server.transport.write("hello", ("225.0.0.250", addr.port))
            return l_defer

        joined.addCallback(cbJoined)

        def cbPacket(_ignored):
            self.assertEqual(len(self.server.packets), 1)
            self.server.transport.setLoopbackMode(0)
            self.assertEqual(self.server.transport.getLoopbackMode(), 0)
            self.server.transport.write("hello", ("225.0.0.250", addr.port))
            # This is fairly lame.
            l_defer = Deferred()
            self.m_pyhouse_obj.Reactor.callLater(0, l_defer.callback, None)
            return l_defer

        joined.addCallback(cbPacket)

        def cbNoPacket(_ignored):
            self.assertEqual(len(self.server.packets), 1)

        joined.addCallback(cbNoPacket)
        return joined

    def test_303_interface(self):
        """
        Test C{getOutgoingInterface} and C{setOutgoingInterface}.
        """
        self.assertEqual(self.client.transport.getOutgoingInterface(), "0.0.0.0")
        self.assertEqual(self.server.transport.getOutgoingInterface(), "0.0.0.0")
        d1 = self.client.transport.setOutgoingInterface("127.0.0.1")
        d2 = self.server.transport.setOutgoingInterface("127.0.0.1")
        result = gatherResults([d1, d2])

        def cbInterfaces(_ignored):
            self.assertEqual(
                self.client.transport.getOutgoingInterface(), "127.0.0.1")
            self.assertEqual(
                self.server.transport.getOutgoingInterface(), "127.0.0.1")

        result.addCallback(cbInterfaces)
        return result

    def test_304_joinLeave(self):
        """
        Test that multicast a group can be joined and left.
        """
        l_defer = self.client.transport.joinGroup("225.0.0.250")

        def clientJoined(_ignored):
            return self.client.transport.leaveGroup("225.0.0.250")
        l_defer.addCallback(clientJoined)

        def clientLeft(_ignored):
            return self.server.transport.joinGroup("225.0.0.250")
        l_defer.addCallback(clientLeft)

        def serverJoined(_ignored):
            return self.server.transport.leaveGroup("225.0.0.250")
        l_defer.addCallback(serverJoined)

        return l_defer

    def test_305_joinFailure(self):
        """
        Test that an attempt to join an address which is not a multicast address fails with L{error.MulticastJoinError}.
        """
        # 127.0.0.1 is not a multicast address, so joining it should fail.
        return self.assertFailure(
            self.client.transport.joinGroup("127.0.0.1"),
            error.MulticastJoinError)

    def test_306_multicast(self):
        """
        Test that a multicast group can be joined and messages sent to and received from it.
        """
        c = Server()
        p = self.m_pyhouse_obj.Reactor.listenMulticast(0, c)
        addr = self.server.transport.getHost()
        joined = self.server.transport.joinGroup("225.0.0.250")

        def cbJoined(_ignored):
            l_defer = self.server.m_packetReceived = Deferred()
            c.transport.write("hello world", ("225.0.0.250", addr.port))
            return l_defer
        joined.addCallback(cbJoined)

        def cbPacket(_ignored):
            self.assertEqual(self.server.packets[0][0], "hello world")
        joined.addCallback(cbPacket)

        def cleanup(passthrough):
            result = maybeDeferred(p.stopListening)
            result.addCallback(lambda _ign: passthrough)
            return result
        joined.addCallback(cleanup)
        return joined

    def test_307_multiListen(self):
        """
        Test that multiple sockets can listen on the same multicast port and
        that they both receive multicast messages directed to that address.
        """
        firstClient = Server()
        firstPort = self.m_pyhouse_obj.Reactor.listenMulticast(0, firstClient, listenMultiple = True)
        portno = firstPort.getHost().port
        secondClient = Server()
        secondPort = self.m_pyhouse_obj.Reactor.listenMulticast(portno, secondClient, listenMultiple = True)
        theGroup = "225.0.0.250"
        joined = gatherResults([self.server.transport.joinGroup(theGroup), firstPort.joinGroup(theGroup), secondPort.joinGroup(theGroup)])

        def serverJoined(_ignored):
            d1 = firstClient.m_packetReceived = Deferred()
            d2 = secondClient.m_packetReceived = Deferred()
            firstClient.transport.write("hello world", (theGroup, portno))
            return gatherResults([d1, d2])

        joined.addCallback(serverJoined)

        def gotPackets(_ignored):
            self.assertEqual(firstClient.packets[0][0], "hello world")
            self.assertEqual(secondClient.packets[0][0], "hello world")

        joined.addCallback(gotPackets)

        def cleanup(passthrough):
            result = gatherResults([
                maybeDeferred(firstPort.stopListening),
                maybeDeferred(secondPort.stopListening)])
            result.addCallback(lambda _ign: passthrough)
            return result

        joined.addBoth(cleanup)
        return joined





# if __name__ == '__main__':
#    unittest.main(verbosity = 2)

    # ## END DBK
