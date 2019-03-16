"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created Feb 20, 2016
@Summary:

"""

__updated__ = '2019-03-07'
__version_info__ = (19, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
# from Modules.Core.data_objects import NodeData, PyHouseData
from Modules.Housing.Entertainment.entertainment import MqttActions as entertainmentMqtt
from Modules.Housing.Lighting.lighting import MqttActions as lightingMqtt
from Modules.Housing.Lighting.lighting_lights import MqttActions as lightsMqtt
from Modules.Housing.Hvac.hvac import MqttActions as hvacMqtt
from Modules.Housing.Scheduling.schedule import MqttActions as scheduleMqtt
from Modules.Housing.Security.security import MqttActions as securityMqtt
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Mqtt_Actions   ')


def get_mqtt_field(p_message, p_field):
    """ Get the given field from a JSON message.
    """
    try:
        l_ret = p_message[p_field]
    except (KeyError, TypeError):
        l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
    return l_ret


class Actions:
    """
    """

    m_disp_computer = None
    m_disp_lights = None
    m_myname = 'Not Initialized.'

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_myname = p_pyhouse_obj.Computer.Name
        self.m_disp_lights = lightsMqtt(p_pyhouse_obj)

    def _decode_weather(self, _p_topic, p_message):
        l_logmsg = '\tWeather:\n'
        l_temp = float(get_mqtt_field(p_message, 'Temperature_F'))
        l_logmsg += '\tName: {}\n'.format(get_mqtt_field(p_message, 'Location'))
        l_logmsg += '\tTemp: {} ({})'.format(l_temp, ((l_temp / 5.0) * 9.0) + 32.0)
        l_logmsg += '\tWeather info {}'.format(p_message)
        return l_logmsg

    def _decodeLWT(self, _p_topic, p_message):
        l_logmsg = '\tLast Will:\n'
        l_logmsg += p_message
        return l_logmsg

    def mqtt_dispatch(self, p_pyhouse_obj, p_topic, p_message):
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
        l_logmsg = 'Dispatch\n\tTopic: {}'.format(p_topic)
        # Lwt can be from any device
        if p_topic[0] == 'lwt':
            l_logmsg += self._decodeLWT(p_topic, p_message)
            LOG.info(l_logmsg)
        else:
            # Every other topic will have the following field(s).
            l_sender = get_mqtt_field(p_message, 'Sender')
            l_logmsg += '\n\tSender: {}\n'.format(l_sender)
        # Now do all the rest of the topic-2 fields.
        # LOG.debug('MqttDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'computer':
            l_logmsg += p_pyhouse_obj.APIs.Computer.ComputerAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'entertainment':
            l_logmsg += entertainmentMqtt(p_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'hvac':
            l_logmsg += hvacMqtt(p_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'house':
            l_logmsg += p_pyhouse_obj.APIs.House.HouseAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'lighting':
            l_logmsg += lightingMqtt(p_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'login':
            l_logmsg += p_pyhouse_obj.APIs.House.HouseAPI.DecodeMqtt(p_topic, p_message)
        elif p_topic[0] == 'schedule':
            l_logmsg += scheduleMqtt(p_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'security':
            l_logmsg += securityMqtt(p_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'weather':
            l_logmsg += self._decode_weather(p_topic, p_message)
        else:
            l_logmsg += '   OTHER: Unknown topic\n'
            l_logmsg += '\tTopic: {};\n'.format(p_topic[0])
            l_logmsg += '\tMessage: {};\n'.format(p_message)
            LOG.warn(l_logmsg)
        # LOG.info(l_logmsg)

#  ## END DBK
