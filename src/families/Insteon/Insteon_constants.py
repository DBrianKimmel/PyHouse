'''
Created on Apr 19, 2013

@author: briank

Note! This is designed for 'from Insteon_constants import *'

'''


STX = 0x02
ACK = 0x06
NAK = 0x15

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
    'plm_get_config': 0x73}

MESSAGE_TYPES = {
    'assign_to_group': 0x01,
    'delete_from_group': 0x02,
    'product_data_request': 0x03,
    'linking_mode': 0x09,
    'unlinking_mode': 0x0A,
    'engine_version': 0x0D,
    'ping': 0x0F,
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
    'on_at_ramp_rate': 0x2e,
    'off_at_ramp_rate': 0x2f,
    #                        sprinkler_valve_on => 0x40,
    #                        sprinkler_valve_off => 0x41,
    #                        sprinkler_program_on => 0x42,
    #                        sprinkler_program_off => 0x43,
    #                        sprinkler_control => 0x44,
    #                        sprinkler_timers_request => 0x45,
    'thermostat_temp_up': 0x68,
    'thermostat_temp_down': 0x69,
    'thermostat_get_zone_temp': 0x6a,
    'thermostat_get_zone_setpoint': 0x6a,
    'thermostat_get_zone_humidity': 0x6a,
    'thermostat_control': 0x6b,
    'thermostat_get_mode': 0x6b,
    'thermostat_get_temp': 0x6b,
    'thermostat_setpoint_cool': 0x6c,
    'thermostat_setpoint_heat': 0x6d}

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
    0x73: 6}

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

# ## END
