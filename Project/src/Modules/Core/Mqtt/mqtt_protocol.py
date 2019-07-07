"""
@name:      PyHouse/src/Modules/Computer/Mqtt/protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 28, 2015
@Summary:   This creates the Twisted (Async) version of MQTT client.

Warning.  There are two things called connect in this module.
The first is a TCP connection to the Mqtt broker.
The second is a MQTT connection to the broker that uses the first connection as a transport.

"""

__updated__ = '2019-07-06'
__version_info__ = (18, 9, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import random
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Core.Mqtt.mqtt_util import EncodeDecode
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import FormatBytes

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Mqtt_Protocol  ')
SUBSCRIBE = 'pyhouse/#'


class Packets():
    """ Routines to create and decode Mqtt Message Packets.
    """

    def _build_fixed_header(self, p_packet_type, p_remaining_length, dup=0, qosLevel=0, retain=0):
        l_header = bytearray()
        l_header.append((p_packet_type & 0x0f) << 4 | (dup & 0x01) << 3 | (qosLevel & 0x03) << 1 | (retain & 0x01))
        l_header.extend(EncodeDecode._encodeLength(p_remaining_length))
        return l_header


class MQTTProtocol(Protocol, Packets):
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
    m_broker = {}

    def dataReceived(self, p_data):
        """ A standard callback when we get data from the broker.

        It might be a portion of a message up to several messages.
        It is up to us to break it down to individual messages and then send the message on to be used.
        """
        self._accumulatePacket(p_data)

    def _accumulatePacket(self, p_data):
        """ Get 1 packet.
        Packet format:
            Fixed Header(2 - 5 bytes)
            Variable Header (0 - 268,435,455 bytes)

        Fixed Header:
           Various Flags: 1 Byte
           RemainingLength = 1-4 Bytes

        Variable Header:
            :
        """
        self.m_buffer.extend(p_data)
        l_RemainingLength = None
        while len(self.m_buffer):
            if l_RemainingLength is None:
                #  Start on a new packet
                if len(self.m_buffer) < 2:
                    break  #  Haven't got enough data to start a new packet, wait for some more
                l_rl_len = 1  # Initial length of the RemainingLength field.
                #  get the variable length RemainingLength field
                while l_rl_len < len(self.m_buffer):  # Find the bytes in the RemainingLength field.
                    if not self.m_buffer[l_rl_len] & 0x80:
                        break  # We have the full RemainingLength field
                    l_rl_len += 1  # Field is longer - get another byte
                # Get the variable part -  We still haven't got all of the remaining length field so quit and wait for another chunk
                if l_rl_len < len(self.m_buffer) and self.m_buffer[l_rl_len] & 0x80:  # Is there more to to come of the RemainingLength field?
                    LOG.debug('### Early return - Another chunk is needed {}'.format(FormatBytes(self.m_buffer)))
                    return
                l_RemainingLength = EncodeDecode._decodeLength(self.m_buffer[1:])
            l_FixedHeaderLength = l_rl_len + 1  # Length of the fixed Header portion of the packet
            l_PacketLength = l_FixedHeaderLength + +l_RemainingLength
            if len(self.m_buffer) >= l_PacketLength:
                l_one_message_packet = self.m_buffer[:l_PacketLength]
                self._processPacket(l_one_message_packet)

                self.m_buffer = self.m_buffer[l_PacketLength:]
                l_RemainingLength = None
            else:
                # LOG.debug('### exit without processing\n\t{}'.format(FormatBytes(self.m_buffer)))
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
        except Exception:
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
            l_packetHandler(packet, qos, dup, retain)  # this will dispatch to the appropriate routine for the packet type.
        else:
            LOG.error("Invalid packet handler for {}".format(packet_type_name))
            return

    #  These are the events - one for each packet type

    def _event_connect(self, packet, _qos, _dup, _retain):
        """This will decode a received 'connect' packet.
        """
        LOG.info('ProtocolEvent "Connect Packet" received.')
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
        byte 0 = Session present flag
        byte 1 = Return Code
                0 = Connection Accepted
                1 = Rejected - wrong protocol
                2 = Rejected - Client ID wrong
                3 = Rejected - Server unavailable
                4 = Rejected - Username/Password incorrect
                5 = Rejected - Not Authorized
        """
        l_rc = packet[1]
        if l_rc != 0:
            LOG.error('ProtocolEvent "Conack Packet" received:\n\tStatus: {}; {};\n\tAddr:{}'.format(packet[0], l_rc, self.m_broker.Host.Name))
        #  Return the status field
        self.connackReceived(l_rc)

    def _event_publish(self, packet, qos, dup, retain):
        """ Receive a "Published" message

        Here we get a published message from the broker.
        Extract the parts of the packet.
        @param packet: is a bytearray containing the variable header and payload combined.
        """
        #  Extract the topic portion of the packet.
        l_topic = EncodeDecode._decodeString(packet)
        packet = packet[len(l_topic) + 2:]
        #  Extract the message ID if appropriate
        messageId = None
        if qos > 0:
            messageId = EncodeDecode._decodeValue(packet[:2])
            packet = packet[2:]
            LOG.debug('Publish MsgID:{}'.format(messageId))
        #  Extract whatever remains as the message
        l_json = EncodeDecode._get_string(packet)
        # l_json = packet.decode('utf-8')
        l_message = json_tools.decode_json_unicode(l_json)
        # l_topic is a string
        # l_message is a string
        self.publishReceived(l_topic, l_message, qos, dup, retain, messageId)

    """{
    "Active": true,
    "Comment": "",
    "ConnectionAddr_IPv4": [],
    "ConnectionAddr_IPv6": [["::1"], ["2001:470:5:417::54", "fe80::12bf:48ff:feb6:eb6f%eth0"], ["2001:470:4:417::2", "fe80::c0a8:136%he-ipv6"],
        ["fe80::4541:2ad4:2335:4372%tun0"]],
    "ControllerCount": 0,
    "ControllerTypes": [],
    "DateTime": "2018-05-27 12:48:35.484189",
    "Key": 0,
    "LastUpdate": "2018-05-27 12:48:20.482007",
    "Name": "Alki",
    "NodeId": null,
    "NodeInterfaces": null,
    "NodeRole": 0,
    "Sender": "Alki",
    "UUID": "c8cbdbe0-14c5-11e7-b450-10bf48b6eb6f"
    }"""

    def _event_puback(self, packet, _qos, _dup, _retain):
        LOG.info('ProtocolEvent "PubAck Packet" received: {} {}\n\tAddr:{}'.format(len(packet), packet, self.m_broker.Host.Name))
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
        LOG.info('ProtocolEvent "Subscribe Packet" received: {} {}'.format(len(packet), packet))
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
        # LOG.info('Event SubAck received - MsgID:{}  Acks: {} {}\n\tAddr:{}'.format(messageId, len(packet), packet, self.m_broker.Host.Name))
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

    def _event_pingreq(self, _packet, _qos, _dup, _retain):
        # LOG.info('Event Pingreq received: {} {}'.format(len(packet), packet))
        self.pingreqReceived()

    def _event_pingresp(self, _packet, _qos, _dup, _retain):
        # LOG.debug('Event Pingresp received: {} {}'.format(len(packet), packet))
        self.pingrespReceived()

    def _event_disconnect(self, packet, _qos, _dup, _retain):
        LOG.info('Event Disconnect received: {} {}\n\tAddr:{}'.format(len(packet), packet, self.m_broker.Host.Name))
        self.disconnectReceived()

    #  these are to be overridden below

    def connectionMade(self):
        raise NotImplementedError  # Subclasses must implement this.

    def connectionLost(self, reason):
        raise NotImplementedError  # Subclasses must implement this.

    # These are packet types

    def connectReceived(self, clientID, keepalive, willTopic, willMessage, willQoS, willRetain, cleanStart, userName, password):
        raise NotImplementedError  # Subclasses must implement this.

    # def connackReceived(self, status):
    #    raise NotImplementedError  # Subclasses must implement this.

    # def publishReceived(self, _topic, _message, _qos=0, _dup=False, _retain=False, _messageId=None):
    #    raise NotImplementedError  # Subclasses must implement this.

    # def pubackReceived(self, _messageId):
    #    raise NotImplementedError  # Subclasses must implement this.

    def pubrecReceived(self, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def pubrelReceived(self, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def pubcompReceived(self, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def subscribeReceived(self, _topics, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def subackReceived(self, grantedQos, _messageId):
        raise NotImplementedError  # Subclasses must implement this.

    def unsubscribeReceived(self, _topics, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def unsubackReceived(self, _messageId):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    def pingreqReceived(self):
        raise NotImplementedError  # Subclasses must implement this.
        pass

    # def pingrespReceived(self):
    #    raise NotImplementedError  # Subclasses must implement this.

    def disconnectReceived(self):
        raise NotImplementedError  # Subclasses must implement this.
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

    def _build_connect(self, p_broker, p_mqtt):
        """
        """
        l_varHeader = bytearray()
        l_payload = bytearray()
        l_varHeader.extend(EncodeDecode._encodeString("MQTT"))
        l_varHeader.append(4)
        varLogin = 0
        if p_broker.UserName is not None:
            varLogin += 2
        if p_broker.Password is not None:
            varLogin += 1
        if p_broker.WillMessage is None or p_broker.WillMessage == '' or p_broker.WillTopic is None:
            #  Clean start, no will message
            l_varHeader.append(varLogin << 6 | 0 << 2 | 1 << 1)
        else:
            l_varHeader.append(varLogin << 6 | p_broker.WillRetain << 5 | p_broker.WillQoS << 3 | 1 << 2 | 1 << 1)
        l_varHeader.extend(EncodeDecode._encodeValue(int(p_broker.Keepalive / 1000)))
        l_payload.extend(EncodeDecode._encodeString(p_mqtt.ClientID))
        if (p_broker.WillMessage is not None or p_broker.WillMessage != '') and p_broker.WillTopic is not None:
            # LOG.debug('Adding last will testiment {}'.format(p_broker.WillMessage + p_broker.WillTopic))
            l_payload.extend(EncodeDecode._encodeString(p_broker.WillTopic))
            l_payload.extend(EncodeDecode._encodeString(p_broker.WillMessage))
        if p_broker.UserName is not None and len(p_broker.UserName) > 0:
            LOG.debug('Adding username "{}"'.format(p_broker.UserName))
            l_payload.extend(EncodeDecode._encodeString(p_broker.UserName))
        if p_broker.Password is not None and len(p_broker.Password) > 0:
            LOG.debug('Adding password "{}"'.format(p_broker.Password))
            l_payload.extend(EncodeDecode._encodeString(p_broker.Password))
        l_fixHeader = self._build_fixed_header(0x01, len(l_varHeader) + len(l_payload))
        return (l_fixHeader, l_varHeader, l_payload)

    def connect(self, p_broker, p_mqtt):
        """
        DBK - Modified this packet to add username and password flags and fields (2016-01-22)
        """
        l_fixHeader, l_varHeader, l_payload = self._build_connect(p_broker, p_mqtt)
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def connack(self, status):
        # LOG.warn('Sending connect ack packet')
        l_varHeader = bytearray()
        l_payload = bytearray()
        l_payload.append(status)
        l_fixHeader = self._build_fixed_header(0x02, len(l_varHeader) + len(l_payload))
        self._send_transport(l_fixHeader, l_varHeader, l_payload)

    def publish(self, p_topic, p_message, qosLevel=0, retain=False, dup=False, messageId=None):
        # LOG.info("Sending publish packet\n\tTopic: {};\n\tHost: {};".format(p_topic, self.m_broker.Host.Name))
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
        # LOG.warn('Sending puback packet')
        header = bytearray()
        varHeader = bytearray()
        header.append(0x04 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubrec(self, messageId):
        # LOG.info("Sending pubrec packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x05 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubrel(self, messageId):
        # LOG.info("Sending pubrel packet")
        header = bytearray()
        varHeader = bytearray()
        header.append(0x06 << 4)
        varHeader.extend(EncodeDecode._encodeValue(messageId))
        header.extend(EncodeDecode._encodeLength(len(varHeader)))
        self.transport.write(header)
        self.transport.write(varHeader)

    def pubcomp(self, messageId):
        # LOG.warn('Sending pubcomp packet')
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
        # LOG.info("Sending subscribe packet - Topic: {}\n\tAddr: {}".format(p_topic, self.m_broker.Host.Name))
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
        # LOG.info("Sending suback packet")
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
        # LOG.info("Sending unsubscribe packet")
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
        # LOG.info("Sending unsuback packet")
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
    m_prefix = ''
    m_mqtt = None
    m_broker = {}

    def __init__(self, p_pyhouse_obj, p_broker,
                 keepalive=None, willQos=0, willTopic=None, willMessage=None, willRetain=False
                 ):
        """ At this point all config has been read in and Set-up """
        _l_comp_name = p_pyhouse_obj.Computer.Name
        self.m_mqtt = p_pyhouse_obj.Core.Mqtt
        try:
            l_house_name = p_pyhouse_obj.House.Name.lower() + '/'
        except AttributeError:
            l_house_name = 'NoName/'
        self.m_prefix = 'pyhouse/' + l_house_name
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        self.m_state = MQTT_FACTORY_START
        if keepalive is not None:
            self.m_keepalive = keepalive
        else:
            self.m_keepalive = 60 * 1000
        self.m_willQos = willQos
        if willTopic is not None:
            willTopic = self.m_prefix + 'lwt'
        self.m_willTopic = willTopic
        self.m_willMessage = willMessage
        self.m_willRetain = willRetain
        self.m_UserName = p_broker.UserName
        self.m_Password = p_broker.Password
        p_pyhouse_obj.Core.Mqtt.Prefix = self.m_prefix
        l_msg = 'MQTTClient(MQTTProtocol)\n\tPrefix: {};\n\tFrom ClientID: {};'.format(self.m_prefix, self.m_pyhouse_obj.Core.Mqtt.ClientID)
        l_msg += "\n\tUser:'{}';\n\tPass:'{}';".format(p_broker.UserName, p_broker.Password)
        l_msg += '\n\tHost: {};'.format(self.m_broker.Host.Name)
        LOG.info(l_msg)

    def connectionMade(self):
        """ Override

        PyHouse logic for TCP/TLS Connection being established.

        Now, send a MQTT connect packet to establish protocol connection.
        """
        LOG.debug("Client TCP or TLS - KeepAlive: {} seconds\n\tAddr; {}".format(self.m_keepalive / 1000, self.m_broker.Host.Name))
        self.m_state = MQTT_FACTORY_CONNECTING
        self.connect(self.m_broker, self.m_pyhouse_obj.Core.Mqtt)
        self.m_pyhouse_obj._Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def connectionLost(self, reason):
        """ Override

        PyHouse logic for what happened when the TCP/TLS connection is broken.
        """
        l_msg = reason.check(error.ConnectionClosed)
        LOG.warn("Disconnected from MQTT Broker:\n\t{}\n\tReason:{}\n\tAddr:{}".format(reason, l_msg, self.m_broker.Host.Name))
        self.m_state = MQTT_FACTORY_START

    def mqttConnected(self):
        """ Now that we have a net connection to the broker, Subscribe.
        """
        l_topic = self.m_pyhouse_obj.Core.Mqtt.Prefix + '#'
        LOG.info("Subscribing to MQTT Feed: {}".format(l_topic))
        if self.m_state == MQTT_FACTORY_CONNECTING:
            self.subscribe(l_topic)
            self.m_state = MQTT_FACTORY_CONNECTED

    def connackReceived(self, p_status):
        """ Override
        """
        LOG.debug("Received Connack from MQTT Broker\n\tAddr:{}".format(self.m_broker.Host.Name))
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
        self.m_pyhouse_obj._APIs.Core.MqttAPI.doPyHouseLogin(self, self.m_pyhouse_obj)

    def pingrespReceived(self):
        """ Override
        """
        self.m_pyhouse_obj._Twisted.Reactor.callLater(self.m_pingPeriod, self.pingreq)

    def publishReceived(self, p_topic, p_message, _qos=0, _dup=False, _retain=False, _messageId=None):
        """ Override

        This is where we receive all the pyhouse messages from the broker.
        Call the dispatcher to send them on to the correct place.
        """
        # LOG.debug('Topic:{};  Msg:{}'.format(p_topic, p_message))
        self.m_broker._ClientAPI.MqttDispatch(p_topic, p_message)

###########################################


class PyHouseMqttFactory(ReconnectingClientFactory):
    """
    This factory holds the state for this broker (there may be more than one).
    """

    m_broker = {}

    def __init__(self, p_pyhouse_obj, p_broker):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_client_id: is the ID of this computer that will be supplied to the broker
        @param p_broker: is the PyHouse object for this broker:  mqtt_data.py - MqttBrokerInformation(BaseObject)
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_broker = p_broker
        l_addr = p_broker.Host.Name
        LOG.info('PyHouseMqttFactory Mqtt Initialized.\n\tBroker Name: {};\n\tClientId: {};\n\tHost: {};'.format(
                p_broker.Name, p_pyhouse_obj.Core.Mqtt.ClientID, l_addr))
        p_broker._ProtocolAPI = self

    def buildProtocol(self, _p_addr):
        """ Override.
        Create an instance of a subclass of Protocol.

        The returned instance will handle input on an incoming server connection,
         and an attribute "factory" pointing to the creating factory.

        Alternatively, None may be returned to immediately close the new connection.
        """
        l_client = MQTTClient(self.m_pyhouse_obj, self.m_broker)
        self.m_broker._ProtocolAPI = l_client
        self.resetDelay()
        LOG.debug('Building MQTT Protocol - Client:{}')
        return l_client

    def startedConnecting(self, p_connector):
        """ Override.
        Called when a connection has been started.
        """
        # LOG.info('Started to connect. {}'.format(p_connector))
        pass

    def clientConnectionFailed(self, p_connector, p_reason):
        """ Override.
        Called when a connection has failed to connect.
        """
        LOG.warn('Factory Connection failed to make.\n\tAddr: {};\n\tReason:{};'.format(self.m_broker.Host.Name, p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def clientConnectionLost(self, p_connector, p_reason):
        """ Override.
        Called when an established connection is lost.
        """
        LOG.warn('Made connection LOST.\n\tAddr: {};\n\tReason:{};'.format(self.m_broker.Host.Name, p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ Override.
            Required.
        """
        LOG.warn('Broker: {};  Port: {}\n\tReason:{}'.format(self.m_broker.Host.Name, self.m_broker.Host.Port, p_reason))

    def makeConnection(self, p_transport):
        """ This is required.
        """
        # LOG.warn('makeConnection - Transport: {}'.format(p_transport))
        pass

#  ## END DBK
