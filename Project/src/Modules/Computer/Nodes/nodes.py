"""
@name:      PyHouse/Project/src/Modules/Computer/Nodes/nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 6, 2014
@summary:   This module does everything for nodes.

Nodes are read in from the config Xml file.

Then node local is run to update the local node

Finally, the nodes are synced between each other.

"""

__updated__ = '2019-06-28'
__version_info__ = (18, 10, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Nodes.node_local import API as localAPI
from Modules.Computer.Nodes.node_sync import API as syncAPI
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import extract_tools

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Nodes          ')


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message, p_logmsg):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p-logmsg: is the partially decoded Mqtt message json
        @param p_topic: is a list of topic part strings ( pyhouse, housename have been dropped
        @param p_message: is the payload that is JSON
        """
        p_logmsg += '\tNodes:\n'
        l_topic = p_topic[0].lower()
        if l_topic == 'browser':
            p_logmsg += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #  computer/ip
        elif l_topic == 'ip':
            l_ip = extract_tools.get_mqtt_field(p_message, 'ExternalIPv4Address')
            p_logmsg += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif l_topic == 'startup':
            self._extract_node(p_message)
            p_logmsg += '\tStartup {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                p_logmsg += '\tMy own startup of PyHouse\n'
            else:
                p_logmsg += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif l_topic == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            p_logmsg += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #
        elif l_topic == 'sync':
            p_logmsg += syncAPI(self.m_pyhouse_obj).DecodeMqttMessage(p_topic[1:], p_message)
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
            LOG.warn('Unknown Node(s0 Topic: {}'.format(l_topic))
        return p_logmsg


class Yaml:

    def LoadYamlConfig(self, p_pyhouse_obj):
        """
        """
        pass

    def SaveYamlConfig(self, p_pyhouse_obj):
        """
        """
        pass


class API():

    def __init__(self, p_pyhouse_obj):
        self.m_local = localAPI(p_pyhouse_obj)
        self.m_sync = syncAPI(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized - Version:{}'.format(__version__))

    def LoadConfig(self, p_pyhouse_obj):
        """ Load the Node xml info.
        """
        # self.m_pyhouse_obj = p_pyhouse_obj
        # l_nodes = nodesXml.read_all_nodes_xml(p_pyhouse_obj)
        # p_pyhouse_obj.Computer.Nodes = l_nodes
        Yaml().LoadYamlConfig(p_pyhouse_obj)
        LOG.info('Loaded Config - Version:{}'.format(__version__))
        return

    def Start(self):
        self.m_local.Start()
        self.m_sync.Start()
        LOG.info('Started - Version:{}'.format(__version__))

    def SaveConfig(self, p_pyhouse_obj):
        # l_xml, l_count = nodesXml.write_nodes_xml(self.m_pyhouse_obj)
        # p_xml.append(l_xml)
        Yaml().SaveYamlConfig(p_pyhouse_obj)
        LOG.info("Saved Config")
        return

    def Stop(self):
        self.m_local.Stop()
        self.m_sync.Stop()

#  ## END DBK
