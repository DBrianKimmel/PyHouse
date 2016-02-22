"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created Feb 20, 2016
@Summary:

"""


from Modules.Utilities.debug_tools import PrettyFormatAny


class Actions(object):
    """
    """
    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def _decode_computer(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tComputer:\n'
        if p_topic[1] == 'ip':
            l_ip = self._get_field(p_message, 'ExternalIPv4Address')
            p_logmsg += '\tIPv4: {}'.format(l_ip)
        elif p_topic[1] == 'startup':
            pass
        elif p_topic[1] == 'shutdown':
            pass
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        return p_logmsg

    def _decode_hvac(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tThermostat:\n\tName: {}'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(self._get_field(p_message, 'CurrentTemperature'))
        return p_logmsg

    def _decode_lighting(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tLighting:\n\tName: {}\n'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\n\tLevel: {}'.format(self._get_field(p_message, 'CurLevel'))
        return p_logmsg

    def _decode_schedule(self, p_logmsg, p_topic, p_message):
        if p_topic[1] == 'execute':
            p_logmsg += '\tSchedule:\n\tType: {}\n'.format(self._get_field(p_message, 'ScheduleType'))
            p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
            p_logmsg += '\tLight: {}\n'.format(self._get_field(p_message, 'LightName'))
            p_logmsg += '\tLevel: {}'.format(self._get_field(p_message, 'Level'))
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Schedule msg', 160))
        return p_logmsg

    def _decode_weather(self, p_logmsg, p_topic, p_message):
        l_temp = self._get_field(p_message, 'tempc')
        p_logmsg += '\tWeather:\n\tName: {}\n'.format(self._get_field(p_message, 'location'))
        p_logmsg += '\tTemp: {} ({})'.format(l_temp, l_temp / 5 * 9 + 32)
        return p_logmsg

    def dispatch(self, p_topic, p_message):
        """
        """
        l_logmsg = 'Dispatch\n\tTopic: {}\n'.format(p_topic)
        l_logmsg += '\tSender: {}\n'.format(self._get_field(p_message, 'Sender'))
        self.m_name = self._get_field(p_message, 'Name')
        self.m_room_name = self._get_field(p_message, 'RoomName')
        if p_topic[0] == 'computer':
            l_logmsg = self._decode_computer(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'hvac':
            l_logmsg = self._decode_hvac(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'lighting':
            l_logmsg = self._decode_lighting(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'schedule':
            l_logmsg = self._decode_schedule(l_logmsg, p_topic, p_message)
        elif p_topic[0] == 'weather':
            l_logmsg = self._decode_weather(l_logmsg, p_topic, p_message)
        else:
            l_logmsg += 'OTHER: Unknown'
            l_logmsg += '\tMessage: {}\n'.format(PrettyFormatAny.form(p_message, 'Message', 160))
        return l_logmsg

#  ## END DBK
