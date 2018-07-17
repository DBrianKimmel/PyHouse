"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created Feb 20, 2016
@Summary:

"""

__updated__ = '2018-07-16'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import NodeData, PyHouseData
from Modules.Housing.Entertainment.entertainment import MqttActions as entertainmentMqtt
from Modules.Housing.Hvac.hvac import MqttActions as hvacMqtt
from Modules.Housing.Security.security import MqttActions as securityMqtt
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Mqtt_Actions   ')


class Actions(object):
    """
    """

    m_myname = 'Not Initialized.'
    m_pyhouse_obj = PyHouseData()

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_myname = p_pyhouse_obj.Computer.Name

    def _get_field(self, p_message, p_field):
        """ Get the given field from a JSON message.
        """
        try:
            l_ret = p_message[p_field]
        except (KeyError, TypeError):
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def _extract_node(self, p_message):
        l_node = NodeData()
        l_node.Name = self._get_field(p_message, 'Name')
        l_node.Key = l_node.Name
        l_node.Active = True
        l_node.Comment = ''
        l_node.ConnectionAddr_IPv4 = self._get_field(p_message, 'ConnectionAddr_IPv4')
        l_node.ConnectionAddr_IPv6 = self._get_field(p_message, 'ConnectionAddr_IPv6')
        l_node.ControllerCount = self._get_field(p_message, 'ControllerCount')
        l_node.ControllerTypes = self._get_field(p_message, 'ControllerTypes')
        l_node.NodeId = self._get_field(p_message, 'NodeId')
        l_node.NodeRole = self._get_field(p_message, 'NodeRole')

    def _decode_lighting(self, _p_topic, p_message):
        l_name = self._get_field(p_message, 'Name')
        l_logmsg = '\tLighting:\n'
        l_logmsg += '\tName: {}\n'.format(l_name)
        l_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        l_logmsg += '\tBrightness: {}'.format(self._get_field(p_message, 'BrightnessPct'))
        return l_logmsg

    def _decode_schedule(self, p_topic, p_message):
        l_logmsg = '\tSchedule:\n'
        if p_topic[1] == 'execute':
            l_logmsg += '\tType: {}\n'.format(self._get_field(p_message, 'ScheduleType'))
            l_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
            l_logmsg += '\tLight: {}\n'.format(self._get_field(p_message, 'LightName'))
            l_logmsg += '\tLevel: {}'.format(self._get_field(p_message, 'Level'))
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(p_message)
        return l_logmsg

    def _decode_weather(self, _p_topic, p_message):
        l_logmsg = '\tWeather:\n'
        l_temp = float(self._get_field(p_message, 'Temperature_F'))
        l_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Location'))
        l_logmsg += '\tTemp: {} ({})'.format(l_temp, ((l_temp / 5.0) * 9.0) + 32.0)
        l_logmsg += '\tWeather info {}'.format(p_message)
        return l_logmsg

    def _decodeLWT(self, _p_topic, p_message):
        l_logmsg = '\tLast Will:\n'
        l_logmsg += p_message
        return l_logmsg

    def mqtt_dispatch(self, p_topic, p_message):
        """ This is the master dispatch table for incoming messages.
        It has two functions:
            Acting on the message received.
            Creating a detail log for the message received.
        these are usually accomplished in the same module dispatch call.

        @param p_topic: is a list of topic part strings ( pyhouse, housename have been dropped
        @param p_message: is the payload that is JSON
        @return: a message to send to the log detailing the Mqtt message received.
        """
        # LOG('Dispatch:|n|tTopic: {}\n\tPayload: {}'.format(p_topic, p_message))
        l_logmsg = 'Dispatch\n\tTopic: {}\n'.format(p_topic)
        # Lwt can be from any device
        if p_topic[0] == 'lwt':
            l_logmsg += self._decodeLWT(p_topic, p_message)
            return l_logmsg
        #
        # Every other topic will have the following fields.
        l_sender = self._get_field(p_message, 'Sender')
        self.m_room_name = self._get_field(p_message, 'RoomName')
        l_logmsg += '\tSender: {}\n'.format(l_sender)
        #
        # Now do all the rest of the topic-2 fields.
        if p_topic[0] == 'computer':
            l_logmsg += self.m_pyhouse_obj.APIs.Computer.ComputerAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'entertainment':
            l_logmsg += entertainmentMqtt(self.m_pyhouse_obj).decode(p_topic, p_message)
        elif p_topic[0] == 'hvac':
            l_logmsg += hvacMqtt(self.m_pyhouse_obj).decode(p_topic, p_message)
        elif p_topic[0] == 'house':
            l_logmsg += self.m_pyhouse_obj.APIs.House.HouseAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'lighting':
            l_logmsg += self._decode_lighting(p_topic, p_message)
        elif p_topic[0] == 'login':
            l_logmsg += self.m_pyhouse_obj.APIs.House.HouseAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'schedule':
            l_logmsg += self._decode_schedule(p_topic, p_message)
        elif p_topic[0] == 'security':
            l_logmsg += securityMqtt(self.m_pyhouse_obj).decode(p_topic, p_message)
        elif p_topic[0] == 'weather':
            l_logmsg += self._decode_weather(p_topic, p_message)
        else:
            l_logmsg += '   OTHER: Unknown topic\n'
            l_logmsg += '\tTopic: {};\n'.format(p_topic[0])
            l_logmsg += '\tMessage: {};\n'.format(p_message)
        return l_logmsg

#  ## END DBK
