"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_PLM -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_PLM.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   This module decodes insteon PLM response messages

For each message passed to this module:
    Decode message and extract information from the message.
    Where possible, get the object that sent the response message and place the gathered data back in that object.
    return a status flag of True if everything was OK.
    return a status flag of False if an error occurred.


This entire section was empirically derived with a little help from the Insteon Developers Manual.

The manual describes the fields in the message and not much more.

PLEASE REFACTOR ME!

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Core import conversions
from Modules.Utilities.tools import PrintBytes
from Modules.Families.Insteon.Insteon_constants import ACK, MESSAGE_TYPES, MESSAGE_LENGTH, NAK, STX
from Modules.Families.Insteon.Insteon_utils import Util
from Modules.Families.Insteon import Insteon_Link
from Modules.Families.Insteon import Insteon_HVAC
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Insteon_decode ')

# OBJ_LIST = [Lights, Controllers, Buttons, Thermostats, Irrigation, Pool]


class D_Util(object):
    """
    """

    @staticmethod
    def _drop_first_byte(p_controller_obj):
        """The first byte is not legal, drop it and try again.
        Silently drop 1st byte if it is a NAK otherwise log it.
        """
        l_msg = "Found a leading char {0:#x} - Rest. - {1:}".format(
                p_controller_obj._Message[0], PrintBytes(p_controller_obj._Message))
        if p_controller_obj._Message[0] != NAK:
            LOG.error(l_msg)
        try:
            p_controller_obj._Message = p_controller_obj._Message[1:]
        except IndexError:
            pass

    @staticmethod
    def _decode_message_type_flag(p_type):
        TYPE_X = ['Direct', 'Direct_ACK', 'AllCleanup', 'All_Cleanup_ACK', 'Broadcast', 'Direct_NAK', 'All_Broadcast', 'All_Cleanup_NAK']
        return TYPE_X[p_type] + ' Msg, '

    @staticmethod
    def _decode_extended_flag(p_extended):
        TYPE_X = [' Standard,', ' Extended,']
        return TYPE_X[p_extended]

    @staticmethod
    def _decode_message_flag(p_byte):
        """ Get the message flag and convert it to a description of the message.
        """
        l_type = (p_byte & 0xE0) >> 5
        l_extended = (p_byte & 0x10)
        l_hops_left = (p_byte & 0x0C) >= 4
        l_max_hops = (p_byte & 0x03)
        l_ret = D_Util._decode_message_type_flag(l_type)
        l_ret += D_Util._decode_extended_flag(l_extended)
        l_ret += " HopsLeft:{0:d}, Hops:{1:d} ({2:#X}); ".format(l_hops_left, l_max_hops, p_byte)
        return l_ret

    @staticmethod
    def _get_message_length(p_message):
        """ Get the documented length that the message is supposed to be.

        Use the message type byte to find out how long the response from the PLM is supposed to be.
        With asynchronous routines, we want to wait till the entire message is received before proceeding with its decoding.
        """
        l_id = p_message[1]
        try:
            l_message_length = MESSAGE_LENGTH[l_id]
        except KeyError:
            l_message_length = 1
        return l_message_length

    def get_device_class(self, p_pyhouse_obj):
        """
        Return a class of objects (Lights, Thermostats) that may have an Insteon <ControllerFamily> within.
        """
        l_house = p_pyhouse_obj.House.DeviceOBJs
        for _l_class in l_house:
            pass
        pass

    def _find_addr_one_class(self, p_class, p_addr):
        """
        Find the address of something Insteon.
        @param p_class: is an OBJ like p_pyhouse_obj.House.DeviceOBJs.Controllers that we will look thru to find the object.
        @param p_addr: is the address that we want to find.
        @return: the object that has the address.  None if not found
        """
        for l_obj in p_class.itervalues():
            if l_obj.ControllerFamily != 'Insteon':
                continue  # ignore any non-Insteon devices in the class
            if l_obj.InsteonAddress == p_addr:
                return l_obj
        return None

    def _find_address_all_classes(self, p_address):
        """ This will search thru all object groups that an inseton device could be in.
        @return: the object that has the address or a dummy object if not found
        """
        l_ret = self._find_addr_one_class(self.m_pyhouse_obj.House.DeviceOBJs.Lights, p_address)
        l_dotted = conversions.int2dotted_hex(p_address, 3)
        if l_ret == None:
            l_ret = self._find_addr_one_class(self.m_pyhouse_obj.House.DeviceOBJs.Controllers, p_address)
        if l_ret == None:
            l_ret = self._find_addr_one_class(self.m_pyhouse_obj.House.DeviceOBJs.Buttons, p_address)
        if l_ret == None:
            l_ret = self._find_addr_one_class(self.m_pyhouse_obj.House.DeviceOBJs.Thermostats, p_address)
        # Add additional classes in here
        if l_ret == None:
            LOG.info("WARNING - Address {} ({}) *NOT* found.".format(l_dotted, p_address))
            l_ret = InsteonData()  # an empty new object
            l_ret.Name = '**NoName-' + l_dotted + '-**'
        return l_ret

    def get_obj_from_message(self, p_message, p_index):
        """ Here we have a message from the PLM.  Find out what device has that address.

        @param p_message: is the message byte array from the PLM we are extracting the Insteon address from.
        @param p_index: is the index of the first byte in the message.
                Various messages contain the address at different offsets.
        @return: The object that contains the address -or- a dummy object with noname in Name
        """
        l_address = Util.message2int(p_message, p_index)  # Extract the 3 byte address from the message and convert to an Int.
        if l_address < (16386 * 16386):
            l_dotted = str(l_address)
            l_device_obj = InsteonData()  # an empty new object
            l_device_obj.Name = '**Group: ' + l_dotted + ' **'
        else:
            l_device_obj = self._find_address_all_classes(l_address)
        return l_device_obj

    @staticmethod
    def get_devcat(p_message, p_obj):
        l_devcat = p_message[5] * 256 + p_message[6]
        p_obj.DevCat = int(l_devcat)
        # self.update_object(p_obj)
        l_debug_msg = "DevCat From={0:}, DevCat={1:#x}, flags={2:} ".format(p_obj.Name, l_devcat, D_Util._decode_message_flag(p_message[8]))
        LOG.info("Got DevCat from light:{}, DevCat:{} ".format(p_obj.Name, conversions.int2dotted_hex(l_devcat, 2)))
        return l_debug_msg

    @staticmethod
    def get_product_code(_p_obj, _p_message, _p_index):
        l_debug_msg = ''
        return l_debug_msg

    @staticmethod
    def update_object(p_obj):
        # TODO: implement
        pass

    def _get_addr_from_message(self, p_message, p_index):
        """Extract the address from a message.

        The message is a byte array returned from the PLM.
        The address is 3 consecutive bytes starting at p_index.

        @param p_message: is the byte array returned by the controller.
        @param p_index: is the offset into the message of a 3 byte field we will fetch and convert to an int
        """
        l_id = Util.message2int(p_message, p_index)
        return l_id

    def _get_ack_nak(self, p_byte):
        if p_byte == 0x06:
            return 'ACK '
        elif p_byte == 0x15:
            return 'NAK '
        else:
            return "{0:#02X} ".format(p_byte)

    def decode_command1(self, l_obj_from, l_name_from, l_name_to, l_9, l_10, l_message):
        l_debug_msg = ''
        if l_obj_from._Command1 == MESSAGE_TYPES['product_data_request']:  # 0x03
            l_debug_msg += " product data request. - Should never happen - S/B 51 response"
        elif l_obj_from._Command1 == MESSAGE_TYPES['engine_version']:  # 0x0D
            l_engine_id = l_10
            l_debug_msg += "Engine version From:{}, Sent to:{}, Id:{}; ".format(l_name_from, l_name_to, l_engine_id)
            LOG.info("Got engine version from light:{}, To:{}, EngineID:{} ".format(l_name_from, l_name_to, l_engine_id))
        elif l_obj_from._Command1 == MESSAGE_TYPES['id_request']:  # 0x10
            l_debug_msg += "Request ID From:{}; ".format(l_name_from)
            LOG.info("Got an ID request. Light:{} ".format(l_name_from,))
        elif l_obj_from._Command1 == MESSAGE_TYPES['on']:  # 0x11
            l_obj_from.CurLevel = 100
            l_debug_msg += "Device:{} turned Full ON  ; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from._Command1 == MESSAGE_TYPES['off']:  # 0x13
            l_obj_from.CurLevel = 0
            l_debug_msg += "Light:{} turned Full OFF; ".format(l_name_from)
            self.update_object(l_obj_from)
        elif l_obj_from._Command1 == MESSAGE_TYPES['status_request']:  # 0x19
            l_level = int(((l_10 + 2) * 100) / 256)
            l_obj_from.CurLevel = l_level
            l_debug_msg += "Status of light:{} is level:{}; ".format(l_name_from, l_level)
            LOG.info("Got Light Status From:{}, Level is:{} ".format(l_name_from, l_level))
            self.update_object(l_obj_from)
        elif l_obj_from._Command1 == MESSAGE_TYPES['thermostat_report']:  # 0x6e
            _l_ret1 = Insteon_HVAC.ihvac_utility().decode_50_record(l_obj_from, l_9, l_10)
            pass
        else:
            l_debug_msg += " unknown type - last command was {0:#x} - {1:}; ".format(l_obj_from._Command1, PrintBytes(l_message))

    @staticmethod
    def get_next_message(p_controller_obj):
        """ Get the next message from the controller.
        Remove the message from the controller object.
        Return None if there is not a full message left.
        """
        while len(p_controller_obj._Message) >= 2:
            if p_controller_obj._Message[0] != STX:
                D_Util._drop_first_byte(p_controller_obj)
                continue  # Loop back for next try at a message
            l_need_len = D_Util._get_message_length(p_controller_obj._Message)
            l_cur_len = len(p_controller_obj._Message)
            if l_cur_len >= l_need_len:
                l_msg = p_controller_obj._Message[0:l_need_len]
                p_controller_obj._Message = p_controller_obj._Message[l_need_len:]
                return l_msg
        return None


class DecodeResponses(D_Util):

    m_pyhouse_obj = None
    m_idex = 0

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        LOG.info('Starting Decode')

    def decode_message(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see Insteon Developers Manual pages 238-241

        Since a controller response may contain multiple messages and the last message may not be complete.
        This should be invoked every time we pick up more messages from the controller.
        It should loop and decode each message present and leave when done

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        # LOG.info('Message = {}'.format(PrintBytes(p_controller_obj._Message)))
        while len(p_controller_obj._Message) >= 2:
            l_stx = p_controller_obj._Message[0]
            if l_stx == STX:
                # LOG.info("{}".format(PrintBytes(p_controller_obj._Message)))
                l_need_len = self._get_message_length(p_controller_obj._Message)
                l_cur_len = len(p_controller_obj._Message)
                if l_cur_len >= l_need_len:
                    self._decode_dispatch(p_controller_obj)
                else:
                    LOG.warning('Message was too short - waiting for rest of message.')
                    return
            else:
                D_Util._drop_first_byte(p_controller_obj)

    def _decode_dispatch(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_message = p_controller_obj._Message
        l_ret = False
        l_cmd = p_controller_obj._Message[1]
        if l_cmd == 0:
            LOG.warning("Found a '0' record ->{}.".format(PrintBytes(l_message)))
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

    def get_message_flags(self, p_message, p_index):
        try:
            l_message_flags = p_message[p_index]
        except IndexError:
            l_message_flags = 0
        return l_message_flags

    def _decode_50_record(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.

        See p 231(244) of developers guide.
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
        l_message_flags = self.get_message_flags(p_controller_obj._Message, 8)
        try:
            l_9 = l_message[9]
            l_10 = l_message[10]
        except IndexError:
            l_9 = 0
            l_10 = 0
            LOG.warning("Short 50 message rxed - {}".format(PrintBytes(l_message)))
        l_data = [l_9, l_10]
        l_debug_msg = 'Standard Message; '
        l_flags = D_Util._decode_message_flag(l_message_flags) + ' From: {}'.format(l_obj_from.Name)
        # Break down bits 7(msb), 6, 5 into message type
        if l_message_flags & 0xE0 == 0x80:  # Broadcast Message (100)
            l_debug_msg += D_Util.get_devcat(l_message, l_obj_from)
        elif l_message_flags & 0xE0 == 0xC0:  # (110) all link broadcast of group id
            l_group = l_7
            l_debug_msg += "All-Link broadcast From:{}, Group:{}, Flags:{}, Data:{}; ".format(l_name_from, l_group, l_flags, l_data)
            LOG.info("== 50B All-link Broadcast From:{}, Group:{}, Flags:{}, Data:{} ==".format(l_name_from, l_group, l_flags, l_data))
        #
        try:
            if l_obj_from._Command1 == MESSAGE_TYPES['product_data_request']:  # 0x03
                l_debug_msg += " product data request. - Should never happen - S/B 51 response"
            elif l_obj_from._Command1 == MESSAGE_TYPES['engine_version']:  # 0x0D
                l_engine_id = l_10
                l_debug_msg += "Engine version From:{}, Sent to:{}, Id:{}; ".format(l_name_from, l_name_to, l_engine_id)
                LOG.info("Got engine version from light:{}, To:{}, EngineID:{}".format(l_name_from, l_name_to, l_engine_id))
            elif l_obj_from._Command1 == MESSAGE_TYPES['id_request']:  # 0x10
                l_debug_msg += "Request ID From:{0:}; ".format(l_name_from)
                LOG.info("Got an ID request. Light:{0:}".format(l_name_from,))
            elif l_obj_from._Command1 == MESSAGE_TYPES['on']:  # 0x11
                l_obj_from.CurLevel = 100
                l_debug_msg += "Device:{} turned Full ON  ; ".format(l_name_from)
                self.update_object(l_obj_from)
            elif l_obj_from._Command1 == MESSAGE_TYPES['off']:  # 0x13
                l_obj_from.CurLevel = 0
                l_debug_msg += "Light:{} turned Full OFF; ".format(l_name_from)
                self.update_object(l_obj_from)
            elif l_obj_from._Command1 == MESSAGE_TYPES['status_request']:  # 0x19
                l_level = int(((l_10 + 2) * 100) / 256)
                l_obj_from.CurLevel = l_level
                l_debug_msg += "Status of light:{} is level:{}; ".format(l_name_from, l_level)
                LOG.info("PLM:{} Got Light Status From:{}, Level is:{} ".format(p_controller_obj.Name, l_name_from, l_level))
                self.update_object(l_obj_from)
            elif l_obj_from._Command1 == MESSAGE_TYPES['thermostat_report']:  # 0x6e
                _l_ret1 = Insteon_HVAC.ihvac_utility().decode_50_record(l_obj_from, l_9, l_10)
                pass
            else:
                l_debug_msg += " Unknown type - last command was {0:#x} - {1:}; ".format(l_obj_from._Command1, PrintBytes(l_message))
        except AttributeError:
            pass
        l_ret = True
        self.m_pyhouse_obj.APIs.Comp.MqttAPI.MqttPublish("pyhouse/lighting/{}/info".format(l_name_from), "InsteonDecoder {}".format(l_debug_msg))
        LOG.info(l_debug_msg)
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

        This is an ack/nak of the command and generally is not very interesting by itself.
        Depending on the command sent, another response MAY follow this message with further data.
        """
        l_message = p_controller_obj._Message
        l_obj = self.get_obj_from_message(l_message, 2)
        _l_msgflags = D_Util._decode_message_flag(l_message[5])
        try:
            l_8 = l_message[8]
        except IndexError:
            l_8 = 0
            LOG.warning("Short 62 message rxed - {p:}".format(PrintBytes(l_message)))
        l_ack = self._get_ack_nak(l_8)
        l_debug_msg = "Device:{0:}, {1:}".format(l_obj.Name, l_ack)
        if g_debug >= 1:
            LOG.info("Got ACK(62) {0:}".format(l_debug_msg))
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
            l_ret = self.decode_message(p_controller_obj)
        else:
            l_msg = "check_for_more_decoding() trying to chop an incomplete message - {0:}".format(
                    PrintBytes(p_controller_obj._Message))
            LOG.error(l_msg)
        return l_ret

# ## END DBK
