"""
@name:      C:/Users/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:   This creates the Twisted (Async) version of MQTT client.

Warning.  There are two things called connect in this module.

The first is a TCP connection to the Mqtt broker.
The second is a MQTT connection to the broker that uses the first connection as a transport.

"""

# Import system type stuff
import random
from twisted.internet.protocol import ClientFactory, Protocol

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.tools import PrettyPrintAny


LOG = Logger.getLogger('PyHouse.MqttProtocol   ')

# BROKERv4 = '192.168.1.71'
BROKERv4 = 'iot.eclipse.org'  # Sandbox Mosquitto broker
# BROKERv6 = '2604:8800:100:8268::1:1'    # Pink Poppy
BROKERv6 = '2001:4830:1600:84ae::1'  # Cannon Trail
PORT = 1883
SUBSCRIBE = 'pyhouse/#'


class EncodeDecode(object):
    # Encode and decode stuff - separate class???

    def _encodeString(self, string):
        encoded = bytearray()
        encoded.append(len(string) >> 8)
        encoded.append(len(string) & 0xFF)
        for i in string:
            encoded.append(i)
        return encoded

    def _decodeString(self, encodedString):
        length = 256 * encodedString[0] + encodedString[1]
        return str(encodedString[2:2 + length])

    def _encodeLength(self, length):
        encoded = bytearray()
        while True:
            digit = length % 128
            length //= 128
            if length > 0:
                digit |= 128
            encoded.append(digit)
            if length <= 0:
                break
        return encoded

    def _encodeValue(self, value):
        encoded = bytearray()
        encoded.append(value >> 8)
        encoded.append(value & 0xFF)
        return encoded

    def _decodeLength(self, lengthArray):
        length = 0
        multiplier = 1
        for i in lengthArray:
            length += (i & 0x7F) * multiplier
            multiplier *= 0x80
            if (i & 0x80) != 0x80:
                break
        return length

    def _decodeValue(self, valueArray):
        value = 0
        multiplier = 1
        for i in valueArray[::-1]:
            value += i * multiplier
            multiplier = multiplier << 8
        return value


class MQTTProtocol(Protocol, EncodeDecode):
    """
    This protocol is used for communication with the MQTT broker.
    """

    # The first 4 bits of a MQTT packet are the packet type.
    _packetTypes = {0x00: "null", 0x01: "connect", 0x02: "connack",
                    0x03: "publish", 0x04: "puback", 0x05: "pubrec",
                    0x06: "pubrel", 0x07: "pubcomp", 0x08: "subscribe",
                    0x09: "suback", 0x0A: "unsubscribe", 0x0B: "unsuback",
                    0x0C: "pingreq", 0x0D: "pingresp", 0x0E: "disconnect"}
    m_buffer = bytearray()

    def dataReceived(self, p_data):
        """ A standard callback when we get data from the broker.

        It might be a portion of a message up to several messages.
        It is up to us to break it down to individual messages and then send the message on to be used.
        """
        # print("dataReceived {}".format(PrintBytes(p_data)))
        self._accumulatePacket(p_data)

    def _accumulatePacket(self, p_data):
        self.m_buffer.extend(p_data)
        l_length = None
        while len(self.m_buffer):
            if l_length is None:
                # Start on a new packet
                # Haven't got enough data to start a new packet, wait for some more
                if len(self.m_buffer) < 2:
                    break
                lenLen = 1
                # Calculate the length of the length field
                while lenLen < len(self.m_buffer):
                    if not self.m_buffer[lenLen] & 0x80:
                        break
                    lenLen += 1
                # We still haven't got all of the remaining length field
                if lenLen < len(self.m_buffer) and self.m_buffer[lenLen] & 0x80:
                    return
                l_length = self._decodeLength(self.m_buffer[1:])
            if len(self.m_buffer) >= l_length + lenLen + 1:
                chunk = self.m_buffer[:l_length + lenLen + 1]
                self._processPacket(chunk)
                self.m_buffer = self.m_buffer[l_length + lenLen + 1:]
                l_length = None
            else:
                break

    def _processPacket(self, packet):
        """Handle the Header (2-5 bytes)
        See http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html
        """
        try:
            packet_type = (packet[0] & 0xF0) >> 4
            packet_type_name = self._packetTypes[packet_type]
            dup = (packet[0] & 0x08) == 0x08
            qos = (packet[0] & 0x06) >> 1
            retain = (packet[0] & 0x01) == 0x01
        except:
            # Invalid packet type, throw away this packet
            print "Invalid packet type %x" % packet_type
            return
        # Strip the fixed header
        lenLen = 1
        while packet[lenLen] & 0x80:
            lenLen += 1
        packet = packet[lenLen + 1:]
        # Get the appropriate handler function
        l_packetHandler = getattr(self, "_event_%s" % packet_type_name, None)
        if l_packetHandler:
            # print("_processPacket {} - {}".format(l_packetHandler, PrintBytes(packet)))
            l_packetHandler(packet, qos, dup, retain)
        else:
            print "Invalid packet handler for %s" % packet_type_name
            return

    # These are the events - one for each packet type

    def _event_connect(self, packet, _qos, _dup, _retain):
        # Strip the protocol name and version number
        packet = packet[len("06MQisdp3"):]
        # Extract the connect flags
        willRetain = packet[0] & 0x20 == 0x20
        willQos = packet[0] & 0x18 >> 3
        willFlag = packet[0] & 0x04 == 0x04
        cleanStart = packet[0] & 0x02 == 0x02
        packet = packet[1:]
        # Extract the keepalive period
        keepalive = self._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the client id
        clientID = self._decodeString(packet)
        packet = packet[len(clientID) + 2:]
        # Extract the will topic and message, if applicable
        willTopic = None
        willMessage = None
        if willFlag:
            # Extract the will topic
            willTopic = self._decodeString(packet)
            packet = packet[len(willTopic) + 2:]
            # Extract the will message
            # Whatever remains is the will message
            willMessage = packet
        self.connectReceived(clientID, keepalive, willTopic,
                             willMessage, willQos, willRetain,
                             cleanStart)

    def _event_connack(self, packet, _qos, _dup, _retain):
        # Return the status field
        self.connackReceived(packet[0])

    def _event_publish(self, packet, qos, dup, retain):
        # Extract the topic name
        topic = self._decodeString(packet)
        packet = packet[len(topic) + 2:]
        # Extract the message ID if appropriate
        messageId = None
        if qos > 0:
            messageId = self._decodeValue(packet[:2])
            packet = packet[2:]
        # Extract the message
        # Whatever remains is the message
        message = str(packet)
        self.publishReceived(topic, message, qos, dup, retain, messageId)

    def _event_puback(self, packet, _qos, _dup, _retain):
        # Extract the message ID
        messageId = self._decodeValue(packet[:2])
        self.pubackReceived(messageId)

    def _event_pubrec(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        self.pubrecReceived(messageId)

    def _event_pubrel(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        self.pubrelReceived(messageId)

    def _event_pubcomp(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        self.pubcompReceived(messageId)

    def _event_subscribe(self, packet, qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        packet = packet[2:]
        topics = []
        while len(packet):
            topic = self._decodeString(packet)
            packet = packet[len(topic) + 2:]
            qos = packet[0]
            packet = packet[1:]
            # Add them to the list of (topic, qos)s
            topics.append((topic, qos))
        self.subscribeReceived(topics, messageId)

    def _event_suback(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the granted QoS levels
        grantedQos = []
        while len(packet):
            grantedQos.append(packet[0])
            packet = packet[1:]
        self.subackReceived(grantedQos, messageId)

    def _event_unsubscribe(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the unsubscribing topics
        topics = []
        while len(packet):
            topic = self._decodeString(packet)
            packet = packet[len(topic) + 2:]
            topics.append(topic)
        self.unsubscribeReceived(topics, messageId)

    def _event_unsuback(self, packet, _qos, _dup, _retain):
        messageId = self._decodeValue(packet[:2])
        self.unsubackReceived(messageId)

    def _event_pingreq(self, _packet, _qos, _dup, _retain):
        self.pingreqReceived()

    def _event_pingresp(self, _packet, _qos, _dup, _retain):
        self.pingrespReceived()

    def _event_disconnect(self, _packet, _qos, _dup, _retain):
        self.disconnectReceived()

    # these are to be overridden below

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def connectReceived(self, clientID, keepalive, willTopic, willMessage, willQoS, willRetain, cleanStart):
        pass

    def connackReceived(self, status):
        pass

    def publishReceived(self, topic, message, qos = 0, dup = False, retain = False, messageId = None):
        raise NotImplementedError, "Subclasses must implement this."
        pass

    def pubackReceived(self, messageId):
        pass

    def pubrecReceived(self, messageId):
        pass

    def pubrelReceived(self, messageId):
        pass

    def pubcompReceived(self, messageId):
        pass

    def subscribeReceived(self, topics, messageId):
        pass

    def subackReceived(self, grantedQos, messageId):
        pass

    def unsubscribeReceived(self, topics, messageId):
        pass

    def unsubackReceived(self, messageId):
        pass

    def pingreqReceived(self):
        pass

    def pingrespReceived(self):
        pass

    def disconnectReceived(self):
        pass

    # these are for sending Mqtt packets.

    def connect(self, p_clientID, keepalive = 3000, willTopic = None, willMessage = None, willQoS = 0, willRetain = False, cleanStart = True):
        print("Sending connect packet  ID: {}".format(p_clientID))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        varHeader.extend(self._encodeString("MQIsdp"))
        varHeader.append(3)
        if willMessage is None or willTopic is None:
            # Clean start, no will message
            varHeader.append(0 << 2 | cleanStart << 1)
        else:
            varHeader.append(willRetain << 5 | willQoS << 3
                             | 1 << 2 | cleanStart << 1)
        varHeader.extend(self._encodeValue(keepalive / 1000))
        payload.extend(self._encodeString(p_clientID))
        if willMessage is not None and willTopic is not None:
            payload.extend(self._encodeString(willTopic))
            payload.extend(self._encodeString(willMessage))
        header.append(0x01 << 4)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def connack(self, status):
        print("Sending connack packet")
        header = bytearray()
        payload = bytearray()
        header.append(0x02 << 4)
        payload.append(status)
        header.extend(self._encodeLength(len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(payload))

    def publish(self, p_topic, p_message, qosLevel = 0, retain = False, dup = False, messageId = None):
        print("Sending publish packet - Topic: {}  Message: {}".format(p_topic, p_message))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = publish
        header.append(0x03 << 4 | dup << 3 | qosLevel << 1 | retain)
        varHeader.extend(self._encodeString(p_topic))
        if qosLevel > 0:
            if messageId is not None:
                varHeader.extend(self._encodeValue(messageId))
            else:
                varHeader.extend(self._encodeValue(random.randint(1, 0xFFFF)))
        payload.extend(p_message)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def puback(self, messageId):
        print("Sending puback packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x04 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrec(self, messageId):
        print("Sending pubrec packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x05 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrel(self, messageId):
        print("Sending pubrel packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x06 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubcomp(self, messageId):
        print("Sending pubcomp packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x07 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def subscribe(self, p_topic, requestedQoS = 0, messageId = None):
        """
        Only supports QoS = 0 subscribes
        Only supports one subscription per message
        """
        print("Sending subscribe packet - Topic: {}".format(p_topic))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = subscribe, QoS = 1
        header.append(0x08 << 4 | 0x01 << 1)
        if messageId is None:
            varHeader.extend(self._encodeValue(random.randint(1, 0xFFFF)))
        else:
            varHeader.extend(self._encodeValue(messageId))
        payload.extend(self._encodeString(p_topic))
        payload.append(requestedQoS)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def suback(self, grantedQos, messageId):
        print("Sending suback packet")
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        header.append(0x09 << 4)
        varHeader.extend(self._encodeValue(messageId))
        for i in grantedQos:
            payload.append(i)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def unsubscribe(self, topic, messageId = None):
        print("Sending unsubscribe packet")
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        header.append(0x0A << 4 | 0x01 << 1)
        if messageId is not None:
            varHeader.extend(self._encodeValue(self.messageID))
        else:
            varHeader.extend(self._encodeValue(random.randint(1, 0xFFFF)))
        payload.extend(self._encodeString(topic))
        header.extend(self._encodeLength(len(payload) + len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def unsuback(self, messageId):
        print("Sending unsuback packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x0B << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pingreq(self):
        # print("Sending pingreq packet")
        header = bytearray()
        header.append(0x0C << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))

    def pingresp(self):
        print("Sending pingresp packet")
        header = bytearray()
        header.append(0x0D << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))

    def disconnect(self):
        print("Sending disconnect packet")
        header = bytearray()
        header.append(0x0E << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))


class MQTTClient(MQTTProtocol):

    m_pingPeriod = 5

    def __init__(self, p_pyhouse_obj, p_clientID = None, keepalive = None, willQos = 0, willTopic = None, willMessage = None, willRetain = False):
        self.m_pyhouse_obj = p_pyhouse_obj
        try:
            l_name = p_pyhouse_obj.Computer.Nodes[0].Name
        except KeyError:
            l_name = "UnknownNode"
        print("Client __init__  ID: {} {}".format(p_clientID, l_name))
        if p_clientID is not None:
            self.m_clientID = p_clientID
        else:
            self.m_clientID = l_name
        if keepalive is not None:
            self.m_keepalive = keepalive
        else:
            self.m_keepalive = 60000
        self.willQos = willQos
        self.willTopic = willTopic
        self.willMessage = willMessage
        self.willRetain = willRetain

    def connectionMade(self):
        """
        TCP Connected
        Now use MQTT connect packet to establish protocol connection.
        """
        print("Client connectionMade Keepalive: {}".format(self.m_keepalive))
        LOG.info("Client TCP connectionMade Keepalive: {}".format(self.m_keepalive))
        self.connect(self.m_clientID, self.m_keepalive, self.willTopic, self.willMessage, self.willQos, self.willRetain, True)
        print("Mqtt-1 {}".format(PrettyPrintAny(self.m_pyhouse_obj, "P1 PyHouse")))
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def connectionLost(self, reason):
        print("\nClient connectionLost\n  Disconnected from MQTT Broker\n  Reason: {}\n".format(reason))
        LOG.info("Disconnected from MQTT Broker: {}".format(reason))

    def mqttConnected(self):
        print("Client mqttConnected")
        self.subscribe(SUBSCRIBE)

    def connackReceived(self, p_status):
        print('Client conackReceived - Status: {}'.format(p_status))
        if p_status == 0:
            self.mqttConnected()

    def pubackReceived(self, _messageId):
        print('Client pubackReceived {}')

    def subackReceived(self, _grantedQos, _messageId):
        """Override
        """
        print("Client subackReceived")
        self.m_pyhouse_obj.APIs.Comp.MqttAPI.doPyHouseLogin(self, self.m_pyhouse_obj)

    def pingrespReceived(self):
        # LOG.info('Client pingrespReceived.')
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def publishReceived(self, p_topic, p_message, _qos = 0, _dup = False, _retain = False, _messageId = None):
        """ This is where we receive all the pyhouse messages.
        Call the dispatcher to send them on to the correct place.
        """
        LOG.info("Client publishReceived\n  Topic: {}\n  Message: {}".format(p_topic, p_message))
        print("Client publishReceived\n  Topic: {}\n  Message: {}".format(p_topic, p_message))
        # self.MqttDispatch(p_topic, p_message)


###########################################

class MqttClientFactory(ClientFactory):
    """
    Holds the persistent State info.
    """

    m_pingPeriod = 5

    def __init__(self, p_pyhouse_obj, p_client_id, p_broker):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        self.m_clientID = p_client_id
        # print("Factory __init__ Broker: {}".format(self.m_broker))

    def startedConnecting(self, _p_connector):
        """
        p_connector is an instance of twisted.internet.tcp.Connector
        """
        # print('Factory startedConnecting.')
        pass

    def connectionMade(self):
        """ Physical connection made to broker, now perform protocol connection.
        """
        print('Factory connectionMade to MQTT Broker')
        LOG.info('Connected to MQTT Broker')
        self.connect(self.m_clientID, keepalive = self.m_pingPeriod * 3000)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def buildProtocol(self, p_addr):
        l_client = MQTTClient(self.m_pyhouse_obj)
        # print('Factory buildProtocol - Addr: {} - {}'.format(p_addr, l_client))
        LOG.info("Mqtt broker address: {}".format(p_addr))
        self.m_pyhouse_obj.Computer.Mqtt.ProtocolAPI = l_client
        print("Mqtt-2 {}".format(PrettyPrintAny(self.m_pyhouse_obj.Computer.Mqtt, "P2 PyHouse.Computer.Mqtt")))
        return l_client

    def clientConnectionLost(self, p_connector, p_reason):
        print('\nFactory clientConnectionLost.\n  Reason: {}\n  Connector: {}'.format(p_reason, p_connector))

    def clientConnectionFailed(self, p_connector, p_reason):
        print('Factory Connection failed. Reason: {} - {}'.format(p_reason, p_connector))

    def pingrespReceived(self):
        print('Factory Ping received from MQTT broker')
        LOG.info('Ping received from MQTT broker')
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def connackReceived(self, status):
        if status == 0:
            self.onBrokerConnected()
        else:
            print('Factory Connection to MQTT broker failed')
            LOG.info('Connection to MQTT broker failed')


# ## END DBK
