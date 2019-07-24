"""
@name:      PyHouse/Projet/src/Modules/Computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
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
            Bridges
            Communication
            Internet
            Mqtt
            Nodes
            Weather
            Web

"""

__updated__ = '2019-07-10'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from datetime import datetime
import platform

#  Import PyHouse files
from Modules.Core.data_objects import ComputerAPIs, ComputerInformation
from Modules.Core.Utilities import extract_tools, uuid_tools, config_tools
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.Bridges.bridges import API as bridgesAPI
from Modules.Computer.Communication.communication import API as communicationAPI
from Modules.Computer.Internet.internet import API as internetAPI
from Modules.Computer.Nodes.nodes import API as nodesAPI, MqttActions as nodesMqtt
from Modules.Computer.Weather.weather import API as weatherAPI
from Modules.Computer.Web.web import API as webAPI
from Modules.Computer.Web.websocket_server import API as websocketAPI

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Computer       ')

COMPUTER_DIVISION = 'ComputerDivision'
UUID_FILE_NAME = 'Computer.uuid'
CONFIG_FILE_NAME = 'computer.yaml'

# MODULES = ['Communication', 'Email', 'Internet' , 'Mqtt', 'Node', 'Weather', 'Web']


class UuidFile:
    """
    """


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p-logmsg: is the partially decoded Mqtt message json
        @param p_topic: is a list of topic part strings ( pyhouse, housename have been dropped
        @param p_message: is the payload that is JSON
        """
        l_logmsg = '\tComputer:\n'
        if p_topic[0] == 'browser':
            l_logmsg += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        elif p_topic[0] == 'node' or p_topic[0] == 'nodes':
            l_logmsg += nodesMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        #  computer/ip
        elif p_topic[1] == 'ip':
            l_ip = extract_tools.get_mqtt_field(p_message, 'ExternalIPv4Address')
            l_logmsg += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif p_topic[1] == 'startup':
            self._extract_node(p_message)
            l_logmsg += '\tStartup {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                l_logmsg += '\tMy own startup of PyHouse\n'
            else:
                l_logmsg += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif p_topic[1] == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            l_logmsg += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #  computer/***
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        return l_logmsg


class Xml:

    def _read_computer_specs(self, p_obj, p_xml):
        """ Read the extra computer info
        """
        p_obj.Priority = PutGetXML.get_int_from_xml(p_xml, "Priority")
        return p_obj

    def _write_computer_specs(self, p_xml, p_obj):
        """
        """
        PutGetXML().put_int_element(p_xml, 'Priority', p_obj.Priority)
        return p_xml

    def read_computer_config(self, p_pyhouse_obj):
        l_section = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision')
        l_obj = p_pyhouse_obj.Computer
        XmlConfigTools.read_base_UUID_object_xml(l_obj, l_section)
        self._read_computer_specs(l_obj, l_section)
        return l_obj

    def write_computer_xml(self, p_pyhouse_obj):
        l_obj = p_pyhouse_obj.Computer
        l_xml = XmlConfigTools.write_base_UUID_object_xml(COMPUTER_DIVISION, l_obj)
        _l_extra_xml = self._write_computer_specs(l_xml, l_obj)
        p_pyhouse_obj._Config.XmlTree.append(l_xml)
        return l_xml


class Yaml:
    """
    """

    def _update_computer_from_yaml(self, p_pyhouse_obj, p_node_yaml):
        """ Copies the data from the yaml config file to the Rooms part of the PyHouse obj.
        Check for duplicate room names!
        @param p_pyhouse_obj: is the entire house object
        @param p_node_yaml: is ConfigYamlNodeInformation filled with room data.
            {'Rooms': [{'Name': 'Outside', 'Active': 'True', 'Comment': 'Things outsi...
        """
        l_rooms = {}
        try:
            l_yaml = p_node_yaml['Rooms']  # Get the rooms info list.
        except:
            LOG.error('The "Rooms" tag is missing in the "rooms.yaml" file!')
            return None
        for l_ix, l_room_yaml in enumerate(l_yaml):
            l_room_obj = self._extract_room_config(l_room_yaml)
            l_rooms.update({l_ix:l_room_obj})
        p_pyhouse_obj.House.Rooms = l_rooms
        return l_rooms  # For testing.

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the computer.yaml file.
        """
        l_yaml = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_obj = p_pyhouse_obj.Computer
        LOG.debug('Computer.Yaml - {}'.format(l_yaml.Yaml))
        return l_obj  # for testing purposes


class Utility:
    """
    There are currently (2019) 8 components - be sure all are in every method.
    """

    m_pyhouse_obj = None

    def _init_component_apis(self, p_pyhouse_obj, p_computer_api):
        """
        Initialize all the computer division APIs
        """
        p_pyhouse_obj._APIs.Computer = ComputerAPIs()
        p_pyhouse_obj._APIs.Computer.ComputerAPI = p_computer_api
        #
        p_pyhouse_obj._APIs.Computer.BridgesAPI = bridgesAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.CommunicationsAPI = communicationAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.InternetAPI = internetAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.NodesAPI = nodesAPI(p_pyhouse_obj)
        # p_pyhouse_obj._APIs.Computer.WeatherAPI = weatherAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.WebAPI = webAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.WebSocketAPI = websocketAPI(p_pyhouse_obj)
        # LOG.debug('{}'.format(PrettyFormatAny.form(p_pyhouse_obj._APIs.Computer, 'Computer Api\'s', 190)))

    def _load_component_config(self):
        self.m_pyhouse_obj._APIs.Computer.NodesAPI.LoadConfig()  # Nodes are sent in Mqtt open
        self.m_pyhouse_obj._APIs.Computer.BridgesAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.Computer.CommunicationsAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.Computer.InternetAPI.LoadConfig
        # self.m_pyhouse_obj._APIs.Computer.WeatherAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.Computer.WebAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.Computer.WebSocketAPI.LoadConfig()

    def _start_component_apis(self, p_pyhouse_obj):
        self.m_pyhouse_obj._APIs.Computer.BridgesAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.CommunicationsAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.InternetAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.NodesAPI.Start()
        # self.m_pyhouse_obj._APIs.Computer.WeatherAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.WebAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.WebSocketAPI.Start()

    def _stop_component_apis(self, p_pyhouse_obj):
        self.m_pyhouse_obj._APIs.Computer.BridgesAPI.Stop()
        self.m_pyhouse_obj._APIs.Computer.CommunicationsAPI.Stop()
        self.m_pyhouse_obj._APIs.Computer.InternetAPI.Stop()
        self.m_pyhouse_obj._APIs.Computer.NodesAPI.Stop()
        # self.m_pyhouse_obj._APIs.Computer.WeatherAPI.Stop()
        self.m_pyhouse_obj._APIs.Computer.WebAPI.Stop()
        self.m_pyhouse_obj._APIs.Computer.WebSocketAPI.Stop()

    def _save_component_apis(self, p_pyhouse_obj, p_xml):
        """ Save the XML for each of the components of the Computer
        """
        self.m_pyhouse_obj._APIs.Computer.BridgesAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.CommunicationsAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.InternetAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.NodesAPI.SaveConfig()
        # self.m_pyhouse_obj._APIs.Computer.WeatherAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.WebAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.WebSocketAPI.SaveConfig()
        return p_xml


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        """ Initialize the computer section of PyHouse.
        """
        LOG.info("Initializing - Version:{}".format(__version__))
        # This overrides any xml saved so we can start Logging and MQTT messages early on.
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Name = platform.node()
        p_pyhouse_obj.Computer.Key = 0
        p_pyhouse_obj.Computer.Active = True
        p_pyhouse_obj.Computer.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, UUID_FILE_NAME)
        p_pyhouse_obj.Computer.Comment = ''
        p_pyhouse_obj.Computer.LastUpdate = datetime.now()
        #
        self._init_component_apis(p_pyhouse_obj, self)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        # Xml().read_computer_config(p_pyhouse_obj)
        Yaml().LoadYamlConfig(self.m_pyhouse_obj)
        self._load_component_config()
        LOG.info('Loaded Config.')

    def Start(self):
        """
        Start processing
        """
        LOG.info('Starting')
        self._start_component_apis(self.m_pyhouse_obj)
        LOG.info('Started.')

    def SaveConfig(self, p_pyhouse_obj):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = Xml().write_computer_xml(self.m_pyhouse_obj)
        self._save_component_apis(self.m_pyhouse_obj, l_xml)
        p_pyhouse_obj._Config.XmlTree.append(l_xml)
        LOG.info("Saved Computer XML Config.")
        return

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        self._stop_component_apis(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def DecodeMqtt(self, p_topic, p_message):
        """ Decode messages sent to the computer module.
        """
        # LOG.debug('\n==Topic: {}\n==Message: {}\n==LogMsg: {}'.format(p_topic, p_message, p_logmsg))
        l_logmsg = MqttActions(self.m_pyhouse_obj).decode(p_topic, p_message)
        return l_logmsg

# ## END DBK
