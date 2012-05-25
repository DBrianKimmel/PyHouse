#!/usr/bin/python

"""Insteon PLM module.
"""

# Import system type stuff
#import binascii
import logging
import Queue

# Import PyMh files
import Device_Insteon
from tools import PrintBytes
#from twisted.internet import reactor


STX = 0x02
ACK = 0x06
NAK = 0x15

#PLM Serial Commands
plm_commands = {
'insteon_received'      : 0x50,
'insteon_ext_received'  : 0x51,
'x10_received'          : 0x52,
'all_link_complete'     : 0x53,
'plm_button_event'      : 0x54,
'user_user_reset'       : 0x55,
'all_link_clean_failed' : 0x56,
'all_link_record'       : 0x57,
'all_link_clean_status' : 0x58,
'plm_info'              : 0x60,
'all_link_send'         : 0x61,
'insteon_send'          : 0x62,
'x10_send'              : 0x63,
'all_link_start'        : 0x64,
'plm_reset'             : 0x67,
'plm_first_all_link'    : 0x69,
'plm_next_all_link'     : 0x6A,
'plm_set_config'        : 0x6B,
'plm_led_on'            : 0x6D,
'plm_led_off'           : 0x6E,
'insteon_nak'           : 0x70,
'insteon_ack'           : 0x71,
'rf_sleep'              : 0x72,
'plm_get_config'        : 0x73,
}
message_types = {
'assign_to_group'       : 0x01,
'delete_from_group'     : 0x02,
'product_data_request'  : 0x03,
'linking_mode'          : 0x09,
'unlinking_mode'        : 0x0A,
'engine_version'        : 0x0D,
'ping'                  : 0x0F,
'id_request'            : 0x10,
'on'                    : 0x11,
'on_fast'               : 0x12,
'off'                   : 0x13,
'off_fast'              : 0x14,
'bright'                : 0x15,
'dim'                   : 0x16,
'start_manual_change'   : 0x17,
'stop_manual_change'    : 0x18,
'status_request'        : 0x19,
'get_operating_flags'   : 0x1f,
'set_operating_flags'   : 0x20,
#                        do_read_ee => 0x24,
'remote_set_button_tap' : 0x25,
'set_led_status'        : 0x27,
'set_address_msb'       : 0x28,
'poke'                  : 0x29,
'poke_extended'         : 0x2a,
'peek'                  : 0x2b,
'peek_internal'         : 0x2c,
'poke_internal'         : 0x2d,
'on_at_ramp_rate'       : 0x2e,
'off_at_ramp_rate'      : 0x2f,
#                        sprinkler_valve_on => 0x40,
#                        sprinkler_valve_off => 0x41,
#                        sprinkler_program_on => 0x42,
#                        sprinkler_program_off => 0x43,
#                        sprinkler_control => 0x44,
#                        sprinkler_timers_request => 0x45,
#                        thermostat_temp_up => 0x68,
#                        thermostat_temp_down => 0x69,
#                        thermostat_get_zone_temp => 0x6a,
#                        thermostat_get_zone_setpoint => 0x6a,
#                        thermostat_get_zone_humidity => 0x6a,
#                        thermostat_control => 0x6b,
#                        thermostat_get_mode => 0x6b,
#                        thermostat_get_temp => 0x6b,
#                        thermostat_setpoint_cool => 0x6c,
#                        thermostat_setpoint_heat => 0x6d
}


Last_Response = bytearray()
m_serial = None


class LightingStatusAPI(Device_Insteon.LightingStatusAPI): pass


class LightingAPI(Device_Insteon.LightingAPI):
    """
    """

    def change_light_setting(self, p_name, p_level):
        #print " insteon_PLM.change_light_settings "
        #self.m_logger.info('change_light_setting()')
        for _l_key, l_obj in Device_Insteon.Light_Data.iteritems():
            if l_obj.get_family() != 'Insteon': continue
            if l_obj.get_name() == p_name:
                if int(p_level) == 0:
                    self.turn_light_off(p_name)
                elif int(p_level) == 100:
                    self.turn_light_on(p_name)
                else:
                    self.turn_light_dim(p_name, p_level)
                Device_Insteon.Light_Status[p_name].CurLevel = p_level
                return

    def turn_light_off(self, p_name):
        """Implement turning off an Insteon light.
        """
        self.m_logger.debug('***Turning off light {0:}'.format(p_name))
        self.send_62_command(p_name, message_types['off'], 0)
        self.m_logger.info('Turned off light {0:}'.format(p_name))

    def turn_light_on(self, p_name):
        """Turn on a light to a level = 0 - 100 %.
        """
        self.m_logger.debug('***Turning on light={0:}'.format(p_name))
        l_level = 0xFF
        self.send_62_command(p_name, message_types['on'], l_level)
        self.m_logger.info('Turned on light={0:}'.format(p_name))

    def turn_light_dim(self, p_name, p_level):
        """Turn on a light to a level = 0 - 100 %.
        """
        self.m_logger.debug('***Dimming light={0:} to level={1:}'.format(p_name, p_level))
        l_level = int(p_level) * 255 / 100
        self.send_62_command(p_name, message_types['on'], l_level)
        self.m_logger.info('Turned on light={0:} to level={1:}'.format(p_name, p_level))

    def update_all_devices(self):
        #Device_Insteon.InsteonLightingAPI.update_all_devices(Device_Insteon.InsteonLightingAPI())
        pass


class LightHandlerAPI(LightingAPI, LightingStatusAPI):
    """This is the API for light control.
    """

    def scan_all_lights(self, p_lights):
        """Exported command - used by other modules.
        """
        print "insteon_PLM.scan_all_lights"
        for l_key, l_obj in p_lights.iteritems():
            if Device_Insteon.LightingData.get_family(l_obj) != 'Insteon': continue
            if l_obj.get_Type == 'Light':
                self._scan_one_light(l_key)

    def initialize_controller_port(self):
        self.m_driver = []
        #Device_Insteon.ControllerAPI.dump_all_controllers(Device_Insteon.ControllerAPI())
        for _l_key, l_obj in Device_Insteon.Controller_Data.iteritems():
            #print " & PLM.initialize_controller_port ", l_key, l_obj
            if l_obj.Family != 'Insteon': continue
            if l_obj.Active != True: continue
            if l_obj.Interface.lower() == 'serial':
                import Driver_Serial
                l_driver = Driver_Serial.SerialDriverMain(l_obj)
            elif l_obj.Interface.lower() == 'ethernet':
                import Driver_Ethernet
                l_driver = Driver_Ethernet.EthernetDriverMain(l_obj)
            elif l_obj.Interface.lower() == 'usb':
                import Driver_USB
                l_driver = Driver_USB.USBDriverMain(l_obj)
            self.m_driver.append(l_driver)

    def ping_plm(self):
        """Send a command to the plm and get its response.
        """
        l_ret = self.send_60_command()
        return l_ret

    def set_plm_mode(self):
        """Set the PLM to a mode 
        """
        self.send_6B_command(0x50)

    def get_all_lights_status(self):
        """Get the status (current level) of all lights.
        """
        self.m_logger.info('Getting light levels of all lights')
        for l_key, l_obj in Device_Insteon.Light_Data.iteritems():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Type == 'Light':
                l_level = self.get_one_light_status(l_key)
                self.update_status_by_name(l_obj.Name, 'Insteon', l_level)
                #print " -- Light {0:} is at level {1:}".format(l_key, l_level)
            else:
                #print " -- Device {0:} is not a light - is a {1:}".format(l_key, l_obj.Type)
                pass
        #print " -- insteon_PLM.get_all_lights_status() completed "

    def get_one_light_status(self, p_name):
        """Get the status of a light.
        
        We will (apparently) get back a 62-ACK followed by a 50 with the level in the response.

        @return: the light current level (0-100%)
        """
        l_level = 0
        self.send_62_command(p_name, message_types['status_request'], 0)
        #print " Last_Response = {0:}".format(PrintBytes(Last_Response))
        if len(Last_Response) > 10:
            l_level = Last_Response[10] * 100 / 255
        self.m_logger.info('Got status of light {0:} - Level={1:}'.format(p_name, l_level))
        return l_level

    def id_request(self, p_name):
        """Get the device DevCat"""
        l_devcat = 0
        self.m_logger.debug('request ID from device {0:}'.format(p_name))
        self.send_62_command(p_name, message_types['id_request'], 0)
        if len(Last_Response) > 9:
            if Last_Response[9] == 1:
                l_devcat = Last_Response[5] * 256 + Last_Response[6]
        return l_devcat

    def get_engine_version(self, p_name):
        """ i1 = pre 2007 I think
            i2 = no checksun - new commands
            i2cs = 2012 add checksums + new commands.
        """
        self.m_logger.debug('***Getting Insteon Envine version')
        self.send_62_command(p_name, message_types['engine_version'], 0)


class InsteonPlmUtility(LightHandlerAPI):

    def _str_to_addr_list(self, p_str):
        l_ret = [1, 2, 3]
        l_ret[0] = int(p_str[0:2], 16)
        l_ret[1] = int(p_str[3:5], 16)
        l_ret[2] = int(p_str[6:8], 16)
        #print "** {0:} = {1:}".format(p_str, PrintBytes(l_ret))
        return l_ret

    def _get_addr_from_name(self, p_name):
        """Given a device name, return a 3 bytearray(3) containing the devices address.
        Addresses are in the data as a string 'C1.A2.33'.
        @return: a list of 3 bytes that are the address.
        """
        for l_obj in Device_Insteon.Light_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Name == p_name: return self._str_to_addr_list(l_obj.Address)
        for l_obj in Device_Insteon.Button_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Name == p_name: return self._str_to_addr_list(l_obj.Address)
        for l_obj in Device_Insteon.Controller_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Name == p_name: return self._str_to_addr_list(l_obj.Address)
        self.m_logger.error("_get_addr_from_name() - Did not find 'Address' for name={0:}".format(p_name))
        return [0x11, 0x22, 0x33]

    def _get_name_from_id(self, p_id):
        """
        Get the Name from the database using the Address (ID)
        
        @param p_id:The addreess in the form AA.BB.CC  
        """
        for l_obj in Device_Insteon.Light_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            #print " **name_from_id {0:}, {1:}".format(p_id, l_obj.Address)
            if l_obj.Address == p_id: return l_obj.Name
        #print " **name_from_id {0:}, {1:}".format(p_id, l_obj.Address)
        for l_obj in Device_Insteon.Button_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Address == p_id: return l_obj.Name
        for l_obj in Device_Insteon.Controller_Data.itervalues():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Address == p_id: return l_obj.Name
        self.m_logger.error("get_name_from_id - Nothing found for Address:{0:}".format(p_id)), l_obj.Address
        return None

    def _get_ack_nak(self, p_byte):
        if p_byte == 0x06:
            return 'ACK'
        elif p_byte == 0x15:
            return 'NAK'
        else:
            return "Unknown response {0:X} ".format(p_byte)

    def _decode_message_flag(self, p_byte):
        """
        """
        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10)
        l_hops_left = (p_byte & 0x0C) >> 2
        l_max_hops = (p_byte & 0x03)
        if l_type == 4:
            l_ret = 'Broadcast'    # Broadcast
        elif l_type == 0:
            l_ret = 'Direct'    # Direct message
        elif l_type == 1:
            l_ret = 'DirACK'    # Direct message ACK
        elif l_type == 5:
            l_ret = 'DirNAK'    # Direct message NAK
        elif l_type == 6:
            l_ret = 'All_Brdcst'    # All-Link Broadcast
        elif l_type == 2:
            l_ret = 'All_Cleanup'    # All-Link Cleanup
        elif l_type == 3:
            l_ret = 'All_Clean_ACK'    # All-Link Cleanup ACK
        else:
            l_ret = 'All_Clean_NAK'    # All-Link Cleanup NAK
        if l_extended == 0:
            l_ret += '-Std-'
        else:
            l_ret += '-Ext-'
        l_ret = "{0:}{1:d}-{2:d}={3:#X}".format(l_ret, l_hops_left, l_max_hops, p_byte)
        return l_ret

    def _scan_one_light(self, p_name):
        """Scan a light.  we are looking for DevCat and any other info about device.
        send message to the light/button/etc
        get ack of message sent
        pause a bit
        get response
        ???
        
        @param p_name: is the key for the entry in Light_Data 
        """
        self.send_62_command(p_name, message_types['product_data_request'], 0x00)
        l_product_data = l_devcat = l_devsubcat = None
        try:
            l_product_data = Last_Response[12:3]
            l_devcat = Last_Response[15]
            l_devsubcat = Last_Response[16]
        except:
            pass
        print "Scanning one light {0:} Prod={1:} DevCat={2:} SubCat={3:}".format(p_name, PrintBytes(l_product_data), l_devcat, l_devsubcat)

    def _get_all_ids(self):
        """Get the devcat from all devices that are 0.
        """
        print "~~PLM.get_all_ids"
        for _l_key, l_obj in Device_Insteon.Light_Data.iteritems():
            if l_obj.Family != 'Insteon': continue
            l_devcat = l_obj.DevCat
            if l_devcat == 0:
                #lighting.Light_Data[l_key].DevCat = self.id_request(l_key)
                #"{0:#04X}".format(l_devcat) self.id_request(l_key)
                pass
        self.update_all_devices()


class InsteonAllLinks(InsteonPlmUtility):

    def get_all_allinks(self):
        """A command to fetch the all-link database from the PLM
        """
        l_ret = self._get_first_allink()
        while l_ret:
            l_ret = self._get_next_allink()

    def _get_first_allink(self):
        """Get the first all-link record from the plm (69 command).
        See p 261 of developers guide.
        """
        return self.send_69_command()

    def _get_next_allink(self):
        """Get the next record - will get a nak if no more (6A command).
        Returns True if more - False if no more.
        """
        return self.send_6A_command()

    def add_link(self, p_link):
        """Add an all link record.
        """

    def delete_link(self, p_link):
        """Delete an all link record.
        """


class DecodeResponses(InsteonAllLinks):

    def _decode_message(self, p_message, p_length = 1):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241
        
        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_stx = p_message[0]
        l_ret = False
        if l_stx == 0x15:
            self.m_logger.warning("Found a NAK - Retrying.")
            return False
        elif l_stx != 0x02:
            self.m_logger.error("Message started with {0:#x} not STX, Message={1:}".format(l_stx, PrintBytes(p_message)))
            return l_ret
        l_cmd = p_message[1]
        if l_cmd == 0:
            self.m_logger.warning("Found a '0' record ->{0:}.".format(PrintBytes(p_message)))
            return l_ret
        elif l_cmd == 0x50: l_ret = self._decode_50_record(p_message, p_length)
        elif l_cmd == 0x51: l_ret = self._decode_51_record(p_message, p_length)
        elif l_cmd == 0x52: l_ret = self._decode_52_record(p_message, p_length)
        elif l_cmd == 0x53: l_ret = self._decode_53_record(p_message, p_length)
        elif l_cmd == 0x54: l_ret = self._decode_54_record(p_message, p_length)
        elif l_cmd == 0x55: l_ret = self._decode_55_record(p_message, p_length)
        elif l_cmd == 0x56: l_ret = self._decode_56_record(p_message, p_length)
        elif l_cmd == 0x57: l_ret = self._decode_57_record(p_message, p_length)
        elif l_cmd == 0x58: l_ret = self._decode_58_record(p_message, p_length)
        #
        elif l_cmd == 0x60: l_ret = self._decode_60_record(p_message, p_length)
        elif l_cmd == 0x61: print "   insteon_PLM._decode got msg type 61"
        elif l_cmd == 0x62: l_ret = self._decode_62_record(p_message, p_length) # print "   insteon_PLM._decode got msg type 62"
        elif l_cmd == 0x63: print "   insteon_PLM._decode got msg type 63"
        elif l_cmd == 0x64: print "   insteon_PLM._decode got msg type 64"
        elif l_cmd == 0x65: print "   insteon_PLM._decode got msg type 65"
        elif l_cmd == 0x66: print "   insteon_PLM._decode got msg type 66"
        elif l_cmd == 0x67: print "   insteon_PLM._decode got msg type 67"
        elif l_cmd == 0x68: print "   insteon_PLM._decode got msg type 68"
        elif l_cmd == 0x69: l_ret = self._decode_69_record(p_message, p_length)
        elif l_cmd == 0x6A: l_ret = self._decode_6A_record(p_message, p_length)
        elif l_cmd == 0x6B: l_ret = self._decode_6B_record(p_message, p_length)
        elif l_cmd == 0x6C: print "   insteon_PLM._decode got msg type 6C"
        else:
            self.m_logger.error("Unknown message >>".format(PrintBytes(p_message)))
        return l_ret

    def _decode_50_record(self, p_message, p_length):
        """ Insteon Standard Message Received.
        See p 246 of developers guide.
        """
        l_id_from = "{0:X}.{1:X}.{2:X}".format(p_message[2], p_message[3], p_message[4]).upper()
        l_name_from = self._get_name_from_id(l_id_from)
        l_flags = self._decode_message_flag(p_message[8])
        if p_message[9] == 1:
            # Save to extract the devcat a bit later.
            Last_Response = p_message
            #l_devcat = p_message[5]
            #l_devsubcat = p_message[6]
            #self.m_logger.info("== 50 From={0:}, DevCat={1:}, SubCat={2:}, flags={3:} ==".format(l_name_from, l_devcat, l_devsubcat, l_flags))
            l_ret = True
        else:
            Last_Response = p_message
            l_id_to = "{0:X}.{1:X}.{2:X}".format(p_message[5], p_message[6], p_message[7]).upper()
            l_data = [p_message[9], p_message[10]]
            l_name_to = self._get_name_from_id(l_id_to)
            Device_Insteon.LightingStatusAPI.update_status_by_name(self, l_name_from, 'Insteon', p_message[10])
            self.m_logger.info("== 50 From={0:}, To={1:}, Flags={2:}, Data={3:} ==".format(l_name_from, l_name_to, l_flags, l_data))
            l_ret = True
        if p_length > 11:
            l_msg = p_message[11:]
            l_ret = self._decode_message(l_msg, p_length - 11)
        return l_ret

    def _decode_51_record(self, p_message, p_length):
        """ Insteon Extended Message Received.
        See p 247 of developers guide.
        """
        l_id_from = "{0:X}.{1:X}.{2:X}".format(p_message[2], p_message[3], p_message[4]).upper()
        l_id_to = "{0:X}.{1:X}.{2:X}".format(p_message[5], p_message[6], p_message[7]).upper()
        l_flags = p_message[8]
        l_data = [p_message[9], p_message[10]]
        l_extended = "{0:X}.{1:X}.{2:X}.{3:X}.{4:X}.{5:X}.{6:X}.{7:X}.{8:X}.{9:X}.{10:X}.{11:X}.{12:X}.{13:X}".format(
                    p_message[11], p_message[12], p_message[13], p_message[14], p_message[15], p_message[16], p_message[17],
                    p_message[18], p_message[19], p_message[20], p_message[21], p_message[22], p_message[23], p_message[24])
        l_name_from = self._get_name_from_id(l_id_from)
        l_name_to = self._get_name_from_id(l_id_to)
        self.m_logger.info("== 51 From={0:}, To={1:}, Flags={2:#x}, Data={3:} Extended={4:} ==".format(l_name_from, l_name_to, l_flags, l_data, l_extended))
        l_ret = True
        if p_length > 25:
            l_msg = p_message[25:]
            l_ret = self._decode_message(l_msg, p_length - 25)
        return l_ret

    def _decode_52_record(self, _p_message, _p_length):
        """Insteon X-10 message received. 
        See p 253 of developers guide.
        """
        self.m_logger.warning("== 52 message not decoded yet.")
        return False

    def _decode_53_record(self, _p_message, _p_length):
        """Insteon All-Linking completed. 
        See p 260 of developers guide.
        """
        self.m_logger.warning("== 53 message not decoded yet.")
        return False

    def _decode_54_record(self, _p_message, _p_length):
        """Insteon Button Press event. 
        See p 276 of developers guide.
        """
        self.m_logger.warning("== 54 message not decoded yet.")
        return False

    def _decode_55_record(self, _p_message, _p_length):
        """Insteon User Reset detected. 
        See p 269 of developers guide.
        """
        self.m_logger.warning("== 55 message not decoded yet.")
        return False

    def _decode_56_record(self, _p_message, _p_length):
        """Insteon All-Link cleanup failure report. 
        See p 256 of developers guide.
        """
        self.m_logger.warning("== 56 message not decoded yet.")
        return False

    def _decode_57_record(self, p_message, p_length):
        """Insteon All-Link Record Response
        See p 264 of developers guide.
        """
        l_flags = p_message[2]
        #l_flag_control = l_flags & 0x40
        l_group = p_message[3]
        l_id = "{0:X}.{1:X}.{2:X}".format(p_message[4], p_message[5], p_message[6]).upper()
        l_data = [p_message[7], p_message[8], p_message[9]]
        l_name = self._get_name_from_id(l_id)
        self.m_logger.info("== 57 All-Link response Name={0:}, Flags={1:#x}, Group={2:#x}, Data={3:} ".format(l_name, l_flags, l_group, l_data))
        l_ret = True
        if p_length > 10:
            l_msg = p_message[10:]
            l_ret = self._decode_message(l_msg, p_length - 10)
        return l_ret

    def _decode_58_record(self, _p_message, _p_length):
        """Insteon All-Link cleanup status report. 
        See p 257 of developers guide.
        """
        self.m_logger.warning("== 58 message not decoded yet.")
        return False

    def _decode_60_record(self, p_message, p_length):
        """Get Insteon Modem Info.
        See p 273 of developers guide.
        """
        l_id = "{0:X}.{1:X}.{2:X}".format(p_message[2], p_message[3], p_message[4]).upper()
        l_devcat = p_message[5]
        l_devsubcat = p_message[6]
        l_firmver = p_message[7]
        l_name = self._get_name_from_id(l_id)
        self.m_logger.info("== 60 - Insteon Modem Info - DevCat={0:}, DevSubCat={1:}, Firmware={2:} - Name={3:}".format(l_devcat, l_devsubcat, l_firmver, l_name))
        if p_message[8] == ACK:
            l_ret = True
        else:
            self.m_logger.error("== 60 - No ACK - Got {0:#x}".format(p_message[8]))
            l_ret = False
        if p_length > 11:
            l_msg = p_message[11:]
            l_ret = self._decode_message(l_msg, p_length - 11)
        return l_ret

    def _decode_62_record(self, p_message, p_length):
        """Get response to Send Insteon standard-length message.
        Basically, a response to the 62 command.
        See p 243 of developers guide.
        """
        l_id = "{0:X}.{1:X}.{2:X}".format(p_message[2], p_message[3], p_message[4]).upper()
        l_msgflags = self._decode_message_flag(p_message[5])
        #l_cmd1 = p_message[6]
        #l_cmd2 = p_message[7]
        l_ack = self._get_ack_nak(p_message[8])
        l_name = self._get_name_from_id(l_id)
        self.m_logger.info("== 62 {0:} {1:} {2:}".format(l_name, l_msgflags, l_ack))
        l_ret = True
        if p_length > 9:
            l_msg = p_message[9:]
            l_ret = self._decode_message(l_msg, p_length - 9)
        return l_ret

    def _decode_69_record(self, p_message, p_length):
        """Get first All-Link record.
        See p 261 of developers guide.
        """
        if p_message[2] == ACK:
            #self.m_logger.info("== 69 - ACK")
            l_ret = True
        else:
            self.m_logger.info("== 69 - NAK")
            l_ret = False
        if l_ret & (p_length > 3):
            l_msg = p_message[3:]
            l_ret = self._decode_message(l_msg, p_length - 3)
        return l_ret

    def _decode_6A_record(self, p_message, p_length):
        """Get next All-Link.
        See p 262 of developers guide.
        """
        if p_message[2] == ACK:
            #self.m_logger.info("== 6A - ACK")
            l_ret = True
        else:
            #self.m_logger.info("== 6A - NAK")
            return False
        if l_ret & (p_length > 3):
            l_msg = p_message[3:]
            l_ret = self._decode_message(l_msg, p_length - 3)
        return l_ret

    def _decode_6B_record(self, p_message, p_length):
        """Get set IM configuration.
        See p 271 of developers guide.
        """
        self.m_logger.info("== 6B - Flags = {0:#x}".format(p_message[2]))
        if p_message[3] == ACK:
            l_ret = True
        else:
            self.m_logger.error("== 6B - NAK/Unknown message type {0:#x}".format(p_message[2]))
            l_ret = False
        if p_length > 4:
            l_msg = p_message[4:]
            l_ret = self._decode_message(l_msg, p_length - 4)
        return l_ret

    def _decode_73_record(self, p_message, p_length):
        """Get the PLM response of get config.
        See p 270 of developers guide.
        """
        l_flags = p_message[2]
        l_spare1 = p_message[3]
        l_spare2 = p_message[4]
        l_ack = self._get_ack_nak(p_message[5])
        self.m_logger.info("== 73 Get IM configuration Flags={0#x:}, Spare 1={1:#x}, Spare 2={2:#x} {3:} ".format(l_flags, l_spare1, l_spare2, l_ack))
        l_ret = True
        if p_length > 11:
            l_msg = p_message[11:]
            l_ret = self._decode_message(l_msg, p_length - 11)
        return l_ret


class CreateCommands(DecodeResponses):
    """Send various commands to the PLM.
    """

    def send_60_command(self):
        """Insteon - get IM info.
        See p 273 of developers guide.
        PLM will respond with a 0x60 response.
        """
        self.m_logger.debug("Send command to get IM info")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_info']
        return self.send_plm_command(l_command)

    def send_62_command(self, p_name, p_cmd1, p_cmd2):
        """Send Insteon Standard Length Message.
        See page 243 of Insteon Developers Guide.
        
        @param p_name: is the name of the device
        @param p_cmd1: is the first command byte
        @param p_cmd2: is the second command byte
        @return: the response from send_plm_command    
        """
        l_addr = self._get_addr_from_name(p_name)
        l_command = bytearray(8)
        l_command[0] = STX
        l_command[1] = plm_commands['insteon_send']
        l_command[2] = l_addr[0]
        l_command[3] = l_addr[1]
        l_command[4] = l_addr[2]
        l_command[5] = 0x0F
        l_command[6] = p_cmd1
        l_command[7] = p_cmd2
        self.m_logger.debug("Send command {0:X},{1:X} to {2:} ({3:x}.{4:x}.{5:x})".format(p_cmd1, p_cmd2, p_name, l_command[2], l_command[3], l_command[4]))
        l_ret = self.send_plm_command(l_command)
        return l_ret

    def send_69_command(self):
        """Get the first all-link record from the plm (69 command).
        See p 261 of developers guide.
        """
        #self.m_logger.debug("Send command to get First all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_first_all_link']
        l_ret = self.send_plm_command(l_command)
        return l_ret

    def send_6A_command(self):
        """Get the next record - will get a nak if no more (6A command).
        Returns True if more - False if no more.
        """
        #self.m_logger.debug("Send command to get Next all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_next_all_link']
        l_ret = self.send_plm_command(l_command)
        return l_ret

    def send_6B_command(self, p_flags):
        """
        See page 271  of Insteon Developers Guide.
        """
        self.m_logger.debug("Send command to set PLM config to {0:X}".format(p_flags))
        l_command = bytearray(3)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_set_config']
        l_command[2] = p_flags
        return self.send_plm_command(l_command)

    def send_73_command(self):
        """Send request for PLM configuration.
        See page 270 of Insteon Developers Guide.
        """
        self.m_logger.debug("Send command to get PLM config.")
        l_command = bytearray(8)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_get_config']
        return self.send_plm_command(l_command)


class InsteonPlmAPI(CreateCommands):
    """
    """

    def get_aldb_record(self, p_addr):
        pass

    def put_aldb_record(self, p_addr, p_record):
        pass


class PlmDriverInterface(InsteonPlmAPI):
    """
    Check the command queue and send the 1st command if available.
    check the plm for received data
    If nothing to send - try again in 3 seconds.
    if nothing received, try again in 1 second.
    """

    def driver_loop_start(self):
        self.m_reactor.callLater(3, self.dequeue_and_send)
        self.m_reactor.callLater(1, self.receive_loop)
        self.m_repeat = 0

    def send_plm_command(self, p_command):
        self.m_queue.put(p_command)

    def dequeue_and_send(self):
        #print "-Dequeue_and_send"
        try:
            l_command = self.m_queue.get(False)
        except:
            # No commands queued
            #print "  nothing to dequeue"
            self.m_reactor.callLater(3, self.dequeue_and_send)
            return
        #print "- Got a command to send ", PrintBytes(l_command)
        try:
            self.m_driver[0].write_device(l_command)
        except IndexError:
            pass
        self.m_reactor.callLater(1, self.dequeue_and_send)

    def receive_loop(self):
        #print "=Receive_loop"
        try:
            (l_bytes, l_msg) = self.m_driver[0].fetch_read_data()
        except IndexError:
            (l_bytes, l_msg) = (0, '')
        #print l_bytes, PrintBytes(l_msg)
        if l_bytes == 0:
            self.m_reactor.callLater(1, self.receive_loop)
            return False
        #print "= Received a buffer of {0:} bytes =>{1:}".format(l_bytes, PrintBytes(l_msg))
        l_ret = self._decode_message(l_msg, l_bytes)
        self.m_reactor.callLater(1, self.receive_loop)
        return l_ret


class PlmTesting(object):
    """
    """

    def test_light_commands(self):
        """Turn some stuff on and off to see if things are working.
        """
        self.ping_plm()
        #self.get_all_allinks()
        self.turn_light_on('wet_bar', 100)
        self._get_one_light_status('wet_bar')
        #time.sleep(1.0)
        self.turn_light_off('wet_bar')
        self._get_one_light_status('wet_bar')
        #time.sleep(1.0)
        pass


class InsteonPLMMain(PlmDriverInterface, PlmTesting):
    """Standard PyHouse control methods.
    """

    def __init__(self):
        """Constructor for the PLM.
        """
        self.m_logger = logging.getLogger('PyHouse.Insteon_PLM')
        self.initialize_controller_port()
        self.m_retry_count = 0
        self.m_queue = Queue.Queue(30)
        self.m_logger.info('Initialized.')

    def start(self, p_reactor):
        self.m_logger.info('Starting.')
        self.m_reactor = p_reactor
        self.driver_loop_start()
        self.set_plm_mode()
        self.get_all_lights_status()
        #self.test_light_commands()
        #self.get_all_allinks()
        #self._get_all_ids()
        self.m_logger.info('Started.')

### END
