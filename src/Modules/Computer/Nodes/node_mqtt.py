"""
@name:      C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/Nodes/node_mqtt.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:


topic scheme:
    PyHouse/<Domain UUID>/<HouseIdentifier>/<Device Specific>
    Where <Device Specific> is:
        <Location>/<Function>/<Action>
            <Location> = Room Name or some other description
            <Function> = Temperature, LightLevel, HumanDetected, Rainfall, WindSpeed etc.
            <Action> = Reading, TurnOn, TurnOff to list a few.
    There are no spaces in any of the sections.


<mqtt>
    <BrokerIp4 />
    <BrokerIp6 />
</mqtt>

"""

# Import system type stuff
# from paho.mqtt import client as mqtt
import datetime
import json
import random
from twisted.internet import defer
from twisted.internet.protocol import ClientCreator
from twisted.internet.protocol import Protocol


# Import PyMh files and modules.
# from Modules.Core.data_objects import NodeData, NodeInterfaceData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Nodes import nodes_xml

LOG = Logger.getLogger('PyHouse.NodeMqtt       ')


class MQTTProtocol(Protocol):

    _packetTypes = {0x00: "null", 0x01: "connect", 0x02: "connack",
                    0x03: "publish", 0x04: "puback", 0x05: "pubrec",
                    0x06: "pubrel", 0x07: "pubcomp", 0x08: "subscribe",
                    0x09: "suback", 0x0A: "unsubscribe", 0x0B: "unsuback",
                    0x0C: "pingreq", 0x0D: "pingresp", 0x0E: "disconnect"}
    buffer = bytearray()

    def dataReceived(self, data):
        self._accumulatePacket(data)

    def _accumulatePacket(self, data):
        self.buffer.extend(data)
        length = None
        while len(self.buffer):
            if length is None:
                # Start on a new packet
                # Haven't got enough data to start a new packet, wait for some more
                if len(self.buffer) < 2:
                    break
                lenLen = 1
                # Calculate the length of the length field
                while lenLen < len(self.buffer):
                    if not self.buffer[lenLen] & 0x80:
                        break
                    lenLen += 1
                # We still haven't got all of the remaining length field
                if lenLen < len(self.buffer) and self.buffer[lenLen] & 0x80:
                    return
                length = self._decodeLength(self.buffer[1:])
            if len(self.buffer) >= length + lenLen + 1:
                chunk = self.buffer[:length + lenLen + 1]
                self._processPacket(chunk)
                self.buffer = self.buffer[length + lenLen + 1:]
                length = None
            else:
                break

    def _processPacket(self, packet):
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
        packetHandler = getattr(self, "_event_%s" % packet_type_name, None)
        if packetHandler:
            packetHandler(packet, qos, dup, retain)
        else:
            print "Invalid packet handler for %s" % packet_type_name
            return

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

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def connectReceived(self, clientID, keepalive, willTopic, willMessage, willQoS, willRetain, cleanStart):
        pass

    def connackReceived(self, status):
        pass

    def publishReceived(self, topic, message, qos = 0, dup = False, retain = False, messageId = None):
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

    def connect(self, clientID, keepalive = 3000, willTopic = None, willMessage = None, willQoS = 0, willRetain = False, cleanStart = True):
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
        payload.extend(self._encodeString(clientID))
        if willMessage is not None and willTopic is not None:
            payload.extend(self._encodeString(willTopic))
            payload.extend(self._encodeString(willMessage))
        header.append(0x01 << 4)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def connack(self, status):
        header = bytearray()
        payload = bytearray()
        header.append(0x02 << 4)
        payload.append(status)
        header.extend(self._encodeLength(len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(payload))

    def publish(self, topic, message, qosLevel = 0, retain = False, dup = False, messageId = None):
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = publish
        header.append(0x03 << 4 | dup << 3 | qosLevel << 1 | retain)
        varHeader.extend(self._encodeString(topic))
        if qosLevel > 0:
            if messageId is not None:
                varHeader.extend(self._encodeValue(messageId))
            else:
                varHeader.extend(self._encodeValue(random.randint(1, 0xFFFF)))
        payload.extend(message)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def puback(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x04 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrec(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x05 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubrel(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x06 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pubcomp(self, messageId):
        header = bytearray()
        varHeader = bytearray()
        header.append(0x07 << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def subscribe(self, topic, requestedQoS = 0, messageId = None):
        """
        Only supports QoS = 0 subscribes
        Only supports one subscription per message
        """
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        # Type = subscribe, QoS = 1
        header.append(0x08 << 4 | 0x01 << 1)
        if messageId is None:
            varHeader.extend(self._encodeValue(random.randint(1, 0xFFFF)))
        else:
            varHeader.extend(self._encodeValue(messageId))
        payload.extend(self._encodeString(topic))
        payload.append(requestedQoS)
        header.extend(self._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))
        self.transport.write(str(payload))

    def suback(self, grantedQos, messageId):
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
        header = bytearray()
        varHeader = bytearray()
        header.append(0x0B << 4)
        varHeader.extend(self._encodeValue(messageId))
        header.extend(self._encodeLength(len(varHeader)))
        self.transport.write(str(header))
        self.transport.write(str(varHeader))

    def pingreq(self):
        header = bytearray()
        header.append(0x0C << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))

    def pingresp(self):
        header = bytearray()
        header.append(0x0D << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))

    def disconnect(self):
        header = bytearray()
        header.append(0x0E << 4)
        header.extend(self._encodeLength(0))
        self.transport.write(str(header))

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


class MQTTClient(MQTTProtocol):

    def __init__(self, clientId = None, keepalive = None, willQos = 0, willTopic = None, willMessage = None, willRetain = False):
        if clientId is not None:
            self.clientId = clientId
        else:
            self.clientId = "Twisted%i" % random.randint(1, 0xFFFF)
        if keepalive is not None:
            self.keepalive = keepalive
        else:
            self.keepalive = 3000
        self.willQos = willQos
        self.willTopic = willTopic
        self.willMessage = willMessage
        self.willRetain = willRetain

    def connectionMade(self):
        self.connect(self.clientId, self.keepalive, self.willTopic, self.willMessage, self.willQos, self.willRetain, True)

    def connackReceived(self, status):
        if status == 0:
            self.mqttConnected()
        else:
            # Error
            pass

    def mqttConnected(self):
        pass



class Util(object):

    @staticmethod
    def on_connect():
        pass

    @staticmethod
    def on_data_received():
        pass


class API(Util):

    m_pyhouse_obj = None
    m_client = None

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # Read xml data
        # self.m_client = mqtt.Client()
        # self.m_client.on_connect = Util.on_connect
        # self.m_client.on_message = Util.on_message
        self.m_client.connect("iot.eclipse.org", 1883, 60)

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        p_xml.append(nodes_xml.Xml().write_nodes_xml(self.m_pyhouse_obj.Computer.Nodes))
        LOG.info("Saved XML.")

    def PublishUpdates(self):
        '''
        Publish updates to MQTT Broker.

        Publish one message from the queue at a time. Reschedule
        calls back to this function until all messages are sent.
        This approach gives some time back to the reactor to handle
        other things.
        '''
        if self.publishQueue:
            topic, message = self.publishQueue.pop()
            self.mqttConnection.publish(topic, message)
            if self.publishQueue:
                self.m_pyhouse_obj.Twisted.Reactor.callLater(0.1, self.publishUpdates)
            else:
                LOG.info("Completed publishing observation updates.")

# ## END DBK


###########################



###########################################

class MQTTPublisher(MQTTProtocol):

    pingPeriod = 60

    def __init__(self, client_id, onBrokerConnected):
        self.client_id = client_id
        self.onBrokerConnected = onBrokerConnected

    def connectionMade(self):
        ''' Physical connection made to broker, now perform protocol connection '''
        LOG.info('Connected to MQTT Broker')
        self.connect(self.client_id, keepalive = self.pingPeriod * 1000)
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.pingPeriod, self.pingreq)

    def connectionLost(self, reason):
        ''' '''
        LOG.info("Disconnected from MQTT Broker: %s" % reason)

    def pingrespReceived(self):
        LOG.info('Ping received from MQTT broker')
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.pingPeriod, self.pingreq)

    def connackReceived(self, status):
        if status == 0:
            self.onBrokerConnected()
        else:
            LOG.info('Connection to MQTT broker failed')


class BomauObservationsClient(object):
    """
    The observations client allows a user to obtain BoM observations for a specified URL.
    """

    def __init__(self, observation_url):
        self.observation_url = observation_url
        # A reference to the task that periodically requests an observation update.
        # This is needed so the task can be stopped later.
        self.periodicRetrievalTask = None
        self.mqttConnection = None
        # This list is used to temporarily hold the list of publish messages.
        self.publishQueue = []

    @defer.inlineCallbacks
    def start(self):
        ''' Start the MQTT publisher '''
        LOG.info('BoM Observation Client starting')
        clientCreator = ClientCreator(self.m_pyhouse_obj.Twisted.Reactor,
                                      MQTTPublisher,
                                      "BomAuPub",
                                      self.onMQTTBrokerCommunicationEstablished)
        LOG.info('Creating MQTT client')
        self.mqttConnection = yield clientCreator.connectTCP('192.168.1.72', 1883)
        defer.returnValue(True)

    def stop(self):
        """
        Stop monitoring sensors in and around the home environment
        """
        LOG.info('BoM Observation Client stopping')
        if self.mqttConnection:
            self.mqttConnection.transport.loseConnection()
        if self.periodicRetrievalTask:
            if self.periodicRetrievalTask.active():
                self.periodicRetrievalTask.cancel()

    def onMQTTBrokerCommunicationEstablished(self):
        '''
        Upon connection to MQTT Broker begin periodic weather
        observation retrievals.
        '''
        self.retrieveObservations()

    @defer.inlineCallbacks
    def retrieveObservations(self):
        """
        Retrieve the latest BoM observation and store it
        """
        observations = yield self.get_observations()
        if observations:
            LOG.info("BoM observations for %i regions retrieved successfully" % len(observations))
            # convert observations into MQTT format messages and add them
            # into a queue for publishing.
            for state in observations:
                # for this demonstration only publish stations for the
                # state of South Australia.
                if state in ['South Australia']:
                    LOG.info("%s has %i stations" % (state, len(observations[state])))
                    for station in observations[state]:
                        # for this demonstration only publish the Adelaide
                        # station data.
                        if station == 'Adelaide':
                            payload = json.dumps(observations[state][station])
                            topic = 'bomau/%s/%s' % (state, station)
                            self.publishQueue.append((topic, payload))
            if self.publishQueue:
                LOG.info("Beginning to publish %i updates to MQTT Broker" % len(self.publishQueue))
                self.publishUpdates()
        defer.returnValue(None)

    @defer.inlineCallbacks
    def get_observations(self):
        """
        Retrieve the latest observations from the BOM in JSON format.

        Returns a deferred that will eventually return an Observation
        object with attributes populated from parsing the JSON update.

        @return: A deferred that returns an Observations object
        @rtype: defer.Deferred
        """
        d = {'updated' : update_time_utc}
        observations = []
        LOG.debug("%s contained %i stations" % (state, len(observations[state])))
        defer.returnValue(observations)

    def publishUpdates(self):
        """
        Publish updates to MQTT Broker.

        Publish one message from the queue at a time.
        Reschedule calls back to this function until all messages are sent.
        This approach gives some time back to the reactor to handle other things.
        """
        if self.publishQueue:
            topic, message = self.publishQueue.pop()
            self.mqttConnection.publish(topic, message)
            if self.publishQueue:
                self.m_pyhouse_obj.Twisted.Reactor.callLater(0.1, self.publishUpdates)
            else:
                LOG.info("Completed publishing observation updates.")


if __name__ == '__main__':

    bomau_weather = BomauObservationsClient(observations_url)
