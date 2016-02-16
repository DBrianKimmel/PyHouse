"""
-*- test-case-name: PyHouse.Modules.Computer.Mqtt.test.test_computer -*-

@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:   Connect this computer node to the household Mqtt Broker.

"""

#  Import system type stuff
import copy
import datetime
from collections import namedtuple
from twisted.internet import defer, protocol, ssl
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.internet.ssl import Certificate

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeData, MqttInformation, MqttJson
from Modules.Computer.Mqtt.mqtt_protocol import PyHouseMqttFactory
from Modules.Computer.Mqtt.mqtt_xml import Xml as mqttXML
from Modules.Utilities import json_tools, xml_tools
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Mqtt_Client    ')

PEM_FILE = '/etc/pyhouse/ca_certs/rootCA.pem'


class Struct:
    def __init__(self, **args):
        self.__dict__.update(args)


class Util(object):
    """
    """

    @staticmethod
    def _dict2Obj(p_dict):
        """Convert a dict to an Object.
        """
        l_obj = namedtuple('MyObj', p_dict)
        return l_obj

    @staticmethod
    def _json2dict(p_json):
        """Convert JSON to Obj.
        """
        l_ret = json_tools.decode_json_unicode(p_json)
        #  print((PrettyFormatAny.form(l_ret, 'mqtt_client dict ')))
        return l_ret

    def client_to_one_broker(self, p_broker):
        l_host = p_broker.BrokerAddress
        l_port = p_broker.BrokerPort
        l_username = p_broker.UserName
        l_password = p_broker.Password
        p_broker._ClientAPI = self
        l_options = ssl.optionsForClientTLS(hostname = l_host.decode('utf-8'))
        print(PrettyFormatAny.form(l_options, 'TLS Options'))

    def connect_to_one_broker_TCP(self, p_pyhouse_obj, p_broker):
        l_clientID = 'PyH-' + p_pyhouse_obj.Computer.Name
        l_host = p_broker.BrokerAddress
        l_port = p_broker.BrokerPort
        l_username = None  #  p_broker.UserName
        l_password = None  #  p_broker.Password
        p_broker._ClientAPI = self
        LOG.info('Connecting via TCP...')
        if l_host == None or l_port == None:
            LOG.error('Bad Mqtt broker Address: {}'.format(l_host))
            p_broker._ProtocolAPI = None
        else:
            l_factory = PyHouseMqttFactory(
                        p_pyhouse_obj, l_clientID, p_broker, l_username, l_password)
            #  l_context_factory = ssl.CertificateOptions()
            _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
            LOG.info('TCP Connected to broker: {}; Host:{}'.format(p_broker.Name, l_host))
        pass

    @defer.inlineCallbacks
    def connect_to_one_broker_TLS(self, p_pyhouse_obj, p_broker):
        l_host = p_broker.BrokerAddress
        l_port = p_broker.BrokerPort
        l_username = p_broker.UserName
        l_password = p_broker.Password
        l_clientID = 'PyH-' + p_pyhouse_obj.Computer.Name
        LOG.info('Connecting via TLS...')
        #  l_factory = protocol.Factory.forProtocol(echoclient.EchoClient)
        l_factory = PyHouseMqttFactory(p_pyhouse_obj, l_clientID, p_broker, l_username, l_password)
        l_certData = PEM_FILE.getContent()
        l_authority = ssl.Certificate.loadPEM(l_certData)
        l_options = ssl.optionsForClientTLS(l_host.decode('utf-8'), l_authority)
        l_endpoint = SSL4ClientEndpoint(p_pyhouse_obj.Twisted.Reactor, l_host, l_port, l_options)
        l_client = yield l_endpoint.connect(l_factory)
        l_done = defer.Deferred()
        l_client.connectionLost = lambda reason: l_done.callback(None)
        yield l_done

    def connect_to_all_brokers(self, p_pyhouse_obj):
        """
        This will create a connection for each active broker in the config file.
        These connections will automatically reconnect if the connection is broken (broker reboots e.g.)
        """
        l_count = 0
        l_clientID = 'PyH-' + p_pyhouse_obj.Computer.Name
        for l_broker in p_pyhouse_obj.Computer.Mqtt.Brokers.itervalues():
            if not l_broker.Active:
                continue
            if l_broker.BrokerPort < 2000:
                self.connect_to_one_broker_TCP(p_pyhouse_obj, l_broker)
            else:
                self.connect_to_one_broker_TLS(p_pyhouse_obj, l_broker)
            l_count += 1
        LOG.info('TCP Connected to {} Broker(s).'.format(l_count))
        return l_count

    def XXXclient_TCP_connect_all_brokers(self, p_pyhouse_obj):
        l_count = 0
        l_clientID = 'PyH-' + p_pyhouse_obj.Computer.Name
        for l_broker in p_pyhouse_obj.Computer.Mqtt.Brokers.itervalues():
            if not l_broker.Active:
                continue
            l_host = l_broker.BrokerAddress
            l_port = l_broker.BrokerPort
            l_username = l_broker.UserName
            l_password = l_broker.Password
            l_broker._ClientAPI = self
            if l_host == None or l_port == None:
                LOG.error('Bad Mqtt broker Address: {}'.format(l_host))
                l_broker._ProtocolAPI = None
            else:
                l_factory = PyHouseMqttFactory(
                            p_pyhouse_obj, l_clientID, l_broker, l_username, l_password)
                l_context_factory = ssl.CertificateOptions()
                _l_connector = p_pyhouse_obj.Twisted.Reactor.connectSSL(
                            l_host, l_port, l_factory, l_context_factory)
                LOG.info('TCP Connected to broker: {}; Host:{}'.format(l_broker.Name, l_host))
                l_count += 1
                self.client_to_one_broker(l_broker)
        LOG.info('TCP Connected to {} Broker(s).'.format(l_count))
        return l_count

    @staticmethod
    def _make_topic(p_pyhouse_obj, p_topic):
        l_topic = p_pyhouse_obj.Computer.Mqtt.Prefix + p_topic
        return l_topic

    @staticmethod
    def _make_message(p_pyhouse_obj, p_message = None):
        """
        @param p_pyhouse_obj: is the entire PyHouse Data tree.
        @param message_json: is message that is already json encoded\
        @param message_obj: is additional object that will be added into the meddage as Json.
        """
        l_message = MqttJson()
        l_message.Sender = p_pyhouse_obj.Computer.Name
        l_message.DateTime = datetime.datetime.now()
        if p_message == None:
            pass
        elif isinstance(p_message, object):
            xml_tools.stuff_new_attrs(l_message, p_message)
        else:
            xml_tools.stuff_new_attrs(l_message, p_message)
        #  print(PrettyFormatAny.form(l_message, 'Mqtt Client - Message'))
        l_json = json_tools.encode_json(l_message)
        return l_json


class API(Util):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI = self
        p_pyhouse_obj.Computer.Mqtt = MqttInformation()
        p_pyhouse_obj.Computer.Mqtt.Prefix = 'ReSeT'
        p_pyhouse_obj.Computer.Mqtt.Brokers = {}
        LOG.info("Initialized.")

    def Start(self):
        self.m_pyhouse_obj.Computer.Mqtt = self.LoadXml(self.m_pyhouse_obj)
        if self.m_pyhouse_obj.Computer.Mqtt.Brokers != {}:
            LOG.info('Connecting to all MQTT Brokers.')
            l_count = self.connect_to_all_brokers(self.m_pyhouse_obj)
            LOG.info("Mqtt {} broker(s) Started.".format(l_count))
        else:
            LOG.info('No Mqtt brokers are configured.')

    def Stop(self):
        self.MqttPublish('computer/shutdown', '')

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        l_mqtt = MqttInformation()
        l_mqtt.Prefix = p_pyhouse_obj.Computer.Name
        l_mqtt.Brokers = mqttXML.read_mqtt_xml(p_pyhouse_obj)
        LOG.info("Loaded {} Brokers".format(len(l_mqtt.Brokers)))
        return l_mqtt

    def SaveXml(self, p_xml):
        l_xml = mqttXML().write_mqtt_xml(self.m_pyhouse_obj.Computer.Mqtt.Brokers)
        p_xml.append(l_xml)
        LOG.info("Saved Mqtt XML.")
        return p_xml

#  ## The following are public commands that may be called from everywhere

    def MqttPublish(self, p_topic, p_message):
        """Send a topic, message to the broker for it to distribute to the subscription list

        # self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("schedule/execute", l_schedule)
        @param p_topic: is the partial topic, the prefix will be prepended.
        @param message_json : is the JSON message we want to send
        @param message_obj: is an additional object that we will convert to JSON and merge it into the message.
        """
        l_topic = Util._make_topic(self.m_pyhouse_obj, p_topic)
        l_message = Util._make_message(self.m_pyhouse_obj, p_message)
        for l_broker in self.m_pyhouse_obj.Computer.Mqtt.Brokers.itervalues():
            if not l_broker.Active:
                continue
            try:
                l_broker._ProtocolAPI.publish(l_topic, l_message)
                LOG.info('Mqtt publishing:\n\tBroker: {}\t\tTopic:{}'.format(l_broker.Name, l_topic))
            except AttributeError as e_err:
                LOG.error("Mqtt Unpublished.\n\tERROR:{}\n\tTopic:{}\n\tMessage:{}".format(e_err, l_topic, l_message))

    def MqttDispatch(self, p_topic, p_message):
        """Dispatch a received MQTT message according to the topic.
        """
        l_topic = p_topic.split('/')[2:]  #  Drop the pyhouse/housename/ as that is all we subscribed to.
        l_message = json_tools.decode_json_unicode(p_message)
        l_logmsg = 'Dispatch\n\tTopic: {}'.format(l_topic)
        try:
            l_logmsg += '\n\tSender: {}'.format(l_message['Sender'])
        except AttributeError:
            pass
        #
        if l_topic[0] == 'computer':
            l_logmsg += 'Computer:\n\tName: {}'.format(l_message['Name'])
        elif l_topic[0] == 'lighting':
            l_logmsg += 'Lighting:\n\tName: {}'.format(l_message['Name'])
            l_logmsg += '\n\tRoom: {}'.format(l_message['RoomName'])
            try:
                l_logmsg += '\n\tLevel: {}'.format(l_message['CurLevel'])
            except:
                pass
        elif l_topic[0] == 'schedule' and l_topic[1] == 'execute':
            l_logmsg += 'Schedule:\n\tType: {}'.format(l_message['ScheduleType'])
            l_logmsg += '\n\tRoom: {}'.format(l_message['RoomName'])
            l_logmsg += '\n\tLight: {}'.format(l_message['LightName'])
            l_logmsg += '\n\tLevel: {}'.format(l_message['Level'])
        elif l_topic[0] == 'hvac':
            l_logmsg += 'Thermostat:\n\tName: {}'.format(l_message['Name'])
            l_logmsg += '\n\tRoom: {}'.format(l_message['RoomName'])
            l_logmsg += '\n\tTemp: {}'.format(l_message['CurrentTemperature'])
        elif l_topic[0] == 'weather':
            l_logmsg += 'Weather:\n\tName: {}'.format(l_message['location'])
            l_logmsg += '\n\tTemp: {}'.format(l_message['tempc'])
        else:
            l_logmsg += 'OTHER: Unknown'
            l_logmsg += '\n\tMessage: {}'.format(PrettyFormatAny.form(l_message, 'Message', 80))
        LOG.info(l_logmsg)

    def doPyHouseLogin(self, p_client, p_pyhouse_obj):
        """Login to PyHouse via MQTT
        """
        self.m_client = p_client
        try:
            l_node = copy.deepcopy(p_pyhouse_obj.Computer.Nodes[0])
        except KeyError:
            l_node = NodeData()
        l_node.NodeInterfaces = {}
        self.MqttPublish('computer/startup', l_node)

#  ## END DBK
