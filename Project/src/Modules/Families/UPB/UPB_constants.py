"""
@name:      PyHouse/src/Modules/Families/UPB/UPB_constants.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2015
@Summary:

"""

__updated__ = '2017-01-20'


pim_commands = {
# Core commands
'null'                      : 0X00,
'write_enable'              : 0x01,
'write_protect'             : 0x02,
'start_setup_mode'          : 0x03,
'stop_setup_mode'           : 0x04,
'get_setup_time'            : 0x05,
'auto_address'              : 0x06,
'get_device_status'         : 0x07,
'set_device_status'         : 0x08,
'add_link'                  : 0x0B,
'delete_link'               : 0x0C,
'transmit_message'          : 0x0D,
'device_reset'              : 0x0E,
'get_device_signature'      : 0x0F,
'get_register_value'        : 0x10,
'set_register_value'        : 0x11,
# Device Control commands
'activate_link'             : 0x20,
'deactivate_link'           : 0x21,
'goto'                      : 0x22,
'fade_start'                : 0x23,
'fade_stop'                 : 0x24,
'blink'                     : 0x25,
'indicate'                  : 0x26,
'toggle'                    : 0x27,
'report_state'              : 0x30,
'store_state'               : 0x31
}


# ## END DBK
