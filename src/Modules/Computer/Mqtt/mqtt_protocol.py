"""
@name:      PyHouse/src/Modules/Computer/Mqtt/protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:   This creates the Twisted (Async) version of MQTT client.

Warning.  There are two things called connect in this module.
The first is a TCP connection to the Mqtt broker.
The second is a MQTT connection to the broker that uses the first connection as a transport.

"""

# Import system type stuff
import random
# from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol, ReconnectingClientFactory

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt.mqtt_util import EncodeDecode


LOG = Logger.getLogger('PyHouse.Mqtt_Protocol  ')

# BROKERv4 = '192.168.1.71'
# BROKERv4 = 'iot.eclipse.org'  # Sandbox Mosquitto broker
# BROKERv6 = '2604:8800:100:8268::1:1'    # Pink Poppy
# BROKERv6 = '2001:4830:1600:84ae::1'  # Cannon Trail
# PORT = 1883
SUBSCRIBE = 'pyhouse/#'


class MQTTProtocol(Protocol):
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
                l_length = EncodeDecode._decodeLength(self.m_buffer[1:])
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
            LOG.error("Invalid packet type {:x}".format(packet_type))
            return
        # Strip the fixed header
        lenLen = 1
        while packet[lenLen] & 0x80:
            lenLen += 1
        packet = packet[lenLen + 1:]
        # Get the appropriate handler function
        l_packetHandler = getattr(self, "_event_%s" % packet_type_name, None)
        if l_packetHandler:
            l_packetHandler(packet, qos, dup, retain)
        else:
            LOG.error("Invalid packet handler for {}".format(packet_type_name))
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
        keepalive = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the client id
        clientID = EncodeDecode._decodeString(packet)
        packet = packet[len(clientID) + 2:]
        # Extract the will topic and message, if applicable
        willTopic = None
        willMessage = None
        if willFlag:
            # Extract the will topic
            willTopic = EncodeDecode._decodeString(packet)
            packet = packet[len(willTopic) + 2:]
            # Extract the will message
            # Whatever remains is the will message
            willMessage = packet
        LOG.info('Mqtt Connected.')
        self.connectReceived(clientID, keepalive, willTopic,
                             willMessage, willQos, willRetain,
                             cleanStart)

    def _event_connack(self, packet, _qos, _dup, _retain):
        # Return the status field
        self.connackReceived(packet[0])

    def _event_publish(self, packet, qos, dup, retain):
        # Extract the topic name
        topic = EncodeDecode._decodeString(packet)
        packet = packet[len(topic) + 2:]
        # Extract the message ID if appropriate
        messageId = None
        if qos > 0:
            messageId = EncodeDecode._decodeValue(packet[:2])
            packet = packet[2:]
        # Extract the message
        # Whatever remains is the message
        message = str(packet)
        LOG.info('Mqtt Publish: {}\n\t{}'.format(topic, message))
        self.publishReceived(topic, message, qos, dup, retain, messageId)

    def _event_puback(self, packet, _qos, _dup, _retain):
        # Extract the message ID
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubackReceived(messageId)

    def _event_pubrec(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubrecReceived(messageId)

    def _event_pubrel(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubrelReceived(messageId)

    def _event_pubcomp(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubcompReceived(messageId)

    def _event_subscribe(self, packet, qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        topics = []
        while len(packet):
            topic = EncodeDecode._decodeString(packet)
            packet = packet[len(topic) + 2:]
            qos = packet[0]
            packet = packet[1:]
            # Add them to the list of (topic, qos)s
            topics.append((topic, qos))
        LOG.info('Mqtt Subscribe: {}'.format(topics))
        self.subscribeReceived(topics, messageId)

    def _event_suback(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the granted QoS levels
        grantedQos = []
        while len(packet):
            grantedQos.append(packet[0])
            packet = packet[1:]
        self.subackReceived(grantedQos, messageId)

    def _event_unsubscribe(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        # Extract the unsubscribing topics
        topics = []
        while len(packet):
            topic = EncodeDecode._decodeString(packet)
            packet = packet[len(topic) + 2:]
            topics.append(topic)
        LOG.info('Mqtt UnSubscribe: {}'.format(topics))
        self.unsubscribeReceived(topics, messageId)


    def _event_unsuback(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.unsubackReceived(messageId)

    def _event_pingreq(self, _packet, _qos, _dup, _retain):
        self.pingreqReceived()

    def _event_pingresp(self, _packet, _qos, _dup, _retain):
        self.pingrespReceived()

    def _event_disconnect(self, _packet, _qos, _dup, _retain):
        LOG.info('Mqtt Disconnect:')
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

    def publishReceived(self, _topic, _message, _qos = 0, _dup = False, _retain = False, _messageId = None):
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
        LOG.info("Sending connect packet  ID: {}".format(p_clientID))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        varHeader.extend(EncodeDecode._encodeString("MQIsdp"))
        varHeader.append(3)
        if willMessage is None or willTopic is None:
            # Clean start, no will message
            varHeader.append(0 << 2 | cleanStart << 1)
        else:
            varHeader.append(willRetain << 5 | willQoS << 3
                             | 1 << 2 | cleanStart << 1)
        varHeader.extend(EncodeDecode._encodeValue(keepalive / 1000))
        payload.extend(EncodeDecode._encodeString(p_clientID))
        if willMessage is not None and willTopic is not None:
            payload.extend(EncodeDecode._encodeString(willTopic))
            payload.extend(EncodeDecode._encodeString(willMessage))
        header.append(0x01 << 4)
        header.extend(EncodeDecode._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def connack(self, status):
        header = bytearray()
        payload = bytearray()
        header.append(0x02 << 4)
        payload.append(status)
        header.extend(EncodeDecode._encodeLength(len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(payload))

    def publish(self, p_topic, p_message, qosLevel = 0, retain = False, dup = False, messageId = None):
        LOG.info("Sending publish packet - Topic: {}  Message: {}".format(p_topic, p_message))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = publish
        header.append(0x03 << 4 | dup << 3 | qosLevel << 1 | retain)
        varHeader.extend(EncodeDecode._encodeString(p_topic))
        if qosLevel > 0:
            if messageId is not None:
                varHeader.extend(EncodeDecode._encodeValue(messageId))
            else:
                varHeader.extend(EncodeDecode._encodeValue(random.randint(1, 0xFFFF)))
        payload.extend(p_message)
        header.extend(EncodeDecode._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def puback(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x04 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrec(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x05 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrel(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x06 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubcomp(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x07 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def subscribe(self, p_topic, requestedQoS = 0, messageId = None):
        """
        Only supports QoS = 0 subscribes
        Only supports one subscription per message
        """
        LOG.info("Sending subscribe packet - Topic: {}".format(p_topic))
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = subscribe, QoS = 1
        header.append(0x08 << 4 | 0x01 << 1)
        if messageId is None:
            varHeader.extend(EncodeDecode._encodeValue(random.randint(1, 0xFFFF)))
        else:
            varHeader.extend(EncodeDecode._encodeValue(messageId))
        payload.extend(EncodeDecode._encodeString(p_topic))
        payload.append(requestedQoS)
        header.extend(EncodeDecode._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def suback(self, grantedQos, messageId):
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        header.append(0x09 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        for i in grantedQos:
            payload.append(i)
        header.extend(EncodeDecode._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def unsubscribe(self, topic, messageId = None):
        LOG.info("Sending unsubscribe packet")
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        header.append(0x0A << 4 | 0x01 << 1)
        if messageId is not None:
            varHeader.extend(EncodeDecode._encodeValue(self.messageID))
        else:
            varHeader.extend(EncodeDecode._encodeValue(random.randint(1, 0xFFFF)))
        payload.extend(EncodeDecode._encodeString(topic))
        header.extend(EncodeDecode._encodeLength(len(payload) + len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def unsuback(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x0B << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pingreq(self):
        header = bytearray()
        header.append(0x0C << 4)
        header.extend(EncodeDecode._encodeLength(0))
        self.transport.write(str(header))

    def pingresp(self):
        header = bytearray()
        header.append(0x0D << 4)
        header.extend(EncodeDecode._encodeLength(0))
        self.transport.write(str(header))

    def disconnect(self):
        LOG.info("Sending disconnect packet")
        header = bytearray()
        header.append(0x0E << 4)
        header.extend(EncodeDecode._encodeLength(0))
        self.transport.write(str(header))


class MQTTClient(MQTTProtocol):

    m_pingPeriod = 5

    def __init__(self, p_pyhouse_obj, p_clientID = None, keepalive = None, willQos = 0, willTopic = None, willMessage = None, willRetain = False):
        self.m_pyhouse_obj = p_pyhouse_obj
        # try:
        #    l_name = p_pyhouse_obj.Computer.Nodes[0].Name
        # except KeyError:
        #    l_name = "UnknownNode"
        if p_clientID is not None:
            self.m_clientID = p_clientID
        else:
            self.m_clientID = 'abc'
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
        LOG.info("Client TCP connectionMade Keepalive: {}".format(self.m_keepalive))
        self.connect(self.m_clientID, self.m_keepalive, self.willTopic, self.willMessage, self.willQos, self.willRetain, True)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def connectionLost(self, reason):
        LOG.info("Disconnected from MQTT Broker: {}".format(reason))

    def mqttConnected(self):
        LOG.info("Client mqttConnected")
        self.subscribe(SUBSCRIBE)

    def connackReceived(self, p_status):
        LOG.info('Client conackReceived - Status: {}'.format(p_status))
        if p_status == 0:
            self.mqttConnected()

    def pubackReceived(self, _messageId):
        pass

    def subackReceived(self, _grantedQos, _messageId):
        """Override
        """
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.doPyHouseLogin(self, self.m_pyhouse_obj)

    def pingrespReceived(self):
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def publishReceived(self, p_topic, p_message, _qos = 0, _dup = False, _retain = False, _messageId = None):
        """ This is where we receive all the pyhouse messages.
        Call the dispatcher to send them on to the correct place.
        """
        LOG.info("Client publishReceived\n  Topic: {}\n  Message: {}".format(p_topic, p_message))
        # self.MqttDispatch(p_topic, p_message)


###########################################


class MqttReconnectingClientFactory(ReconnectingClientFactory):

    def __init__(self, p_pyhouse_obj, p_client_id, p_broker):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_client_id: is the ID of this computer that will be supplied to the broker
        @param p_broker: is ???
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        p_broker.ProtocolAPI = self
        self.m_clientID = p_client_id

    def startedConnecting(self, _p_connector):
        LOG.warn('Started to connect.')

    def buildProtocol(self, p_addr):
        l_client = MQTTClient(self.m_pyhouse_obj)
        self.m_broker.ProtocolAPI = l_client
        LOG.info("Mqtt broker address: {}".format(p_addr))
        self.resetDelay()
        # self.m_pyhouse_obj.Computer.Mqtt.ProtocolAPI = l_client
        return l_client

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.  Reason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed. Reason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """
        Added to sample code - I don't know why it is required.
        """
        LOG.error('ConnectionLost Err:{}'.format(p_reason))

    def makeConnection(self, p_transport):
        """
        Added to sample code - I don't know why it is required.
        """
        LOG.warn('makeConnection {}'.format(p_transport))

# ## END DBK
