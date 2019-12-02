"""
@name:      Modules/House/Hvac/hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

This is the controlling portion of a complete HVAC system.

PyHouse.House.Hvac.
                   Thermostats

"""

__updated__ = '2019-12-02'
__version_info__ = (19, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities import extract_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hvac           ')


class HvacInformation:
    """
    DeviceType = 'Hvac'

    ==> PyHouse.House.Hvac.xxx as in the def below
    """

    def __init__(self):
        self.Thermostats = {}  # ThermostatData()  Sub = 1


class lightingUtilityHvac:
    """
    """


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_thermostat(self, p_msg):
        """
        """
        p_msg.LogMessage += '\tThermostat: {}\n'.format(extract_tools.get_mqtt_field(p_msg.Payload, 'Name'))

    def decode(self, p_msg):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/house/hvac/<type>/<Name>/...
        <type> = thermostat, ...
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tHVAC:\n'
        if l_topic[0] == 'thermostat':
            self._decode_thermostat(p_msg)
        else:
            p_msg.Topic += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Message', 160))
        return p_msg.Topic

    def _decode_hvac(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tThermostat:\n'
        # p_logmsg += '\tName: {}'.p_msg.LogMessageelf.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(extract_tools.get_mqtt_field(p_message, 'CurrentTemperature'))
        return p_logmsg


class Api(lightingUtilityHvac):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pyhouse_obj.House.Hvac = HvacInformation()
        LOG.info("Initialized.")

    def LoadConfig(self):
        """ Load the HVAC config info.
        """

    def Start(self):
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveConfig(self):
        # hvacXML.write_hvac_xml()
        LOG.info("Saved Hvac XML.")

#  ## END DBK
