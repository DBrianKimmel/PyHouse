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

__updated__ = '2019-10-06'
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


class lightingUtility(object):
    """
    """


class MqttActions():
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_thermostat(self, _p_topic, p_message, p_logmsg):
        """
        """
        p_logmsg += '\tThermostat: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        return p_logmsg

    def decode(self, p_topic, p_message, p_logmsg):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/house/hvac/<type>/<Name>/...
        <type> = thermostat, ...
        """
        p_logmsg += '\tHVAC:\n'
        if p_topic[0] == 'thermostat':
            p_logmsg += self._decode_thermostat(p_topic[1:], p_message, p_logmsg)
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Message', 160))
        return p_logmsg

    def _decode_hvac(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tThermostat:\n'
        p_logmsg += '\tName: {}'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(extract_tools.get_mqtt_field(p_message, 'CurrentTemperature'))
        return p_logmsg


class Api(lightingUtility):

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
