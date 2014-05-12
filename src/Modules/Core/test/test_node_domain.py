"""
@name: PyHouse/Modules/Core/node_domain.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Apr 25, 2014
@license: MIT License
@summary: This module is for testing the AMP request/response protocol

This code was taken of some test for the twisted AMP module but it has been changed almost
completely to what we need.
"""

"""
Tests for L{twisted.protocols.amp}.
"""

# Import system type stuff
# from twisted.python import filepath
from twisted.python.failure import Failure
from twisted.protocols import amp
from twisted.trial import unittest
from twisted.internet import protocol, defer, error, reactor  # , interfaces
from twisted.test import iosim
from twisted.test.proto_helpers import StringTransport

# Import PyMh files and modules.
from Modules.Core import node_domain
# from Modules.Core.data_objects import PyHouseData

class TestProtocol(protocol.Protocol):

    def __init__(self, onConnLost, dataToSend):
        self.onConnLost = onConnLost
        self.dataToSend = dataToSend

    def connectionMade(self):
        self.data = []
        self.transport.write(self.dataToSend)

    def dataReceived(self, p_bytes):
        self.data.append(p_bytes)
        # self.transport.loseConnection()

    def connectionLost(self, _p_reason):
        self.onConnLost.callback(self.data)



class XXSimpleSymmetricProtocol(amp.AMP):

    def XXXsendHello(self, text):
        print('SimpleSymetricProtocol sendHello.')
        return self.callRemoteString(
            "hello",
            hello = text)

    def XXamp_HELLO(self, box):
        return amp.Box(hello = box['hello'])

    def XXamp_HOWDOYOUDO(self, _p_box):
        return amp.QuitBox(howdoyoudo = 'world')



class UnfriendlyGreeting(Exception):
    """Greeting was insufficiently kind.
    """

class DeathThreat(Exception):
    """Greeting was insufficiently kind.
    """

class UnknownProtocol(Exception):
    """Asked to switch to the wrong protocol.
    """


class TransportPeer(amp.Argument):
    # this serves as some informal documentation for how to get variables from
    # the protocol or your environment and pass them to methods as arguments.
    def retrieve(self, _p_d, _p_name, _p_proto):
        return ''

    def fromStringProto(self, _p_notAString, p_proto):
        return p_proto.transport.getPeer()

    def toBox(self, _p_name, _p_strings, _p_objects, _p_proto):
        return


class Hello(amp.Command):
    commandName = 'hello'
    arguments = [('hello', amp.String()),
                 ('optional', amp.Boolean(optional = True)),
                 ('print', amp.Unicode(optional = True)),
                 ('from', TransportPeer(optional = True)),
                 ('mixedCase', amp.String(optional = True)),
                 ('dash-arg', amp.String(optional = True)),
                 ('underscore_arg', amp.String(optional = True))]
    response = [('hello', amp.String()),
                ('print', amp.Unicode(optional = True))]
    errors = {UnfriendlyGreeting: 'UNFRIENDLY'}
    fatalErrors = {DeathThreat: 'DEAD'}


class NoAnswerHello(Hello):
    commandName = Hello.commandName
    requiresAnswer = False


class FutureHello(amp.Command):
    commandName = 'hello'
    arguments = [('hello', amp.String()),
                 ('optional', amp.Boolean(optional = True)),
                 ('print', amp.Unicode(optional = True)),
                 ('from', TransportPeer(optional = True)),
                 ('bonus', amp.String(optional = True)),
                 # addt'l arguments should generally be added at the end, and be optional...
                 ]
    response = [('hello', amp.String()),
                ('print', amp.Unicode(optional = True))]
    errors = {UnfriendlyGreeting: 'UNFRIENDLY'}


class BrokenReturn(amp.Command):
    """ An example of a perfectly good command, but the handler is going to return None...
    """
    commandName = 'broken_return'


class Goodbye(amp.Command):
    # commandName left blank on purpose: this tests implicit command names.
    response = [('goodbye', amp.String())]
    responseType = amp.QuitBox


class WaitForever(amp.Command):
    commandName = 'wait_forever'


class GetList(amp.Command):
    commandName = 'getlist'
    arguments = [('length', amp.Integer())]
    response = [('body', amp.AmpList([('x', amp.Integer())]))]


class SecuredPing(amp.Command):
    # TO DO: actually make this refuse to send over an insecure connection
    response = [('pinged', amp.Boolean())]


class TestSwitchProto(amp.ProtocolSwitchCommand):
    commandName = 'Switch-Proto'
    arguments = [
        ('name', amp.String()),
        ]
    errors = {UnknownProtocol: 'UNKNOWN'}


class SingleUseFactory(protocol.ClientFactory):
    def __init__(self, proto):
        self.proto = proto
        self.proto.factory = self

    def buildProtocol(self, _p_addr):
        l_pump, self.proto = self.proto, None
        return l_pump

    reasonFailed = None

    def clientConnectionFailed(self, _p_connector, reason):
        self.reasonFailed = reason
        return

THING_I_DONT_UNDERSTAND = 'gwebol nargo'
class ThingIDontUnderstandError(Exception):
    pass

class FactoryNotifier(amp.AMP):
    factory = None
    def connectionMade(self):
        if self.factory is not None:
            self.factory.theProto = self
            if hasattr(self.factory, 'onMade'):
                self.factory.onMade.callback(None)


class SimpleSymmetricCommandProtocol(FactoryNotifier):
    maybeLater = None
    greeted = False

    def __init__(self, onConnLost = None):
        amp.AMP.__init__(self)
        self.onConnLost = onConnLost

    def sendHello(self, p_text):
        # TODO:
        print('DBK SimpleSymetricCommandProtocol - sendHello')
        return self.callRemote(Hello, hello = p_text, mixedCase = 'DBK - mixedCase - SimpleSymetricCommandProtocol')

    def sendInfo(self, p_text):
        print('DBK SimpleSymetricCommandProtocol - sendHello')
        return self.callRemote(node_domain.NodeInformationCommand, Name = p_text, Address = '192.168.1.2')

    def receive_Hello(self, hello, From, optional = None, Print = None, mixedCase = None, dash_arg = None, underscore_arg = None):
        From = From; optional = optional; Print = Print; mixedCase = mixedCase; dash_arg = dash_arg; underscore_arg = underscore_arg
        assert From == self.transport.getPeer()
        if hello == THING_I_DONT_UNDERSTAND:
            raise ThingIDontUnderstandError()
        if hello.startswith('screw'):
            raise UnfriendlyGreeting("Don't be a dick.")
        if hello == 'die':
            raise DeathThreat("aieeeeeeeee")
        result = dict(hello = hello, mixedCase = mixedCase)
        if Print is not None:
            result.update(dict(Print = Print))
        self.greeted = True
        print('DBK SimpleSymetricCommandProtocol - receive_Hello = {0:}'.format(result))
        return result
    Hello.responder(receive_Hello)

    """
    def cmdHello2(self, hello2, From, optional = None, Print = None, mixedCase = None, dash_arg = None, underscore_arg = None):
        From = From; optional = optional; Print = Print; mixedCase = mixedCase; dash_arg = dash_arg; underscore_arg = underscore_arg
        assert From == self.transport.getPeer()
        if hello2 == THING_I_DONT_UNDERSTAND:
            raise ThingIDontUnderstandError()
        if hello2.startswith('screw'):
            raise UnfriendlyGreeting("Don't be a dick.")
        if hello2 == 'die':
            raise DeathThreat("aieeeeeeeee")
        result = dict(hello2 = hello2)
        if Print is not None:
            result.update(dict(Print = Print))
        self.greeted = True
        print('DBK in cmdHello2 {0:} {1:}'.format(result, From))
        return result
    Hello2.responder(cmdHello2)
    """

    def cmdGetlist(self, length):
        return {'body': [dict(x = 1)] * length}
    GetList.responder(cmdGetlist)

    def waitforit(self):
        self.waiting = defer.Deferred()
        return self.waiting
    WaitForever.responder(waitforit)

    def saybye(self):
        return dict(goodbye = "everyone")
    Goodbye.responder(saybye)

    def switchToTestProtocol(self, fail = False):
        if fail:
            name = 'no-proto'
        else:
            name = 'test-proto'
        l_pump = TestProtocol(self.onConnLost, SWITCH_CLIENT_DATA)
        return self.callRemote(
            TestSwitchProto,
            SingleUseFactory(l_pump), name = name).addCallback(lambda _ign: l_pump)

    def switchit(self, name):
        if name == 'test-proto':
            return TestProtocol(self.onConnLost, SWITCH_SERVER_DATA)
        raise UnknownProtocol(name)
    TestSwitchProto.responder(switchit)

    def donothing(self):
        return None
    BrokenReturn.responder(donothing)


class DeferredSymmetricCommandProtocol(SimpleSymmetricCommandProtocol):
    def switchit(self, name):
        if name == 'test-proto':
            self.maybeLaterProto = TestProtocol(self.onConnLost, SWITCH_SERVER_DATA)
            self.maybeLater = defer.Deferred()
            return self.maybeLater
        raise UnknownProtocol(name)
    TestSwitchProto.responder(switchit)

class BadNoAnswerCommandProtocol(SimpleSymmetricCommandProtocol):
    def badResponder(self, hello, From, optional = None, Print = None, mixedCase = None, dash_arg = None, underscore_arg = None):
        """
        This responder does nothing and forgets to return a dictionary.
        """
    NoAnswerHello.responder(badResponder)

class NoAnswerCommandProtocol(SimpleSymmetricCommandProtocol):
    def goodNoAnswerResponder(self, hello, From, optional = None, Print = None, mixedCase = None, dash_arg = None, underscore_arg = None):
        From = From; optional = optional; Print = Print; mixedCase = mixedCase; dash_arg = dash_arg; underscore_arg = underscore_arg
        return dict(hello = hello + "-noanswer")
    NoAnswerHello.responder(goodNoAnswerResponder)


def connectedServerAndClient(ServerClass = SimpleSymmetricCommandProtocol, ClientClass = SimpleSymmetricCommandProtocol, *args, **kwargs):
    """Returns a 3-tuple: (client, server, pump)
    """
    return iosim.connectedServerAndClient(ServerClass, ClientClass, *args, **kwargs)


class TotallyDumbProtocol(protocol.Protocol):
    buf = ''
    def dataReceived(self, data):
        self.buf += data

class LiteralAmp(amp.AMP):
    def __init__(self):
        self.boxes = []

    def ampBoxReceived(self, box):
        self.boxes.append(box)
        return


"""  ========================================================================================
This section will test the dispatcher.
Data will NOT actually be sent.
"""

class FakeLocator(object):
    """
    This is a fake implementation of the interface implied by L{CommandLocator}.
    """
    def __init__(self):
        """
        Remember the given keyword arguments as a set of responders.
        """
        self.commands = {}

    def locateResponder(self, commandName):
        """
        Look up and return a function passed as a keyword argument of the given name to the constructor.
        """
        return self.commands[commandName]


class FakeSender:
    """
    This is a fake implementation of the 'box sender' interface implied by L{AMP}.
    """
    def __init__(self):
        """
        Create a fake sender and initialize the list of received boxes and unhandled errors.
        """
        self.sentBoxes = []
        self.unhandledErrors = []
        self.expectedErrors = 0

    def expectError(self):
        """
        Expect one error, so that the test doesn't fail.
        """
        self.expectedErrors += 1

    def sendBox(self, box):
        """
        Accept a box, but don't do anything.
        """
        self.sentBoxes.append(box)

    def unhandledError(self, failure):
        """
        Deal with failures by instantly re-raising them for easier debugging.
        """
        self.expectedErrors -= 1
        if self.expectedErrors < 0:
            failure.raiseException()
        else:
            self.unhandledErrors.append(failure)


class Test_02_CommandDispatch(unittest.TestCase):
    """
    The AMP CommandDispatcher class dispatches converts AMP boxes into commands and responses using Command.responder decorator.

    Note: Originally, AMP's factoring was such that many tests for this functionality are now implemented as full round-trip tests in L{AMPTest}.
    Future tests should be written at this level instead, to ensure API compatibility and to provide more granular, readable units of test coverage.
    """

    def setUp(self):
        """
        Create a dispatcher to use.
        """
        self.locator = FakeLocator()
        self.sender = FakeSender()
        self.dispatcher = amp.BoxDispatcher(self.locator)
        self.dispatcher.startReceivingBoxes(self.sender)

    def test_0201_receivedAsk(self):
        """
        L{CommandDispatcher.ampBoxReceived} should locate the appropriate command in its responder lookup, based on the '_ask' key.
        """
        received = []
        def thunk(box):
            received.append(box)
            return amp.Box({"hello": "goodbye"})
        l_input = amp.Box(_command = "hello", _ask = "test-command-id", hello = "world")
        self.locator.commands['hello'] = thunk
        self.dispatcher.ampBoxReceived(l_input)
        self.assertEquals(received, [l_input])

    def test_0202_sendUnhandledError(self):
        """
        L{CommandDispatcher} should relay its unhandled errors in responding to boxes to its boxSender.
        """
        err = RuntimeError("something went wrong, oh no")
        self.sender.expectError()
        self.dispatcher.unhandledError(Failure(err))
        self.assertEqual(len(self.sender.unhandledErrors), 1)
        self.assertEqual(self.sender.unhandledErrors[0].value, err)

    def test_0203_unhandledSerializationError(self):
        """
        Errors during serialization ought to be relayed to the sender's unhandledError method.
        """
        err = RuntimeError("something undefined went wrong")
        def thunk(_result):
            class BrokenBox(amp.Box):
                def _sendTo(self, proto):
                    raise err
            return BrokenBox()
        self.locator.commands['hello'] = thunk
        l_input = amp.Box(_command = "hello", _ask = "test-command-id", hello = "world")
        self.sender.expectError()
        self.dispatcher.ampBoxReceived(l_input)
        self.assertEquals(len(self.sender.unhandledErrors), 1)
        self.assertEquals(self.sender.unhandledErrors[0].value, err)

    def Xtest_0204_callRemote(self):
        """
        L{CommandDispatcher.callRemote} should emit a properly formatted '_ask' box to its boxSender and record an outstanding L{Deferred}.
        When a corresponding '_answer' packet is received, the L{Deferred} should be fired,
         and the results translated via the given L{Command}'s response de-serialization.
        """
        l_defer = self.dispatcher.callRemote(Hello, hello = 'world_0204')
        self.assertEquals(self.sender.sentBoxes, [amp.AmpBox(_command = "hello", _ask = "1", hello = "world_0204")])
        answers = []
        l_defer.addCallback(answers.append)
        self.assertEquals(answers, [])
        self.dispatcher.ampBoxReceived(amp.AmpBox({'hello': "yay", 'print': "ignored", '_answer': "1"}))
        self.assertEquals(answers, [dict(hello = "yay", Print = u"ignored")])

    def test_0205_DBK_NodeInfo(self):
        l_defer = self.dispatcher.callRemote(node_domain.NodeInformationCommand, Name = 'DBK - 0205')
        self.assertEquals(self.sender.sentBoxes, [amp.AmpBox(_command = "NodeInformationCommand", _ask = "1", Name = "DBK - 0205")])
        answers = []
        l_defer.addCallback(answers.append)
        self.assertEquals(answers, [])
        self.dispatcher.ampBoxReceived(amp.AmpBox({'Answer': "yay-0205", 'Name': "Marcia", '_answer': "1"}))
        print('Answers {0:}'.format(answers))
        self.assertEquals(answers, [dict(Answer = "yay-0205", Name = "Marcia")])


"""  ========================================================================================
This section will test command locators

The CommandLocator should enable users to specify responders to commands as functions that take structured objects, annotated with metadata.
"""

class SimpleGreeting(amp.Command):
    """
    A very simple greeting command that uses a few basic argument types.
    """
    commandName = 'simple'
    arguments = [('greeting', amp.Unicode()),
                 ('cookie', amp.Integer())]
    response = [('cookieplus', amp.Integer())]


class TestLocator(amp.CommandLocator):
    """
    A locator which implements a responder to a 'hello' command.
    """
    def __init__(self):
        self.greetings = []

    def greetingResponder(self, greeting, cookie):
        self.greetings.append((greeting, cookie))
        return dict(cookieplus = cookie + 3)
    greetingResponder = SimpleGreeting.responder(greetingResponder)


class OverrideLocatorAMP(amp.AMP):

    def __init__(self):
        amp.AMP.__init__(self)
        self.customResponder = object()
        self.expectations = {"custom": self.customResponder}
        self.greetings = []

    def lookupFunction(self, name):
        """
        Override the deprecated lookupFunction function.
        """
        if name in self.expectations:
            result = self.expectations[name]
            return result
        else:
            return super(OverrideLocatorAMP, self).lookupFunction(name)

    def greetingResponder(self, greeting, cookie):
        self.greetings.append((greeting, cookie))
        return dict(cookieplus = cookie + 3)
    greetingResponder = SimpleGreeting.responder(greetingResponder)


class Test_03_CommandLocator(unittest.TestCase):
    """
    The CommandLocator should enable users to specify responders to commands as functions that take structured objects, annotated with metadata.
    """

    def test_0301_responderDecorator(self):
        """
        A method on a L{CommandLocator} subclass decorated with a L{Command} subclass's L{responder} decorator should be returned from
        locateResponder, wrapped in logic to serialize and deserialize its arguments.
        """
        locator = TestLocator()
        responderCallable = locator.locateResponder("simple")
        result = responderCallable(amp.Box(greeting = "ni hao", cookie = "5"))
        def done(values):
            self.assertEquals(values, amp.AmpBox(cookieplus = '8'))
        return result.addCallback(done)

    def Xtest_0302_lookupFunctionDeprecatedOverride(self):
        """
        Subclasses which override locateResponder under its old name, lookupFunction, should have the override invoked instead.
        (This tests an AMP subclass, because in the version of the code that could invoke this deprecated code path, there was no L{CommandLocator}.)
        """
        locator = OverrideLocatorAMP()
        customResponderObject = self.assertWarns(PendingDeprecationWarning, "Override locateResponder, not lookupFunction.",
                                        __file__, lambda : locator.locateResponder("custom"))
        self.assertEquals(locator.customResponder, customResponderObject)
        # Make sure upcalling works too
        normalResponderObject = self.assertWarns(PendingDeprecationWarning, "Override locateResponder, not lookupFunction.",
                                        __file__, lambda : locator.locateResponder("simple"))
        result = normalResponderObject(amp.Box(greeting = "ni hao", cookie = "5"))
        def done(values):
            self.assertEquals(values, amp.AmpBox(cookieplus = '8'))
        return result.addCallback(done)

    def Xtest_0303_lookupFunctionDeprecatedInvoke(self):
        """
        Invoking locateResponder under its old name, lookupFunction, should emit a deprecation warning, but do the same thing.
        """
        locator = TestLocator()
        responderCallable = self.assertWarns(PendingDeprecationWarning, "Call locateResponder, not lookupFunction.", __file__,
            lambda : locator.lookupFunction("simple"))
        result = responderCallable(amp.Box(greeting = "ni hao", cookie = "5"))
        def done(values):
            self.assertEquals(values, amp.AmpBox(cookieplus = '8'))
        return result.addCallback(done)



"""  ========================================================================================
This section will test binary box protocols
"""

SWITCH_CLIENT_DATA = 'Success!'
SWITCH_SERVER_DATA = 'No, really.  Success.'

class Test_04_BinaryProtocol(unittest.TestCase):
    """
    Tests for L{amp.BinaryBoxProtocol}.

    @ivar _boxSender: After C{startReceivingBoxes} is called, the L{IBoxSender} which was passed to it.
    """

    def setUp(self):
        """
        Keep track of all boxes received by this test in its capacity as an L{IBoxReceiver} implementor.
        """
        self.boxes = []
        self.data = []

    def startReceivingBoxes(self, sender):
        """
        Implement L{IBoxReceiver.startReceivingBoxes} to just remember the value passed in.
        """
        self._boxSender = sender

    def ampBoxReceived(self, box):
        """
        A box was received by the protocol.
        """
        self.boxes.append(box)

    stopReason = None
    def stopReceivingBoxes(self, reason):
        """
        Record the reason that we stopped receiving boxes.
        """
        self.stopReason = reason

    # fake ITransport
    def getPeer(self):
        return 'no peer'

    def getHost(self):
        return 'no host'

    def write(self, data):
        self.data.append(data)

    def test_0401_startReceivingBoxes(self):
        """
        When L{amp.BinaryBoxProtocol} is connected to a transport, it calls C{startReceivingBoxes} on its L{IBoxReceiver} with itself
         as the L{IBoxSender} parameter.
        """
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(None)
        self.assertIdentical(self._boxSender, protocol)

    def Xtest_0402_sendBoxInStartReceivingBoxes(self):
        """
        The L{IBoxReceiver} which is started when L{amp.BinaryBoxProtocol} is connected to a transport can call C{sendBox} on the L{IBoxSender}
        passed to it before C{startReceivingBoxes} returns and have that box sent.
        """
        class SynchronouslySendingReceiver:
            def startReceivingBoxes(self, sender):
                sender.sendBox(amp.Box({'foo': 'bar'}))

        transport = StringTransport()
        protocol = amp.BinaryBoxProtocol(SynchronouslySendingReceiver())
        protocol.makeConnection(transport)
        self.assertEqual(transport.value(), '\x00\x03foo\x00\x03bar\x00\x00')

    def Xtest_0403_receiveBoxStateMachine(self):
        """
        When a binary box protocol receives:
            * a key
            * a value
            * an empty string
        it should emit a box and send it to its boxReceiver.
        """
        a = amp.BinaryBoxProtocol(self)
        a.stringReceived("hello")
        a.stringReceived("world")
        a.stringReceived("")
        self.assertEquals(self.boxes, [amp.AmpBox(hello = "world")])

    def Xtest_0404_firstBoxFirstKeyExcessiveLength(self):
        """
        L{amp.BinaryBoxProtocol} drops its connection if the length prefix for the first a key it receives is larger than 255.
        """
        transport = StringTransport()
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(transport)
        protocol.dataReceived('\x01\x00')
        self.assertTrue(transport.disconnecting)

    def Xtest_0405_firstBoxSubsequentKeyExcessiveLength(self):
        """
        L{amp.BinaryBoxProtocol} drops its connection if the length prefix for a subsequent key in the first box it receives is larger than 255.
        """
        transport = StringTransport()
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(transport)
        protocol.dataReceived('\x00\x01k\x00\x01v')
        self.assertFalse(transport.disconnecting)
        protocol.dataReceived('\x01\x00')
        self.assertTrue(transport.disconnecting)

    def Xtest_0406_subsequentBoxFirstKeyExcessiveLength(self):
        """
        L{amp.BinaryBoxProtocol} drops its connection if the length prefix for the first key in a subsequent box it receives is larger than 255.
        """
        transport = StringTransport()
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(transport)
        protocol.dataReceived('\x00\x01k\x00\x01v\x00\x00')
        self.assertFalse(transport.disconnecting)
        protocol.dataReceived('\x01\x00')
        self.assertTrue(transport.disconnecting)

    def Xtest_0407_excessiveKeyFailure(self):
        """
        If L{amp.BinaryBoxProtocol} disconnects because it received a key length prefix which was too large, the L{IBoxReceiver}'s
        C{stopReceivingBoxes} method is called with a L{TooLong} failure.
        """
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(StringTransport())
        protocol.dataReceived('\x01\x00')
        protocol.connectionLost(Failure(error.ConnectionDone("simulated connection done")))
        self.stopReason.trap(amp.TooLong)
        self.assertTrue(self.stopReason.value.isKey)
        self.assertFalse(self.stopReason.value.isLocal)
        self.assertIdentical(self.stopReason.value.value, None)
        self.assertIdentical(self.stopReason.value.keyName, None)

    def test_0408_receiveBoxData(self):
        """
        When a binary box protocol receives the serialized form of an AMP box, it should emit a similar box to its boxReceiver.
        """
        a = amp.BinaryBoxProtocol(self)
        a.dataReceived(amp.Box({"testKey": "valueTest", "anotherKey": "anotherValue"}).serialize())
        self.assertEquals(self.boxes, [amp.Box({"testKey": "valueTest", "anotherKey": "anotherValue"})])

    def test_0409_receiveLongerBoxData(self):
        """
        An L{amp.BinaryBoxProtocol} can receive serialized AMP boxes with values of up to (2 ** 16 - 1) bytes.
        """
        length = (2 ** 16 - 1)
        value = 'x' * length
        transport = StringTransport()
        protocol = amp.BinaryBoxProtocol(self)
        protocol.makeConnection(transport)
        protocol.dataReceived(amp.Box({'k': value}).serialize())
        self.assertEqual(self.boxes, [amp.Box({'k': value})])
        self.assertFalse(transport.disconnecting)

    def test_0410_sendBox(self):
        """
        When a binary box protocol sends a box, it should emit the serialized bytes of that box to its transport.
        """
        a = amp.BinaryBoxProtocol(self)
        a.makeConnection(self)
        aBox = amp.Box({"testKey": "valueTest", "someData": "hello"})
        a.makeConnection(self)
        a.sendBox(aBox)
        self.assertEquals(''.join(self.data), aBox.serialize())

    def test_0411_connectionLostStopSendingBoxes(self):
        """
        When a binary box protocol loses its connection, it should notify its box receiver that it has stopped receiving boxes.
        """
        a = amp.BinaryBoxProtocol(self)
        a.makeConnection(self)
        _l_aBox = amp.Box({"sample": "data"})
        a.makeConnection(self)
        connectionFailure = Failure(RuntimeError())
        a.connectionLost(connectionFailure)
        self.assertIdentical(self.stopReason, connectionFailure)

    def Xtest_0412_protocolSwitch(self):
        """
        L{BinaryBoxProtocol} has the capacity to switch to a different protocol on a box boundary.
        When a protocol is in the process of switching, it cannot receive traffic.
        """
        otherProto = TestProtocol(None, "outgoing data")
        test = self
        class SwitchyReceiver:
            switched = False
            def startReceivingBoxes(self, sender):
                pass
            def ampBoxReceived(self, _p_box):
                test.assertFalse(self.switched, "Should only receive one box!")
                self.switched = True
                a._lockForSwitch()
                a._switchTo(otherProto)
        a = amp.BinaryBoxProtocol(SwitchyReceiver())
        anyOldBox = amp.Box({"include": "lots", "of": "data"})
        a.makeConnection(self)
        # Include a 0-length box at the beginning of the next protocol's data,
        # to make sure that AMP doesn't eat the data or try to deliver extra
        # boxes either...
        moreThanOneBox = anyOldBox.serialize() + "\x00\x00Hello, world!"
        a.dataReceived(moreThanOneBox)
        self.assertIdentical(otherProto.transport, self)
        self.assertEquals("".join(otherProto.data), "\x00\x00Hello, world!")
        self.assertEquals(self.data, ["outgoing data"])
        a.dataReceived("more data")
        self.assertEquals("".join(otherProto.data), "\x00\x00Hello, world!more data")
        self.assertRaises(amp.ProtocolSwitched, a.sendBox, anyOldBox)

    def Xtest_0413_protocolSwitchInvalidStates(self):
        """
        In order to make sure the protocol never gets any invalid data sent into the middle of a box, it must be locked for switching before it is switched.
        It can only be unlocked if the switch failed, and attempting to send a box while it is locked should raise an exception.
        """
        a = amp.BinaryBoxProtocol(self)
        a.makeConnection(self)
        sampleBox = amp.Box({"some": "data"})
        a._lockForSwitch()
        self.assertRaises(amp.ProtocolSwitched, a.sendBox, sampleBox)
        a._unlockFromSwitch()
        a.sendBox(sampleBox)
        self.assertEquals(''.join(self.data), sampleBox.serialize())
        a._lockForSwitch()
        otherProto = TestProtocol(None, "outgoing data")
        a._switchTo(otherProto)
        self.assertRaises(amp.ProtocolSwitched, a._unlockFromSwitch)

    def Xtest_0414_protocolSwitchLoseConnection(self):
        """
        When the protocol is switched, it should notify its nested protocol of disconnection.
        """
        class Loser(protocol.Protocol):
            reason = None
            def connectionLost(self, reason):
                self.reason = reason
        connectionLoser = Loser()
        a = amp.BinaryBoxProtocol(self)
        a.makeConnection(self)
        a._lockForSwitch()
        a._switchTo(connectionLoser)
        connectionFailure = Failure(RuntimeError())
        a.connectionLost(connectionFailure)
        self.assertEquals(connectionLoser.reason, connectionFailure)

    def Xtest_0415_protocolSwitchLoseClientConnection(self):
        """
        When the protocol is switched, it should notify its nested client protocol factory of disconnection.
        """
        class ClientLoser:
            reason = None
            def clientConnectionLost(self, _p_connector, reason):
                self.reason = reason
        a = amp.BinaryBoxProtocol(self)
        connectionLoser = protocol.Protocol()
        clientLoser = ClientLoser()
        a.makeConnection(self)
        a._lockForSwitch()
        a._switchTo(connectionLoser, clientLoser)
        connectionFailure = Failure(RuntimeError())
        a.connectionLost(connectionFailure)
        self.assertEquals(clientLoser.reason, connectionFailure)

    def test_0416_DBK_sendBox(self):
        """
        When a binary box protocol sends a box, it should emit the serialized bytes of that box to its transport.
        """
        a = amp.BinaryBoxProtocol(self)
        a.makeConnection(self)
        aBox = amp.Box({"testKey": "valueTest", "someData": "hello"})
        a.makeConnection(self)
        a.sendBox(aBox)
        self.assertEquals(''.join(self.data), aBox.serialize())



"""  ========================================================================================
This section tests AMP???
"""

class Test_05_AMP(unittest.TestCase):

    def test_0507_brokenReturnValue(self):
        """
        It can be very confusing if you write some code which responds to a command, but gets the return value wrong.
        Most commonly you end up returning None instead of a dictionary.
        Verify that if that happens, the framework logs a useful error.
        """
        L = []
        SimpleSymmetricCommandProtocol().dispatchCommand(amp.AmpBox(_command = BrokenReturn.commandName)).addErrback(L.append)
        _blr = L[0].trap(amp.BadLocalReturn)
        print('0507 L[]:{0:}'.format(L))
        self.failUnlessIn('None', repr(L[0].value))

    def test_0508_unknownArgument(self):
        """
        Verify that unknown arguments are ignored, and not passed to a Python function which can't accept them.
        """
        l_client, _l_server, l_pump = connectedServerAndClient()
        L = []
        HELLO = 'world'
        l_client.callRemote(FutureHello, hello = HELLO, bonus = "I'm not in the book!").addCallback(L.append)
        l_pump.flush()
        print('0508 L[]:{0:}'.format(L))
        self.assertEquals(L[0]['hello'], HELLO)

    def test_0512_helloWorldCommand(self):
        """ TODO:
        Verify that a simple command can be sent and its response received with the high-level value parsing API.
        """
        l_client, _l_server, l_pump = connectedServerAndClient()
        L = []
        HELLO = '0512 - world'
        l_client.sendHello(HELLO).addCallback(L.append)
        l_pump.flush()
        print('0512-A Client:{0:}'.format(l_client))
        print('0512-B Server:{0:}'.format(_l_server))
        print('0512-C Pump:{0:}'.format(l_pump))
        print('0512-D L[]: {0:}'.format(L))
        self.assertEquals(L[0]['hello'], HELLO)

    def test_0512A_DBK_InfoCommand(self):
        """ TODO:
        Verify that a simple command can be sent and its response received with the high-level value parsing API.
        """
        l_client, _l_server, l_pump = connectedServerAndClient()
        L = []
        HELLO = '0512 - world'
        l_defer = l_client.sendHello(HELLO)
        l_defer.addCallback(L.append)
        l_pump.flush()
        print('0512A-1 L[]: {0:}'.format(L))
        self.assertEquals(L[0]['hello'], HELLO)

    def test_0513_helloErrorHandling(self):
        """
        Verify that if a known error type is raised and handled, it will be properly relayed to the other end of the connection
        and translated into an exception, and no error will be logged.
        """
        L = []
        l_client, _l_server, l_pump = connectedServerAndClient()
        HELLO = 'screw you'
        l_client.sendHello(HELLO).addErrback(L.append)
        l_pump.flush()
        L[0].trap(UnfriendlyGreeting)
        self.assertEquals(str(L[0].value), "Don't be a dick.")

    def test_0514_helloFatalErrorHandling(self):
        """
        Verify that if a known, fatal error type is raised and handled, it will be properly relayed to the other end of the connection and translated
        into an exception, no error will be logged, and the connection will be terminated.
        """
        L = []
        l_client, _l_server, l_pump = connectedServerAndClient()
        HELLO = 'die'
        l_client.sendHello(HELLO).addErrback(L.append)
        l_pump.flush()
        L.pop().trap(DeathThreat)
        l_client.sendHello(HELLO).addErrback(L.append)
        l_pump.flush()
        L.pop().trap(error.ConnectionDone)

    def test_0515_helloNoErrorHandling(self):
        """
        Verify that if an unknown error type is raised, it will be relayed to the other end of the connection and translated into an exception,
         it will be logged, and then the connection will be dropped.
        """
        L = []
        l_client, _l_server, l_pump = connectedServerAndClient()
        HELLO = THING_I_DONT_UNDERSTAND
        l_client.sendHello(HELLO).addErrback(L.append)
        l_pump.flush()
        ure = L.pop()
        ure.trap(amp.UnknownRemoteError)
        l_client.sendHello(HELLO).addErrback(L.append)
        cl = L.pop()
        cl.trap(error.ConnectionDone)
        # The exception should have been logged.
        self.failUnless(self.flushLoggedErrors(ThingIDontUnderstandError))

    def test_0516_lateAnswer(self):
        """
        Verify that a command that does not get answered until after the connection terminates will not cause any errors.
        """
        l_client, l_server, l_pump = connectedServerAndClient()
        L = []
        _HELLO = 'world'
        l_client.callRemote(WaitForever).addErrback(L.append)
        l_pump.flush()
        self.assertEquals(L, [])
        l_server.transport.loseConnection()
        l_pump.flush()
        L.pop().trap(error.ConnectionDone)
        # Just make sure that it doesn't error...
        l_server.waiting.callback({})
        return l_server.waiting

    def test_0517_requiresNoAnswer(self):
        """
        Verify that a command that requires no answer is run.
        """
        _L = []
        l_client, l_server, l_pump = connectedServerAndClient()
        print('517 Client:{0:}'.format(l_client))
        HELLO = 'world'
        l_client.callRemote(NoAnswerHello, hello = HELLO)
        l_pump.flush()
        self.failUnless(l_server.greeted)

    def test_0518_requiresNoAnswerFail(self):
        """
        Verify that commands sent after a failed no-answer request do not complete.
        """
        L = []
        l_client, l_server, l_pump = connectedServerAndClient()
        HELLO = 'screw you'
        l_client.callRemote(NoAnswerHello, hello = HELLO)
        l_pump.flush()
        # This should be logged locally.
        self.failUnless(self.flushLoggedErrors(amp.RemoteAmpError))
        HELLO = 'world'
        l_client.callRemote(Hello, hello = HELLO).addErrback(L.append)
        l_pump.flush()
        L.pop().trap(error.ConnectionDone)
        self.failIf(l_server.greeted)

    def test_0519_noAnswerResponderBadAnswer(self):
        """
        Verify that responders of requiresAnswer=False commands have to return a dictionary anyway.
        (requiresAnswer is a hint from the _client_ - the server may be called upon to answer commands in any case, if the client wants to know when they complete.)
        """
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = BadNoAnswerCommandProtocol, ClientClass = SimpleSymmetricCommandProtocol)
        l_client.callRemote(NoAnswerHello, hello = "hello")
        l_pump.flush()
        le = self.flushLoggedErrors(amp.BadLocalReturn)
        self.assertEquals(len(le), 1)


    def test_0520_noAnswerResponderAskedForAnswer(self):
        """
        Verify that responders with requiresAnswer=False will actually respond if the client sets requiresAnswer=True.
        In other words, verify that requiresAnswer is a hint honored only by the client.
        """
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = NoAnswerCommandProtocol, ClientClass = SimpleSymmetricCommandProtocol)
        L = []
        l_client.callRemote(Hello, hello = "Hello!").addCallback(L.append)
        l_pump.flush()
        self.assertEquals(len(L), 1)
        self.assertEquals(L, [dict(hello = "Hello!-noanswer", Print = None)])  # Optional response argument

    def test_0521_ampListCommand(self):
        """
        Test encoding of an argument that uses the AmpList encoding.
        """
        l_client, _l_server, l_pump = connectedServerAndClient()
        L = []
        l_client.callRemote(GetList, length = 10).addCallback(L.append)
        l_pump.flush()
        values = L.pop().get('body')
        self.assertEquals(values, [{'x': 1}] * 10)

    def test_0522_failEarlyOnArgSending(self):
        """
        Verify that if we pass an invalid argument list (omitting an argument), an exception will be raised.
        """
        _okayCommand = Hello(hello = "What?")
        self.assertRaises(amp.InvalidSignature, Hello)

    def test_0523_doubleProtocolSwitch(self):
        """
        As a debugging aid, a protocol system should raise a L{ProtocolSwitched} exception when asked to switch a protocol that is already switched.
        """
        serverDeferred = defer.Deferred()
        serverProto = SimpleSymmetricCommandProtocol(serverDeferred)
        clientDeferred = defer.Deferred()
        clientProto = SimpleSymmetricCommandProtocol(clientDeferred)
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = lambda: serverProto, ClientClass = lambda: clientProto)
        def switched(_p_result):
            self.assertRaises(amp.ProtocolSwitched, l_client.switchToTestProtocol)
            self.testSucceeded = True
        l_client.switchToTestProtocol().addCallback(switched)
        l_pump.flush()
        self.failUnless(self.testSucceeded)

    def test_0524_protocolSwitch(self, switcher = SimpleSymmetricCommandProtocol, spuriousTraffic = False, spuriousError = False):
        """
        Verify that it is possible to switch to another protocol mid-connection and send data to it successfully.
        """
        self.testSucceeded = False
        serverDeferred = defer.Deferred()
        serverProto = switcher(serverDeferred)
        clientDeferred = defer.Deferred()
        clientProto = switcher(clientDeferred)
        l_client, l_server, l_pump = connectedServerAndClient(ServerClass = lambda: serverProto, ClientClass = lambda: clientProto)
        if spuriousTraffic:
            wfdr = []  # remote
            _wfd = l_client.callRemote(WaitForever).addErrback(wfdr.append)
        switchDeferred = l_client.switchToTestProtocol()
        if spuriousTraffic:
            self.assertRaises(amp.ProtocolSwitched, l_client.sendHello, 'world')

        def cbConnsLost(((serverSuccess, serverData), (clientSuccess, clientData))):
            self.failUnless(serverSuccess)
            self.failUnless(clientSuccess)
            self.assertEquals(''.join(serverData), SWITCH_CLIENT_DATA)
            self.assertEquals(''.join(clientData), SWITCH_SERVER_DATA)
            self.testSucceeded = True

        def cbSwitch(_p_proto):
            return defer.DeferredList(
                [serverDeferred, clientDeferred]).addCallback(cbConnsLost)

        switchDeferred.addCallback(cbSwitch)
        l_pump.flush()
        if serverProto.maybeLater is not None:
            serverProto.maybeLater.callback(serverProto.maybeLaterProto)
            l_pump.flush()
        if spuriousTraffic:
            # switch is done here; do this here to make sure that if we're
            # going to corrupt the connection, we do it before it's closed.
            if spuriousError:
                l_server.waiting.errback(amp.RemoteAmpError("SPURIOUS", "Here's some traffic in the form of an error."))
            else:
                l_server.waiting.callback({})
            l_pump.flush()
        l_client.transport.loseConnection()  # close it
        l_pump.flush()
        self.failUnless(self.testSucceeded)

    def test_0525_protocolSwitchDeferred(self):
        """
        Verify that protocol-switching even works if the value returned from the command that does the switch is deferred.
        """
        return self.test_0524_protocolSwitch(switcher = DeferredSymmetricCommandProtocol)

    def test_0526_protocolSwitchFail(self, switcher = SimpleSymmetricCommandProtocol):
        """
        Verify that if we try to switch protocols and it fails, the connection stays up and we can go back to speaking AMP.
        """
        self.testSucceeded = False

        serverDeferred = defer.Deferred()
        serverProto = switcher(serverDeferred)
        clientDeferred = defer.Deferred()
        clientProto = switcher(clientDeferred)
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = lambda: serverProto, ClientClass = lambda: clientProto)
        L = []
        _switchDeferred = l_client.switchToTestProtocol(fail = True).addErrback(L.append)
        l_pump.flush()
        L.pop().trap(UnknownProtocol)
        self.failIf(self.testSucceeded)
        # It's a known error, so let's send a "hello" on the same connection;
        # it should work.
        l_client.sendHello('world').addCallback(L.append)
        l_pump.flush()
        self.assertEqual(L.pop()['hello'], 'world')

    def test_0527_trafficAfterSwitch(self):
        """
        Verify that attempts to send traffic after a switch will not corrupt the nested protocol.
        """
        return self.test_0524_protocolSwitch(spuriousTraffic = True)

    def test_0528_errorAfterSwitch(self):
        """
        Returning an error after a protocol switch should record the underlying error.
        """
        return self.test_0524_protocolSwitch(spuriousTraffic = True, spuriousError = True)

    def test_0529_quitBoxQuits(self):
        """
        Verify that commands with a responseType of QuitBox will in fact terminate the connection.
        """
        l_client, _l_server, l_pump = connectedServerAndClient()
        L = []
        HELLO = 'world'
        GOODBYE = 'everyone'
        l_client.sendHello(HELLO).addCallback(L.append)
        l_pump.flush()
        self.assertEquals(L.pop()['hello'], HELLO)
        l_client.callRemote(Goodbye).addCallback(L.append)
        l_pump.flush()
        self.assertEquals(L.pop()['goodbye'], GOODBYE)
        l_client.sendHello(HELLO).addErrback(L.append)
        L.pop().trap(error.ConnectionDone)

    def test_0530_basicLiteralEmit(self):
        """
        Verify that the command dictionaries for a callRemote look correct after being serialized and parsed.
        """
        l_client, l_server, l_pump = connectedServerAndClient()
        L = []
        l_server.ampBoxReceived = L.append
        l_client.callRemote(Hello, hello = 'hello test', mixedCase = 'mixed case arg test', dash_arg = 'x', underscore_arg = 'y')
        l_pump.flush()
        self.assertEquals(len(L), 1)
        for k, v in [('_command', Hello.commandName),
                     ('hello', 'hello test'),
                     ('mixedCase', 'mixed case arg test'),
                     ('dash-arg', 'x'),
                     ('underscore_arg', 'y')]:
            self.assertEquals(L[-1].pop(k), v)
        L[-1].pop('_ask')
        self.assertEquals(L[-1], {})

    def Xtest_0531_basicStructuredEmit(self):
        """
        Verify that a call similar to basicLiteralEmit's is handled properly with high-level quoting and passing to Python methods,
         and that argument names are correctly handled.
        """
        L = []
        class StructuredHello(amp.AMP):
            def h(self, *a, **k):
                L.append((a, k))
                return dict(hello = 'aaa')
            Hello.responder(h)
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = StructuredHello)
        l_client.callRemote(Hello, hello = 'hello test', mixedCase = 'mixed case arg test',
                     dash_arg = 'x', underscore_arg = 'y').addCallback(L.append)
        l_pump.flush()
        print('0531-A L[]:{0:}'.format(L))
        self.assertEquals(len(L), 2)
        self.assertEquals(L[0], ((), dict(
                    hello = 'hello test',
                    mixedCase = 'mixed case arg test',
                    dash_arg = 'x',
                    underscore_arg = 'y',
                    # XXX - should optional arguments just not be passed?
                    # passing None seems a little odd, looking at the way it
                    # turns out here... -glyph
                    From = ('file', 'file'),
                    # Print = None,
                    # optional = None,
                    )))
        # self.assertEquals(L[1], dict(Print = None, hello = 'aaa'))



"""  ========================================================================================
"""
class PretendRemoteCertificateAuthority:
    def checkIsPretendRemote(self):
        return True

class IOSimCert:
    verifyCount = 0

    def options(self, *_ign):
        return self

    def iosimVerify(self, otherCert):
        """
        This isn't a real certificate, and wouldn't work on a real socket, but
        iosim specifies a different API so that we don't have to do any crypto
        math to demonstrate that the right functions get called in the right
        places.
        """
        assert otherCert is self
        self.verifyCount += 1
        return True

class OKCert(IOSimCert):
    def options(self, x):
        assert x.checkIsPretendRemote()
        return self

class GrumpyCert(IOSimCert):
    def iosimVerify(self, _otherCert):
        self.verifyCount += 1
        return False

class DroppyCert(IOSimCert):
    def __init__(self, toDrop):
        self.toDrop = toDrop

    def iosimVerify(self, _otherCert):
        self.verifyCount += 1
        self.toDrop.loseConnection()
        return True

class SecurableProto(FactoryNotifier):

    factory = None

    def verifyFactory(self):
        return [PretendRemoteCertificateAuthority()]

    def getTLSVars(self):
        cert = self.certFactory()
        verify = self.verifyFactory()
        return dict(
            tls_localCertificate = cert,
            tls_verifyAuthorities = verify)
    amp.StartTLS.responder(getTLSVars)



class Test_06_TLS(unittest.TestCase):

    def Xtest_0601_startingTLS(self):
        """
        Verify that starting TLS and succeeding at handshaking sends all the notifications to all the right places.
        """
        cli, svr, l_pump = connectedServerAndClient(ServerClass = SecurableProto, ClientClass = SecurableProto)

        okc = OKCert()
        svr.certFactory = lambda : okc

        cli.callRemote(
            amp.StartTLS, tls_localCertificate = okc,
            tls_verifyAuthorities = [PretendRemoteCertificateAuthority()])

        # let's buffer something to be delivered securely
        L = []
        _d = cli.callRemote(SecuredPing).addCallback(L.append)
        l_pump.flush()
        # once for client once for server
        self.assertEquals(okc.verifyCount, 2)
        L = []
        _d = cli.callRemote(SecuredPing).addCallback(L.append)
        l_pump.flush()
        self.assertEqual(L[0], {'pinged': True})

    def Xtest_0602_startTooManyTimes(self):
        """
        Verify that the protocol will complain if we attempt to renegotiate TLS, which we don't support.
        """
        cli, svr, l_pump = connectedServerAndClient(ServerClass = SecurableProto, ClientClass = SecurableProto)
        okc = OKCert()
        svr.certFactory = lambda : okc
        cli.callRemote(amp.StartTLS, tls_localCertificate = okc, tls_verifyAuthorities = [PretendRemoteCertificateAuthority()])
        l_pump.flush()
        cli.noPeerCertificate = True  # this is totally fake
        self.assertRaises(
            amp.OnlyOneTLS,
            cli.callRemote,
            amp.StartTLS,
            tls_localCertificate = okc,
            tls_verifyAuthorities = [PretendRemoteCertificateAuthority()])

    def Xtest_0603_negotiationFailed(self):
        """
        Verify that starting TLS and failing on both sides at handshaking sends notifications to all the right places and terminates the connection.
        """
        badCert = GrumpyCert()
        cli, svr, l_pump = connectedServerAndClient(ServerClass = SecurableProto, ClientClass = SecurableProto)
        svr.certFactory = lambda : badCert
        cli.callRemote(amp.StartTLS, tls_localCertificate = badCert)
        l_pump.flush()
        # once for client once for server - but both fail
        self.assertEquals(badCert.verifyCount, 2)
        d = cli.callRemote(SecuredPing)
        l_pump.flush()
        self.assertFailure(d, iosim.NativeOpenSSLError)

    def Xtest_0604_negotiationFailedByClosing(self):
        """
        Verify that starting TLS and failing by way of a lost connection notices that it is probably an SSL problem.
        """
        cli, svr, l_pump = connectedServerAndClient(ServerClass = SecurableProto, ClientClass = SecurableProto)
        droppyCert = DroppyCert(svr.transport)
        svr.certFactory = lambda : droppyCert
        _secure = cli.callRemote(amp.StartTLS, tls_localCertificate = droppyCert)
        l_pump.flush()
        self.assertEquals(droppyCert.verifyCount, 2)
        d = cli.callRemote(SecuredPing)
        l_pump.flush()
        # it might be a good idea to move this exception somewhere more
        # reasonable.
        self.assertFailure(d, error.PeerVerifyError)



"""  ========================================================================================
"""
class InheritedError(Exception):
    """
    This error is used to check inheritance.
    """


class OtherInheritedError(Exception):
    """
    This is a distinct error for checking inheritance.
    """



class BaseCommand(amp.Command):
    """
    This provides a command that will be subclassed.
    """
    errors = {InheritedError: 'INHERITED_ERROR'}


class InheritedCommand(BaseCommand):
    """
    This is a command which subclasses another command but does not override anything.
    """


class AddErrorsCommand(BaseCommand):
    """
    This is a command which subclasses another command but adds errors to the list.
    """
    arguments = [('other', amp.Boolean())]
    errors = {OtherInheritedError: 'OTHER_INHERITED_ERROR'}


class NormalCommandProtocol(amp.AMP):
    """
    This is a protocol which responds to L{BaseCommand}, and is used to test that inheritance does not interfere with the normal handling of errors.
    """
    def resp(self):
        raise InheritedError()
    BaseCommand.responder(resp)


class InheritedCommandProtocol(amp.AMP):
    """
    This is a protocol which responds to L{InheritedCommand}, and is used to test that inherited commands inherit their bases' errors
     if they do not respond to any of their own.
    """
    def resp(self):
        raise InheritedError()
    InheritedCommand.responder(resp)


class AddedCommandProtocol(amp.AMP):
    """
    This is a protocol which responds to L{AddErrorsCommand}, and is used to test that inherited commands can add their own new types of errors,
     but still respond in the same way to their parents types of errors.
    """
    def resp(self, other):
        if other:
            raise OtherInheritedError()
        else:
            raise InheritedError()
    AddErrorsCommand.responder(resp)


class Test_07_CommandInheritance(unittest.TestCase):
    """
    These tests verify that commands inherit error conditions properly.
    """

    def errorCheck(self, err, proto, cmd, **kw):
        """
        Check that the appropriate kind of error is raised when a given command is sent to a given protocol.
        """
        l_client, _l_server, l_pump = connectedServerAndClient(ServerClass = proto, ClientClass = proto)
        d = l_client.callRemote(cmd, **kw)
        d2 = self.failUnlessFailure(d, err)
        l_pump.flush()
        return d2

    def test_0701_basicErrorPropagation(self):
        """
        Verify that errors specified in a superclass are respected normally even if it has subclasses.
        """
        return self.errorCheck(InheritedError, NormalCommandProtocol, BaseCommand)

    def test_0702_inheritedErrorPropagation(self):
        """
        Verify that errors specified in a superclass command are propagated to its subclasses.
        """
        return self.errorCheck(InheritedError, InheritedCommandProtocol, InheritedCommand)

    def test_0703_inheritedErrorAddition(self):
        """
        Verify that new errors specified in a subclass of an existing command are honored even if the superclass defines some errors.
        """
        return self.errorCheck(OtherInheritedError, AddedCommandProtocol, AddErrorsCommand, other = True)

    def test_0704_additionWithOriginalError(self):
        """
        Verify that errors specified in a command's superclass are respected even if that command defines new errors itself.
        """
        return self.errorCheck(InheritedError, AddedCommandProtocol, AddErrorsCommand, other = False)



"""  ========================================================================================
"""

def _loseAndPass(err, proto):
    # be specific, pass on the error to the client.
    err.trap(error.ConnectionLost, error.ConnectionDone)
    del proto.connectionLost
    proto.connectionLost(err)


class LiveFireBase:
    """
    Utility for connected reactor-using tests.
    """

    def setUp(self):
        """
        Create an amp server and connect a client to it.
        """
        # from twisted.internet import reactor
        self.serverFactory = protocol.ServerFactory()
        self.serverFactory.protocol = self.serverProto
        self.clientFactory = protocol.ClientFactory()
        self.clientFactory.protocol = self.clientProto
        self.clientFactory.onMade = defer.Deferred()
        self.serverFactory.onMade = defer.Deferred()
        self.serverPort = reactor.listenTCP(0, self.serverFactory)
        self.addCleanup(self.serverPort.stopListening)
        self.clientConn = reactor.connectTCP('127.0.0.1', self.serverPort.getHost().port, self.clientFactory)
        self.addCleanup(self.clientConn.disconnect)
        def getProtos(_rlst):
            self.cli = self.clientFactory.theProto
            self.svr = self.serverFactory.theProto
        dl = defer.DeferredList([self.clientFactory.onMade, self.serverFactory.onMade])
        return dl.addCallback(getProtos)

    def tearDown(self):
        """
        Cleanup client and server connections, and check the error got at
        C{connectionLost}.
        """
        L = []
        for conn in self.cli, self.svr:
            if conn.transport is not None:
                # depend on amp's function connection-dropping behavior
                d = defer.Deferred().addErrback(_loseAndPass, conn)
                conn.connectionLost = d.errback
                conn.transport.loseConnection()
                L.append(d)
        return defer.gatherResults(L).addErrback(lambda first: first.value.subFailure)

def show(x):
    import sys
    sys.stdout.write(x + '\n')
    sys.stdout.flush()


# def XXtempSelfSigned():
    # from twisted.internet import ssl

    # sharedDN = ssl.DN(CN = 'shared')
    # key = ssl.KeyPair.generate()
    # cr = key.certificateRequest(sharedDN)
    # sscrd = key.signCertificateRequest(sharedDN, cr, lambda dn: True, 1234567)
    # cert = key.newCertificate(sscrd)
    # return cert

# tempcert = tempSelfSigned()
tempcert = None


class Test_08_LiveFireTLSTestCase(LiveFireBase, unittest.TestCase):
    clientProto = SecurableProto
    serverProto = SecurableProto

    def Xtest_0801_liveFireCustomTLS(self):
        """
        Using real, live TLS, actually negotiate a connection.

        This also looks at the 'peerCertificate' attribute's correctness, since that's actually loaded using OpenSSL calls,
         but the main purpose is to make sure that we didn't miss anything obvious in iosim about TLS negotiations.
        """
        cert = tempcert
        self.svr.verifyFactory = lambda : [cert]
        self.svr.certFactory = lambda : cert
        # only needed on the server, we specify the client below.
        def secured(_rslt):
            x = cert.digest()
            def pinged(_rslt2):
                # Interesting.  OpenSSL won't even _tell_ us about the peer
                # cert until we negotiate.  we should be able to do this in
                # 'secured' instead, but it looks like we can't.  I think this
                # is a bug somewhere far deeper than here.
                self.failUnlessEqual(x, self.cli.hostCertificate.digest())
                self.failUnlessEqual(x, self.cli.peerCertificate.digest())
                self.failUnlessEqual(x, self.svr.hostCertificate.digest())
                self.failUnlessEqual(x, self.svr.peerCertificate.digest())
            return self.cli.callRemote(SecuredPing).addCallback(pinged)
        return self.cli.callRemote(amp.StartTLS, tls_localCertificate = cert, tls_verifyAuthorities = [cert]).addCallback(secured)



"""  ========================================================================================
"""

class SlightlySmartTLS(SimpleSymmetricCommandProtocol):
    """
    Specific implementation of server side protocol with different management of TLS.
    """
    def getTLSVars(self):
        """
        @return: the global C{tempcert} certificate as local certificate.
        """
        return dict(tls_localCertificate = tempcert)
    amp.StartTLS.responder(getTLSVars)



class Test_09_PlainVanillaLiveFire(LiveFireBase, unittest.TestCase):

    clientProto = SimpleSymmetricCommandProtocol
    serverProto = SimpleSymmetricCommandProtocol

    def Xtest_0901_liveFireDefaultTLS(self):
        """
        Verify that out of the box, we can start TLS to at least encrypt the connection, even if we don't have any certificates to use.
        """
        def secured(_result):
            return self.cli.callRemote(SecuredPing)
        return self.cli.callRemote(amp.StartTLS).addCallback(secured)



"""  ========================================================================================
"""

class Test_10_WithServerTLSVerification(LiveFireBase, unittest.TestCase):
    clientProto = SimpleSymmetricCommandProtocol
    serverProto = SlightlySmartTLS

    def Xtest_1001_anonymousVerifyingClient(self):
        """
        Verify that anonymous clients can verify server certificates.
        """
        def secured(_result):
            return self.cli.callRemote(SecuredPing)
        return self.cli.callRemote(amp.StartTLS, tls_verifyAuthorities = [tempcert]).addCallback(secured)



"""  ========================================================================================
"""

class ProtocolIncludingArgument(amp.Argument):
    """
    An L{amp.Argument} which encodes its parser and serializer arguments *including the protocol* into its parsed and serialized forms.
    """

    def fromStringProto(self, string, protocol):
        """
        Don't decode anything; just return all possible information.

        @return: A two-tuple of the input string and the protocol.
        """
        return (string, protocol)

    def toStringProto(self, obj, protocol):
        """
        Encode identifying information about L{object} and protocol into a string for later verification.

        @type obj: L{object}
        @type protocol: L{amp.AMP}
        """
        return "%s:%s" % (id(obj), id(protocol))



class ProtocolIncludingCommand(amp.Command):
    """
    A command that has argument and response schemas which use L{ProtocolIncludingArgument}.
    """
    arguments = [('weird', ProtocolIncludingArgument())]
    response = [('weird', ProtocolIncludingArgument())]



class MagicSchemaCommand(amp.Command):
    """
    A command which overrides L{parseResponse}, L{parseArguments}, and L{makeResponse}.
    """
    def parseResponse(self, strings, protocol):
        """
        Don't do any parsing, just jam the input strings and protocol onto the C{protocol.parseResponseArguments} attribute as a two-tuple.
        Return the original strings.
        """
        protocol.parseResponseArguments = (strings, protocol)
        return strings
    parseResponse = classmethod(parseResponse)

    def parseArguments(cls, strings, protocol):
        """
        Don't do any parsing, just jam the input strings and protocol onto the C{protocol.parseArgumentsArguments} attribute as a two-tuple.
        Return the original strings.
        """
        protocol.parseArgumentsArguments = (strings, protocol)
        return strings
    parseArguments = classmethod(parseArguments)

    def makeArguments(cls, objects, protocol):
        """
        Don't do any serializing, just jam the input strings and protocol onto the C{protocol.makeArgumentsArguments} attribute as a two-tuple.
        Return the original strings.
        """
        protocol.makeArgumentsArguments = (objects, protocol)
        return objects
    makeArguments = classmethod(makeArguments)


class NoNetworkProtocol(amp.AMP):
    """
    An L{amp.AMP} subclass which overrides private methods to avoid testing the network.
    It also provides a responder for L{MagicSchemaCommand} that does nothing, so that tests can test aspects of the interaction of L{amp.Command}s and L{amp.AMP}.

    @ivar parseArgumentsArguments: Arguments that have been passed to any L{MagicSchemaCommand},
    if L{MagicSchemaCommand} has been handled by this protocol.

    @ivar parseResponseArguments: Responses that have been returned from a L{MagicSchemaCommand},
    if L{MagicSchemaCommand} has been handled by this protocol.

    @ivar makeArgumentsArguments: Arguments that have been serialized by any L{MagicSchemaCommand},
    if L{MagicSchemaCommand} has been handled by this protocol.
    """
    def _sendBoxCommand(self, _p_commandName, strings, _p_requiresAnswer):
        """
        Return a Deferred which fires with the original strings.
        """
        return defer.succeed(strings)

    MagicSchemaCommand.responder(lambda _p_s, _p_weird: {})


class MyBox(dict):
    """
    A unique dict subclass.
    """


class ProtocolIncludingCommandWithDifferentCommandType(
    ProtocolIncludingCommand):
    """
    A L{ProtocolIncludingCommand} subclass whose commandType is L{MyBox}
    """
    commandType = MyBox


class Test_11_CommandTestCase(unittest.TestCase):
    """
    Tests for L{amp.Command}.
    """

    def test_1101_parseResponse(self):
        """
        There should be a class method of Command which accepts a mapping of argument names to serialized forms and
        returns a similar mapping whose values have been parsed via the Command's response schema.
        """
        protocol = object()
        result = 'whatever'
        strings = {'weird': result}
        self.assertEqual(ProtocolIncludingCommand.parseResponse(strings, protocol), {'weird': (result, protocol)})

    def test_1102_callRemoteCallsParseResponse(self):
        """
        Making a remote call on a L{amp.Command} subclass which overrides the C{parseResponse} method
        should call that C{parseResponse} method to get the response.
        """
        client = NoNetworkProtocol()
        thingy = "weeoo"
        response = client.callRemote(MagicSchemaCommand, weird = thingy)
        def gotResponse(_ign):
            self.assertEquals(client.parseResponseArguments, ({"weird": thingy}, client))
        response.addCallback(gotResponse)
        return response

    def test_1103_parseArguments(self):
        """
        There should be a class method of L{amp.Command} which accepts a mapping of argument names to serialized forms and
        returns a similar mapping whose values have been parsed via the command's argument schema.
        """
        protocol = object()
        result = 'whatever'
        strings = {'weird': result}
        self.assertEqual(ProtocolIncludingCommand.parseArguments(strings, protocol), {'weird': (result, protocol)})

    def Xtest_1104_responderCallsParseArguments(self):
        """
        Making a remote call on a L{amp.Command} subclass which overrides the C{parseArguments} method should call that C{parseArguments} method to get the arguments.
        """
        protocol = NoNetworkProtocol()
        responder = protocol.locateResponder(MagicSchemaCommand.commandName)
        argument = object()
        response = responder(dict(weird = argument))
        response.addCallback(lambda _ign: self.assertEqual(protocol.parseArgumentsArguments, ({"weird": argument}, protocol)))
        return response

    def test_1105_makeArguments(self):
        """
        There should be a class method of L{amp.Command} which accepts a mapping of argument names to objects and
        returns a similar mapping whose values have been serialized via the command's argument schema.
        """
        protocol = object()
        argument = object()
        objects = {'weird': argument}
        self.assertEqual(ProtocolIncludingCommand.makeArguments(objects, protocol), {'weird': "%d:%d" % (id(argument), id(protocol))})

    def test_1106_makeArgumentsUsesCommandType(self):
        """
        L{amp.Command.makeArguments}'s return type should be the type of the result of L{amp.Command.commandType}.
        """
        protocol = object()
        objects = {"weird": "whatever"}
        result = ProtocolIncludingCommandWithDifferentCommandType.makeArguments(objects, protocol)
        self.assertIdentical(type(result), MyBox)

    def test_1107_callRemoteCallsMakeArguments(self):
        """
        Making a remote call on a L{amp.Command} subclass which overrides the C{makeArguments} method
        should call that C{makeArguments} method to get the response.
        """
        def cb_gotResponse(_ignore):
            self.assertEqual(client.makeArgumentsArguments, ({"weird": argument}, client))
        client = NoNetworkProtocol()
        argument = object()
        response = client.callRemote(MagicSchemaCommand, weird = argument)
        response.addCallback(cb_gotResponse)
        return response

# ## END DBK
