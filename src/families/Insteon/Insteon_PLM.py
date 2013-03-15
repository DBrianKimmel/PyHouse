#!/usr/bin/python

"""Insteon PLM module.

Create commands and interpret results from any Insteon controller regardless of interface.

TODO: Work toward getting one instance per controller.
        We will then need to assign lights to a particular controller if there is more than one in a house.

This module carries state information about the controller.
This is necessary since the responses may follow a command at any interval.
Responses do not all have to follow the command that caused them.
"""

# Import system type stuff
import logging
import Queue
from twisted.internet import reactor

# Import PyMh files
import Device_Insteon
import Insteon_Link
from utils.tools import PrintBytes

g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = sent commands high level
# 3 = decode response
# 4 = sent command detail (number)
# 5 = diagnostics
# 6


g_driver = []
g_logger = None
g_queue = None

callLater = reactor.callLater


STX = 0x02
ACK = 0x06
NAK = 0x15

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for fetching data in the rx buffer

# Modes for setting PLM mode
MODE_DISABLE_DEADMAN = 0x10
MODE_DISABLE_AUTO_LED = 0x20
MODE_MONITOR = 0x40
MODE_DISABLE_AUTO_LINK = 0x80

# Message flag bits (Page 55 of Developers Manual).
FLAG_BROADCAST_NAK = 0x80
FLAG_ALL_LINK = 0x40
FLAG_ACKNOWLEDGEMENT = 0x20
FLAG_EXTENDED_CMD = 0x10
FLAG_HOPS_LEFT = 0x0C
FLAG_MAX_HOPS = 0x03


# PLM Serial Commands
plm_commands = {
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
'plm_get_config': 0x73,
}
message_types = {
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
'thermostat_setpoint_heat': 0x6d
}


class InsteonPlmUtility(object):

    def _get_addr_from_message(self, p_message, p_index):
        l_id = "{0:0X}.{1:0X}.{2:0X}".format(p_message[p_index], p_message[p_index + 1], p_message[p_index + 2]).upper()
        return l_id

    def _str_to_addr_list(self, p_str):
        l_ret = [0, 0, 0]
        try:
            l_ret[0] = int(p_str[0:2], 16)
            l_ret[1] = int(p_str[3:5], 16)
            l_ret[2] = int(p_str[6:8], 16)
        except ValueError:
            pass
        return l_ret

    def _get_ack_nak(self, p_byte):
        if p_byte == 0x06:
            return 'ACK '
        elif p_byte == 0x15:
            return 'NAK '
        else:
            return "{0:#02X} ".format(p_byte)

    def _decode_message_flag(self, p_byte):
        """
        """
        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10)
        l_hops_left = (p_byte & 0x0C) >= 4
        l_max_hops = (p_byte & 0x03)
        if l_type == 4:
            l_ret = 'Broadcast'  # Broadcast
        elif l_type == 0:
            l_ret = 'Direct'  # Direct message
        elif l_type == 1:
            l_ret = 'DirACK'  # Direct message ACK
        elif l_type == 5:
            l_ret = 'DirNAK'  # Direct message NAK
        elif l_type == 6:
            l_ret = 'All_Brdcst'  # All-Link Broadcast
        elif l_type == 2:
            l_ret = 'All_Cleanup'  # All-Link Cleanup
        elif l_type == 3:
            l_ret = 'All_Clean_ACK'  # All-Link Cleanup ACK
        else:
            l_ret = 'All_Clean_NAK'  # All-Link Cleanup NAK
        if l_extended == 0:
            l_ret += '-Std-'
        else:
            l_ret += '-Ext-'
        l_ret = "{0:}{1:d}-{2:d}={3:#X}".format(
                        l_ret, l_hops_left, l_max_hops, p_byte)
        return l_ret


class PlmDriverInterface(object):
    """
    Check the command queue and send the 1st command if available.
    check the plm for received data
    If nothing to send - try again in 3 seconds.
    if nothing received, try again in 1 second.
    """
    m_queue = None

    def driver_loop_start(self, _p_house_obj):
        if g_debug >= 1:
            print "Insteon_PLM.driver_loop_start()"
        self.m_queue = Queue.Queue(300)
        callLater(SEND_TIMEOUT, self.dequeue_and_send)
        callLater(RECEIVE_TIMEOUT, self.receive_loop)

    def driver_loop_stop(self):
        if g_debug >= 1:
            print "Insteon_PLM.driver_loop_stop()"
        pass

    def queue_plm_command(self, p_command):
        self.m_queue.put(p_command)
        if g_debug >= 5:
            print "Insteon_PLM.queue_plm_command() - Q-Size:{0:}, Command:{1:}".format(self.m_queue.qsize(), PrintBytes(p_command))

    def dequeue_and_send(self):
        """Check the sending queue every SEND_TIMEOUT seconds and send if
        anything to send.

        Uses twisted to get a callback when the timer expires.
        """
        callLater(SEND_TIMEOUT, self.dequeue_and_send)
        # print "Insteon_PLM.dequeue_and_send() - Size:{0:}".format(self.m_queue.qsize())
        try:
            l_command = self.m_queue.get(False)
        except Queue.Empty:
            return
        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
            if l_controller_obj.Family.lower() != 'insteon':
                continue
            if l_controller_obj.Active != True:
                continue
            if l_controller_obj.Driver != None:
                l_controller_obj.Command = l_command
                l_controller_obj.Driver.write_device(l_command)
                if g_debug >= 5:
                    print "Insteon_PLM.dequeue_and_send() to {0:}, Message: {1:}".format(l_controller_obj.Name, PrintBytes(l_command))
                    g_logger.debug("Send to controller:{0:}, Message:{1:}".format(l_controller_obj.Name, PrintBytes(l_command)))

    def receive_loop(self):
        """Check the driver to see if the controller returned any messages.
        """
        callLater(RECEIVE_TIMEOUT, self.receive_loop)
        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
            l_bytes = 0
            if g_debug >= 7:
                print "Insteon_PLM.receive_loop()", l_controller_obj.Name
            if l_controller_obj.Driver != None:
                (l_bytes, l_msg) = l_controller_obj.Driver.fetch_read_data()
                if l_bytes == 0:
                    continue
                l_controller_obj.Message = l_msg
                self._decode_message(l_controller_obj)



class CreateCommands(PlmDriverInterface, InsteonPlmUtility):
    """Send various commands to the PLM.
    """

    def queue_60_command(self):
        """Insteon - get IM info (2 bytes).
        See p 273 of developers guide.
        PLM will respond with a 0x60 response.
        """
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_info']
        if g_debug >= 4:
            print "Insteon_PLM.queue_60_command() - get IM info."
            g_logger.debug("Queue command to get IM info")
        return self.queue_plm_command(l_command)

    def queue_61_command(self, p_obj):
        """Send ALL-Link Command (5 bytes)
        See p 254 of developers guide.
        """
        pass

    def queue_62_command(self, p_light_obj, p_cmd1, p_cmd2):
        """Send Insteon Standard Length Message (8 bytes).
        See page 243 of Insteon Developers Guide.

        @param p_light_obj: is the Light object of the device
        @param p_cmd1: is the first command byte
        @param p_cmd2: is the second command byte
        @return: the response from queue_plm_command
        """
        l_addr = self._str_to_addr_list(p_light_obj.Address)
        l_command = bytearray(8)
        l_command[0] = STX
        l_command[1] = p_light_obj.Command = plm_commands['insteon_send']
        l_command[2] = l_addr[0]
        l_command[3] = l_addr[1]
        l_command[4] = l_addr[2]
        l_command[5] = FLAG_MAX_HOPS + FLAG_HOPS_LEFT  # 0x0F
        l_command[6] = p_light_obj.Command1 = p_cmd1
        l_command[7] = p_light_obj.Command2 = p_cmd2
        if g_debug >= 4:
            print "Insteon_PLM.queue_62_command() ", p_light_obj.Name, p_cmd1, p_cmd2
            g_logger.debug("Queue62 command to device: {2:}, Command: {0:#X},{1:#X}, Address: ({3:x}.{4:x}.{5:x})".format(p_cmd1, p_cmd2, p_light_obj.Name, l_command[2], l_command[3], l_command[4]))
        return self.queue_plm_command(l_command)

    def queue_63_command(self, p_obj):
        """
        """
        pass

    def queue_64_command(self, p_obj):
        """
        """
        pass

    def queue_65_command(self, p_obj):
        """
        """
        pass

    def queue_66_command(self, p_obj):
        """
        """
        pass

    def queue_67_command(self):
        """Reset the PLM
        See p 268 of developers guide.
        """
        if g_debug >= 4:
            print "Insteon_PLM.queue_67_command() - Reset the PLM."
            g_logger.debug("Queue command to reset the PLM.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_reset']
        return self.queue_plm_command(l_command)

    def queue_68_command(self, p_obj):
        """
        """
        pass

    def queue_69_command(self):
        """Get the first all-link record from the plm (2 bytes).
        See p 261 of developers guide.
        """
        if g_debug >= 4:
            print "Insteon_PLM.queue_69_command() - Get first all-link record."
            g_logger.debug("Queue command to get First all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_first_all_link']
        return self.queue_plm_command(l_command)

    def queue_6A_command(self):
        """Get the next record - will get a nak if no more (2 bytes).
        See p 262 of developers guide.
        Returns True if more - False if no more.
        """
        if g_debug >= 4:
            print "Insteon_PLM.queue_6A_command() get Next all-link record."
            g_logger.debug("Queue command to get Next all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_next_all_link']
        return self.queue_plm_command(l_command)

    def queue_6B_command(self, p_flags):
        """Set IM configuration flags (3 bytes).
        See page 271  of Insteon Developers Guide.
        """
        if g_debug >= 4:
            print "Insteon_PLM.queue_6B_command() to set PLM config flag"
            g_logger.debug("Queue command to set PLM config flag to {0:#X}".format(p_flags))
        l_command = bytearray(3)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_set_config']
        l_command[2] = p_flags
        return self.queue_plm_command(l_command)

    def queue_6C_command(self, p_obj):
        """
        """
        pass

    def queue_6D_command(self, p_obj):
        """
        """
        pass

    def queue_6E_command(self, p_obj):
        """
        """
        pass

    def queue_6F_command(self, p_light_obj, p_code, p_flag, p_data):
        """Manage All-Link Record (11 bytes)
        """
        if g_debug >= 4:
            print "Insteon_PLM.queue_6F_command() to manage all-link record"
            g_logger.debug("Queue command to manage all-link record")
        l_addr = self._str_to_addr_list(p_light_obj.Address)
        l_command = bytearray(11)
        l_command[0] = STX
        l_command[1] = plm_commands['manage_all_link_record']  # 0x6F
        l_command[2] = p_code
        l_command[3] = p_flag
        l_command[4] = p_light_obj.GroupNumber
        l_command[5] = l_addr[0]
        l_command[6] = l_addr[1]
        l_command[7] = l_addr[2]
        l_command[8] = p_data[0]
        l_command[9] = p_data[1]
        l_command[10] = p_data[2]
        return self.queue_plm_command(l_command)


    def queue_70_command(self, p_obj):
        """
        """
        pass

    def queue_71_command(self, p_obj):
        """
        """
        pass

    def queue_72_command(self, p_obj):
        """RF Sleep
        """
        pass

    def queue_73_command(self, p_light_obj):
        """Send request for PLM configuration (2 bytes).
        See page 270 of Insteon Developers Guide.
        """
        if g_debug >= 5:
            print "Insteon_PLM.queue_73_command() to get plm config."
            g_logger.debug("Queue command to get PLM config.")
        l_command = bytearray(8)
        l_command[0] = STX
        l_command[1] = p_light_obj.Command = plm_commands['plm_get_config']
        return self.queue_plm_command(l_command)


class LightingAPI(Device_Insteon.LightingAPI, CreateCommands):

    def change_light_setting(self, p_light_obj, p_level):
        l_debug_msg = "Change light:{0:} to level:{1:}".format(p_light_obj.Name, p_level)
        if g_debug >= 2:
            print "Insteon_PLM.change_light_settings()  {0:}".format(l_debug_msg)
            g_logger.debug("Change light setting. {0:}".format(l_debug_msg))
        if int(p_level) == 0:
            self.queue_62_command(p_light_obj, message_types['off'], 0)
        elif int(p_level) == 100:
            self.queue_62_command(p_light_obj, message_types['on'], 255)
        else:
            l_level = int(p_level) * 255 / 100
            self.queue_62_command(p_light_obj, message_types['on'], l_level)

    def scan_all_lights(self, p_lights):
        """Exported command - used by other modules.
        """
        if g_debug >= 2:
            print "insteon_PLM.scan_all_lights"
        for l_obj in p_lights.itervalues():
            if Device_Insteon.LightData.get_family(l_obj) != 'Insteon':
                continue
            if l_obj.get_Type == 'Light':
                self.scan_one_light(l_obj.Name)
                pass


class InsteonPlmCommands(LightingAPI):

    def scan_one_light(self, p_name):
        """Scan a light.  we are looking for DevCat and any other info about
        device.
        send message to the light/button/etc
        get ack of message sent
        pause a bit
        get response
        ???

        @param p_name: is the key for the entry in Light_Data
        """
        self.queue_62_command(p_name, message_types['product_data_request'], 0x00)

    def update_object(self, p_obj):
        # TODO: implement
        pass


class InsteonAllLinks(InsteonPlmCommands):
    # TODO: implement

    def get_all_allinks(self, p_controller_obj):
        """A command to fetch the all-link database from the PLM
        """
        if g_debug >= 2:
            print "insteon_PLM.get_all_allinks"
            g_logger.debug("Get all All-Links from controller {0:}.".format(p_controller_obj.Name))
        l_ret = self._get_first_allink()
        while l_ret:
            l_ret = self._get_next_allink()

    def _get_first_allink(self):
        """Get the first all-link record from the plm (69 command).
        See p 261 of developers guide.
        """
        return self.queue_69_command()

    def _get_next_allink(self):
        """Get the next record - will get a nak if no more (6A command).
        Returns True if more - False if no more.
        """
        return self.queue_6A_command()

    def add_link(self, p_link):
        """Add an all link record.
        """

    def delete_link(self, p_address, p_group, p_flag):
        """Delete an all link record.
        """
        if g_debug >= 2:
            print "Insteon_PLM.delete_link() - Address:{0}, Group:{1:#02X}".format(p_address, p_group)
        p_light_obj = Device_Insteon.LightData()
        p_light_obj.Address = p_address
        p_light_obj.GroupNumber = p_group
        # p_code = 0x00  # Find First
        p_code = 0x00  # Delete First Found record
        # p_flag = 0xE2
        p_data = bytearray(3)
        g_logger.info("Delete All-link record - Address:{0:}, Group:{1:#02X}".format(p_light_obj.Address, p_group))
        l_ret = self.queue_6F_command(p_light_obj, p_code, p_flag, p_data)
        return l_ret

    def reset_plm(self):
        """This will clear out the All-Links database.
        """
        l_debug_msg = "Resetting PLM - Name:{0:}".format(self.m_controller_obj)
        if g_debug >= 2:
            print "Insteon_PLM.reset_plm() - delete the PLM all-link database. {0:}".format(l_debug_msg)
        self.queue_67_command()
        g_logger.info("Reset PLM")


class DecodeResponses(InsteonAllLinks):

    m_house_obj = None

    def _find_addr(self, p_class, p_addr):
        for l_obj in p_class.itervalues():
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.Address == p_addr:
                if g_debug >= 7:
                    print "Insteon_PLM._get_obj_using_addr(1) - Address:{0:}, found:{1:}".format(p_addr, l_obj.Name)
                return l_obj
        if g_debug >= 7:
            print "Insteon_PLM._get_obj_using_addr(2) - not found ", p_addr, p_class
        return None

    def _get_obj_using_addr(self, p_addr):
        """
        @param p_addr: String 'aa.bb.cc' is the address
        @return: the entire Lighting Device object
        """
        if g_debug >= 7:
            print "Insteon_PLM._get_obj_using_addr(4) - Address:{0:}".format(p_addr)
        l_ret = self._find_addr(self.m_house_obj.Lights, p_addr)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Controllers, p_addr)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Buttons, p_addr)
        if l_ret == None:
            l_ret = Device_Insteon.LightData()  # an empty new object
            l_ret.Name = '**' + str(p_addr) + '**'
        if g_debug >= 6:
            print "Insteon_PLM._get_obj_using_addr(5) - Address:{0:}, found:{1:}".format(p_addr, l_ret.Name)
        return l_ret

    def _decode_message(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see Insteon Developers Manual pages 238-241

        Since a controller response may contain multiple messages and the last message may not be complete.
        This should be invoked every time we pick up more messages from the controller.
        It should loop and decode each message present and leave when done


        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_message = p_controller_obj.Message
        l_done = False
        while not l_done:
            # Are we out of message?
            if len(p_controller_obj.Message) == 0:
                l_done = True
                return
            if g_debug >= 5:
                print "Insteon_PLM._decode_message() - {0:}".format(PrintBytes(l_message))
            l_stx = p_controller_obj.Message[0]
            # If we have a leading NAK, drop it and try again if we have more message
            if l_stx == 0x15:
                if g_debug >= 1:
                    print "Insteon_PLM._decode_message() - Found a leading NAK - Retrying. - {0:}".format(PrintBytes(l_message))
                p_controller_obj.Message = p_controller_obj.Message[1:]
                continue
            # If we have a leading ACK, drop it and try again if we have more message
            elif l_stx == 0x06:
                if g_debug >= 1:
                    print "Insteon_PLM._decode_message() - Found a leading ACK - Ignoring - {0:}".format(PrintBytes(l_message))
                p_controller_obj.Message = p_controller_obj.Message[1:]
                continue
            # We have a good message start.
            elif l_stx == 0x02:
                if g_debug >= 5:
                    print "Insteon_PLM._decode_message() - Found a message - {0:}".format(PrintBytes(l_message))
                self._decode_dispatch(p_controller_obj)
            # We have garbage.
            else:
                if g_debug >= 1:
                    print "Insteon_PLM._decode_message() - Found a mistake - {0:}".format(PrintBytes(l_message))
                g_logger.error("Rx Message started with {0:#x} not STX, Message={1:}".format(l_stx, PrintBytes(l_message)))

    def _decode_dispatch(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        p_message = p_controller_obj.Message
        l_ret = False
        l_cmd = p_controller_obj.Message[1]
        if l_cmd == 0:
            g_logger.warning("Found a '0' record ->{0:}.".format(PrintBytes(p_message)))
            return l_ret
        elif l_cmd == 0x50: l_ret = self._decode_50_record(p_controller_obj)
        elif l_cmd == 0x51: l_ret = self._decode_51_record(p_controller_obj)
        elif l_cmd == 0x52: l_ret = self._decode_52_record(p_controller_obj)
        elif l_cmd == 0x53: l_ret = self._decode_53_record(p_controller_obj)
        elif l_cmd == 0x54: l_ret = self._decode_54_record(p_controller_obj)
        elif l_cmd == 0x55: l_ret = self._decode_55_record(p_controller_obj)
        elif l_cmd == 0x56: l_ret = self._decode_56_record(p_controller_obj)
        elif l_cmd == 0x57: l_ret = self._decode_57_record(p_controller_obj)
        elif l_cmd == 0x58: l_ret = self._decode_58_record(p_controller_obj)
        elif l_cmd == 0x60: l_ret = self._decode_60_record(p_controller_obj)
        elif l_cmd == 0x61: l_ret = self._decode_61_record(p_controller_obj)
        elif l_cmd == 0x62: l_ret = self._decode_62_record(p_controller_obj)
        elif l_cmd == 0x63: print "   insteon_PLM._decode got msg type 63"
        elif l_cmd == 0x64: l_ret = self._decode_64_record(p_controller_obj)
        elif l_cmd == 0x65: print "   insteon_PLM._decode got msg type 65"
        elif l_cmd == 0x66: print "   insteon_PLM._decode got msg type 66"
        elif l_cmd == 0x67: print "   insteon_PLM._decode got msg type 67"
        elif l_cmd == 0x68: print "   insteon_PLM._decode got msg type 68"
        elif l_cmd == 0x69: l_ret = self._decode_69_record(p_controller_obj)
        elif l_cmd == 0x6A: l_ret = self._decode_6A_record(p_controller_obj)
        elif l_cmd == 0x6B: l_ret = self._decode_6B_record(p_controller_obj)
        elif l_cmd == 0x6C: print "   insteon_PLM._decode got msg type 6C"
        elif l_cmd == 0x6F: l_ret = self._decode_6F_record(p_controller_obj)
        elif l_cmd == 0x73: l_ret = self._decode_73_record(p_controller_obj)
        else:
            g_logger.error("Unknown message {0:}, Cmd:{1:}".format(PrintBytes(p_controller_obj.Message), l_cmd))
            self._check_for_more_decoding(p_controller_obj, 1, l_ret)
        return l_ret

    def _get_devcat(self, p_message, p_light_obj):
        l_devcat = p_message[5] * 256 + p_message[6]
        p_light_obj.DevCat = int(l_devcat)
        self.update_object(p_light_obj)
        l_debug_msg = "DevCat From={0:}, DevCat={1:#x}, flags={2:}".format(p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        if g_debug >= 1:
            print "Insteon_PLM._decode_50_record() - Got devcat type  From={0:}, DevCat={1:#x}, flags={2:}".format(
                            p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        g_logger.info("Got DevCat from light:{0:}, DevCat:{1:}".format(p_light_obj.Name, l_devcat))
        return l_debug_msg

    def _decode_50_record(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.

        See p 246 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_obj_from = self._get_obj_using_addr(self._get_addr_from_message(l_message, 2))
        l_name_from = l_obj_from.Name
        l_flags = self._decode_message_flag(l_message[8])
        l_obj_to = self._get_obj_using_addr(self._get_addr_from_message(l_message, 5))
        l_name_to = l_obj_to.Name
        l_data = [l_message[9], l_message[10]]
        l_debug_msg = 'Standard Message; '
        # Break down bits 7, 6, 5 into message type
        if l_message[8] & 0xE0 == 0x00:  # (000) Direct message type
            l_debug_msg += "DirectMessage from {0:}; ".format(l_name_from)
        elif l_message[8] & 0xE0 == 0x20:  # (001) ACK of Direct message type
            l_debug_msg += "AckDirectMessage from {0:}; ".format(l_name_from)
        elif l_message[8] & 0xE0 == 0x40:  # (010) All-Link Broadcast Clean-Up message type
            l_debug_msg += "All-Link Broadcast clean up from {0:}; ".format(l_name_from)
        elif l_message[8] & 0xE0 == 0x60:  # (011) All-Link Clean-Up ACK response message type
            l_debug_msg += "All-Link Clean up ACK from {0:}; ".format(l_name_from)
        elif l_message[8] & 0xE0 == 0x80:  # Broadcast Message (100)
            l_debug_msg += self._get_devcat(l_message, l_obj_from)
        elif l_message[8] & 0xE0 == 0xA0:  # (101) NAK of Direct message type
            l_debug_msg += "NAK of direct message(1) from {0:}; ".format(l_name_from)
        elif l_message[8] & 0xE0 == 0xC0:  # (110) all link broadcast of group is
            l_group = l_message[7]
            l_debug_msg += "All-Link broadcast From:{0:}, Group:{1:}, Flags:{2:}, Data:{3:}; ".format(l_name_from, l_group, l_flags, l_data)
            g_logger.info("== 50B All-link Broadcast From:{0:}, Group:{1:}, Flags:{2:}, Data:{3:} ==".format(l_name_from, l_group, l_flags, l_data))
        elif l_message[8] & 0xE0 == 0xE0:  # (111) NAK of Direct message type
            l_debug_msg += "NAK of direct message(2) from {0:}; ".format(l_name_from)
        #
        if l_obj_from.Command1 == message_types['product_data_request']:  # 0x03
            l_debug_msg += " product data request. - Should never happen - S/B 51 response"
        elif l_obj_from.Command1 == message_types['engine_version']:  # 0x0D
            l_engine_id = l_message[10]
            l_debug_msg += "Engine version From:{0:}, Sent to:{1:}, Id:{2:}; ".format(l_name_from, l_name_to, l_engine_id)
            g_logger.info("Got engine version from light:{0:}, To:{1:}, EngineID:{2:}".format(l_name_from, l_name_to, l_engine_id))
        elif l_obj_from.Command1 == message_types['id_request']:  # 0x10
            l_debug_msg += "Request ID From:{0:}; ".format(l_name_from)
            g_logger.info("Got an ID request. Light:{0:}".format(l_name_from,))
        elif l_obj_from.Command1 == message_types['on']:  # 0x11
            l_obj_from.CurLevel = 100
            l_debug_msg += "Light:{0:} turned Full ON; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from.Command1 == message_types['off']:  # 0x13
            l_obj_from.CurLevel = 0
            l_debug_msg += "Light:{0:} turned Full OFF; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from.Command1 == message_types['status_request']:  # 0x19
            l_level = int(((l_message[10] + 2) * 100) / 256)
            l_obj_from.CurLevel = l_level
            l_debug_msg += "Status of light:{0:} is level:{1:}; ".format(l_name_from, l_level)
            g_logger.info("PLM:{0:} Got Light Status From:{1:}, Level is:{2:}".format(p_controller_obj.Name, l_name_from, l_level))
            self.update_object(l_obj_from)
        else:
            l_debug_msg += "Insteon_PLM._decode_50_record() unknown type - last command was {0:#x} - {1:}; ".format(l_obj_from.Command1, PrintBytes(l_message))
        l_ret = True

        if g_debug >= 3:
            print "Insteon_PLM._decode_50_record() {0:}".format(l_debug_msg)
            g_logger.debug(l_debug_msg)
        return self._check_for_more_decoding(p_controller_obj, 11, l_ret)

    def _decode_51_record(self, p_controller_obj):
        """ Insteon Extended Message Received (25 bytes).
        See p 247 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_id_from = self._get_addr_from_message(l_message, 2)
        l_obj_from = self._get_obj_using_addr(l_id_from)
        l_id_to = self._get_addr_from_message(l_message, 5)
        l_obj_to = self._get_obj_using_addr(l_id_to)
        l_flags = l_message[8]
        l_data = [l_message[9], l_message[10]]
        l_extended = "{0:X}.{1:X}.{2:X}.{3:X}.{4:X}.{5:X}.{6:X}.{7:X}.{8:X}.{9:X}.{10:X}.{11:X}.{12:X}.{13:X}".format(
                    l_message[11], l_message[12], l_message[13], l_message[14], l_message[15], l_message[16], l_message[17],
                    l_message[18], l_message[19], l_message[20], l_message[21], l_message[22], l_message[23], l_message[24])
        l_product_key = self._get_addr_from_message(l_message, 12)
        l_devcat = l_message[15] * 256 + l_message[16]
        self.update_object(l_obj_from)
        if g_debug >= 3:
            print "Insteon_PLM._decode_51_record() - Response from:{0:}, Devcat:{1:}, ProduckKey:{2:}".format(l_obj_from.Name, l_devcat, l_product_key), l_extended
        g_logger.info("== 51 From={0:}, To={1:}, Flags={2:#x}, Data={3:} Extended={4:} ==".format(l_obj_from.Name, l_obj_to.Name, l_flags, l_data, l_extended))
        l_obj_from.ProductKey = l_product_key
        l_obj_from.DevCat = l_devcat
        l_ret = True
        return self._check_for_more_decoding(p_controller_obj, 25, l_ret)

    def _decode_52_record(self, p_controller_obj):
        """Insteon X-10 message received (4 bytes).
        See p 253 of developers guide.
        """
        g_logger.warning("== 52 message not decoded yet.")
        l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_52_record()"
        return self._check_for_more_decoding(p_controller_obj, 4, l_ret)

    def _decode_53_record(self, p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 260 of developers guide.
        """
        g_logger.warning("== 53 message not decoded yet.")
        l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_53_record()"
        return self._check_for_more_decoding(p_controller_obj, 10, l_ret)

    def _decode_54_record(self, p_controller_obj):
        """Insteon Button Press event (3 bytes).
        See p 276 of developers guide.
        """
        g_logger.warning("== 54 message not decoded yet.")
        l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_54_record()"
        return self._check_for_more_decoding(p_controller_obj, 2, l_ret)

    def _decode_55_record(self, p_controller_obj):
        """Insteon User Reset detected (2 bytes).
        See p 269 of developers guide.
        """
        l_debug_msg = "User Reset Detected! "
        l_ret = False
        g_logger.info("".format(l_debug_msg))
        if g_debug >= 3:
            print "Insteon_PLM.decode_55_record() {0:}".format(l_debug_msg)
        return self._check_for_more_decoding(p_controller_obj, 2, l_ret)

    def _decode_56_record(self, p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 256 of developers guide.
        """
        g_logger.warning("== 56 message not decoded yet.")
        l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_56_record()"
        return self._check_for_more_decoding(p_controller_obj, 7, l_ret)

    def _decode_57_record(self, p_controller_obj):
        """All-Link Record Response (10 bytes).
        See p 264 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_link_obj = Insteon_Link.LinkData()
        l_link_obj.Flag = l_flags = l_message[2]
        l_link_obj.Group = l_group = l_message[3]
        l_link_obj.Addess = l_address = self._get_addr_from_message(l_message, 4)
        l_link_obj.Data = l_data = [l_message[7], l_message[8], l_message[9]]
        l_obj = self._get_obj_using_addr(l_address)
        l_flag_control = l_flags & 0x40
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        g_logger.info("All-Link response-57 - Group={0:#02X}, Name={1:}, Flags={2:#x}, Data={3:}, {4:}".format(l_group, l_obj.Name, l_flags, l_data, l_type))
        l_ret = True
        if g_debug >= 3:
            print "Insteon_PLM.decode_57_record() - Group:{0:#02X}, Name:{1:}, Flags:{2:#0x}, Data:{3:}".format(l_group, l_obj.Name, l_flags, l_data)
        return self._check_for_more_decoding(p_controller_obj, 10, l_ret)

    def _decode_58_record(self, p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 257 of developers guide.
        """
        g_logger.warning("== 58 message not decoded yet.")
        l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_58_record()"
        return self._check_for_more_decoding(p_controller_obj, 3, l_ret)

    def _decode_60_record(self, p_controller_obj):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_id = self._get_addr_from_message(l_message, 2)
        l_devcat = l_message[5]
        l_devsubcat = l_message[6]
        l_firmver = l_message[7]
        l_obj = self._get_obj_using_addr(l_id)
        g_logger.info("== 60 - Insteon Modem Info - DevCat={0:}, DevSubCat={1:}, Firmware={2:} - Name={3:}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if l_message[8] == ACK:
            l_ret = True
        else:
            g_logger.error("== 60 - No ACK - Got {0:#x}".format(l_message[8]))
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_60_record()"
        return self._check_for_more_decoding(p_controller_obj, 9, l_ret)

    def _decode_61_record(self, p_controller_obj):
        """Get Insteon Modem Info (6 bytes).
        See p 254 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_cmd2 = l_message[4]
        l_ack = l_message[5]
        g_logger.info("All-Link Ack - Group:{0:}, Cmd:{1:}, Bcst:{2:}, Ack:{3:}".format(l_grp, l_cmd1, l_cmd2, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            g_logger.error("== 61 - No ACK - Got {0:#x}".format(l_ack))
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_61_record()"
        return self._check_for_more_decoding(p_controller_obj, 6, l_ret)

    def _decode_62_record(self, p_controller_obj):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 243 of developers guide.

        This is an ack of the command.
        A 50 response MAY immediately follow this response with any data requested.
        """
        l_message = p_controller_obj.Message
        l_id = self._get_addr_from_message(l_message, 2)
        l_msgflags = self._decode_message_flag(l_message[5])
        l_ack = self._get_ack_nak(l_message[8])
        l_obj = self._get_obj_using_addr(l_id)
        l_debug_msg = "Device:{0:}, {1:}".format(l_obj.Name, l_ack)
        if g_debug >= 3:
            print "Insteon_PLM.decode_62_record() {0:}".format(l_debug_msg)
            g_logger.debug("Got ACK(62) {0:}".format(l_debug_msg))
        return self._check_for_more_decoding(p_controller_obj, 9)

    def _decode_64_record(self, p_controller_obj):
        """Start All-Link ACK response (5 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_ack = l_message[4]
        g_logger.info("All-Link Ack - Group:{0:}, Cmd:{1:}, Ack:{2:}".format(l_grp, l_cmd1, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            g_logger.error("== 64 - No ACK - Got {0:#x}".format(l_ack))
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_64_record()"
        return self._check_for_more_decoding(p_controller_obj, 5, l_ret)

    def _decode_67_record(self, p_controller_obj):
        """Reset IM ACK response (3 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_ack = self._get_ack_nak(l_message[2])
        l_debug_msg = "Reset IM(PLM) {0:}".format(l_ack)
        g_logger.info("{0:}".format(l_debug_msg))
        if g_debug >= 3:
            print "Insteon_PLM.decode_64_record() {0:}".format(l_debug_msg)
        return self._check_for_more_decoding(p_controller_obj, 3)

    def _decode_69_record(self, p_controller_obj):
        """Get first All-Link record response (3 bytes).
        See p 261 of developers guide.
        """
        l_message = p_controller_obj.Message
        if l_message[2] == ACK:
            l_ret = True
            self.queue_6A_command()
        else:
            g_logger.info("All-Link first record - NAK")
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_69_record() - {0:}".format(self._get_ack_nak(l_message[2]))
        return self._check_for_more_decoding(p_controller_obj, 3, l_ret)

    def _decode_6A_record(self, p_controller_obj):
        """Get next All-Link (3 bytes).
        See p 262 of developers guide.
        """
        l_message = p_controller_obj.Message
        if l_message[2] == ACK:
            l_ret = True
            self.queue_6A_command()
        else:
            g_logger.info("All-Link Next record - NAK")
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_6A_record() - {0:}".format(self._get_ack_nak(l_message[2]))
        return self._check_for_more_decoding(p_controller_obj, 3, l_ret)

    def _decode_6B_record(self, p_controller_obj):
        """Get set IM configuration (4 bytes).
        See p 271 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_flag = l_message[2]
        l_ack = self._get_ack_nak(l_message[3])
        l_debug_msg = "from PLM:{0:} - ConfigFlag:{1:#02X}, {2:}".format(p_controller_obj.Name, l_flag, l_ack)
        g_logger.info("Received from {0:}".format(l_debug_msg))
        if l_message[3] == ACK:
            l_ret = True
        else:
            g_logger.error("== 6B - NAK/Unknown message type {0:#x}".format(l_flag))
            l_ret = False
        if g_debug >= 3:
            print "Insteon_PLM.decode_6B_record() - {0:}".format(l_debug_msg)
        return self._check_for_more_decoding(p_controller_obj, 4, l_ret)

    def _decode_6F_record(self, p_controller_obj):
        """All-Link manage Record Response (12 bytes).
        See p 267 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_code = l_message[2]
        l_flags = l_message[3]
        l_flag_control = l_flags & 0x40
        l_group = l_message[4]
        l_id = self._get_addr_from_message(l_message, 5)
        l_data = [l_message[8], l_message[9], l_message[10]]
        l_ack = self._get_ack_nak(l_message[11])
        l_obj = self._get_obj_using_addr(l_id)
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        l_message = "Manage All-Link response(6F)"
        l_message += " Group:{0:#02X}, Name:{1:}, Flags:{2:#02X}, Data:{3:}, CtlCode:{4:#02x},".format(l_group, l_obj.Name, l_flags, l_data, l_code)
        l_message += " Ack:{0:}, Type:{1:}".format(l_ack, l_type)
        g_logger.info("{0:}".format(l_message))
        l_ret = True
        if g_debug >= 3:
            print "Insteon_PLM.decode_6F_record() - {0:}".format(l_message)
        return self._check_for_more_decoding(p_controller_obj, 12, l_ret)

    def _decode_73_record(self, p_controller_obj):
        """Get the PLM response of 'get config' (6 bytes).
        See p 270 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_flags = l_message[2]
        l_spare1 = l_message[3]
        l_spare2 = l_message[4]
        l_ack = self._get_ack_nak(l_message[5])
        if g_debug >= 3:
            print "Insteon_PLM.decode_73_record() - got plm config response."
        g_logger.info("== 73 Get IM configuration Flags={0#x:}, Spare 1={1:#x}, Spare 2={2:#x} {3:} ".format(l_flags, l_spare1, l_spare2, l_ack))
        return self._check_for_more_decoding(p_controller_obj, 6)

    def _check_for_more_decoding(self, p_controller_obj, p_chop, p_ret = True):
        """
        @param l_message: is the possibly compound message.
        @param p_chop: is the number of characters to chop off the beginning of the message.
        @param p_ret: is the result to return.
        """

        l_ret = p_ret
        l_length = len(p_controller_obj.Message)
        if l_length >= p_chop:
            p_controller_obj.Message = p_controller_obj.Message[p_chop:]
            l_ret = self._decode_message(p_controller_obj)
        return l_ret


class InsteonPlmAPI(DecodeResponses):
    """
    """

    def get_aldb_record(self, p_addr):
        pass

    def put_aldb_record(self, p_addr, p_record):
        pass

    def get_engine_version(self, p_obj):
        """ i1 = pre 2007 I think
            i2 = no checksum - new commands
            i2cs = 2012 add checksums + new commands.
        """
        g_logger.debug('Request Insteon Engine version from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, message_types['engine_version'], 0)  # 0x0D

    def get_id_request(self, p_obj):
        """Get the device DevCat
        """
        g_logger.debug('Request Insteon ID(devCat) from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, message_types['id_request'], 0)  # 0x10

    def ping_plm(self):
        """Send a command to the plm and get its response.
        """
        return self.queue_60_command()

    def get_link_records(self, _p_house_obj):
        self.get_all_allinks()


class LightHandlerAPI(InsteonPlmAPI):
    """This is the API for light control.
    """

    def start_controller(self, p_controller_obj):
        if g_debug >= 1:
            print "Insteon_PLM.start_controller() - Name:{0:}".format(p_controller_obj.Name)
        if g_debug >= 1:
            print "Insteon_PLM.start_controller() - Family:{0:}, Interface:{1:}, Active:{2:}".format(p_controller_obj.Family, p_controller_obj.Interface, p_controller_obj.Active)
        if p_controller_obj.Interface.lower() == 'serial':
            from drivers import Driver_Serial
            l_driver = Driver_Serial.API()
        elif p_controller_obj.Interface.lower() == 'ethernet':
            from drivers import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif p_controller_obj.Interface.lower() == 'usb':
            from drivers import Driver_USB_0403_6001
            l_driver = Driver_USB_0403_6001.API()
        # TODO: Detect any other controllers here and load them
        p_controller_obj.Driver = l_driver
        l_driver.Start(p_controller_obj)
        if g_debug >= 1:
            print "  Insteon_PLM has just started a driver.  Name: {0:}".format(p_controller_obj.Name)

    def stop_controller(self, p_controller_obj):
        if g_debug >= 1:
            print "Insteon_PLM.stop__controller()"
        if p_controller_obj.Driver != None:
            p_controller_obj.Driver.Stop()

    def set_plm_mode(self, p_controller_obj):
        """Set the PLM to a mode
        """
        g_logger.info('Setting mode of Insteon controller {0:}.'.format(p_controller_obj.Name))
        if g_debug >= 2:
            print "Insteon_PLM.set_plm_mode() - Sending mode command to Insteon PLM"
        self.queue_6B_command(MODE_MONITOR)

    def get_all_lights_status(self):
        """Get the status (current level) of all lights.
        """
        if g_debug >= 2:
            print "Insteon_PLM.get_all_lights_status() for House:{0:}".format(self.m_house_obj.Name)
        g_logger.info('Getting light levels of all Insteon lights')
        for l_light_obj in self.m_house_obj.Lights.itervalues():
            if l_light_obj.Family != 'Insteon':
                continue
            if l_light_obj.Active != True:
                continue
            self._get_one_light_status(l_light_obj)

    def _get_one_light_status(self, p_light_obj):
        """Get the status of a light.
        We will (apparently) get back a 62-ACK followed by a 50 with the level in the response.
        """
        if g_debug >= 6:
            print "Insteon_PLM._get_one_light_status() {0:}".format(p_light_obj.Name)
        self.queue_62_command(p_light_obj, message_types['status_request'], 0)  # 0x19


class PlmTesting(object):
    """
    """

    def test_light_commands(self):
        """Turn some stuff on and off to see if things are working.
        """
        # self.ping_plm()
        # self._turn_light_on('wet_bar', 100)
        # self._get_one_light_status('wet_bar')
        # self._turn_light_off('wet_bar')
        # self._get_one_light_status('wet_bar')
        pass


class API(LightHandlerAPI):

    def __init__(self):
        """Constructor for the PLM.
        """
        if g_debug >= 1:
            print "Insteon_PLM.__init__()"
        global g_logger, g_driver, g_queue
        g_logger = logging.getLogger('PyHouse.Insteon_PLM')
        g_logger.info('Initializing.')
        g_driver = []
        g_queue = Queue.Queue(300)
        g_logger.info('Initialized.')

    def Start(self, p_house_obj, p_controller_obj):
        if g_debug >= 1:
            print "Insteon_PLM.Start() - HouseName:{0:}".format(p_house_obj.Name)
        g_logger.info('Starting.')
        self.m_house_obj = p_house_obj
        self.m_controller_obj = p_controller_obj
        self.start_controller(p_controller_obj)
        self.driver_loop_start(p_house_obj)
        self.set_plm_mode(p_controller_obj)
        self.get_all_lights_status()
        g_logger.info('Started.')
        if g_debug >= 1:
            print "Insteon_PLM.Start() has completed."

    def Stop(self, p_controller_obj):
        if g_debug >= 1:
            print "Insteon_PLM.Stop()"
        g_logger.info('Stopping.')
        self.driver_loop_stop()
        self.stop_controller(p_controller_obj)
        g_logger.info('Stopped.')

    def SpecialTest(self):
        if g_debug >= 1:
            print "Insteon_PLM.SpecialTest() ", self.m_controller_obj.Name
        self.delete_link('1C.A3.1A', 1, 0xA2)
        self.delete_link('1C.A3.1A', 1, 0xE2)
        self.delete_link('1C.98.EF', 1, 0XA2)
        self.delete_link('1C.98.EF', 0, 0XA2)
        self.delete_link('1D.3F.AD', 1, 0xA2)
        self.delete_link('1D.3F.AD', 0, 0xA2)
        self.delete_link('1D.2A.CE', 1, 0x00)
        self.delete_link('1D.2A.CE', 0, 0xA2)
        self.get_all_allinks(self.m_controller_obj)

# ## END
