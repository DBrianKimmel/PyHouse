"""
@name:      PyHouse/src/Modules/Hvac/hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

This is the controlling portion of a complete HVAC system.

PyHouse.House.Hvac.
                   Thermostats

"""

__updated__ = '2018-07-16'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
# from Modules.Core.data_objects import ThermostatData
from Modules.Housing.Hvac.hvac_xml import XML as hvacXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Hvac           ')


class Utility(object):
    """
    """


class MqttActions(object):
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

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/hvac/<type>/<Name>/...
        <type> = thermostat, ...
        """
        l_logmsg = '\tHVAC:\n'
        if p_topic[1] == 'Thermostat':
            l_logmsg += '\tThermostat: {}\n'.format(self._get_field(p_message, 'Name'))
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Security msg', 160))
        return l_logmsg

    def _decode_hvac(self, p_logmsg, _p_topic, p_message):
        p_logmsg += '\tThermostat:\n'
        p_logmsg += '\tName: {}'.format(self.m_name)
        p_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
        p_logmsg += '\tTemp: {}'.format(self._get_field(p_message, 'CurrentTemperature'))
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
