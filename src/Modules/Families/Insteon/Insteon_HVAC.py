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

My Device seems to put out codes 6E thru 72


"""


#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.InsteonHVAC    ')

FACTOR = 1.0  #  Multiplier to convert Thermostat units to Real World units
HALF = 0.5


class Util(object):
    """
    """

    def get_device_obj(self, p_pyhouse_obj, p_address):
        l_ret = self._find_addr(p_pyhouse_obj.House.Hvac.Thermostats, p_address)
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
            l_mqtt_message += " Set Mode; {}".format(l_cmd2)

        if l_cmd1 == 0x11:
            p_device_obj.ThermostatStatus = 'On'
            l_mqtt_message += " On; "

        if l_cmd1 == 0x13:
            p_device_obj.ThermostatStatus = 'Off'
            l_mqtt_message += " Off; "

        if l_cmd1 == 0x68:  #  Set thermostat temperature up (half degrees)
            l_mqtt_topic += '/temperature'
            l_mqtt_message += ' temp UP = {}; '.format(l_cmd2)

        if l_cmd1 == 0x69:  #  Set Thermostat temperature down (half degrees)
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_mqtt_topic += '/temperature'
            l_mqtt_message += ' temp DOWN = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6A:  #  Send request for thermostat status
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_mqtt_topic += '/temperature'
            l_mqtt_message += ' Status = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6B:  #  Response for thermostat status
            p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_mqtt_topic += '/temperature'
            l_mqtt_message += ' temp = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6C:  #  Thermostat Set cool set point
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_mqtt_topic += '/ThermostatSetCoolSetpointCommand'
            l_mqtt_message += ' cool set point = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6D:  #  Set heat set point
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_mqtt_topic += '/ThermostatSetHeatSetpointCommand'
            l_mqtt_message += ' Heat set point = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6e:  #  Status report Temperature
            p_device_obj.CurrentTemperature = l_cmd2 * FACTOR
            l_mqtt_topic += '/ThermostatTemperatureReport'
            l_mqtt_message += ' temp = {}; '.format(l_cmd2)

        if l_cmd1 == 0x6f:  #  Status Report Humidity
            l_mqtt_topic += '/ThermostatHumidityReport'

        if l_cmd1 == 0x70:  #  Status Report Mode / Fan Status
            l_mqtt_topic += '/ThermostatStatusReport'

        if l_cmd1 == 0x71:  #  Status Report Cool Set Point
            p_device_obj.CoolSetPoint = l_cmd2 * FACTOR
            l_mqtt_topic += '/ThermostatCoolSetPointReport'

        if l_cmd1 == 0x72:  #  Status Report Heat Set Point
            p_device_obj.HeatSetPoint = l_cmd2 * FACTOR
            l_mqtt_topic += '/ThermostatHeatSetPointReport'

        LOG.info('HVAC {}'.format(l_mqtt_message))
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_mqtt_topic, p_device_obj)  #  /temperature
        return

#  ## END DBK
