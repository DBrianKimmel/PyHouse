"""
@name:      Modules/House/Family/insteon/insteon_hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
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

__updated__ = '2019-12-06'

#  Import system type stuff

#  Import PyMh files
from Modules.House.Family.insteon.insteon_constants import MESSAGE_TYPES
from Modules.House.Family.insteon.insteon_utils import Decode as utilDecode
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.InsteonHVAC    ')

FACTOR = 1.0  #  Multiplier to convert Thermostat units to Real World units
HALF = 0.5

THERMOSTAT_CMD_1 = {
    'assign_to_group' : 0x01,  # Assign to All Link Group
    'delete_from_group' : 0x02,  # Delete from all link group
    'cleanup_success' : 0x06,  # Broadcast Cleanup
    'engine_version' : 0x0d,  # Insteon Engine version
    'ping' : 0x0F,
    'id_request' : 0x10,
    'on_status' : 0x11,  #
    'off_status' : 0x13,  #
    'increase_setpoints' : 0x15,  # Increase set points by 1 degree
    'decrease_setpoints' : 0x16,  #
    'read_operating_flag' : 0x1f,  #
    'set_operating_flags' : 0x20,  #
    'read_and_set_data' : 0x2e,  #
    'get_database' : 0x2f,  #
    'beep' : 0x30,

    'thermostat_temp_up' : 0x68,
    'thermostat_temp_down' : 0x69,
    'thermostat_status' : 0x6a,
    'thermostat_control' : 0x6b,
    'thermostat_setpoint_cool' : 0x6c,
    'thermostat_setpoint_heat' : 0x6d,
    'thermostat_report_temperature' : 0x6e,
    'thermostat_report_humidity' : 0x6f,
    'thermostat_report_mode' : 0x70,
    'thermostat_report_cool_setpoint' : 0x71,
    'thermostat_report_heat_setpoint' : 0x72
}


class InsteonThermostatStatus:

    def __init__(self):
        self.Name = None
        self.Family = 'insteon'
        self.Temperature = None
        self.Humidity = None
        self.CoolSetpoint = None
        self.HeatSetPoint = None
        self.Fan = None  # On, Off, Auto
        self.Mode = None  # Off, Heat, Cool, ManualAuto, Auto


class Util:
    """
    """

    def get_device_obj(self, p_pyhouse_obj, p_address):
        l_ret = self._find_addr(p_pyhouse_obj.House.Hvac.Thermostats, p_address)
        return l_ret


class DecodeResponses:

    def decode_0x50(self, p_pyhouse_obj, p_device_obj, p_controller_obj):
        """
        @param p_device_obj: is the Device (light, thermostat...) we are decoding.
        @param p_controller_obj: The controller sending the response.

        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.
        See p 233(246) of 2009 developers guide.
        [0] = x02
        [1] = 0x50
        [2-4] = from address
        [5-7] = to address / group
        [8] = message flags
        [9] = command 1
        [10] = command 2
        """

        l_message = p_controller_obj._Message
        l_topic = 'house/hvac/thermostat/{}'.format(p_device_obj.Name)
        l_mqtt_message = "thermostat: "
        l_status = InsteonThermostatStatus()
        l_status.Family = 'insteon'
        l_status.Name = p_device_obj.Name

        l_firmware = l_message[7]
        l_flags = utilDecode._decode_insteon_message_flag(l_message[8])
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]

        l_mqtt_message += ' Cmd1:{:#02X}/{:#02X}({:d}) '.format(l_cmd1, l_cmd2, l_cmd2)
        l_debug_msg = 'Fm:"{}"; Flg:{}; C1:{:#x},{:#x}; '.format(p_device_obj.Name, l_flags, l_cmd1, l_cmd2)

        if l_cmd1 == MESSAGE_TYPES['assign_to_group']:  # 0x01
            l_mqtt_message += " assign_to_group:{}; ".format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['delete_from_group']:  # 0x02
            l_mqtt_message += " delete_from_group:{}; ".format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['cleanup_success']:  #  0x06
            l_mqtt_message += 'CleanupSuccess with {} failures; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['engine_version']:  # 0x0d
            p_device_obj.EngineVersion = l_cmd2
            l_mqtt_message += " EngineId:{}; ".format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['ping']:  # 0x0f
            l_mqtt_message += " ping:{}; ".format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['id_request']:  # 0x10
            p_device_obj.FirmwareVersion = l_firmware
            l_mqtt_message += " id_request:{}; ".format(l_firmware)

        elif l_cmd1 == MESSAGE_TYPES['on']:  # 0x11
            p_device_obj.ThermostatStatus = 'On'
            l_mqtt_message += " On; "
        elif l_cmd1 == MESSAGE_TYPES['off']:  # 0x13
            p_device_obj.ThermostatStatus = 'Off'
            l_mqtt_message += " Off; "

        elif l_cmd1 == MESSAGE_TYPES['thermostat_temp_up']:  # 0x68:  #  Set thermostat temperature up (half degrees)
            l_topic += '/temperature'
            l_mqtt_message += ' temp UP = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_temp_down']:  # 0x69:  #  Set Thermostat temperature down (half degrees)
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALFdecode_0x50decode_0x50
            l_topic += '/temperature'
            l_mqtt_message += ' temp DOWN = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_status']:  # 0x6A:  #  Send request for thermostat status
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_topic += '/temperature'
            l_mqtt_message += ' Status = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_control']:  # 0x6B:  #  Response for thermostat status
            p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_topic += '/temperature'
            l_mqtt_message += ' temp = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_setpoint_cool']:  # 0x6C:  #  Thermostat Set cool set point
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_topic += '/ThermostatSetCoolSetpointCommand'
            l_mqtt_message += ' cool set point = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_setpoint_heat']:  # 0x6D:  #  Set heat set point
            #  p_device_obj.CurrentTemperature = l_cmd2 * HALF
            l_topic += '/ThermostatSetHeatSetpointCommand'
            l_mqtt_message += ' Heat set point = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_report_temperature']:  # 0x6E:  #  Status report Temperature
            p_device_obj.CurrentTemperature = l_cmd2 * FACTOR
            l_topic += '/ThermostatTemperatureReport'
            l_mqtt_message += ' Temperature = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_report_humidity']:  # 0x6f:  #  Status Report Humidity
            l_topic += '/ThermostatHumidityReport'
            l_mqtt_message += ' Humidity = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_report_mode']:  # 0x70:  #  Status Report Mode / Fan Status
            l_topic += '/ThermostatStatusReport'
            l_mqtt_message += ' StatusMode = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_report_cool_setpoint']:  # 0x71:  #  Status Report Cool Set Point
            p_device_obj.CoolSetPoint = l_cmd2 * FACTOR
            l_topic += '/ThermostatCoolSetPointReport'
            l_mqtt_message += ' CoolSetPoint = {}; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['thermostat_report_heat_setpoint']:  # 0x72:  #  Status Report Heat Set Point
            p_device_obj.HeatSetPoint = l_cmd2 * FACTOR
            l_topic += '/ThermostatHeatSetPointReport'
            # l_mqtt_message += ' HeatSetPoint = {}; '.format(l_cmd2)
            l_status.HeatSetPoint = l_cmd2
        else:
            l_mqtt_message += 'Unknown cmd1 '

        LOG.info('HVAC {}'.format(l_mqtt_message))
        p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_device_obj)  #  /temperature
        return

#  ## END DBK
