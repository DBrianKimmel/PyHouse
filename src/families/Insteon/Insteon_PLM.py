#!/usr/bin/python

"""Insteon PLM module.

Create commands and interpret results from any Insteon controller regardless
 of interface.
"""

# Import system type stuff
import logging
import Queue
from twisted.internet import reactor

# Import PyMh files
import Device_Insteon
from main.tools import PrintBytes
from house import house

g_debug = 1

g_driver = []
g_logger = None
g_queue = None
g_house_obj = None

House_Data = house.House_Data

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
            return 'ACK'
        elif p_byte == 0x15:
            return 'NAK'
        else:
            return "Unknown response {0:#X} ".format(p_byte)

    def _decode_message_flag(self, p_byte):
        """
        """
        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10)
        l_hops_left = (p_byte & 0x0C) >> 2
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

    def driver_loop_start(self, p_house_obj):
        if g_debug > 1:
            print "Insteon_PLM.driver_loop_start()"
        global g_queue
        g_queue = Queue.Queue(300)
        callLater(SEND_TIMEOUT, self.dequeue_and_send)
        callLater(RECEIVE_TIMEOUT, self.receive_loop)

    def driver_loop_stop(self):
        if g_debug > 0:
            print "Insteon_PLM.driver_loop_stop()"
        pass

    def queue_plm_command(self, p_command):
        if g_debug > 5:
            print "Insteon_PLM.queue_plm_command() - {0:}".format(PrintBytes(p_command))
        g_queue.put(p_command)

    def dequeue_and_send(self):
        """Check the sending queue every SEND_TIMEOUT seconds and send if
        anything to send.

        Uses twisted to get a callback when the timer expires.
        """
        # get the command to send
        try:
            l_command = g_queue.get(False)
        except Queue.Empty:
            callLater(SEND_TIMEOUT, self.dequeue_and_send)
            return
        # call the correct driver to send the command
        # try:
        #    g_driver[0].write_device(l_command)
        # except IndexError:
        #    pass
        for l_controller_obj in g_house_obj.Controllers.itervalues():
            if l_controller_obj.Driver != None:
                l_controller_obj.Driver.write_device(l_command)
                if g_debug > 5:
                    print "Insteon_PLM.dequeue_and_send() to {0:}, Message: {1:}".format(l_controller_obj.Name, PrintBytes(l_command))
        callLater(SEND_TIMEOUT, self.dequeue_and_send)

    def receive_loop(self):
        """Check the driver to see if the controller returned any messages.
        """
        callLater(RECEIVE_TIMEOUT, self.receive_loop)
        # try:
        #    (l_bytes, l_msg) = g_driver[0].fetch_read_data()
        # except IndexError:
        #    (l_bytes, l_msg) = (0, '')
        for l_controller_obj in g_house_obj.Controllers.itervalues():
            if g_debug > 4:
                print "Insteon_PLM.receive_loop()", g_house_obj.Controllers, l_controller_obj
            if l_controller_obj.Driver != None:
                (l_bytes, l_msg) = l_controller_obj.Driver.fetch_read_data()
                if g_debug > 5:
                    print "Insteon_PLM.receive_loop() from {0:}, Message: {1:}".format(l_controller_obj.Name, PrintBytes(l_msg))
        if l_bytes == 0:
            return False
        if g_debug > 5:
            print "Insteon_PLM.receive_loop() - {0:}".format(PrintBytes(l_msg))
        l_ret = DecodeResponses()._decode_message(l_msg, l_bytes)
        return l_ret


class CreateCommands(PlmDriverInterface, InsteonPlmUtility):
    """Send various commands to the PLM.
    """

    def send_60_command(self):
        """Insteon - get IM info (2 bytes).
        See p 273 of developers guide.
        PLM will respond with a 0x60 response.
        """
        g_logger.debug("Send command to get IM info")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_info']
        return self.queue_plm_command(l_command)

    def send_61_command(self, p_obj):
        """Send ALL-Link Command (5 bytes)
        See p 254 of developers guide.
        """
        pass

    def send_62_command(self, p_light_obj, p_cmd1, p_cmd2):
        """Send Insteon Standard Length Message (8 bytes).
        See page 243 of Insteon Developers Guide.

        @param p_light_obj: is the Light object of the device
        @param p_cmd1: is the first command byte
        @param p_cmd2: is the second command byte
        @return: the response from queue_plm_command
        """
        if g_debug > 1:
            print "Insteon_PLM.send_62_command() ", p_light_obj, p_cmd1, p_cmd2
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
        g_logger.debug("Send 62 command to device: {2:}, Command: {0:#X},{1:#X}, Address: ({3:x}.{4:x}.{5:x})".format(p_cmd1, p_cmd2, p_light_obj.Name, l_command[2], l_command[3], l_command[4]))
        return self.queue_plm_command(l_command)

    def send_63_command(self, p_obj):
        """
        """
        pass

    def send_64_command(self, p_obj):
        """
        """
        pass

    def send_65_command(self, p_obj):
        """
        """
        pass

    def send_66_command(self, p_obj):
        """
        """
        pass

    def send_67_command(self, p_obj):
        """
        """
        pass

    def send_68_command(self, p_obj):
        """
        """
        pass

    def send_69_command(self):
        """Get the first all-link record from the plm (2 bytes).
        See p 261 of developers guide.
        """
        g_logger.debug("Send command to get First all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_first_all_link']
        return self.queue_plm_command(l_command)

    def send_6A_command(self):
        """Get the next record - will get a nak if no more (2 bytes).
        See p 262 of developers guide.
        Returns True if more - False if no more.
        """
        g_logger.debug("Send command to get Next all-link record.")
        l_command = bytearray(2)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_next_all_link']
        return self.queue_plm_command(l_command)

    def send_6B_command(self, p_flags):
        """Set IM configuration flags (3 bytes).
        See page 271  of Insteon Developers Guide.
        """
        g_logger.debug("Send command to set PLM config flag to {0:#X}"\
                       .format(p_flags))
        l_command = bytearray(3)
        l_command[0] = STX
        l_command[1] = plm_commands['plm_set_config']
        l_command[2] = p_flags
        return self.queue_plm_command(l_command)

    def send_6C_command(self, p_obj):
        """
        """
        pass

    def send_6D_command(self, p_obj):
        """
        """
        pass

    def send_6E_command(self, p_obj):
        """
        """
        pass

    def send_6F_command(self, p_obj):
        """Manage All-Link Record (11 bytes)
        """
        pass

    def send_70_command(self, p_obj):
        """
        """
        pass

    def send_71_command(self, p_obj):
        """
        """
        pass

    def send_72_command(self, p_obj):
        """RF Sleep
        """
        pass

    def send_73_command(self, p_light_obj):
        """Send request for PLM configuration (2 bytes).
        See page 270 of Insteon Developers Guide.
        """
        g_logger.debug("Send command to get PLM config.")
        l_command = bytearray(8)
        l_command[0] = STX
        l_command[1] = p_light_obj.Command = plm_commands['plm_get_config']
        return self.queue_plm_command(l_command)


class LightingAPI(Device_Insteon.LightingAPI, CreateCommands):

    def change_light_setting(self, p_obj, p_level):
        if g_debug > 0:
            print "Insteon_PLM.change_light_settings()  {0:} to {1:}".format(p_obj.Name, p_level)
        if int(p_level) == 0:
            self.send_62_command(p_obj, message_types['off'], 0)
        elif int(p_level) == 100:
            self.send_62_command(p_obj, message_types['on'], 255)
        else:
            l_level = int(p_level) * 255 / 100
            self.send_62_command(p_obj, message_types['on'], l_level)

    def scan_all_lights(self, p_lights):
        """Exported command - used by other modules.
        """
        if g_debug > 0:
            print "insteon_PLM.scan_all_lights"
        for l_obj in p_lights.itervalues():
            if Device_Insteon.LightData.get_family(l_obj) != 'Insteon':
                continue
            if l_obj.get_Type == 'Light':
                self.scan_one_light(l_obj.Name)
                pass

    def update_all_devices(self):
        Device_Insteon.LightingAPI().update_all_devices()


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
        self.send_62_command(p_name, message_types['product_data_request'], 0x00)

    def update_object(self, p_obj):
        pass


class InsteonAllLinks(InsteonPlmCommands):

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

    m_obj = None

    def _get_obj_using_addr(self, p_addr):
        """
        @param p_addr: String 'aa.bb.cc' is the address
        @return: the entire Lighting Device object
        """
        if g_debug > 4:
            print "Insteon_PLM._get_obj_using_addr()", p_addr
        for l_obj in g_house_obj.Lights.itervalues():
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.Address == p_addr:
                return l_obj
        for l_obj in g_house_obj.Controllers.itervalues():
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.Address == p_addr:
                return l_obj
        for l_obj in g_house_obj.Buttons.itervalues():
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.Address == p_addr:
                return l_obj
        print "Insteon_PLM._get_obj_using_addr() No object has string {0:} for an Address.".format(p_addr)
        return Device_Insteon.LightData()  # an empty new object

    def _decode_message(self, p_message, p_length):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        if g_debug > 2:
            print "== Decoding Message - Len: {0:}, {1:}".format(p_length, PrintBytes(p_message))
        l_ret = False
        if p_length < 1:
            return l_ret
        l_stx = p_message[0]
        # If we have a leading NAK, drop it and try again if we have more message
        if l_stx == 0x15:
            if g_debug > 7:
                print "== Found a leading NAK - Retrying. - {0:}".format(PrintBytes(p_message))
            # g_logger.warning("Found a NAK - Retrying. {0:} - {1:}".format(p_length, PrintBytes(p_message)))
            p_message = p_message[1:]
            p_length -= 1
            self._decode_message(p_message, p_length)
        # If we have a leading ACK, drop it and try again if we have more message
        elif l_stx == 0x06:
            if g_debug > 7:
                print "== Found a leading ACK - Ignoring - {0:}".format(PrintBytes(p_message))
            p_message = p_message[1:]
            p_length -= 1
            self._decode_message(p_message, p_length)
        elif l_stx == 0x02:
            if g_debug > 7:
                print "== Found a message - {0:}".format(PrintBytes(p_message))
            l_ret = self._decode_dispatch(p_message, p_length)
            return l_ret
        else:
            if g_debug > 7:
                print "== Found a mistake - {0:}".format(PrintBytes(p_message))
            g_logger.error("Message started with {0:#x} not STX, Message={1:}"\
                           .format(l_stx, PrintBytes(p_message)))
            return l_ret

    def _decode_dispatch(self, p_message, p_length = 1):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_ret = False
        l_cmd = p_message[1]
        if l_cmd == 0:
            g_logger.warning("Found a '0' record ->{0:}.".format(PrintBytes(p_message)))
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
        elif l_cmd == 0x62: l_ret = self._decode_62_record(p_message, p_length)  # print "   insteon_PLM._decode got msg type 62"
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
            g_logger.error("Unknown message >>".format(PrintBytes(p_message)))
        return l_ret

    def _get_devcat(self, p_message, p_light_obj):
        l_devcat = p_message[5] * 256 + p_message[6]
        p_light_obj.DevCat = int(l_devcat)
        self.update_object(p_light_obj)
        if g_debug > 1:
            print "Insteon_PLM._decode_50_record() - Got devcat type  From={0:}, DevCat={1:#x}, flags={2:}".format(
                            p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        g_logger.info("Got DevCat from light:{0:}, DevCat:{1:}".format(p_light_obj.Name, l_devcat))
        pass

    def _decode_50_record(self, p_message, p_length):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.

        See p 246 of developers guide.
        """
        l_obj_from = self._get_obj_using_addr(self._get_addr_from_message(p_message, 2))
        l_name_from = l_obj_from.Name
        l_flags = self._decode_message_flag(p_message[8])
        l_obj_to = self._get_obj_using_addr(self._get_addr_from_message(p_message, 5))
        l_name_to = l_obj_to.Name
        l_data = [p_message[9], p_message[10]]
        g_logger.debug("PLM got 50 message - From={0:}, To={1:}, Flags={2:}, Data={3:}".format(l_name_from, l_name_to, l_flags, l_data))
        # Break down bits 7, 6, 5 into message type
        if p_message[8] & 0xE0 == 0x00:  # (000) Direct message type
            pass
        elif p_message[8] & 0xE0 == 0x20:  # (001) ACK of Direct message type
            pass
        elif p_message[8] & 0xE0 == 0x40:  # (010) All-Link Broadcast Clean-Up message type
            pass
        elif p_message[8] & 0xE0 == 0x60:  # (011) All-Link Clean-Up ACK response message type
            pass
        elif p_message[8] & 0xE0 == 0x80:  # Broadcast Message (100)
            self._get_devcat(p_message, l_obj_from)
        elif p_message[8] & 0xE0 == 0xA0:  # (101) NAK of Direct message type
            pass
        elif p_message[8] & 0xE0 == 0xC0:  # (110) all link broadcast of group is
            l_group = p_message[7]
            if g_debug > 1:
                print "Got all-link broadcast  From={0:}, Group={1:}, Flags={2:}, Data={3:} ".format(l_name_from, l_group, l_flags, l_data)
            g_logger.info("== 50B All-link Broadcast From={0:}, Group={1:}, Flags={2:}, Data={3:} ==".format(l_name_from, l_group, l_flags, l_data))
        elif p_message[8] & 0xE0 == 0xE0:  # (111) NAK of Direct message type
            pass
        #
        if l_obj_from.Command1 == message_types['product_data_request']:  # 0x03
            if g_debug > 1:
                print "Got product data request. - Should never happen - S/B 51 response"
        elif l_obj_from.Command1 == message_types['engine_version']:  # 0x0D
            l_engine_id = p_message[10]
            if g_debug > 1:
                print "Got Engine version from: {0:}, Sent to: {1:}, Id: {2:}".format(l_name_from, l_name_to, l_engine_id)
            g_logger.info("Got engine version from light: {0:}, To={1:}, EngineID={2:}".format(l_name_from, l_name_to, l_engine_id))
        elif l_obj_from.Command1 == message_types['id_request']:  # 0x10
            if g_debug > 1:
                print " --- Got Request ID From={0:}".format(l_name_from,)
            g_logger.info("Got an ID request. Light: {0:}".format(l_name_from,))
        elif l_obj_from.Command1 == message_types['on']:  # 0x11
            l_obj_from.CurLevel = 100
            self.update_object(l_obj_from)
        elif l_obj_from.Command1 == message_types['off']:  # 0x13
            l_obj_from.CurLevel = 0
            self.update_object(l_obj_from)
        #
        elif l_obj_from.Command1 == message_types['status_request']:  # 0x19
            l_level = int(((p_message[10] + 2) * 100) / 256)
            if g_debug > 1:
                print "Got status of light: {0:} - at level {1:}".format(l_name_from, l_level)
            g_logger.info("Got Light Status from: {0:}, Level is: {1:}".format(l_name_from, l_level))
            l_obj_from.CurLevel = l_level
            self.update_object(l_obj_from)
        #
        else:
            print "Insteon_PLM._decode_50_record() unknown type - last command was {0:#x} - {1:}".format(l_obj_from.Command1, PrintBytes(p_message))
        l_ret = True
        if p_length > 11:
            l_msg = p_message[11:]
            l_ret = self._decode_message(l_msg, p_length - 11)
        return l_ret

    def _decode_51_record(self, p_message, p_length):
        """ Insteon Extended Message Received (25 bytes).
        See p 247 of developers guide.
        """
        l_id_from = self._get_addr_from_message(p_message, 2)
        l_obj_from = self._get_obj_using_addr(l_id_from)
        l_id_to = self._get_addr_from_message(p_message, 5)
        l_obj_to = self._get_obj_using_addr(l_id_to)
        l_flags = p_message[8]
        l_data = [p_message[9], p_message[10]]
        l_extended = "{0:X}.{1:X}.{2:X}.{3:X}.{4:X}.{5:X}.{6:X}.{7:X}.{8:X}.{9:X}.{10:X}.{11:X}.{12:X}.{13:X}".format(
                    p_message[11], p_message[12], p_message[13], p_message[14], p_message[15], p_message[16], p_message[17],
                    p_message[18], p_message[19], p_message[20], p_message[21], p_message[22], p_message[23], p_message[24])
        l_product_key = self._get_addr_from_message(p_message, 12)
        l_devcat = p_message[15] * 256 + p_message[16]
        self.update_object(l_obj_from)
        print " --- Got Product Data response from={0:}, ".format(l_obj_from.Name), l_extended
        g_logger.info("== 51 From={0:}, To={1:}, Flags={2:#x}, Data={3:} Extended={4:} ==".format(l_obj_from.Name, l_obj_to.Name, l_flags, l_data, l_extended))
        l_obj_from.ProductKey = l_product_key
        l_obj_from.DevCat = l_devcat
        l_ret = True
        if p_length > 25:
            l_msg = p_message[25:]
            l_ret = self._decode_message(l_msg, p_length - 25)
        return l_ret

    def _decode_52_record(self, p_message, p_length):
        """Insteon X-10 message received (4 bytes).
        See p 253 of developers guide.
        """
        g_logger.warning("== 52 message not decoded yet.")
        l_ret = False
        if p_length > 4:
            l_msg = p_message[4:]
            l_ret = self._decode_message(l_msg, p_length - 4)
        return l_ret

    def _decode_53_record(self, p_message, p_length):
        """Insteon All-Linking completed (10 bytes).
        See p 260 of developers guide.
        """
        g_logger.warning("== 53 message not decoded yet.")
        l_ret = False
        if p_length > 10:
            l_msg = p_message[10:]
            l_ret = self._decode_message(l_msg, p_length - 10)
        return l_ret

    def _decode_54_record(self, p_message, p_length):
        """Insteon Button Press event (3 bytes).
        See p 276 of developers guide.
        """
        g_logger.warning("== 54 message not decoded yet.")
        l_ret = False
        if p_length > 3:
            l_msg = p_message[3:]
            l_ret = self._decode_message(l_msg, p_length - 3)
        return l_ret

    def _decode_55_record(self, p_message, p_length):
        """Insteon User Reset detected (2 bytes).
        See p 269 of developers guide.
        """
        g_logger.warning("== 55 message not decoded yet.")
        l_ret = False
        if p_length > 2:
            l_msg = p_message[2:]
            l_ret = self._decode_message(l_msg, p_length - 2)
        return l_ret

    def _decode_56_record(self, p_message, p_length):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 256 of developers guide.
        """
        g_logger.warning("== 56 message not decoded yet.")
        l_ret = False
        if p_length > 7:
            l_msg = p_message[7:]
            l_ret = self._decode_message(l_msg, p_length - 7)
        return l_ret

    def _decode_57_record(self, p_message, p_length):
        """Insteon All-Link Record Response (10 bytes).
        See p 264 of developers guide.
        """
        l_flags = p_message[2]
        # l_flag_control = l_flags & 0x40
        l_group = p_message[3]
        l_id = self._get_addr_from_message(p_message, 4)
        l_data = [p_message[7], p_message[8], p_message[9]]
        l_obj = self._get_obj_using_addr(l_id)
        g_logger.info("== 57 All-Link response Name={0:}, Flags={1:#x}, Group={2:#x}, Data={3:} ".format(l_obj.Name, l_flags, l_group, l_data))
        l_ret = True
        if p_length > 10:
            l_msg = p_message[10:]
            l_ret = self._decode_message(l_msg, p_length - 10)
        return l_ret

    def _decode_58_record(self, p_message, p_length):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 257 of developers guide.
        """
        g_logger.warning("== 58 message not decoded yet.")
        l_ret = False
        if p_length > 3:
            l_msg = p_message[3:]
            l_ret = self._decode_message(l_msg, p_length - 3)
        return l_ret

    def _decode_60_record(self, p_message, p_length):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_id = self._get_addr_from_message(p_message, 2)
        l_devcat = p_message[5]
        l_devsubcat = p_message[6]
        l_firmver = p_message[7]
        l_obj = self._get_obj_using_addr(l_id)
        g_logger.info("== 60 - Insteon Modem Info - DevCat={0:}, DevSubCat={1:}, Firmware={2:} - Name={3:}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if p_message[8] == ACK:
            l_ret = True
        else:
            g_logger.error("== 60 - No ACK - Got {0:#x}".format(p_message[8]))
            l_ret = False
        if p_length > 9:
            l_msg = p_message[9:]
            l_ret = self._decode_message(l_msg, p_length - 9)
        return l_ret

    def _decode_62_record(self, p_message, p_length):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 243 of developers guide.

        This is an ack of the command.
        It seems that a 50 response MAY immediately follow this response with any data requested.
        """
        l_id = self._get_addr_from_message(p_message, 2)
        l_msgflags = self._decode_message_flag(p_message[5])
        # self.m_last_command = p_message[6]  # save for following 50 record
        l_ack = self._get_ack_nak(p_message[8])
        l_obj = self._get_obj_using_addr(l_id)
        if g_debug > 7:
            print "62 - Device: {0:}, {1:} - {2:}".format(l_obj.Name, l_ack, PrintBytes(p_message))
        g_logger.debug("Got Ack/Nak from light: {0:}, Acked: {1:}, and got flags {2:}".format(l_obj.Name, l_ack, l_msgflags))
        return self._check_for_more_decoding(p_message, p_length, 9)

    def _decode_69_record(self, p_message, p_length):
        """Get first All-Link record (3 bytes).
        See p 261 of developers guide.
        """
        if p_message[2] == ACK:
            g_logger.info("== 69 - ACK")
            l_ret = True
        else:
            g_logger.info("== 69 - NAK")
            l_ret = False
        return self._check_for_more_decoding(p_message, p_length, 3, l_ret)

    def _decode_6A_record(self, p_message, p_length):
        """Get next All-Link (3 bytes).
        See p 262 of developers guide.
        """
        if p_message[2] == ACK:
            g_logger.info("== 6A - ACK")
            l_ret = True
        else:
            g_logger.info("== 6A - NAK")
            l_ret = False
        return self._check_for_more_decoding(p_message, p_length, 3, l_ret)

    def _decode_6B_record(self, p_message, p_length):
        """Get set IM configuration (4 bytes).
        See p 271 of developers guide.
        """
        g_logger.info("Received configuration flag from PLM: {0:#x}".format(p_message[2]))
        if p_message[3] == ACK:
            l_ret = True
        else:
            g_logger.error("== 6B - NAK/Unknown message type {0:#x}".format(p_message[2]))
            l_ret = False
        return self._check_for_more_decoding(p_message, p_length, 4, l_ret)

    def _decode_73_record(self, p_message, p_length):
        """Get the PLM response of 'get config' (6 bytes).
        See p 270 of developers guide.
        """
        l_flags = p_message[2]
        l_spare1 = p_message[3]
        l_spare2 = p_message[4]
        l_ack = self._get_ack_nak(p_message[5])
        g_logger.info("== 73 Get IM configuration Flags={0#x:}, Spare 1={1:#x}, Spare 2={2:#x} {3:} ".format(l_flags, l_spare1, l_spare2, l_ack))
        return self._check_for_more_decoding(p_message, p_length, 6)

    def _check_for_more_decoding(self, p_message, p_length, p_chop, p_ret = True):
        """
        @param p_message: is the possibly compound message.
        @param p_length: is the current length of the message.
        @param p_chop: is the number of characters to chop off the beginning of the message.
        @param p_ret: is the result to return.
        """
        l_ret = p_ret
        if p_length > p_chop:
            l_msg = p_message[p_chop:]
            l_ret = self._decode_message(l_msg, p_length - p_chop)
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
        self.send_62_command(p_obj.Name, message_types['engine_version'], 0)  # 0x0D

    def get_id_request(self, p_obj):
        """Get the device DevCat
        """
        g_logger.debug('Request Insteon ID(devCat) from device: {0:}'.format(p_obj.Name))
        self.send_62_command(p_obj.Name, message_types['id_request'], 0)  # 0x10

    def ping_plm(self):
        """Send a command to the plm and get its response.
        """
        return self.send_60_command()


class LightHandlerAPI(InsteonPlmAPI):
    """This is the API for light control.
    """

    def start_all_controllers(self, p_house_obj):
        l_count = 0
        if g_debug > 0:
            print "Insteon_PLM.start_all_controllers() ", p_house_obj
        for l_key, l_controller_obj in p_house_obj.Controllers.iteritems():
            if g_debug > 4:
                print "Insteon_PLM.start_all_controllers() - Iterating for ", l_controller_obj.Name
            if l_controller_obj.Active != True:
                continue
            if l_controller_obj.Family != 'Insteon':
                continue
            if g_debug > 1:
                print "Insteon_PLM.start_all_controllers() - Family:{0:}, Interface:{1:}, Active:{2:}".format(l_controller_obj.Family, l_controller_obj.Interface, l_controller_obj.Active)
            if l_controller_obj.Interface.lower() == 'serial':
                from drivers import Driver_Serial
                l_driver = Driver_Serial.API()
            elif l_controller_obj.Interface.lower() == 'ethernet':
                from drivers import Driver_Ethernet
                l_driver = Driver_Ethernet.API()
            elif l_controller_obj.Interface.lower() == 'usb':
                from drivers import Driver_USB_0403_6001
                l_driver = Driver_USB_0403_6001.API()
            p_house_obj.Controllers[l_key].Driver = l_driver
            l_driver.Start(l_controller_obj)
            if g_debug > 2:
                print "Insteon_PLM has just started a driver.  Name: {0:}".format(l_controller_obj.Name)
            l_count += 1
        if g_debug > 1:
            print "Insteon_PLM.start_all_controllers() has completed.  Found {0:} active controllers, configured and initialized {1:} of them.".format(l_count, len(g_driver))

    def stop_all_controllers(self, p_house_obj):
        if g_debug > 0:
            print "Insteon_PLM.stop_all_controllers()"
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            if g_debug > 1:
                print "Insteon_PLM.stop_all_controllers() - Driver:{0:}".format(l_controller_obj.Name)
            if l_controller_obj.Driver != None:
                l_controller_obj.Driver.Stop()

    def set_plm_mode(self):
        """Set the PLM to a mode
        """
        if g_debug > 5:
            print "Insteon_PLM.set_plm_mode() - Sending mode command to Insteon PLM"
        self.send_6B_command(MODE_MONITOR)

    def get_all_lights_status(self):
        """Get the status (current level) of all lights.
        """
        if g_debug > 1:
            print "Insteon_PLM.get_all_lights_status() ", self.m_obj
        g_logger.info('Getting light levels of all Insteon lights')
        for l_obj in self.m_obj.Lights.itervalues():
            if g_debug > 2:
                print "Insteon_PLM.get_all_lights_status() ", l_obj
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.Active != True:
                continue
            self._get_one_light_status(l_obj)

    def _get_one_light_status(self, p_obj):
        """Get the status of a light.

        We will (apparently) get back a 62-ACK followed by a 50 with the level in the response.

        @return: the light current level (0-100%)
        """
        if g_debug > 3:
            print "Insteon_PLM._get_one_light_status() {0:}".format(p_obj.Name)
        self.send_62_command(p_obj, message_types['status_request'], 0)  # 0x19


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
        if g_debug > 0:
            print "Insteon_PLM.__init__()"
        global g_logger, g_driver, g_queue
        g_logger = logging.getLogger('PyHouse.Insteon_PLM')
        g_logger.info('Initializing.')
        g_driver = []
        g_queue = Queue.Queue(300)
        g_logger.info('Initialized.')

    def Start(self, p_house_obj):
        if g_debug > 0:
            print "Insteon_PLM.Start()"
        g_logger.info('Starting.')
        self.m_obj = p_house_obj
        global g_house_obj
        g_house_obj = p_house_obj
        self.start_all_controllers(p_house_obj)
        self.driver_loop_start(p_house_obj)
        self.set_plm_mode()
        self.get_all_lights_status()
        g_logger.info('Started.')
        if g_debug > 1:
            print "Insteon_PLM.Start() has completed."

    def Stop(self):
        if g_debug > 0:
            print "Insteon_PLM.Stop()"
        g_logger.info('Stopping.')
        self.driver_loop_stop()
        self.stop_all_controllers(g_house_obj)
        g_logger.info('Stopped.')

# ## END
