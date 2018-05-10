"""
-*- test-case-name: PyHouse.src.Modules.Computer.test.test_computer -*-

@name:      PyHouse/src/Modules/Computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "House").

This takes care of starting all the computer modules (In Order).
    Logging
    Mqtt Broker(s)
    Bridges
    Nodes
    Internet Connection(s)
    Web Server(s)

PyHouse.Computer.
            Communication
            Internet
            Mqtt
            Nodes
            Weather
            Web

"""

__updated__ = '2018-03-26'

#  Import system type stuff
import platform

#  Import PyHouse files
from Modules.Core.data_objects import ComputerAPIs, ComputerInformation
from Modules.Computer.Bridges.bridges import API as bridgesAPI
from Modules.Computer.Communication.communication import API as communicationAPI
from Modules.Computer.Internet.internet import API as internetAPI
from Modules.Computer.Mqtt.mqtt import API as mqttAPI
from Modules.Computer.Nodes.nodes import API as nodesAPI
from Modules.Computer.Nodes.node_sync import API as syncAPI
from Modules.Computer.weather import API as weatherAPI
from Modules.Computer.Web.web import API as webAPI
from Modules.Computer.Web.websocket_server import API as websocketAPI
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Core.Utilities import uuid_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Computer       ')

COMPUTER_DIVISION = 'ComputerDivision'
UUID_FILE_NAME = 'Computer.uuid'

# MODULES = ['Communication', 'Email', 'Internet' , 'Mqtt', 'Node', 'Weather', 'Web']


class UuidFile(object):
    """
    """


class MqttActions(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tComputer:\n'
        #  computer/browser/***
        if p_topic[1] == 'browser':
            _l_name = 'unknown'
            p_logmsg += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #  computer/ip
        elif p_topic[1] == 'ip':
            l_ip = self._get_field(p_message, 'ExternalIPv4Address')
            p_logmsg += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif p_topic[1] == 'startup':
            self._extract_node(p_message)
            p_logmsg += '\tStartup {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                p_logmsg += '\tMy own startup of PyHouse\n'
            else:
                p_logmsg += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif p_topic[1] == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            p_logmsg += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #  computer/node/???
        elif p_topic[1] == 'node':
            p_logmsg += syncAPI(self.m_pyhouse_obj).DecodeMqttMessage(p_topic, p_message)
        #  computer/***
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        return p_logmsg


class Xml(object):

    @staticmethod
    def create_computer_xml(p_pyhouse_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml(COMPUTER_DIVISION, p_pyhouse_obj.Computer)
        return l_xml

    @staticmethod
    def read_computer_xml(p_pyhouse_obj):
        l_xml = XmlConfigTools.read_base_UUID_object_xml(COMPUTER_DIVISION, p_pyhouse_obj.Computer)
        return l_xml

    @staticmethod
    def write_computer_xml(p_pyhouse_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml(COMPUTER_DIVISION, p_pyhouse_obj.Computer)
        return l_xml


class Utility(object):

    m_pyhouse_obj = None

    @staticmethod
    def _init_component_apis(p_pyhouse_obj, p_api):
        """
        Initialize all the computer division APIs
        """
        p_pyhouse_obj.APIs.Computer = ComputerAPIs()
        p_pyhouse_obj.APIs.Computer.ComputerAPI = p_api
        p_pyhouse_obj.APIs.Computer.BridgesAPI = bridgesAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI = communicationAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.InternetAPI = internetAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.NodesAPI = nodesAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WeatherAPI = weatherAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WebAPI = webAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WebSocketAPI = websocketAPI(p_pyhouse_obj)

    @staticmethod
    def _load_component_xml(p_pyhouse_obj):
        p_pyhouse_obj.APIs.Computer.MqttAPI.LoadXml(p_pyhouse_obj)  # Start this first so we can send messages/
        p_pyhouse_obj.APIs.Computer.NodesAPI.LoadXml(p_pyhouse_obj)  # Nodes are sent in Mqtt open
        #
        p_pyhouse_obj.APIs.Computer.BridgesAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.InternetAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WeatherAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WebAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.WebSocketAPI.LoadXml(p_pyhouse_obj)

    @staticmethod
    def _start_component_apis(p_pyhouse_obj):
        p_pyhouse_obj.APIs.Computer.MqttAPI.Start()  # Start this first so we can send messages/
        p_pyhouse_obj.APIs.Computer.BridgesAPI.Start()
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.Start()
        p_pyhouse_obj.APIs.Computer.InternetAPI.Start()
        p_pyhouse_obj.APIs.Computer.NodesAPI.Start()
        p_pyhouse_obj.APIs.Computer.WeatherAPI.Start()
        p_pyhouse_obj.APIs.Computer.WebAPI.Start()
        p_pyhouse_obj.APIs.Computer.WebSocketAPI.Start()

    @staticmethod
    def _stop_component_apis(p_pyhouse_obj):
        p_pyhouse_obj.APIs.Computer.BridgesAPI.Stop()
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.Stop()
        p_pyhouse_obj.APIs.Computer.InternetAPI.Stop()
        p_pyhouse_obj.APIs.Computer.MqttAPI.Stop()
        p_pyhouse_obj.APIs.Computer.NodesAPI.Stop()
        p_pyhouse_obj.APIs.Computer.WeatherAPI.Stop()
        p_pyhouse_obj.APIs.Computer.WebAPI.Stop()
        p_pyhouse_obj.APIs.Computer.WebSocketAPI.Stop()

    @staticmethod
    def _save_component_apis(p_pyhouse_obj, p_xml):
        """ Save the XML for each of the components of the Computer
        """
        p_pyhouse_obj.APIs.Computer.BridgesAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.CommunicationsAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.InternetAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.MqttAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.NodesAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.WeatherAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.WebAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.Computer.WebSocketAPI.SaveXml(p_xml)
        return p_xml


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        """ Initialize the computer section of PyHouse.
        """
        LOG.info('Initializing')
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Name = platform.node()
        p_pyhouse_obj.Key = 0
        p_pyhouse_obj.Active = True
        p_pyhouse_obj.Computer.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, UUID_FILE_NAME)
        Utility._init_component_apis(p_pyhouse_obj, self)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized.')

    def LoadXml(self, p_pyhouse_obj):
        """
        """
        # LOG.info('Loading XML')
        Utility._load_component_xml(p_pyhouse_obj)
        LOG.info('Loaded XML.')

    def Start(self):
        """
        Start processing
        """
        LOG.info('Starting')
        Utility._start_component_apis(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = Xml.write_computer_xml(self.m_pyhouse_obj)
        Utility._save_component_apis(self.m_pyhouse_obj, l_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Computer XML.")
        return p_xml

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        Utility._stop_component_apis(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def DecodeMqtt(self, p_logmsg, p_topic, p_message):
        """ Decode messages sent to the computer module.
        """
        MqttActions(self.m_pyhouse_obj).decode(p_logmsg, p_topic, p_message)

# ## END DBK
