"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_decoder -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_decoder.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2016 by D. Brian Kimmel
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

__updated__ = '2016-10-26'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_HVAC, Insteon_utils
from Modules.Families.Insteon.Insteon_Link import Decode as linkDecode
from Modules.Families.Insteon.Insteon_constants import ACK, MESSAGE_TYPES, NAK, STX
from Modules.Families.Insteon.Insteon_utils import Decode as utilDecode, Util as utilUtil
from Modules.Utilities.tools import PrintBytes


LOG = Logger.getLogger('PyHouse.Insteon_decode ')

#  OBJ_LIST = [Lights, Controllers, Buttons, Thermostats, Irrigation, Pool]


class DecodeResponses(object):

    m_pyhouse_obj = None
    m_idex = 0

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        self.m_link = linkDecode(p_pyhouse_obj, p_controller_obj)
        LOG.info('Starting Decode')

    def decode_message(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see Insteon Developers Manual pages 238-241

        Since a controller response may contain multiple messages and the last message may not be complete.
        This should be invoked every time we pick up more messages from the controller.
        It should loop and decode each message present and leave when done

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        while len(p_controller_obj._Message) >= 2:
            l_stx = p_controller_obj._Message[0]
            if l_stx == STX:
                l_need_len = utilUtil.get_message_length(p_controller_obj._Message)
                l_cur_len = len(p_controller_obj._Message)
                if l_cur_len >= l_need_len:
                    self._decode_dispatch(p_controller_obj)
                else:
                    LOG.warning('Message was too short - waiting for rest of message.')
                    return
            elif l_stx == NAK:
                LOG.warn("Dropping a leading char {:#x}".format(l_stx))
                continue
            elif l_stx == 0:
                LOG.warn("Dropping a leading char {:#x}".format(l_stx))
                continue
            else:
                p_controller_obj._Message = p_controller_obj._Message[1:]
                continue


    def check_for_more_decoding(self, p_controller_obj, p_ret=True):
        """Chop off the current message from the head of the buffered response stream from the controller.
        @param p_ret: is the result to return.
        """
        l_ret = p_ret
        l_cur_len = len(p_controller_obj._Message)
        l_chop = utilUtil.get_message_length(p_controller_obj._Message)
        if l_cur_len >= l_chop:
            p_controller_obj._Message = p_controller_obj._Message[l_chop:]
            l_ret = self.decode_message(p_controller_obj)
        else:
            l_msg = "check_for_more_decoding() trying to chop an incomplete message - {}".format(
                    PrintBytes(p_controller_obj._Message))
            LOG.error(l_msg)
        return l_ret

    def _decode_dispatch(self, p_controller_obj):
        """Decode a message that was ACKed / NAked.
        see IDM pages 238-241

        @return: a flag that is True for ACK and False for NAK/Invalid response.
        """
        l_message = p_controller_obj._Message
        l_ret = False
        l_cmd = p_controller_obj._Message[1]
        # LOG.debug('  Dispatch: {:#02x}'.format(l_cmd))
        if l_cmd == 0:
            LOG.warning("Found a '0' record ->{}.".format(PrintBytes(l_message)))
            return l_ret
        elif l_cmd == 0x50: l_ret = self._decode_50(p_controller_obj)
        elif l_cmd == 0x51: l_ret = self._decode_51(p_controller_obj)
        elif l_cmd == 0x52: l_ret = self._decode_52_record(p_controller_obj)
        elif l_cmd == 0x53: self.m_link.decode_53()
        elif l_cmd == 0x54: linkDecode.decode_54(p_controller_obj)
        elif l_cmd == 0x55: l_ret = self._decode_55_record(p_controller_obj)
        elif l_cmd == 0x56: linkDecode.decode_56(p_controller_obj)
        elif l_cmd == 0x57: self.m_link.decode_57()
        elif l_cmd == 0x58: linkDecode.decode_58(p_controller_obj)
        elif l_cmd == 0x60: l_ret = self._decode_60_record(p_controller_obj)
        elif l_cmd == 0x61: l_ret = self._decode_61_record(p_controller_obj)
        elif l_cmd == 0x62: l_ret = self._decode_62_record(p_controller_obj)
        elif l_cmd == 0x64: l_ret = self._decode_64_record(p_controller_obj)
        elif l_cmd == 0x65: l_ret = self._decode_65_record(p_controller_obj)
        elif l_cmd == 0x69: l_ret = self._decode_69_record(p_controller_obj)
        elif l_cmd == 0x6A: l_ret = self._decode_6A_record(p_controller_obj)
        elif l_cmd == 0x6B: l_ret = self._decode_6B_record(p_controller_obj)
        elif l_cmd == 0x6C: l_ret = self._decode_6C_record(p_controller_obj)
        elif l_cmd == 0x6F: l_ret = self._decode_6F_record(p_controller_obj)
        elif l_cmd == 0x73: l_ret = self._decode_73_record(p_controller_obj)
        else:
            LOG.error("Unknown message {}, Cmd:{}".format(PrintBytes(p_controller_obj._Message), l_cmd))
            # self.check_for_more_decoding(p_controller_obj, l_ret)
        self.check_for_more_decoding(p_controller_obj, l_ret)
        return l_ret



    def _publish(self, p_pyhouse_obj, p_device_obj):
        l_topic = "lighting/{}/info".format(p_device_obj.Name)
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_device_obj)  #  /lighting/{}/info

    def _decode_50(self, p_controller_obj):
        """ Insteon Standard Message Received (11 bytes)
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
        l_device_obj = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        if l_device_obj.DeviceType == 2:
            Insteon_HVAC.ihvac_utility().decode_50_record(self.m_pyhouse_obj, l_device_obj, p_controller_obj)
            return
        l_flags = utilDecode._decode_message_flag(l_message[8])
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_data = [l_cmd1, l_cmd2]
        l_debug_msg = 'Std-Msg-fm:"{}"; Flags:{}; Cmd1:{:#x}, Cmd2:{:#x}; '.format(l_device_obj.Name, l_flags, l_cmd1, l_cmd2)
        #
        #  Break down bits 7(msb), 6, 5 into message type
        #
        if l_message[8] & 0xE0 == 0x80:  #  100 - SB [Broadcast]
            l_debug_msg += utilDecode._devcat(l_message[5:7], l_device_obj)
        #
        elif l_message[8] & 0xE0 == 0xC0:  #  110 - SA Broadcast = all link broadcast of group id
            l_group = l_message[7]
            l_debug_msg += 'All-Link-brdcst-Group:"{}", Data:"{}"; '.format(l_group, l_data)
            # LOG.info("== 50B All-link Broadcast Group:{}, Data:{} ==".format(l_group, l_data))
        #
        try:
            if l_cmd1 == MESSAGE_TYPES['product_data_request']:  #  0x03
                l_debug_msg += " Product-data-request."

            elif l_cmd1 == MESSAGE_TYPES['engine_version']:  #  0x0D
                l_device_obj.EngineVersion = l_cmd2
                l_debug_msg += 'Engine-version:"{}"; '.format(l_cmd2)
                # self._publish(self.m_pyhouse_obj, l_device_obj)

            elif l_cmd1 == MESSAGE_TYPES['id_request']:  #  0x10
                l_debug_msg += 'Request-ID-From:"{}"; '.format(l_device_obj.Name)

            elif l_cmd1 == MESSAGE_TYPES['on']:  #  0x11
                l_device_obj.CurLevel = 100
                l_debug_msg += 'Device:"{}"-turned-Full-ON; '.format(l_device_obj.Name)
                # self._publish(self.m_pyhouse_obj, l_device_obj)

            elif l_cmd1 == MESSAGE_TYPES['off']:  #  0x13
                l_device_obj.CurLevel = 0
                l_debug_msg += 'Device:"{}"-turned-Full-OFF; '.format(l_device_obj.Name)
                # self._publish(self.m_pyhouse_obj, l_device_obj)

            elif l_cmd1 == MESSAGE_TYPES['status_request']:  #  0x19
                l_level = int(((l_cmd2 + 2) * 100) / 256)
                l_device_obj.CurLevel = l_level
                l_debug_msg += 'Status of light:"{}"-level:"{}"; '.format(l_device_obj.Name, l_level)
                # LOG.info("PLM:{} Got Light Status From:{}, Level is:{} ".format(p_controller_obj.Name, l_device_obj.Name, l_level))

            elif l_cmd1 >= MESSAGE_TYPES['thermostat_temp_up'] and l_cmd1 <= MESSAGE_TYPES['thermostat_report']:  #  0x6e
                Insteon_HVAC.ihvac_utility().decode_50_record(l_device_obj, l_cmd1, l_cmd2)

            elif l_cmd1 >= 0x68 and l_cmd1 <= 0x75:  #  0x6e
                Insteon_HVAC.ihvac_utility().decode_50_record(l_device_obj, l_cmd1, l_cmd2)

            elif l_message[8] & 0xE0 == 0x80 and l_cmd1 == 01:
                l_debug_msg += ' Device-Set-Button-Pressed '

            elif l_message[8] & 0xE0 == 0x80 and l_cmd1 == 02:
                l_debug_msg += ' Controller-Set-Button-Pressed '

            else:
                l_debug_msg += '\n\tUnknown-type-last-command"{}"-"{}"; '.format(l_device_obj._Command1, PrintBytes(l_message))
                LOG.warn('Decoding 50 type {}'.format(l_debug_msg))

        except AttributeError as e_err:
            LOG.error('ERROR decoding 50 record {}'.format(e_err))

        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_device_obj)
        p_controller_obj.Ret = True
        LOG.info('{}'.format(l_debug_msg))
        return

    def _decode_51(self, p_controller_obj):
        """ Insteon Extended Message Received (25 bytes).
        See p 247 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj_from = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        _l_obj_to = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[5:8])
        _l_flags = l_message[8]
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_extended = "{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}.{:X}".format(
                    l_message[11], l_message[12], l_message[13], l_message[14], l_message[15], l_message[16], l_message[17],
                    l_message[18], l_message[19], l_message[20], l_message[21], l_message[22], l_message[23], l_message[24])
        if l_cmd1 == 0x03 and l_cmd2 == 0:  # Product Data request response
            l_product_key = self._get_addr_from_message(l_message, 12)
            l_devcat = l_message[15] * 256 + l_message[16]
            LOG.info('ProdData Fm:"{}"; ProductID:"{}"; DevCat:"{}"; Data:"{}"'.format(l_obj_from.Name, l_product_key, l_devcat, l_extended))
            l_obj_from.ProductKey = l_product_key
            l_obj_from.DevCat = l_devcat
        p_controller_obj.Ret = True
        Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_obj_from)
        return

    def _decode_52_record(self, p_controller_obj):
        """Insteon X-10 message received (4 bytes).
        See p 253 of developers guide.
        """
        LOG.warning("52 Resp: not decoded yet.")

    def _decode_55_record(self, p_controller_obj):
        """Insteon User Reset detected (2 bytes).
        See p 269 of developers guide.
        """
        l_debug_msg = "User Reset Detected! "
        p_controller_obj.Ret = linkDecode.decode_55(p_controller_obj)
        LOG.info("".format(l_debug_msg))

    def _decode_60_record(self, p_controller_obj):
        """Get Insteon Modem Info (9 bytes).
        See p 273 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        l_devcat = l_message[5]
        l_devsubcat = l_message[6]
        l_firmver = l_message[7]
        LOG.info("== 60 - Insteon Modem Info - DevCat={}, DevSubCat={}, Firmware={} - Name={}".format(l_devcat, l_devsubcat, l_firmver, l_obj.Name))
        if l_message[8] == ACK:
            Insteon_utils.update_insteon_obj(self.m_pyhouse_obj, l_obj)
            p_controller_obj.Ret = True
        else:
            LOG.error("== 60 - No ACK - Got {:#x}".format(l_message[8]))
            p_controller_obj.Ret = False
        return

    def _decode_61_record(self, p_controller_obj):
        """Get Insteon Modem Info (6 bytes).
        See p 254 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_cmd2 = l_message[4]
        l_ack = l_message[5]
        LOG.info("All-Link Ack - Group:{}, Cmd:{}, Bcst:{}, Ack:{}".format(l_grp, l_cmd1, l_cmd2, l_ack))
        if l_ack == ACK:
            p_controller_obj.Ret = True
        else:
            LOG.error("== 61 - No ACK - Got {:#x}".format(l_ack))
            p_controller_obj.Ret = False
        return

    def _decode_62_record(self, p_controller_obj):
        """Get response to Send Insteon standard-length message (9 bytes).
        Basically, a response to the 62 command.
        See p 230(243) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x62
        [2-4] = address
        [5] = message flags
        [6] = command 1
        [7] = command 2
        [8] = ACK/NAK

        [8] = User Data 1
        [9] = User Data 2
        [10] = User Data 3
        [11] = User Data 4
        [12] = User Data 5
        [13] = User Data 6
        [14] = User Data 7
        [15] = User Data 8
        [16] = User Data 9
        [17] = User Data 10
        [18] = User Data 11
        [19] = User Data 12
        [20] = User Data 13
        [21] = User Data 14
        [22] = ACK/NAK
        This is an ack/nak of the command and generally is not very interesting by itself.
        Depending on the command sent, another response MAY follow this message with further data.
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[2:5])
        _l_msgflags = utilDecode._decode_message_flag(l_message[5])
        l_ack = utilDecode.get_ack_nak(l_message[8])
        l_debug_msg = "Device: {}, {}".format(l_obj.Name, l_ack)
        if l_ack == 'NAK':
            LOG.info("Got ACK(62); {}".format(l_debug_msg))
        return

    def _decode_64_record(self, p_controller_obj):
        p_controller_obj.Ret = linkDecode.decode_64(p_controller_obj)
        return

    def _decode_65_record(self, p_controller_obj):
        p_controller_obj.Ret = linkDecode.decode_65(p_controller_obj)
        return

    def _decode_67_record(self, p_controller_obj):
        """Reset IM ACK response (3 bytes).
        See p 258 of developers guide.
        """
        l_message = p_controller_obj._Message
        l_ack = utilDecode.get_ack_nak(l_message[2])
        l_debug_msg = "Reset IM(PLM) {}".format(l_ack)
        LOG.info("{}".format(l_debug_msg))
        return

    def _decode_69_record(self, p_controller_obj):
        p_controller_obj.Ret = linkDecode.decode_69(p_controller_obj)
        return

    def _decode_6A_record(self, p_controller_obj):
        p_controller_obj.Ret = linkDecode.decode_6A(p_controller_obj)
        return

    def _decode_6B_record(self, p_controller_obj):
        """Get set IM configuration (4 bytes).
        See p 258(271) of 2009 developers guide.
        [0] = x02
        [1] = 0x6B
        [2] = Flags
        [3] = ACK/NAK
         """
        l_message = p_controller_obj._Message
        l_flag = l_message[2]
        l_ack = utilDecode.get_ack_nak(l_message[3])
        l_debug_msg = "Config flag from PLM:{} - ConfigFlag:{:#02X}, {}".format(p_controller_obj.Name, l_flag, l_ack)
        LOG.info("Received from {}".format(l_debug_msg))
        if l_message[3] == ACK:
            p_controller_obj.Ret = True
        else:
            LOG.error("== 6B - NAK/Unknown message type {:#x}".format(l_flag))
            p_controller_obj.Ret = False
        return

    def _decode_6C_record(self, p_controller_obj):
        p_controller_obj.Ret = linkDecode.decode_6C(p_controller_obj)
        return

    def _decode_6F_record(self, p_controller_obj):
        """All-Link manage Record Response (12 bytes).
        See p 252(265) of 2009 developers guide.

        Modify the IM's All-Link Database (ALDB) with the All-Link data you send.
        Use caution with this command - the IM does not check the validity of the data you send.

        [0] = x02
        [1] = 0x6F
        [2] = Control Code
        [3] = All-Link Record Flag
        [4] = All Lpink Grou
        [5-7] = ID
        [8] = Link Data 1
        [9] = Link Data 2
        [10] = Link Data 3
        [11] = ACK/NAK
         """
        l_message = p_controller_obj._Message
        l_code = l_message[2]
        l_flags = l_message[3]
        l_flag_control = l_flags & 0x40
        l_group = l_message[4]
        l_obj = utilDecode.get_obj_from_message(self.m_pyhouse_obj, l_message[5:8])
        l_data = [l_message[8], l_message[9], l_message[10]]
        l_ack = utilDecode.get_ack_nak(l_message[11])
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        l_message = "Manage All-Link response(6F)"
        l_message += " Group:{:#02X}, Name:{}, Flags:{:#02X}, Data:{}, CtlCode:{:#02x},".format(l_group, l_obj.Name, l_flags, l_data, l_code)
        l_message += " Ack:{}, Type:{}".format(l_ack, l_type)
        LOG.info("{}".format(l_message))
        p_controller_obj.Ret = True
        return

    def _decode_73_record(self, p_controller_obj):
        """Get the PLM response of 'get config' (6 bytes).
        See p 257(270) of the 2009 developers guide.
        [0] = x02
        [1] = IM Control Flag
        [2] = Spare 1
        [3] = Spare 2
        [4] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        l_flags = l_message[2]
        l_spare1 = l_message[3]
        l_spare2 = l_message[4]
        l_ack = utilDecode.get_ack_nak(l_message[5])
        LOG.info("== 73 Get IM configuration Flags={:#x}, Spare 1={:#x}, Spare 2={:#x} {} ".format(
                    l_flags, l_spare1, l_spare2, l_ack))
        return

#  ## END DBK
