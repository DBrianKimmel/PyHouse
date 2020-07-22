"""
@name:      Modules/House/Family/insteon/insteon_constants.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 19, 2013
@summary:   This module is for communicating with Insteon controllers.

Note! This is designed for: 'from Insteon_constants import *'

"""

__updated__ = '2020-02-18'

STX = 0x02
ACK = 0x06
NAK = 0x15

DEVICE_TYPE = ['N/A', 'Lighting', 'HVAC', 'Security']  # documenting it

# PLM Serial Commands
PLM_COMMANDS = {
    'insteon_received': 0x50,
    'insteon_ext_received': 0x51,
    'x10_received': 0x52,
    'all_link_complete': 0x53,
    'plm_button_event': 0x54,
    'user_user_reset': 0x55,
    'all_link_clean_failed': 0x56,
    'all_link_record': 0x57,
    'all_link_clean_status': 0x58,
    'plm_info': 0x60,
    'all_link_send': 0x61,
    'insteon_send': 0x62,
    'x10_send': 0x63,
    'all_link_start': 0x64,
    'plm_reset': 0x67,
    'plm_first_all_link': 0x69,
    'plm_next_all_link': 0x6A,
    'plm_set_config': 0x6B,
    'plm_led_on': 0x6D,
    'plm_led_off': 0x6E,
    'manage_all_link_record': 0x6F,
    'insteon_nak': 0x70,
    'insteon_ack': 0x71,
    'rf_sleep': 0x72,
    'plm_get_config': 0x73
}

MESSAGE_TYPES = {
    'assign_to_group': 0x01,
    'delete_from_group': 0x02,
    'product_data_request': 0x03,
    'cleanup_success': 0x06,
    'linking_mode': 0x09,
    'unlinking_mode': 0x0A,
    'engine_version': 0x0D,
    'ping' : 0x0F,
    'id_request': 0x10,
    'on': 0x11,
    'on_fast': 0x12,
    'off': 0x13,
    'off_fast': 0x14,
    'bright': 0x15,
    'dim': 0x16,
    'start_manual_change': 0x17,
    'stop_manual_change': 0x18,
    'status_request': 0x19,
    'get_operating_flags': 0x1f,
    'set_operating_flags': 0x20,
    'do_read_ee': 0x24,
    'remote_set_button_tap': 0x25,
    'set_led_status': 0x27,
    'set_address_msb': 0x28,
    'poke': 0x29,
    'poke_extended': 0x2a,
    'peek': 0x2b,
    'peek_internal': 0x2c,
    'poke_internal': 0x2d,
    'on_at_ramp_rate': 0x2e,  # 'extended_set_get'
    'off_at_ramp_rate': 0x2f,
    'read_write_aldb': 0x2f,
    #                        sprinkler_valve_on => 0x40,
    #                        sprinkler_valve_off => 0x41,
    #                        sprinkler_program_on => 0x42,
    #                        sprinkler_program_off => 0x43,
    #                        sprinkler_control => 0x44,
    #                        sprinkler_timers_request => 0x45,
    'thermostat_temp_up': 0x68,
    'thermostat_temp_down': 0x69,
    'thermostat_status': 0x6a,
    'thermostat_control': 0x6b,
    'thermostat_setpoint_cool': 0x6c,
    'thermostat_setpoint_heat': 0x6d,
    'thermostat_report_temperature': 0x6e,
    'thermostat_report_humidity': 0x6f,
    'thermostat_report_mode': 0x70,
    'thermostat_report_cool_setpoint': 0x71,
    'thermostat_report_heat_setpoint': 0x72
}

# This is the length of the response from the PLM.
# Wait till we get the proper number of bytes before decoding the response.
# we sometimes only have a partial response when reading async.
MESSAGE_LENGTH = {
    0x50: 11,
    0x51: 25,
    0x52: 4,
    0x53: 10,
    0x54: 3,
    0x55: 2,
    0x56: 7,
    0x57: 10,
    0x58: 3,

    0x60: 9,
    0x61: 6,
    0x62: 9,
    0x63: 5,
    0x64: 5,
    0x65: 3,
    0x66: 6,
    0x67: 3,
    0x68: 4,
    0x69: 3,
    0x6A: 3,
    0x6B: 4,
    0x6C: 3,
    0x6D: 3,
    0x6E: 3,
    0x6F: 12,
    0x70: 4,
    0x71: 5,
    0x72: 3,
    0x73: 6
}

COMMAND_LENGTH = {
    0x60: 2,
    0x61: 5,
    0x62: 8,
    0x63: 4,
    0x64: 4,
    0x65: 2,
    0x66: 5,
    0x67: 2,
    0x68: 3,
    0x69: 2,
    0x6A: 2,
    0x6B: 3,
    0x6C: 2,
    0x6D: 2,
    0x6E: 2,
    0x6F: 11,
    0x70: 3,
    0x71: 4,
    0x72: 2,
    0x73: 2
}

X10_HOUSE = {
    0x00: 'M',
    0x01: 'E',
    0x02: 'C',
    0x03: 'K',
    0x04: 'O',
    0x05: 'G',
    0x06: 'A',
    0x07: 'I',
    0x08: 'N',
    0x09: 'F',
    0x0A: 'D',
    0x0B: 'L',
    0x0C: 'P',
    0x0D: 'H',
    0x0E: 'B',
    0x0F: 'J'
}

X10_UNIT = {
    0x00: '13',
    0x01: '5',
    0x02: '3',
    0x03: '11',
    0x04: '15',
    0x05: '7',
    0x06: '1',
    0x07: '9',
    0x08: '14',
    0x09: '6',
    0x0A: '4',
    0x0B: '12',
    0x0C: '16',
    0x0D: '8',
    0x0E: '2',
    0x0F: '10'
}

X10_COMMAND = {
    0x00: 'All Units Off',
    0x01: 'All Lights On',
    0x02: 'On',
    0x03: 'Off',
    0x04: 'Dim',
    0x05: 'Bright',
    0x06: 'All Lights Off',
    0x07: 'Extend Code',
    0x08: 'Hail Request',
    0x09: 'Hail Acknowledge',
    0x0A: 'Preset Dim',
    0x0B: 'Preset Dim',
    0x0C: 'Extended Data (analog)',
    0x0D: 'Status = On',
    0x0E: 'Status = Off',
    0x0F: 'Status Request'
}


class InsteonError(Exception):
    """
    General Insteon error.
    """

# ## END DBK
