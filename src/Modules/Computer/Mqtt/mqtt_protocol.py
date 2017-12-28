"""
@name:      PyHouse/src/Modules/Computer/Mqtt/protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:   This creates the Twisted (Async) version of MQTT client.

Warning.  There are two things called connect in this module.
The first is a TCP connection to the Mqtt broker.
The second is a MQTT connection to the broker that uses the first connection as a transport.

"""

__updated__ = '2017-12-28'

#  Import system type stuff
import random
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
#  from twisted.internet import ssl
#  from twisted.internet.ssl import Certificate
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt.mqtt_util import EncodeDecode
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import FormatBytes, PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Mqtt_Protocol  ')
SUBSCRIBE = 'pyhouse/#'


class MQTTProtocol(Protocol):
    """
    This protocol is used for communication with the MQTT broker.
    """

    #  The first 4 bits of a MQTT packet are the packet type.
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
                #  Start on a new packet
                #  Haven't got enough data to start a new packet, wait for some more
                if len(self.m_buffer) < 2:
                    break
                lenLen = 1
                #  Calculate the length of the length field
                while lenLen < len(self.m_buffer):
                    if not self.m_buffer[lenLen] & 0x80:
                        break
                    lenLen += 1
                #  We still haven't got all of the remaining length field
                if lenLen < len(self.m_buffer) and self.m_buffer[lenLen] & 0x80:
                    #  LOG.warn('### Early return {}'.format(FormatBytes(self.m_buffer)))
                    return
                l_length = EncodeDecode._decodeLength(self.m_buffer[1:])

            if len(self.m_buffer) >= l_length + lenLen + 1:
                chunk = self.m_buffer[:l_length + lenLen + 1]
                self._processPacket(chunk)

                self.m_buffer = self.m_buffer[l_length + lenLen + 1:]
                l_length = None
            else:
                #  LOG.warn('### exit without processing {}'.format(FormatBytes(self.m_buffer)))
                break

    def _processPacket(self, packet):
        """Handle the Header (2-5 bytes)
        See http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html

        @param packet: is a bytearray containing the packet
        """
        # LOG.debug('Processing packet: {}'.format(FormatBytes(packet)))
        try:
            packet_type = (packet[0] & 0xF0) >> 4
            packet_type_name = self._packetTypes[packet_type]
            dup = (packet[0] & 0x08) == 0x08
            qos = (packet[0] & 0x06) >> 1
            retain = (packet[0] & 0x01) == 0x01
        except:
            #  Invalid packet type, throw away this packet
            LOG.error("Invalid packet type {:x}".format(packet_type))
            return
        #  Strip the fixed header
        lenLen = 1
        while packet[lenLen] & 0x80:
            lenLen += 1
        packet = packet[(lenLen + 1):]  # Now we have the variable header and the payload.
        #  Get the appropriate handler function
        l_packetHandler = getattr(self, "_event_%s" % packet_type_name, None)
        if l_packetHandler:
            l_packetHandler(packet, qos, dup, retain)  # this will dispatch to the appropriate routine for the packet type "_event_publish" for example.
        else:
            LOG.error("Invalid packet handler for {}".format(packet_type_name))
            return

    #  These are the events - one for each packet type

    def _event_connect(self, packet, _qos, _dup, _retain):
        """This will decode a received 'connect' packet.
        """
        LOG.info('Event Connect received.')
        #  Strip variable header
        packet = packet[10:]
        #  Extract the connect flags
        f_username = packet[0] & 0x80 == 0x80
        f_password = packet[0] & 0x40 == 0x40
        f_willRetain = packet[0] & 0x20 == 0x20
        l_willQos = packet[0] & 0x18 >> 3
        f_willFlag = packet[0] & 0x04 == 0x04
        f_cleanStart = packet[0] & 0x02 == 0x02
        packet = packet[1:]
        keepalive = EncodeDecode._decodeValue(packet[:2])  # Extract the keepalive period
        packet = packet[2:]
        clientID = EncodeDecode._decodeString(packet)  # Extract the client id_event_connect
        packet = packet[len(clientID) + 2:]
        # Extract the will topic and message, if applicable
        l_willTopic = None
        l_willMessage = None
        if f_willFlag:
            #  Extract the will topic
            l_willTopic = EncodeDecode._decodeString(packet)
            packet = packet[len(l_willTopic) + 2:]
            #  Extract the will message
            #  Whatever remains is the will message
            #  ##  l_willMessage = packet
            l_willMessage = EncodeDecode._decodeString(packet)
            packet = packet[len(l_willMessage) + 2:]
        l_username = None
        if f_username:  # Extract user name if one is present.
            l_username = EncodeDecode._decodeString(packet)
            packet = packet[len(l_username) + 2:]
        l_password = None
        if f_password:  # Extract password if one is present.
            l_password = EncodeDecode._decodeString(packet)
            packet = packet[len(l_password) + 2:]
        LOG.info('Mqtt Connected.')
        self.connectReceived(clientID, keepalive, l_willTopic,
                             l_willMessage, l_willQos, f_willRetain,
                             f_cleanStart, l_username, l_password)

    def _event_connack(self, packet, _qos, _dup, _retain):
        """ We just received a connck packet.
        The broker has confirmed our MQTT connection.
        """
        LOG.info('Event Conack received: {} {}'.format(len(packet), FormatBytes(packet)))
        #  Return the status field
        self.connackReceived(packet[0])

    def _event_publish(self, packet, qos, dup, retain):
        """ Receive a "Published" message

        Here we get a published message from the broker.
        Extract the parts of the packet.
        @param packet: is a bytearray containing the variable header and payload combined.
        """
        #  Extract the topic portion of the packet.
        l_topic = EncodeDecode._decodeString(packet)
        packet = packet[len(l_topic) + 2:]
        # LOG.debug('Publish qos:{}'.format(qos))
        # LOG.debug('Publish topic:{}'.format(l_topic))
        #  Extract the message ID if appropriate
        messageId = None
        if qos > 0:
            messageId = EncodeDecode._decodeValue(packet[:2])
            packet = packet[2:]
            LOG.debug('Publish MsgID:{}'.format(messageId))
        #  Extract whatever remains as the message
        l_json = EncodeDecode._get_string(packet)
        # l_json = packet.decode('utf-8')
        # LOG.debug('Publish message:{}'.format(l_json))
        l_message = json_tools.decode_json_unicode(l_json)
        LOG.info('Publish:\n\tTopic: {}\n\tPayload: {}'.format(l_topic, PrettyFormatAny.form(l_message, 'Publish')))
        # l_topic is a string
        # l_message is a string
        self.publishReceived(l_topic, l_message, qos, dup, retain, messageId)

    def _event_puback(self, packet, _qos, _dup, _retain):
        LOG.info('Event PubAck received: {} {}'.format(len(packet), packet))
        #  Extract the message ID
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubackReceived(messageId)

    def _event_pubrec(self, packet, _qos, _dup, _retain):
        LOG.info('Event PubRec received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubrecReceived(messageId)

    def _event_pubrel(self, packet, _qos, _dup, _retain):
        LOG.info('Event PubRel received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubrelReceived(messageId)

    def _event_pubcomp(self, packet, _qos, _dup, _retain):
        LOG.info('Event PubComp received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.pubcompReceived(messageId)

    def _event_subscribe(self, packet, qos, _dup, _retain):
        LOG.info('Event Subscribe received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        topics = []
        while len(packet):
            topic = EncodeDecode._decodeString(packet)
            packet = packet[len(topic) + 2:]
            qos = packet[0]
            packet = packet[1:]
            #  Add them to the list of (topic, qos)s
            topics.append((topic, qos))
        LOG.info('Mqtt Subscribe: {}'.format(topics))
        self.subscribeReceived(topics, messageId)

    def _event_suback(self, packet, _qos, _dup, _retain):
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        LOG.info('Event SubAck received - MsgID:{}  Acks: {} {}'.format(messageId, len(packet), packet))
        #  Extract the granted QoS levels
        grantedQos = []
        while len(packet):
            grantedQos.append(packet[0])
            packet = packet[1:]
        self.subackReceived(grantedQos, messageId)

    def _event_unsubscribe(self, packet, _qos, _dup, _retain):
        LOG.info('Event Unsubscribe received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        packet = packet[2:]
        #  Extract the unsubscribing topics
        topics = []
        while len(packet):
            topic = EncodeDecode._decodeString(packet)
            packet = packet[len(topic) + 2:]
            topics.append(topic)
        LOG.info('Mqtt UnSubscribe: {}'.format(topics))
        self.unsubscribeReceived(topics, messageId)

    def _event_unsuback(self, packet, _qos, _dup, _retain):
        LOG.info('Event UnsubAck received: {} {}'.format(len(packet), packet))
        messageId = EncodeDecode._decodeValue(packet[:2])
        self.unsubackReceived(messageId)

    def _event_pingreq(self, packet, _qos, _dup, _retain):
        # LOG.info('Event Pingreq received: {} {}'.format(len(packet), packet))
        self.pingreqReceived()

    def _event_pingresp(self, packet, _qos, _dup, _retain):
        # LOG.debug('Event Pingresp received: {} {}'.format(len(packet), packet))
        self.pingrespReceived()

    def _event_disconnect(self, packet, _qos, _dup, _retain):
        LOG.info('Event Publish received: {} {}'.format(len(packet), packet))
        self.disconnectReceived()

    #  these are to be overridden below

    def connectionMade(self):
        raise NotImplementedError  # Subclasses must implement this.

    def connectionLost(self, reason):
        raise NotImplementedError  # Subclasses must implement this.

    # These are packet types

    def connectReceived(self, clientID, keepalive, willTopic, willMessage, willQoS, willRetain, cleanStart, userName, password):
        raise NotImplementedError  # Subclasses must implement this.

    def connackReceived(self, status):
        raise NotImplementedError  # Subclasses must implement this.

    def publishReceived(self, _topic, _message, _qos=0, _dup=False, _retain=False, _messageId=None):
        raise NotImplementedError  # Subclasses must implement this.

    def pubackReceived(self, messageId):
        raise NotImplementedError  # Subclasses must implement this.

    def pubrecReceived(self, messageId):
        pass

    def pubrelReceived(self, messageId):
        pass

    def pubcompReceived(self, messageId):
        pass

    def subscribeReceived(self, topics, messageId):
        pass

    def subackReceived(self, grantedQos, messageId):
        raise NotImplementedError  # Subclasses must implement this.

    def unsubscribeReceived(self, topics, messageId):
        pass

    def unsubackReceived(self, messageId):
        pass

    def pingreqReceived(self):
        pass

    def pingrespReceived(self):
        raise NotImplementedError  # Subclasses must implement this.

    def disconnectReceived(self):
        pass

    #  these are for sending Mqtt packets.

    def _build_fixed_header(self, p_packet_type, p_remaining_length, dup=0, qosLevel=0, retain=0):
        l_header = bytearray()
        l_header.append((p_packet_type & 0x0f) << 4 | (dup & 0x01) << 3 | (qosLevel & 0x03) << 1 | (retain & 0x01))
        l_header.extend(EncodeDecode._encodeLength(p_remaining_length))
        return l_header

    def _send_transport(self, p_fixed, p_var, p_payload):
        """
        @param p_fixed: is a bytearray containing the fixed header
        @param p_var: is a bytearray containing the variable header if any
        @param p_payload: is a bytearray containing the payload of the packet if any
        """
        # LOG.debug('MQTT   Fixed:({}) {}'.format(len(p_fixed), FormatBytes(p_fixed)))
        # LOG.debug('MQTT     Var:({}) {}'.format(len(p_var), FormatBytes(p_var)))
        # LOG.debug('MQTT Payload:({}) {}'.format(len(p_payload), FormatBytes(p_payload)))
        l_packet = bytearray()
        l_packet += p_fixed
        l_packet += p_var
        l_packet += p_payload
        self.transport.write(l_packet)

    def connect(self, p_clientID, keepalive=30000,
                willTopic=None, willMessage=None, willQoS=0, willRetain=False,
                cleanStart=True,
                username=None,
                password=None
                ):
        """
        DBK - Modified this packet to add username and password flags and fields (2016-01-22)
        """
        LOG.info("Sending 'connect' packet - ID: {}".format(p_clientID))
        l_varHeader = bytearray()
        l_payload = bytearray()
        # Version 3.0
        # l_varHeader.extend(EncodeDecode._encodeString("MQIsdp"))
        # l_varHeader.append(3)
        # Version 3.1.1
        l_varHeader.extend(EncodeDecode._encodeString("MQTT"))
        l_varHeader.append(4)
        varLogin = 0
        if username is not None:
            varLogin += 2
        if password is not None:
            varLogin += 1
        if willMessage is None or willTopic is None:
            #  Clean start, no will message
            l_varHeader.append(varLogin << 6 | 0 << 2 | cleanStart << 1)
        else:
            l_varHeader.append(varLogin << 6 | willRetain << 5 | willQoS << 3 | 1 << 2 | cleanStart << 1)
        l_varHeader.extend(EncodeDecode._encodeValue(int(keepalive / 1000)))
        l_payload.extend(EncodeDecode._encodeString(p_clientID))
        if willMessage is not None and willTopic is not None:
            LOG.debug('Adding last will testiment {}'.format(willMessage + willTopic))
            l_payload.extend(EncodeDecode._encodeString(willTopic))
            l_payload.extend(EncodeDecode._encodeString(willMessage))
        if username is not None and len(username) > 0:
            LOG.debug('Adding username "{}"'.format(username))
            l_payload.extend(EncodeDecode._encodeString(username))
        if password is not None and len(password) > 0:
            LOG.debug('Adding password "{}"'.format(password))
            l_payload.extend(EncodeDecode._encodeString(password))
        l_fixHeader = self._build_fixed_header(0x01, len(l_varHeader) + len(l_payload))
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def connack(self, status):
        LOG.warn('Sending connect ack packet')
        l_varHeader = bytearray()
        l_payload = bytearray()
        l_payload.append(status)
        l_fixHeader = self._build_fixed_header(0x02, len(l_varHeader) + len(l_payload))
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def publish(self, p_topic, p_message, qosLevel=0, retain=False, dup=False, messageId=None):
        LOG.info("Sending publish packet - Topic: {}".format(p_topic))
        l_varHeader = bytearray()
        l_payload = bytearray()
        #  Type = publish
        l_varHeader.extend(EncodeDecode._encodeString(p_topic))
        if qosLevel > 0:
            if messageId is not None:
                l_varHeader.extend(EncodeDecode._encodeValue(messageId))
            else:
                l_varHeader.extend(EncodeDecode._encodeValue(random.randint(1, 0xFFFF)))
        l_payload.extend(EncodeDecode._put_string(p_message))
        # l_payload.extend(p_message)
        l_fixHeader = self._build_fixed_header(0x03, len(l_varHeader) + len(l_payload), dup, qosLevel, retain)
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def puback(self, messageId):
        LOG.warn('Sending puback packet')
        header = bytearray()
        varHeader = bytearray()
        header.append(0x04 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubrec(self, messageId):
        LOG.info("Sending pubrec packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x05 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubrel(self, messageId):
        LOG.info("Sending pubrel packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x06 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubcomp(self, messageId):
        LOG.warn('Sending pubcomp packet')
        header = bytearray()
        varHeader = bytearray()
        header.append(0x07 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def subscribe(self, p_topic, requestedQoS=0, messageId=None):
        """
        Only supports QoS = 0 subscribes
        Only supports one subscription per message
        """
        LOG.info("Sending subscribe packet - Topic: {}".format(p_topic))
        l_varHeader = bytearray()
        l_payload = bytearray()
        #  Type = subscribe, QoS = 1
        if messageId is None:
            l_varHeader.extend(EncodeDecode._encodeValue(random.randint(1, 0xFFFF)))
        else:
            l_varHeader.extend(EncodeDecode._encodeValue(messageId))
        l_payload.extend(EncodeDecode._encodeString(p_topic))
        l_payload.append(requestedQoS)
        l_fixHeader = self._build_fixed_header(0x08, len(l_varHeader) + len(l_payload), qosLevel=1)
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def suback(self, grantedQos, messageId):
        LOG.info("Sending suback packet")
        header = bytearray()
        varHeader = bytearray()
        payload = bytearray()
        header.append(0x09 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        for i in grantedQos:
            payload.append(i)
        header.extend(EncodeDecode._encodeLength(len(varHeader) + len(payload)))
        self.transport.write(header)
        self.transport.write(varHeader)
        self.transport.write(payload)

    def unsubscribe(self, topic, messageId=None):
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
        self.transport.write(header)
        self.transport.write(varHeader)
        self.transport.write(payload)

    def unsuback(self, messageId):
        LOG.info("Sending unsuback packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x0B << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pingreq(self):
        # LOG.warn('Sending ping packet')
        l_empty = bytearray()
        l_fixHeader = self._build_fixed_header(0x0C, 0)
        self._send_transport(l_fixHeader, l_empty, l_empty)

    def pingresp(self):
        LOG.warn('Got ping ack packet')
        header = bytearray()
        header.append(0x0D << 4)
        header.extend(EncodeDecode._encodeLength(0))
        self.transport.write(header)

    def disconnect(self):
        LOG.info("Sending disconnect packet")
        header = bytearray()
        header.append(0x0E << 4)
        header.extend(EncodeDecode._encodeLength(0))
        self.transport.write(header)


MQTT_FACTORY_START = 0
MQTT_FACTORY_CONNECTING = 1
MQTT_FACTORY_CONNECTED = 2


class MQTTClient(MQTTProtocol):
    """
    """

    m_pingPeriod = 50

    def __init__(self, p_pyhouse_obj, p_broker, p_clientID=None,
                 userName=None, passWord=None,
                 keepalive=None,
                 willQos=0, willTopic=None, willMessage=None, willRetain=False
                 ):
        """ At this point all config has been read in and Set-up """
        l_comp_name = p_pyhouse_obj.Computer.Name
        try:
            l_house_name = p_pyhouse_obj.House.Name.lower() + '/'
        except AttributeError:
            l_house_name = 'NoName/'
        self.m_prefix = 'pyhouse/' + l_house_name
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        self.m_state = MQTT_FACTORY_START
        if p_clientID is not None:
            self.m_clientID = p_clientID
        else:
            self.m_clientID = l_comp_name + 'RasPi'
        if keepalive is not None:
            self.m_keepalive = keepalive
        else:
            self.m_keepalive = 60 * 1000
        self.m_willQos = willQos
        if willTopic != None:
            willTopic = self.m_prefix + 'lwt'
        self.m_willTopic = willTopic
        if willMessage != None:
            willMessage = self.m_clientID + 'Offline'
        self.m_willMessage = willMessage
        self.m_willRetain = willRetain
        self.m_UserName = userName
        self.m_Password = passWord
        p_pyhouse_obj.Computer.Mqtt.Prefix = self.m_prefix
        l_msg = 'MQTTClient(MQTTProtocol) \n\tPrefix: {}\n\tFrom: {}'.format(self.m_prefix, self.m_clientID)
        l_msg += '\n\tUser: {};  Pass: {}'.format(userName, passWord)
        LOG.info(l_msg)

    def connectionMade(self):
        """ Override

        PyHouse logic for TCP/TLS Connection being established.

        Now, send a MQTT connect packet to establish protocol connection.
        """
        LOG.info("Client TCP or TLS - KeepAlive: {} seconds".format(self.m_keepalive / 1000))
        self.m_state = MQTT_FACTORY_CONNECTING
        self.connect(self.m_clientID, self.m_keepalive,
                     self.m_willTopic, self.m_willMessage, self.m_willQos, self.m_willRetain, True,
                     self.m_UserName, self.m_Password
                     )
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def connectionLost(self, reason):
        """ Override

        PyHouse logic for what happened when the TCP/TLS connection is broken.
        """
        l_msg = reason.check(error.ConnectionClosed)
        LOG.info("Disconnected from MQTT Broker: {}  {}".format(reason, l_msg))
        self.m_state = MQTT_FACTORY_START

    def mqttConnected(self):
        """ Now that we have a net connection to the broker, Subscribe.
        """
        LOG.info("Subscribing to MQTT Feed")
        l_topic = self.m_pyhouse_obj.Computer.Mqtt.Prefix + '#'
        if self.m_state == MQTT_FACTORY_CONNECTING:
            self.subscribe(l_topic)
            self.m_state = MQTT_FACTORY_CONNECTED

    def connackReceived(self, p_status):
        """ Override
        """
        LOG.info("Received Connack from MQTT Broker: {}".format(p_status))
        if p_status == 0:
            self.mqttConnected()

    def pubackReceived(self, _messageId):
        """ Override
        """
        pass

    def subackReceived(self, _grantedQos, _messageId):
        """ Override
        Subscribe Ack message
        """
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.doPyHouseLogin(self, self.m_pyhouse_obj)

    def pingrespReceived(self):
        """ Override
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def publishReceived(self, p_topic, p_message, _qos=0, _dup=False, _retain=False, _messageId=None):
        """ Override

        This is where we receive all the pyhouse messages from the broker.
        Call the dispatcher to send them on to the correct place.
        """
        self.m_broker._ClientAPI.MqttDispatch(p_topic, p_message)

###########################################


class PyHouseMqttFactory(ReconnectingClientFactory):
    """This factory holds the state for this broker (there may be more than one).
    """

    def __init__(self, p_pyhouse_obj, p_client_id, p_broker, p_username, p_password):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_client_id: is the ID of this computer that will be supplied to the broker
        @param p_broker: is the PyHouse object for this broker
        """
        LOG.info('Mqtt Factory Initialized.  Broker: {};  Client: {}'.format(p_broker.Name, p_client_id))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        self.m_clientID = p_client_id
        self.m_username = p_username
        self.m_password = p_password
        p_broker._ProtocolAPI = self

    def startedConnecting(self, p_connector):
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        l_client = MQTTClient(self.m_pyhouse_obj, self.m_broker, self.m_clientID, self.m_username, self.m_password)
        self.m_broker._ProtocolAPI = l_client
        LOG.info("Mqtt buildProtocol - broker address: {}".format(p_addr))
        self.resetDelay()
        return l_client

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed. {} {}\n\tReason:{}'.format(self.m_broker.BrokerAddress, self.m_broker.BrokerPort, p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ This is required. """
        LOG.error('ConnectionLost.\n\tReason: {}'.format(p_reason))

    def makeConnection(self, p_transport):
        """ This is required. """
        LOG.warn('makeConnection - Transport: {}'.format(p_transport))

#  ## END DBK
