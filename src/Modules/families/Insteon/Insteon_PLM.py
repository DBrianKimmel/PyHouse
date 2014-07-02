"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Insteon_PLM -*-

@name: PyHouse/src/Modules/families/Insteon/Insteon_PLM.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Feb 18, 2010
@license: MIT License
@summary: This module is for driving serial devices




Insteon PLM module.

Create commands and interpret results from any Insteon controller regardless of interface.

TODO: Work toward getting one instance per controller.
        We will then need to assign lights to a particular controller if there is more than one in a house.

This module carries state information about the controller.
This is necessary since the responses may follow a command at any interval.
Responses do not all have to follow the command that caused them.


TODO: implement all-links

"""

# Import system type stuff
import Queue
from twisted.internet import reactor

# Import PyMh files
# from Modules.lights.lighting import LightData
from Modules.utils.tools import PrintBytes
from Modules.families.Insteon.Insteon_constants import *
from Modules.families.Insteon import Insteon_utils
from Modules.families.Insteon import Insteon_Link
from Modules.families.Insteon.Device_Insteon import InsteonData
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Insteon_PLM ')

callLater = reactor.callLater

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


class ControllerData(InsteonData):
    """Holds statefull information about a single Insteon controller device.

    There are several different control devices - this is 2412x and 2413x
    where x is 'S' for serial interface and 'U' for a USB interface.

    The USB controller that I have actually uses the Serial protocol so the serial driver
    is used.

    Although there is a manual for Insteon controllers, much of the development was
    empirically derived.  For this reason, there is a whole lot of debugging code and
    output.
    """

    def __init__(self):
        super(ControllerData, self).__init__()
        self._Command1 = 0
        self._Command2 = 0


class InsteonPlmUtility(ControllerData):

    def _get_message_length(self, p_message):
        """Get the documented length that the message is supposed to be.

        Use the message type byte to find out how long the response from the PLM
        is supposed to be.
        With asynchronous routines, we want to wait till the entire message is
        received before proceeding with its decoding.
        """
        l_id = p_message[1]
        try:
            l_message_length = MESSAGE_LENGTH[l_id]
        except KeyError:
            l_message_length = 1
        return l_message_length

    def _extract_bytes_from_message(self, p_message, p_offset, p_length):
        l_ret = p_message[p_offset:p_offset + p_length - 1]
        return l_ret

    def _get_addr_from_message(self, p_message, p_index):
        """Extract the address from a message.

        The message is a byte array returned from the PLM.
        The address is 3 consecutive bytes starting at p_index.
        Return a string 'A1.B2.C3' (upper case) that is the address.
        """
        l_id = Insteon_utils.message2int(p_message, p_index)
        return l_id

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


class CreateCommands(InsteonPlmUtility):
    """Send various commands to the PLM.
    """

    def queue_plm_command(self, p_command):
        self.m_controller_obj._Queue.put(p_command)
        if g_debug >= 1:
            LOG.debug("Insteon_PLM.queue_plm_command() - Q-Size:{0:}, Command:{1:}".format(self.m_controller_obj._Queue.qsize(), PrintBytes(p_command)))

    def _queue_command(self, p_command):
        l_cmd = PLM_COMMANDS[p_command]
        l_command_bytes = bytearray(COMMAND_LENGTH[l_cmd])
        l_command_bytes[0] = STX
        l_command_bytes[1] = l_cmd
        return l_command_bytes

    def queue_60_command(self):
        """Insteon - get IM info (2 bytes).
        See p 273 of developers guide.
        PLM will respond with a 0x60 response.
        """
        l_command = self._queue_command('plm_info')
        if g_debug >= 1:
            LOG.debug("Queue command to get IM info")
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
        l_command = self._queue_command('insteon_send')
        Insteon_utils.int2message(p_light_obj.InsteonAddress, l_command, 2)
        l_command[5] = FLAG_MAX_HOPS + FLAG_HOPS_LEFT  # 0x0F
        l_command[6] = p_light_obj._Command1 = p_cmd1
        l_command[7] = p_light_obj._Command2 = p_cmd2
        if g_debug >= 1:
            LOG.debug("Queue62 command to device: {2:}, Command: {0:#X},{1:#X}, Address: ({3:x}.{4:x}.{5:x})".format(p_cmd1, p_cmd2, p_light_obj.Name, l_command[2], l_command[3], l_command[4]))
        return self.queue_plm_command(l_command)

    def queue_63_command(self, p_obj):
        pass

    def queue_64_command(self, p_obj):
        pass

    def queue_65_command(self, p_obj):
        pass

    def queue_66_command(self, p_obj):
        pass

    def queue_67_command(self):
        """Reset the PLM
        See p 268 of developers guide.
        """
        if g_debug >= 1:
            LOG.debug("Queue command to reset the PLM.")
        l_command = self._queue_command('plm_reset')
        return self.queue_plm_command(l_command)

    def queue_68_command(self, p_obj):
        pass

    def queue_69_command(self):
        """Get the first all-link record from the plm (2 bytes).
        See p 261 of developers guide.
        """
        if g_debug >= 1:
            LOG.debug("Queue command to get First all-link record.")
        l_command = self._queue_command('plm_first_all_link')
        return self.queue_plm_command(l_command)

    def queue_6A_command(self):
        """Get the next record - will get a nak if no more (2 bytes).
        See p 262 of developers guide.
        Returns True if more - False if no more.
        """
        if g_debug >= 1:
            LOG.debug("Queue command to get Next all-link record.")
        l_command = self._queue_command('plm_next_all_link')
        return self.queue_plm_command(l_command)

    def queue_6B_command(self, p_flags):
        """Set IM configuration flags (3 bytes).
        See page 271  of Insteon Developers Guide.
        """
        if g_debug >= 1:
            LOG.debug("Queue command to set PLM config flag to {0:#X}".format(p_flags))
        l_command = self._queue_command('plm_set_config')
        l_command[2] = p_flags
        return self.queue_plm_command(l_command)

    def queue_6C_command(self, p_obj):
        pass

    def queue_6D_command(self, p_obj):
        pass

    def queue_6E_command(self, p_obj):
        pass

    def queue_6F_command(self, p_light_obj, p_code, p_flag, p_data):
        """Manage All-Link Record (11 bytes)
        """
        if g_debug >= 1:
            LOG.debug("Queue command to manage all-link record")
        l_command = self._queue_command('manage_all_link_record')
        l_command[2] = p_code
        l_command[3] = p_flag
        l_command[4] = p_light_obj.GroupNumber
        Insteon_utils.int2message(p_light_obj.InsteonAddress, l_command, 5)
        l_command[8:11] = p_data
        return self.queue_plm_command(l_command)

    def queue_70_command(self, p_obj):
        pass

    def queue_71_command(self, p_obj):
        pass

    def queue_72_command(self, p_obj):
        """RF Sleep
        """
        pass

    def queue_73_command(self, _p_obj):
        """Send request for PLM configuration (2 bytes).
        See page 270 of Insteon Developers Guide.
        """
        if g_debug >= 1:
            LOG.debug("Queue command to get PLM config.")
        l_command = self._queue_command('plm_get_config')
        return self.queue_plm_command(l_command)


class DecodeResponses(CreateCommands):

    m_house_obj = None
    m_pyhouse_obj = None

    def _find_addr(self, p_class, p_addr):
        """
        Find the address of something Insteon.
        @param p_class: is an OBJ like p_pyhouse_obj.House.OBJs.Controllers
        """
        # print(p_class)
        for l_obj in p_class.itervalues():
            PrettyPrintAny(l_obj, 'InsteonPLM - _findAddr - obj', 100)
            if l_obj.ControllerFamily == 'Insteon':
                continue
            if l_obj.InsteonAddress == p_addr:
                return l_obj
        # LOG.warning("Address {0:} NOT found".format(Insteon_utils.int2dotted_hex(p_addr)))
        return None

    def get_obj_from_message(self, p_message, p_index):
        """Here we have a message from the PLM.  Find out what device has that address.

        @param p_message: is the message from the plm we are extracting the Insteon address from.
        @param p_index: is the index of the first byte in the message.
                Various messages contain the address at different offsets.

        We need to check:
            Lighting devices
            Thermostat devices
            Add other devices if we add them.
        """
        l_id = Insteon_utils.message2int(p_message, p_index)  # Extract the 3 byte address from the message and convert to an Int.
        l_ret = self._find_addr(self.m_house_obj.Lights, l_id)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Controllers, l_id)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Buttons, l_id)
        if l_ret == None:
            l_ret = self._find_addr(self.m_pyhouse_obj.House.OBJs.Thermostat, l_id)
        if l_ret == None:
            LOG.warning("Address {0:} NOT found".format(Insteon_utils.int2dotted_hex(l_id)))
            l_ret = InsteonData()  # an empty new object
            l_ret.Name = '**' + str(l_id) + '**'
        if g_debug >= 2:
            LOG.debug("Insteon_PLM.get_obj_from_message - Address:{0:}({1:}), found:{2:}".format(Insteon_utils.int2dotted_hex(l_id), l_id, l_ret.Name))
        return l_ret

    def _drop_first_byte(self, p_controller_obj):
        """The first byte is not legal, drop it and try again.
        """
        l_msg = "Insteon_PLM._drop_first_byte() Found a leading char {0:#x} - Rest. - {1:}".format(
                p_controller_obj._Message[0], PrintBytes(p_controller_obj._Message))
        if p_controller_obj._Message[0] != NAK:
            LOG.error(l_msg)
        try:
            p_controller_obj._Message = p_controller_obj._Message[1:]
        except IndexError:
            pass

    def _decode_message(self, p_controller_obj, p_house_obj):
        """Decode a message that was ACKed / NAked.
        see Insteon Developers Manual pages 238-241

        Since a controller response may contain multiple messages and the last message may not be complete.
        This should be invoked every time we pick up more messages from the controller.
        It should loop and decode each message present and leave when done


        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        self.m_house_obj = p_house_obj
        while len(p_controller_obj._Message) >= 2:
            l_stx = p_controller_obj._Message[0]
            LOG.debug("decode_message() - {0:}".format(PrintBytes(p_controller_obj._Message)))
            if l_stx == STX:
                l_need_len = self._get_message_length(p_controller_obj._Message)
                l_cur_len = len(p_controller_obj._Message)
                if l_cur_len >= l_need_len:
                    self._decode_dispatch(p_controller_obj)
                else:
                    return
            else:
                self._drop_first_byte(p_controller_obj)

    def _decode_dispatch(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_message = p_controller_obj._Message
        l_ret = False
        l_cmd = p_controller_obj._Message[1]
        if l_cmd == 0:
            LOG.warning("Found a '0' record ->{0:}.".format(PrintBytes(l_message)))
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
        elif l_cmd == 0x64: l_ret = self._decode_64_record(p_controller_obj)
        elif l_cmd == 0x69: l_ret = self._decode_69_record(p_controller_obj)
        elif l_cmd == 0x6A: l_ret = self._decode_6A_record(p_controller_obj)
        elif l_cmd == 0x6B: l_ret = self._decode_6B_record(p_controller_obj)
        elif l_cmd == 0x6F: l_ret = self._decode_6F_record(p_controller_obj)
        elif l_cmd == 0x73: l_ret = self._decode_73_record(p_controller_obj)
        else:
            LOG.error("Unknown message {0:}, Cmd:{1:}".format(PrintBytes(p_controller_obj._Message), l_cmd))
            self.check_for_more_decoding(p_controller_obj, l_ret)
        return l_ret

    def _get_devcat(self, p_message, p_light_obj):
        l_devcat = p_message[5] * 256 + p_message[6]
        p_light_obj.DevCat = int(l_devcat)
        self.update_object(p_light_obj)
        l_debug_msg = "DevCat From={0:}, DevCat={1:#x}, flags={2:}".format(p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        LOG.info("Got DevCat from light:{0:}, DevCat:{1:}".format(p_light_obj.Name, l_devcat))
        return l_debug_msg

    def _decode_50_record(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.

        See p 246 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj_from = self.get_obj_from_message(l_message, 2)
        l_name_from = l_obj_from.Name
        l_obj_to = self.get_obj_from_message(l_message, 5)
        l_name_to = l_obj_to.Name
        try:
            l_7 = l_message[7]
        except IndexError:
            l_7 = 0
        try:
            l_8 = l_message[8]
        except IndexError:
            l_8 = 0
        try:
            l_9 = l_message[9]
        except IndexError:
            l_9 = 0
        try:
            l_10 = l_message[10]
        except IndexError:
            l_10 = 0
            LOG.warning("Short 50 message rxed - {0:}".format(PrintBytes(l_message)))
        l_data = [l_9, l_10]
        l_debug_msg = 'Standard Message; '
        l_flags = self._decode_message_flag(l_8)
        # Break down bits 7, 6, 5 into message type
        if l_8 & 0xE0 == 0x00:  # (000) Direct message type
            l_debug_msg += "DirectMessage from {0:}; ".format(l_name_from)
        elif l_8 & 0xE0 == 0x20:  # (001) ACK of Direct message type
            l_debug_msg += "AckDirectMessage from {0:}; ".format(l_name_from)
        elif l_8 & 0xE0 == 0x40:  # (010) All-Link Broadcast Clean-Up message type
            l_debug_msg += "All-Link Broadcast clean up from {0:}; ".format(l_name_from)
        elif l_8 & 0xE0 == 0x60:  # (011) All-Link Clean-Up ACK response message type
            l_debug_msg += "All-Link Clean up ACK from {0:}; ".format(l_name_from)
        elif l_8 & 0xE0 == 0x80:  # Broadcast Message (100)
            l_debug_msg += self._get_devcat(l_message, l_obj_from)
        elif l_8 & 0xE0 == 0xA0:  # (101) NAK of Direct message type
            l_debug_msg += "NAK of direct message(1) from {0:}; ".format(l_name_from)
        elif l_8 & 0xE0 == 0xC0:  # (110) all link broadcast of group is
            l_group = l_7
            l_debug_msg += "All-Link broadcast From:{0:}, Group:{1:}, Flags:{2:}, Data:{3:}; ".format(l_name_from, l_group, l_flags, l_data)
            LOG.info("== 50B All-link Broadcast From:{0:}, Group:{1:}, Flags:{2:}, Data:{3:} ==".format(l_name_from, l_group, l_flags, l_data))
        elif l_8 & 0xE0 == 0xE0:  # (111) NAK of Direct message type
            l_debug_msg += "NAK of direct message(2) from {0:}; ".format(l_name_from)
        #
        try:
            if l_obj_from._Command1 == MESSAGE_TYPES['product_data_request']:  # 0x03
                l_debug_msg += " product data request. - Should never happen - S/B 51 response"
            elif l_obj_from._Command1 == MESSAGE_TYPES['engine_version']:  # 0x0D
                l_engine_id = l_10
                l_debug_msg += "Engine version From:{0:}, Sent to:{1:}, Id:{2:}; ".format(l_name_from, l_name_to, l_engine_id)
                LOG.info("Got engine version from light:{0:}, To:{1:}, EngineID:{2:}".format(l_name_from, l_name_to, l_engine_id))
            elif l_obj_from._Command1 == MESSAGE_TYPES['id_request']:  # 0x10
                l_debug_msg += "Request ID From:{0:}; ".format(l_name_from)
                LOG.info("Got an ID request. Light:{0:}".format(l_name_from,))
            elif l_obj_from._Command1 == MESSAGE_TYPES['on']:  # 0x11
                l_obj_from.CurLevel = 100
                l_debug_msg += "Light:{0:} turned Full ON; ".format(l_name_from)
                self.update_object(l_obj_from)
            elif l_obj_from._Command1 == MESSAGE_TYPES['off']:  # 0x13
                l_obj_from.CurLevel = 0
                l_debug_msg += "Light:{0:} turned Full OFF; ".format(l_name_from)
                self.update_object(l_obj_from)
            elif l_obj_from._Command1 == MESSAGE_TYPES['status_request']:  # 0x19
                l_level = int(((l_10 + 2) * 100) / 256)
                l_obj_from.CurLevel = l_level
                l_debug_msg += "Status of light:{0:} is level:{1:}; ".format(l_name_from, l_level)
                LOG.info("PLM:{0:} Got Light Status From:{1:}, Level is:{2:}".format(p_controller_obj.Name, l_name_from, l_level))
                self.update_object(l_obj_from)
            else:
                l_debug_msg += "Insteon_PLM._decode_50_record() unknown type - last command was {0:#x} - {1:}; ".format(l_obj_from._Command1, PrintBytes(l_message))
        except AttributeError:
            pass
        l_ret = True

        if g_debug >= 1:
            LOG.debug(l_debug_msg)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_51_record(self, p_controller_obj):
        """ Insteon Extended Message Received (25 bytes).
        See p 247 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj_from = self.get_obj_from_message(l_message, 2)
        l_obj_to = self.get_obj_from_message(l_message, 5)
        l_flags = l_message[8]
        l_data = [l_message[9], l_message[10]]
        l_extended = "{0:X}.{1:X}.{2:X}.{3:X}.{4:X}.{5:X}.{6:X}.{7:X}.{8:X}.{9:X}.{10:X}.{11:X}.{12:X}.{13:X}".format(
                    l_message[11], l_message[12], l_message[13], l_message[14], l_message[15], l_message[16], l_message[17],
                    l_message[18], l_message[19], l_message[20], l_message[21], l_message[22], l_message[23], l_message[24])
        l_product_key = self._get_addr_from_message(l_message, 12)
        l_devcat = l_message[15] * 256 + l_message[16]
        self.update_object(l_obj_from)
        LOG.info("== 51 From={0:}, To={1:}, Flags={2:#x}, Data={3:} Extended={4:} ==".format(l_obj_from.Name, l_obj_to.Name, l_flags, l_data, l_extended))
        l_obj_from.ProductKey = l_product_key
        l_obj_from.DevCat = l_devcat
        l_ret = True
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_52_record(self, p_controller_obj):
        """Insteon X-10 message received (4 bytes).
        See p 253 of developers guide.
        """
        LOG.warning("== 52 message not decoded yet.")
        l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_53_record(self, p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 260 of developers guide.
        """
        LOG.warning("== 53 Insteon All linking Completed - message not decoded yet.")
        l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_54_record(self, p_controller_obj):
        """Insteon Button Press event (3 bytes).
        See p 276 of developers guide.
        """
        LOG.warning("== 54 Insteon Button Press - message not decoded yet.")
        l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_55_record(self, p_controller_obj):
        """Insteon User Reset detected (2 bytes).
        See p 269 of developers guide.
        """
        l_debug_msg = "User Reset Detected! "
        l_ret = False
        LOG.info("".format(l_debug_msg))
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_56_record(self, p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 256 of developers guide.
        """
        LOG.warning("== 56 message not decoded yet.")
        l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_57_record(self, p_controller_obj):
        """All-Link Record Response (10 bytes).
        See p 264 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj = self.get_obj_from_message(l_message, 4)
        l_link_obj = Insteon_Link.LinkData()
        l_link_obj.Flag = l_flags = l_message[2]
        l_link_obj.Group = l_group = l_message[3]
        l_link_obj.InsteonAddess = l_obj.InsteonAddress
        l_link_obj.Data = l_data = [l_message[7], l_message[8], l_message[9]]
        l_flag_control = l_flags & 0x40
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        LOG.info("All-Link response-57 - Group={0:#02X}, Name={1:}, Flags={2:#x}, Data={3:}, {4:}".format(l_group, l_obj.Name, l_flags, l_data, l_type))
        l_ret = True
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_58_record(self, p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 257 of developers guide.
        """
        LOG.warning("== 58 message not decoded yet.")
        l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_60_record(self, p_controller_obj):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj = self.get_obj_from_message(l_message, 2)
        l_devcat = l_message[5]
        l_devsubcat = l_message[6]
        l_firmver = l_message[7]
        LOG.info("== 60 - Insteon Modem Info - DevCat={0:}, DevSubCat={1:}, Firmware={2:} - Name={3:}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if l_message[8] == ACK:
            l_ret = True
        else:
            LOG.error("== 60 - No ACK - Got {0:#x}".format(l_message[8]))
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_61_record(self, p_controller_obj):
        """Get Insteon Modem Info (6 bytes).
        See p 254 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_cmd2 = l_message[4]
        l_ack = l_message[5]
        LOG.info("All-Link Ack - Group:{0:}, Cmd:{1:}, Bcst:{2:}, Ack:{3:}".format(l_grp, l_cmd1, l_cmd2, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            LOG.error("== 61 - No ACK - Got {0:#x}".format(l_ack))
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_62_record(self, p_controller_obj):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 243 of developers guide.

        This is an ack/nak of the command and generally is not very interesting.
        Another response MAY follow this message with further data.
        """
        l_message = p_controller_obj._Message
        l_obj = self.get_obj_from_message(l_message, 2)
        _l_msgflags = self._decode_message_flag(l_message[5])
        try:
            l_8 = l_message[8]
        except IndexError:
            l_8 = 0
            LOG.warning("Short 62 message rxed - {p:}".format(PrintBytes(l_message)))
        l_ack = self._get_ack_nak(l_8)
        l_debug_msg = "Device:{0:}, {1:}".format(l_obj.Name, l_ack)
        if g_debug >= 1:
            LOG.debug("Got ACK(62) {0:}".format(l_debug_msg))
        return self.check_for_more_decoding(p_controller_obj)

    def _decode_64_record(self, p_controller_obj):
        """Start All-Link ACK response (5 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_ack = l_message[4]
        LOG.info("All-Link Ack - Group:{0:}, Cmd:{1:}, Ack:{2:}".format(l_grp, l_cmd1, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            LOG.error("== 64 - No ACK - Got {0:#x}".format(l_ack))
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_67_record(self, p_controller_obj):
        """Reset IM ACK response (3 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_ack = self._get_ack_nak(l_message[2])
        l_debug_msg = "Reset IM(PLM) {0:}".format(l_ack)
        LOG.info("{0:}".format(l_debug_msg))
        return self.check_for_more_decoding(p_controller_obj)

    def _decode_69_record(self, p_controller_obj):
        """Get first All-Link record response (3 bytes).
        See p 261 of developers guide.
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ret = True
            self.queue_6A_command()
        else:
            LOG.info("All-Link first record - NAK")
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_6A_record(self, p_controller_obj):
        """Get next All-Link (3 bytes).
        See p 262 of developers guide.
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ret = True
            self.queue_6A_command()
        else:
            LOG.info("All-Link Next record - NAK")
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_6B_record(self, p_controller_obj):
        """Get set IM configuration (4 bytes).
        See p 271 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_flag = l_message[2]
        l_ack = self._get_ack_nak(l_message[3])
        l_debug_msg = "from PLM:{0:} - ConfigFlag:{1:#02X}, {2:}".format(p_controller_obj.Name, l_flag, l_ack)
        LOG.info("Received from {0:}".format(l_debug_msg))
        if l_message[3] == ACK:
            l_ret = True
        else:
            LOG.error("== 6B - NAK/Unknown message type {0:#x}".format(l_flag))
            l_ret = False
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_6F_record(self, p_controller_obj):
        """All-Link manage Record Response (12 bytes).
        See p 267 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_code = l_message[2]
        l_flags = l_message[3]
        l_flag_control = l_flags & 0x40
        l_group = l_message[4]
        l_obj = self.get_obj_from_message(l_message, 5)
        l_data = [l_message[8], l_message[9], l_message[10]]
        l_ack = self._get_ack_nak(l_message[11])
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        l_message = "Manage All-Link response(6F)"
        l_message += " Group:{0:#02X}, Name:{1:}, Flags:{2:#02X}, Data:{3:}, CtlCode:{4:#02x},".format(l_group, l_obj.Name, l_flags, l_data, l_code)
        l_message += " Ack:{0:}, Type:{1:}".format(l_ack, l_type)
        LOG.info("{0:}".format(l_message))
        l_ret = True
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_73_record(self, p_controller_obj):
        """Get the PLM response of 'get config' (6 bytes).
        See p 270 of developers guide.
        """
        l_message = p_controller_obj._Message
        try:
            l_5 = l_message[5]
        except IndexError:
            l_5 = 0
            LOG.warning("Short 73 message rxed - {p:}".format(PrintBytes(l_message)))
        l_flags = l_message[2]
        l_spare1 = l_message[3]
        l_spare2 = l_message[4]
        l_ack = self._get_ack_nak(l_5)
        LOG.info("== 73 Get IM configuration Flags={0#x:}, Spare 1={1:#x}, Spare 2={2:#x} {3:} ".format(
                    l_flags, l_spare1, l_spare2, l_ack))
        return self.check_for_more_decoding(p_controller_obj)

    def check_for_more_decoding(self, p_controller_obj, p_ret = True):
        """Chop off the current message from the head of the buffered response stream from the controller.
        @param p_ret: is the result to return.
        """
        l_ret = p_ret
        l_cur_len = len(p_controller_obj._Message)
        l_chop = self._get_message_length(p_controller_obj._Message)
        if l_cur_len >= l_chop:
            p_controller_obj._Message = p_controller_obj._Message[l_chop:]
            l_ret = self._decode_message(p_controller_obj, self.m_house_obj)
        else:
            l_msg = "check_for_more_decoding() trying to chop an incomplete message - {0:}".format(
                    PrintBytes(p_controller_obj._Message))
            LOG.error(l_msg)
        return l_ret

    def update_object(self, p_obj):
        # TODO: implement
        pass


class PlmDriverProtocol(DecodeResponses):
    """
    Check the command queue and send the 1st command if available.
    check the plm for received data
    If nothing to send - try again in 3 seconds.
    if nothing received, try again in 1 second.
    """

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.OBJs
        if g_debug >= 1:
            LOG.debug("Insteon_PLM.PlmDriverProtocol.__init__()")
        p_controller_obj._Queue = Queue.Queue(300)
        self.m_controller_obj = p_controller_obj
        self.dequeue_and_send()
        self.receive_loop()

    def driver_loop_stop(self):
        pass

    def dequeue_and_send(self):
        """Check the sending queue every SEND_TIMEOUT seconds and send if
        anything to send.

        Uses twisted to get a callback when the timer expires.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(SEND_TIMEOUT, self.dequeue_and_send)
        try:
            l_command = self.m_controller_obj._Queue.get(False)
        except Queue.Empty:
            return
        if self.m_controller_obj._DriverAPI != None:
            self.m_controller_obj._Command1 = l_command
            self.m_controller_obj._DriverAPI.write_device(l_command)
            if g_debug >= 6:
                LOG.debug("Send to controller:{0:}, Message:{1:}".format(self.m_controller_obj.Name, PrintBytes(l_command)))

    def receive_loop(self):
        """Check the driver to see if the controller returned any messages.

        Decode message only when we get enough bytes to complete a message.
        Note that there may be more bytes than we need - preserve them.

        TODO: instead of fixed time, callback to here from driver when bytes are rx'ed.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(RECEIVE_TIMEOUT, self.receive_loop)
        if self.m_controller_obj._DriverAPI != None:
            l_msg = self.m_controller_obj._DriverAPI.fetch_read_data(self.m_controller_obj)
            self.m_controller_obj._Message += l_msg
            if len(self.m_controller_obj._Message) < 2:
                return
            l_cur_len = len(self.m_controller_obj._Message)
            l_response_len = self._get_message_length(self.m_controller_obj._Message)
            if l_cur_len >= l_response_len:
                self._decode_message(self.m_controller_obj, self.m_house_obj)


class InsteonPlmCommands(CreateCommands):

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
        self.queue_62_command(p_name, MESSAGE_TYPES['product_data_request'], 0x00)


class InsteonAllLinks(InsteonPlmCommands):

    def get_all_allinks(self, p_controller_obj):
        """A command to fetch the all-link database from the PLM
        """
        if g_debug >= 1:
            LOG.debug("Get all All-Links from controller {0:}.".format(p_controller_obj.Name))
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
        # p_light_obj = LightData()
        p_light_obj = InsteonData()
        p_light_obj.InsteonAddress = self.dotted_hex2int(p_address)
        p_light_obj.GroupNumber = p_group
        # p_code = 0x00  # Find First
        p_code = 0x00  # Delete First Found record
        # p_flag = 0xE2
        p_data = bytearray(b'\x00\x00\x00')
        LOG.info("Delete All-link record - Address:{0:}, Group:{1:#02X}".format(p_light_obj.InsteonAddress, p_group))
        l_ret = self.queue_6F_command(p_light_obj, p_code, p_flag, p_data)
        return l_ret

    def reset_plm(self):
        """This will clear out the All-Links database.
        """
        l_debug_msg = "Resetting PLM - Name:{0:}".format(self.m_controller_obj)
        self.queue_67_command()
        LOG.info(l_debug_msg)


class InsteonPlmAPI(InsteonAllLinks):
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
        LOG.debug('Request Insteon Engine version from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, MESSAGE_TYPES['engine_version'], 0)  # 0x0D

    def get_id_request(self, p_obj):
        """Get the device DevCat
        """
        LOG.debug('Request Insteon ID(devCat) from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, MESSAGE_TYPES['id_request'], 0)  # 0x10

    def ping_plm(self):
        """Send a command to the plm and get its response.
        """
        return self.queue_60_command()

    def get_link_records(self, _p_house_obj, p_controller_obj):
        self.get_all_allinks(p_controller_obj)


class LightHandlerAPI(InsteonPlmAPI):
    """This is the API for light control.
    """

    def start_controller_driver(self, p_controller_obj, p_house_obj):
        self.m_house_obj = p_house_obj
        if g_debug >= 3:
            l_msg = "Insteon_PLM.start_controller_driver() - Controller:{0:}, ".format(p_controller_obj.Name)
            l_msg += "ControllerFamily:{0:}, InterfaceType:{1:}, Active:{2:}".format(
                    p_controller_obj.ControllerFamily, p_controller_obj.InterfaceType, p_controller_obj.Active)
        if p_controller_obj.InterfaceType.lower() == 'serial':
            from Modules.drivers import Driver_Serial
            l_driver = Driver_Serial.API()
        elif p_controller_obj.InterfaceType.lower() == 'ethernet':
            from Modules.drivers import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif p_controller_obj.InterfaceType.lower() == 'usb':
            # from drivers import Driver_USB_0403_6001
            # l_driver = Driver_USB_0403_6001.API()
            from Modules.drivers import Driver_USB
            l_driver = Driver_USB.API()
        p_controller_obj._DriverAPI = l_driver
        l_ret = l_driver.Start(p_controller_obj)
        return l_ret

    def stop_controller_driver(self, p_controller_obj):
        if p_controller_obj._DriverAPI != None:
            p_controller_obj._DriverAPI.Stop()

    def set_plm_mode(self, p_controller_obj):
        """Set the PLM to a mode
        """
        LOG.info('Setting mode of Insteon controller {0:}.'.format(p_controller_obj.Name))
        self.queue_6B_command(MODE_MONITOR)

    def get_all_lights_status(self):
        """Get the status (current level) of all lights.
        """
        LOG.info('Getting light levels of all Insteon lights')
        for l_light_obj in self.m_house_obj.Lights.itervalues():
            if l_light_obj.ControllerFamily != 'Insteon':
                continue
            if l_light_obj.Active != True:
                continue
            self._get_one_light_status(l_light_obj)

    def _get_one_light_status(self, p_light_obj):
        """Get the status of a light.
        We will (apparently) get back a 62-ACK followed by a 50 with the level in the response.
        """
        self.queue_62_command(p_light_obj, MESSAGE_TYPES['status_request'], 0)  # 0x19


class API(LightHandlerAPI):

    def __init__(self):
        """Constructor for the PLM.
        """
        pass

    def Start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        LOG.info('Starting Controller:{0:}'.format(p_controller_obj.Name))
        if self.start_controller_driver(p_controller_obj, p_pyhouse_obj.House.OBJs):
            self.m_protocol = PlmDriverProtocol(p_pyhouse_obj, self.m_controller_obj)
            self.set_plm_mode(self.m_controller_obj)
            self.get_all_lights_status()
            LOG.info('Started.')
            return True
        return False

    def Stop(self, p_controller_obj):
        self.m_protocol.driver_loop_stop()
        self.stop_controller_driver(p_controller_obj)
        LOG.info('Stopped.')

    def ChangeLight(self, p_light_obj, p_level, p_rate = 0):
        """
        Send a command to change a light's level
        """
        if g_debug >= 1:
            LOG.debug("Change light:{0:} to level:{1:} at rate:{2:}".format(p_light_obj.Name, p_level, p_rate))
        if int(p_level) == 0:
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['off'], 0)
        elif int(p_level) == 100:
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['on'], 255)
        else:
            l_level = int(p_level) * 255 / 100
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['on'], l_level)

# ## END DBK
