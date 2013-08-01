#!/usr/bin/python

"""Insteon PLM module.

Create commands and interpret results from any Insteon controller regardless of interface.

TODO: Work toward getting one instance per controller.
        We will then need to assign lights to a particular controller if there is more than one in a house.

This module carries state information about the controller.
This is necessary since the responses may follow a command at any interval.
Responses do not all have to follow the command that caused them.


TODO: implement all-links

"""

# Import system type stuff
import logging
import Queue
from twisted.internet import reactor

# Import PyMh files
from src.lights.lighting import LightData
from src.families.Insteon import Insteon_Link
from src.utils.tools import PrintBytes
from src.families.Insteon.Insteon_constants import *
from src.families.Insteon import Insteon_utils

g_debug = 5
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Minor routine entry
# 4 = sent commands high level
# 5 = decode response
# 6 = sent command detail (number)
# 7 = diagnostics
# + = NOT USED HERE
g_logger = None

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


class InsteonPlmUtility(object):

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


class DecodeResponses(InsteonPlmUtility):

    m_house_obj = None

    def _find_addr(self, p_class, p_addr):
        for l_obj in p_class.itervalues():
            if l_obj.Family != 'Insteon':
                continue
            if l_obj.InsteonAddress == p_addr:
                return l_obj
        if g_debug >= 7:
            print "Insteon_PLM._find_addr - not found {0:}({1:})".format(Insteon_utils.int2dotted_hex(p_addr), p_addr)
        return None

    def get_obj_from_message(self, p_message, p_index):
        l_id = Insteon_utils.message2int(p_message, p_index)
        l_ret = self._find_addr(self.m_house_obj.Lights, l_id)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Controllers, l_id)
        if l_ret == None:
            l_ret = self._find_addr(self.m_house_obj.Buttons, l_id)
        if l_ret == None:
            l_ret = LightData()  # an empty new object
            l_ret.Name = '**' + str(l_id) + '**'
        if g_debug >= 7:
            print "Insteon_PLM.get_obj_from_message - Address:{0:}({1:}), found:{2:}".format(Insteon_utils.int2dotted_hex(l_id), l_id, l_ret.Name)
        return l_ret

    def _drop_first_byte(self, p_controller_obj):
        """The first byte is not legal, drop it and try again.
        """
        l_msg = "Insteon_PLM._drop_first_byte() Found a leading char {0:} - Rest. - {1:}".format(
                p_controller_obj.Message[0], PrintBytes(p_controller_obj.Message))
        if g_debug >= 2:
            print l_msg
        g_logger.error(l_msg)
        try:
            p_controller_obj.Message = p_controller_obj.Message[1:]
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
        if g_debug >= 5:
            print "Insteon_PLM._decode_message()"
        while len(p_controller_obj.Message) >= 2:
            l_stx = p_controller_obj.Message[0]
            if g_debug >= 6:
                print "Insteon_PLM._decode_message() - {0:}".format(PrintBytes(p_controller_obj.Message))
            if l_stx == STX:
                l_need_len = self._get_message_length(p_controller_obj.Message)
                l_cur_len = len(p_controller_obj.Message)
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
        l_message = p_controller_obj.Message
        l_ret = False
        l_cmd = p_controller_obj.Message[1]
        if l_cmd == 0:
            g_logger.warning("Found a '0' record ->{0:}.".format(PrintBytes(l_message)))
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
            self.check_for_more_decoding(p_controller_obj, l_ret)
        return l_ret

    def _get_devcat(self, p_message, p_light_obj):
        l_devcat = p_message[5] * 256 + p_message[6]
        p_light_obj.DevCat = int(l_devcat)
        self.update_object(p_light_obj)
        l_debug_msg = "DevCat From={0:}, DevCat={1:#x}, flags={2:}".format(p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        if g_debug >= 3:
            print "Insteon_PLM._get_devcat() - Got devcat type  From={0:}, DevCat={1:#x}, flags={2:}".format(
                            p_light_obj.Name, l_devcat, self._decode_message_flag(p_message[8]))
        g_logger.info("Got DevCat from light:{0:}, DevCat:{1:}".format(p_light_obj.Name, l_devcat))
        return l_debug_msg

    def _decode_50_record(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.

        See p 246 of developers guide.
        """
        l_message = p_controller_obj.Message
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
            g_logger.warn("Short 50 message rxed - {p:}".format(PrintBytes(l_message)))
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
            g_logger.info("== 50B All-link Broadcast From:{0:}, Group:{1:}, Flags:{2:}, Data:{3:} ==".format(l_name_from, l_group, l_flags, l_data))
        elif l_8 & 0xE0 == 0xE0:  # (111) NAK of Direct message type
            l_debug_msg += "NAK of direct message(2) from {0:}; ".format(l_name_from)
        #
        if l_obj_from.Command1 == MESSAGE_TYPES['product_data_request']:  # 0x03
            l_debug_msg += " product data request. - Should never happen - S/B 51 response"
        elif l_obj_from.Command1 == MESSAGE_TYPES['engine_version']:  # 0x0D
            l_engine_id = l_10
            l_debug_msg += "Engine version From:{0:}, Sent to:{1:}, Id:{2:}; ".format(l_name_from, l_name_to, l_engine_id)
            g_logger.info("Got engine version from light:{0:}, To:{1:}, EngineID:{2:}".format(l_name_from, l_name_to, l_engine_id))
        elif l_obj_from.Command1 == MESSAGE_TYPES['id_request']:  # 0x10
            l_debug_msg += "Request ID From:{0:}; ".format(l_name_from)
            g_logger.info("Got an ID request. Light:{0:}".format(l_name_from,))
        elif l_obj_from.Command1 == MESSAGE_TYPES['on']:  # 0x11
            l_obj_from.CurLevel = 100
            l_debug_msg += "Light:{0:} turned Full ON; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from.Command1 == MESSAGE_TYPES['off']:  # 0x13
            l_obj_from.CurLevel = 0
            l_debug_msg += "Light:{0:} turned Full OFF; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from.Command1 == MESSAGE_TYPES['status_request']:  # 0x19
            l_level = int(((l_10 + 2) * 100) / 256)
            l_obj_from.CurLevel = l_level
            l_debug_msg += "Status of light:{0:} is level:{1:}; ".format(l_name_from, l_level)
            g_logger.info("PLM:{0:} Got Light Status From:{1:}, Level is:{2:}".format(p_controller_obj.Name, l_name_from, l_level))
            self.update_object(l_obj_from)
        else:
            l_debug_msg += "Insteon_PLM._decode_50_record() unknown type - last command was {0:#x} - {1:}; ".format(l_obj_from.Command1, PrintBytes(l_message))
        l_ret = True

        if g_debug >= 4:
            print "Insteon_PLM._decode_50_record() {0:}".format(l_debug_msg)
            g_logger.debug(l_debug_msg)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_51_record(self, p_controller_obj):
        """ Insteon Extended Message Received (25 bytes).
        See p 247 of developers guide.
        """
        l_message = p_controller_obj.Message
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
        if g_debug >= 5:
            print "Insteon_PLM._decode_51_record() - Response from:{0:}, Devcat:{1:}, ProduckKey:{2:}".format(l_obj_from.Name, l_devcat, l_product_key), l_extended
        g_logger.info("== 51 From={0:}, To={1:}, Flags={2:#x}, Data={3:} Extended={4:} ==".format(l_obj_from.Name, l_obj_to.Name, l_flags, l_data, l_extended))
        l_obj_from.ProductKey = l_product_key
        l_obj_from.DevCat = l_devcat
        l_ret = True
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_52_record(self, p_controller_obj):
        """Insteon X-10 message received (4 bytes).
        See p 253 of developers guide.
        """
        g_logger.warning("== 52 message not decoded yet.")
        l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_52_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_53_record(self, p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 260 of developers guide.
        """
        g_logger.warning("== 53 message not decoded yet.")
        l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_53_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_54_record(self, p_controller_obj):
        """Insteon Button Press event (3 bytes).
        See p 276 of developers guide.
        """
        g_logger.warning("== 54 message not decoded yet.")
        l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_54_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_55_record(self, p_controller_obj):
        """Insteon User Reset detected (2 bytes).
        See p 269 of developers guide.
        """
        l_debug_msg = "User Reset Detected! "
        l_ret = False
        g_logger.info("".format(l_debug_msg))
        if g_debug >= 5:
            print "Insteon_PLM.decode_55_record() {0:}".format(l_debug_msg)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_56_record(self, p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 256 of developers guide.
        """
        g_logger.warning("== 56 message not decoded yet.")
        l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_56_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_57_record(self, p_controller_obj):
        """All-Link Record Response (10 bytes).
        See p 264 of developers guide.
        """
        l_message = p_controller_obj.Message
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
        g_logger.info("All-Link response-57 - Group={0:#02X}, Name={1:}, Flags={2:#x}, Data={3:}, {4:}".format(l_group, l_obj.Name, l_flags, l_data, l_type))
        l_ret = True
        if g_debug >= 5:
            print "Insteon_PLM.decode_57_record() - Group:{0:#02X}, Name:{1:}, Flags:{2:#0x}, Data:{3:}".format(l_group, l_obj.Name, l_flags, l_data)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_58_record(self, p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 257 of developers guide.
        """
        g_logger.warning("== 58 message not decoded yet.")
        l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_58_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_60_record(self, p_controller_obj):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_obj = self.get_obj_from_message(l_message, 2)
        l_devcat = l_message[5]
        l_devsubcat = l_message[6]
        l_firmver = l_message[7]
        g_logger.info("== 60 - Insteon Modem Info - DevCat={0:}, DevSubCat={1:}, Firmware={2:} - Name={3:}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if l_message[8] == ACK:
            l_ret = True
        else:
            g_logger.error("== 60 - No ACK - Got {0:#x}".format(l_message[8]))
            l_ret = False
        if g_debug >= 5:
            print "Insteon_PLM.decode_60_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

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
        if g_debug >= 5:
            print "Insteon_PLM.decode_61_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_62_record(self, p_controller_obj):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 243 of developers guide.

        This is an ack/nak of the command and generally is not very interesting.
        Another response MAY follow this message with further data.
        """
        l_message = p_controller_obj.Message
        l_obj = self.get_obj_from_message(l_message, 2)
        _l_msgflags = self._decode_message_flag(l_message[5])
        try:
            l_8 = l_message[8]
        except IndexError:
            l_8 = 0
            g_logger.warn("Short 62 message rxed - {p:}".format(PrintBytes(l_message)))
        l_ack = self._get_ack_nak(l_8)
        l_debug_msg = "Device:{0:}, {1:}".format(l_obj.Name, l_ack)
        if g_debug >= 5:
            print "Insteon_PLM.decode_62_record() {0:}".format(l_debug_msg)
            g_logger.debug("Got ACK(62) {0:}".format(l_debug_msg))
        return self.check_for_more_decoding(p_controller_obj)

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
        if g_debug >= 5:
            print "Insteon_PLM.decode_64_record()"
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_67_record(self, p_controller_obj):
        """Reset IM ACK response (3 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj.Message
        l_ack = self._get_ack_nak(l_message[2])
        l_debug_msg = "Reset IM(PLM) {0:}".format(l_ack)
        g_logger.info("{0:}".format(l_debug_msg))
        if g_debug >= 5:
            print "Insteon_PLM.decode_64_record() {0:}".format(l_debug_msg)
        return self.check_for_more_decoding(p_controller_obj)

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
        if g_debug >= 5:
            print "Insteon_PLM.decode_69_record() - {0:}".format(self._get_ack_nak(l_message[2]))
        return self.check_for_more_decoding(p_controller_obj, l_ret)

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
        if g_debug >= 5:
            print "Insteon_PLM.decode_6A_record() - {0:}".format(self._get_ack_nak(l_message[2]))
        return self.check_for_more_decoding(p_controller_obj, l_ret)

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
        if g_debug >= 5:
            print "Insteon_PLM.decode_6B_record() - {0:}".format(l_debug_msg)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_6F_record(self, p_controller_obj):
        """All-Link manage Record Response (12 bytes).
        See p 267 of developers guide.
        """
        l_message = p_controller_obj.Message
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
        g_logger.info("{0:}".format(l_message))
        l_ret = True
        if g_debug >= 5:
            print "Insteon_PLM.decode_6F_record() - {0:}".format(l_message)
        return self.check_for_more_decoding(p_controller_obj, l_ret)

    def _decode_73_record(self, p_controller_obj):
        """Get the PLM response of 'get config' (6 bytes).
        See p 270 of developers guide.
        """
        l_message = p_controller_obj.Message
        try:
            l_5 = l_message[5]
        except IndexError:
            l_5 = 0
            g_logger.warn("Short 73 message rxed - {p:}".format(PrintBytes(l_message)))
        l_flags = l_message[2]
        l_spare1 = l_message[3]
        l_spare2 = l_message[4]
        l_ack = self._get_ack_nak(l_5)
        if g_debug >= 5:
            print "Insteon_PLM.decode_73_record() - got plm config response."
        g_logger.info("== 73 Get IM configuration Flags={0#x:}, Spare 1={1:#x}, Spare 2={2:#x} {3:} ".format(
                    l_flags, l_spare1, l_spare2, l_ack))
        return self.check_for_more_decoding(p_controller_obj)

    def check_for_more_decoding(self, p_controller_obj, p_ret = True):
        """Chop off the current message from the head of the buffered response stream from the controller.
        @param p_ret: is the result to return.
        """
        l_ret = p_ret
        l_cur_len = len(p_controller_obj.Message)
        l_chop = self._get_message_length(p_controller_obj.Message)
        if l_cur_len >= l_chop:
            p_controller_obj.Message = p_controller_obj.Message[l_chop:]
            l_ret = self._decode_message(p_controller_obj, self.m_house_obj)
        else:
            l_msg = "check_for_more_decoding() trying to chop an incomplete message - {0:}".format(
                    PrintBytes(p_controller_obj.Message))
            g_logger.error(l_msg)
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

    def __init__(self, p_controller_obj, p_house_obj):
        self.m_house_obj = p_house_obj
        if g_debug >= 3:
            print "Insteon_PLM.PlmDriverProtocol.__init__()"
        p_controller_obj.Queue = Queue.Queue(300)
        self.m_controller_obj = p_controller_obj
        self.dequeue_and_send()
        self.receive_loop()

    def driver_loop_stop(self):
        if g_debug >= 3:
            print "Insteon_PLM.driver_loop_stop()"
        pass

    def queue_plm_command(self, p_command):
        if g_debug >= 7:
            print "Insteon_PLM.queue_plm_command() - ", vars()
        self.m_controller_obj.Queue.put(p_command)
        if g_debug >= 6:
            print "Insteon_PLM.queue_plm_command() - Q-Size:{0:}, Command:{1:}".format(self.m_controller_obj.Queue.qsize(), PrintBytes(p_command))

    def dequeue_and_send(self):
        """Check the sending queue every SEND_TIMEOUT seconds and send if
        anything to send.

        Uses twisted to get a callback when the timer expires.
        """
        callLater(SEND_TIMEOUT, self.dequeue_and_send)
        try:
            l_command = self.m_controller_obj.Queue.get(False)
        except Queue.Empty:
            return
        if self.m_controller_obj.DriverAPI != None:
            self.m_controller_obj.Command1 = l_command
            self.m_controller_obj.DriverAPI.write_device(l_command)
            if g_debug >= 6:
                print "Insteon_PLM.dequeue_and_send() to {0:}, Message: {1:}".format(self.m_controller_obj.Name, PrintBytes(l_command))
                g_logger.debug("Send to controller:{0:}, Message:{1:}".format(self.m_controller_obj.Name, PrintBytes(l_command)))

    def receive_loop(self):
        """Check the driver to see if the controller returned any messages.

        Decode message only when we get enough bytes to complete a message.
        Note that there may be more bytes than we need - preserve them.

        TODO: instead of fixed time, callback to here from driver when bytes are rx'ed.
        """
        callLater(RECEIVE_TIMEOUT, self.receive_loop)
        if self.m_controller_obj.DriverAPI != None:
            l_msg = self.m_controller_obj.DriverAPI.fetch_read_data(self.m_controller_obj)
            self.m_controller_obj.Message += l_msg
            if len(self.m_controller_obj.Message) < 2:
                return
            if g_debug >= 7:
                print "Insteon_PLM.receive_loop() - Controller:{0:}".format(self.m_controller_obj.Name), PrintBytes(self.m_controller_obj.Message)
            l_cur_len = len(self.m_controller_obj.Message)
            l_response_len = self._get_message_length(self.m_controller_obj.Message)
            if l_cur_len >= l_response_len:
                self._decode_message(self.m_controller_obj, self.m_house_obj)


class CreateCommands(PlmDriverProtocol):
    """Send various commands to the PLM.
    """

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
        if g_debug >= 6:
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
        l_command = self._queue_command('insteon_send')
        Insteon_utils.int2message(p_light_obj.InsteonAddress, l_command, 2)
        l_command[5] = FLAG_MAX_HOPS + FLAG_HOPS_LEFT  # 0x0F
        l_command[6] = p_light_obj.Command1 = p_cmd1
        l_command[7] = p_light_obj.Command2 = p_cmd2
        if g_debug >= 6:
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
        if g_debug >= 6:
            print "Insteon_PLM.queue_67_command() - Reset the PLM."
            g_logger.debug("Queue command to reset the PLM.")
        l_command = self._queue_command('plm_reset')
        return self.queue_plm_command(l_command)

    def queue_68_command(self, p_obj):
        """
        """
        pass

    def queue_69_command(self):
        """Get the first all-link record from the plm (2 bytes).
        See p 261 of developers guide.
        """
        if g_debug >= 6:
            print "Insteon_PLM.queue_69_command() - Get first all-link record."
            g_logger.debug("Queue command to get First all-link record.")
        l_command = self._queue_command('plm_first_all_link')
        return self.queue_plm_command(l_command)

    def queue_6A_command(self):
        """Get the next record - will get a nak if no more (2 bytes).
        See p 262 of developers guide.
        Returns True if more - False if no more.
        """
        if g_debug >= 6:
            print "Insteon_PLM.queue_6A_command() get Next all-link record."
            g_logger.debug("Queue command to get Next all-link record.")
        l_command = self._queue_command('plm_next_all_link')
        return self.queue_plm_command(l_command)

    def queue_6B_command(self, p_flags):
        """Set IM configuration flags (3 bytes).
        See page 271  of Insteon Developers Guide.
        """
        if g_debug >= 6:
            print "Insteon_PLM.queue_6B_command() to set PLM config flag"
            g_logger.debug("Queue command to set PLM config flag to {0:#X}".format(p_flags))
        l_command = self._queue_command('plm_set_config')
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
        if g_debug >= 6:
            print "Insteon_PLM.queue_6F_command() to manage all-link record"
            g_logger.debug("Queue command to manage all-link record")
        l_command = self._queue_command('manage_all_link_record')
        l_command[2] = p_code
        l_command[3] = p_flag
        l_command[4] = p_light_obj.GroupNumber
        Insteon_utils.int2message(p_light_obj.InsteonAddress, l_command, 5)
        l_command[8:11] = p_data
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
        if g_debug >= 6:
            print "Insteon_PLM.queue_73_command() to get plm config."
            g_logger.debug("Queue command to get PLM config.")
        p_light_obj.Command1 = PLM_COMMANDS['plm_get_config']
        l_command = self._queue_command('plm_get_config')
        return self.queue_plm_command(l_command)


class LightingAPI(CreateCommands):

    def change_light_setting(self, p_light_obj, p_level):
        l_debug_msg = "Change light:{0:} to level:{1:}".format(p_light_obj.Name, p_level)
        if g_debug >= 4:
            print "Insteon_PLM.change_light_settings()  {0:}".format(l_debug_msg)
            g_logger.debug("Change light setting. {0:}".format(l_debug_msg))
        if int(p_level) == 0:
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['off'], 0)
        elif int(p_level) == 100:
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['on'], 255)
        else:
            l_level = int(p_level) * 255 / 100
            self.queue_62_command(p_light_obj, MESSAGE_TYPES['on'], l_level)

    def scan_all_lights(self, p_lights):
        """Exported command - used by other modules.
        """
        if g_debug >= 4:
            print "insteon_PLM.scan_all_lights"
        for l_obj in p_lights.itervalues():
            if LightData.Family(l_obj) != 'Insteon':
                continue
            if l_obj.Type == 'Light':
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
        self.queue_62_command(p_name, MESSAGE_TYPES['product_data_request'], 0x00)


class InsteonAllLinks(InsteonPlmCommands):

    def get_all_allinks(self, p_controller_obj):
        """A command to fetch the all-link database from the PLM
        """
        if g_debug >= 4:
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
        if g_debug >= 4:
            print "Insteon_PLM.delete_link() - Address:{0}, Group:{1:#02X}".format(p_address, p_group)
        p_light_obj = LightData()
        p_light_obj.InsteonAddress = self.dotted_hex2int(p_address)
        p_light_obj.GroupNumber = p_group
        # p_code = 0x00  # Find First
        p_code = 0x00  # Delete First Found record
        # p_flag = 0xE2
        p_data = bytearray(b'\x00\x00\x00')
        g_logger.info("Delete All-link record - Address:{0:}, Group:{1:#02X}".format(p_light_obj.InsteonAddress, p_group))
        l_ret = self.queue_6F_command(p_light_obj, p_code, p_flag, p_data)
        return l_ret

    def reset_plm(self):
        """This will clear out the All-Links database.
        """
        l_debug_msg = "Resetting PLM - Name:{0:}".format(self.m_controller_obj)
        if g_debug >= 4:
            print "Insteon_PLM.reset_plm() - delete the PLM all-link database. {0:}".format(l_debug_msg)
        self.queue_67_command()
        g_logger.info("Reset PLM")


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
        g_logger.debug('Request Insteon Engine version from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, MESSAGE_TYPES['engine_version'], 0)  # 0x0D

    def get_id_request(self, p_obj):
        """Get the device DevCat
        """
        g_logger.debug('Request Insteon ID(devCat) from device: {0:}'.format(p_obj.Name))
        self.queue_62_command(p_obj.Name, MESSAGE_TYPES['id_request'], 0)  # 0x10

    def ping_plm(self):
        """Send a command to the plm and get its response.
        """
        return self.queue_60_command()

    def get_link_records(self, _p_house_obj):
        self.get_all_allinks()


class LightHandlerAPI(InsteonPlmAPI):
    """This is the API for light control.
    """

    def start_controller_driver(self, p_controller_obj, p_house_obj):
        self.m_house_obj = p_house_obj
        if g_debug >= 3:
            l_msg = "Insteon_PLM.start_controller_driver() - Controller:{0:}, ".format(p_controller_obj.Name)
            l_msg += "Family:{0:}, Interface:{1:}, Active:{2:}".format(
                    p_controller_obj.Family, p_controller_obj.Interface, p_controller_obj.Active)
            print l_msg
        if p_controller_obj.Interface.lower() == 'serial':
            from src.drivers import Driver_Serial
            l_driver = Driver_Serial.API()
        elif p_controller_obj.Interface.lower() == 'ethernet':
            from src.drivers import Driver_Ethernet
            l_driver = Driver_Ethernet.API()
        elif p_controller_obj.Interface.lower() == 'usb':
            # from drivers import Driver_USB_0403_6001
            # l_driver = Driver_USB_0403_6001.API()
            from src.drivers import Driver_USB
            l_driver = Driver_USB.API()
        p_controller_obj.DriverAPI = l_driver
        l_ret = l_driver.Start(p_controller_obj)
        if g_debug >= 3:
            print "Insteon_PLM.start_controller_driver() - Just started a driver.  Name: {0:}".format(p_controller_obj.Name), l_ret
        return l_ret

    def stop_controller_driver(self, p_controller_obj):
        if g_debug >= 3:
            print "Insteon_PLM.stop__controller()"
        if p_controller_obj.DriverAPI != None:
            p_controller_obj.DriverAPI.Stop()

    def set_plm_mode(self, p_controller_obj):
        """Set the PLM to a mode
        """
        g_logger.info('Setting mode of Insteon controller {0:}.'.format(p_controller_obj.Name))
        if g_debug >= 4:
            print "Insteon_PLM.set_plm_mode() - Sending mode command to Insteon PLM"
        self.queue_6B_command(MODE_MONITOR)

    def get_all_lights_status(self):
        """Get the status (current level) of all lights.
        """
        if g_debug >= 4:
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
        if g_debug >= 4:
            print "Insteon_PLM._get_one_light_status() {0:}".format(p_light_obj.Name)
        self.queue_62_command(p_light_obj, MESSAGE_TYPES['status_request'], 0)  # 0x19


class API(LightHandlerAPI):

    def __init__(self, p_house_obj):
        """Constructor for the PLM.
        """
        global g_logger
        g_logger = logging.getLogger('PyHouse.Inst_PLM')
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "Insteon_PLM.API()"
        g_logger.info('Initialized for house {0:}.'.format(p_house_obj.Name))

    def Start(self, p_controller_obj):
        self.m_controller_obj = p_controller_obj
        if g_debug >= 2:
            print "Insteon_PLM.API.Start() - House:{0:}, Controller:{1:}".format(self.m_house_obj.Name, p_controller_obj.Name)
        g_logger.info('Starting Controller:{0:}'.format(p_controller_obj.Name))
        if self.start_controller_driver(p_controller_obj, self.m_house_obj):
            self.m_protocol = PlmDriverProtocol(self.m_controller_obj, self.m_house_obj)
            # self.m_protocol.driver_loop_start(self.m_house_obj)
            self.set_plm_mode(self.m_controller_obj)
            self.get_all_lights_status()
            g_logger.info('Started.')
            if g_debug >= 2:
                print "Insteon_PLM.API.Start() has completed for PLM:{0:}.".format(p_controller_obj.Name)
            return True
        return False

    def Stop(self, p_controller_obj):
        if g_debug >= 2:
            print "Insteon_PLM.API.Stop()"
        g_logger.info('Stopping.')
        self.m_protocol.driver_loop_stop()
        self.stop_controller_driver(p_controller_obj)
        g_logger.info('Stopped.')

    def SpecialTest(self):
        if g_debug >= 2:
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

# ## END DBK
