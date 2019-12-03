"""
@name:      Modules/Computer/Nodes/nodes.py
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

__updated__ = '2019-12-02'
__version_info__ = (18, 10, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Nodes.node_local import Api as localApi
from Modules.Computer.Nodes.node_sync import Api as syncApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import extract_tools

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Nodes          ')


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p-logmsg: is the partially decoded Mqtt message json
        @param p_msg.Topic: is a list of topic part strings ( pyhouse, housename have been dropped
        @param p_message: is the payload that is JSON
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tNodes:\n'
        l_topic = l_topic[0].lower()
        if l_topic == 'browser':
            p_msg.LogMessage += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))
        #  computer/ip
        elif l_topic == 'ip':
            l_ip = extract_tools.get_mqtt_field(p_msg.Payload, 'ExternalIPv4Address')
            p_msg.LogMessage += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif l_topic == 'startup':
            self._extract_node(p_msg.Payload)
            p_msg.LogMessage += '\tStartup {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                p_msg.LogMessage += '\tMy own startup of PyHouse\n'
            else:
                p_msg.LogMessage += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif l_topic == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            p_msg.LogMessage += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg'))
        #
        elif l_topic == 'sync':
            p_msg.LogMessage += syncApi(self.m_pyhouse_obj).DecodeMqttMessage(p_msg.Topic[1:], p_msg.Payload)
        else:
            p_msg.LogMessage += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg'))
            LOG.warning('Unknown Node sub-topic: {}\n\tMsg: {}'.format(l_topic, p_msg.Payload))


class Yaml:

    def load_yaml_config(self, p_pyhouse_obj):
        """
        """
        pass

    def save_yaml_config(self, p_pyhouse_obj):
        """
        """
        pass


class Api():

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_local = localApi(p_pyhouse_obj)
        self.m_sync = syncApi(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized - Version:{}'.format(__version__))

    def LoadConfig(self):
        """ Load the Node xml info.
        """
        Yaml().load_yaml_config(self.m_pyhouse_obj)
        # p_pyhouse_obj.Computer.Nodes = l_nodes
        LOG.info('Loaded Config - Version:{}'.format(__version__))
        return

    def Start(self):
        self.m_local.Start()
        self.m_sync.Start()
        LOG.info('Started - Version:{}'.format(__version__))

    def SaveConfig(self):
        # l_xml, l_count = nodesXml.write_nodes_xml(self.m_pyhouse_obj)
        # p_xml.append(l_xml)
        Yaml().save_yaml_config(self.m_pyhouse_obj)
        LOG.info("Saved Config")
        return

    def Stop(self):
        self.m_local.Stop()
        self.m_sync.Stop()

#  ## END DBK
