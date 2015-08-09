"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_HVAC -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_HVAC.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   This module decodes Insteon PLM response messages

Insteon HVAC module.

Adds HVAC (Heating Ventilation Air Conditioning) to the Insteon suite.
Specifically developed for the Venstar 1-day programmable digital thermostat.
This contains an Insteon radio modem.

Models 2491T1E and 2491T7E = (2491TxE)

see: 2441xxx pdf guides

"""


# Import system type stuff

# Import PyMh files
from Modules.Utilities import json_tools


class Util(object):
    """
    """

    def get_device_obj(self, p_pyhouse_obj, p_address):
        l_ret = self._find_addr(p_pyhouse_obj.House.Thermostats, p_address)
        return l_ret


class ihvac_utility(object):

    def decode_50_record(self, p_pyhouse_obj, p_device_obj, p_controller_obj):
        """
        @param p_device_obj: is the Device (light, thermostat...) we are decoding.
        """
        l_mqtt_topic = 'thermostat/{}'.format(p_device_obj.Name)
        l_mqtt_message = "Thermostat: "
        l_message = p_controller_obj._Message
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_mqtt_message += ' Command1: {:#X},  Command2:{:#X}({:d})'.format(l_cmd1, l_cmd2, l_cmd2)
        if l_cmd1 == 0x01:
            l_mqtt_message += " Set Mode; "
        if l_cmd1 == 0x11:
            p_device_obj.ThermostatStatus = 'On'
            l_mqtt_message += " On; "
        if l_cmd1 == 0x13:
            p_device_obj.ThermostatStatus = 'Off'
            l_mqtt_message += " Off; "
        if l_cmd1 == 0x6e:
            p_device_obj.CurrentTemperature = l_cmd2
            l_mqtt_topic += '/temperature'
            l_mqtt_message += ' temp = {}; '.format(l_cmd2)
        l_json = json_tools.encode_json(p_device_obj)
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_mqtt_topic, l_json)
        return

# ## END DBK
