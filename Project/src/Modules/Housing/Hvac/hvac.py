"""
@name:      PyHouse/Project/src/Modules/Housing/Hvac/hvac.py
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

__updated__ = '2019-06-04'
__version_info__ = (19, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.data_objects import DeviceData
from Modules.Housing.Hvac.hvac_xml import XML as hvacXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hvac           ')


class HvacData():
    """
    DeviceType = 2

    ==> PyHouse.House.Hvac.xxx as in the def below
    """

    def __init__(self):
        self.Thermostats = {}  # ThermostatData()  Sub = 1


class ThermostatData(DeviceData):
    """

    ==> PyHouse.House.Hvac.Thermostats.xxx as in the def below
    """

    def __init__(self):
        super(ThermostatData, self).__init__()
        self.CoolSetPoint = 0
        self.CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.ThermostatScale = 'F'  # F | C
        self.ThermostatStatus = 'Off'  # On
        self.UUID = None


class ThermostatStatus():
    """
    """

    def __init__(self):
        self.Name = None
        self.Status = None
        self.Fan = None
        self.Mode = None
        self.Family = 'Insteon'
        self.BrightnessPct = None


class Utility(object):
    """
    """


class MqttActions():
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_thermostat(self, p_topic, p_message, p_logmsg):
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
            LOG.warn('Unknown HVAC Topic: {}'.format(p_topic[0]))
        return p_logmsg

    def _decode_hvac(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tThermostat:\n'
        p_logmsg += '\tName: {}'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(extract_tools.get_mqtt_field(p_message, 'CurrentTemperature'))
        return p_logmsg


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        l_obj = hvacXML.read_hvac_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Hvac = l_obj
        return l_obj

    def Start(self):
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = hvacXML.write_hvac_xml(self.m_pyhouse_obj, p_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Hvac XML.")
        return l_xml

#  ## END DBK
