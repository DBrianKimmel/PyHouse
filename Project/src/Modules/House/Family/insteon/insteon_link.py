"""
@name:      Modules/House/Family/insteon/insteon_link.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   Handle the all-link database(s) in Insteon devices.

This will maintain the all-link database in all Insteon devices.

Invoked periodically and when any Insteon device changes.
"""

__updated__ = '2019-09-07'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities import convert
from Modules.House.Family.insteon.insteon_data import InsteonData
from Modules.House.Family.insteon.insteon_constants import ACK
from Modules.House.Family.insteon import insteon_utils
from Modules.House.Family.insteon.insteon_utils import Decode as utilDecode

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_link   ')


class LinkData():
    """
    """

    def __init__(self):
        self.Addess = 12345  #  3 bytes
        self.Control = 0x0000  #  2 Bytes
        self.Data = '00.00.00'  #  3 bytes
        self.Flag = 0xC2
        self.Group = 0
        self.IsController = False


class Send():
    """
    """

    def queue_0x67_command(self, p_controller_obj):
        """Reset the PLM (2 bytes)
        Puts the IM into the factory reset state which clears the All-Link Database.
        See p 255(268) of 2009 developers guide.
        """
        LOG.info("Queue command to reset the PLM (67).")
        l_command = insteon_utils.create_command_message('plm_reset')
        insteon_utils.queue_command(p_controller_obj, l_command, 'Reset PLM')

    def queue_0x69_command(self, p_controller_obj):
        """Get the first all-link record from the plm (2 bytes).
        See p 248(261) of 2009 developers guide.
        """
        LOG.info("Command to get First all-link record (0x69).")
        l_command = insteon_utils.create_command_message('plm_first_all_link')
        insteon_utils.queue_command(p_controller_obj, l_command, 'First All-Link')

    def queue_0x6A_command(self, p_controller_obj):
        """Get the next all-link record from the plm (2 bytes).
        See p 249(262) of 2009 developers guide.
        """
        LOG.info("Command to get the next all-link record (0x6A).")
        l_command = insteon_utils.create_command_message('plm_next_all_link')
        insteon_utils.queue_command(p_controller_obj, l_command, 'Next All-Link')

    def queue_0x6F_command(self, p_controller_obj, p_light_obj, p_code, p_flag, p_data):
        """Manage All-Link Record (11 bytes)
         See p 252(265) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6F
        [2] = Control Code
        [3] = All-Link record flag
        [4] = All-Link ecord group
        [5-7] = 3 Byte Link to address
        [8] = Data
        [9] = Data
        [10] = Data
       """
        LOG.info("Command to manage all-link record (6F).")
        l_command = insteon_utils.create_command_message('manage_all_link_record')
        l_command[2] = p_code
        l_command[3] = p_flag
        l_command[4] = p_light_obj.GroupNumber
        insteon_utils.insert_address_into_message(p_light_obj.Family.Address, l_command, 5)
        l_command[8:11] = p_data
        insteon_utils.queue_command(p_controller_obj, l_command, 'Manage ALDB record')

    def read_aldb_v2(self, p_controller_obj):
        """
        """
        # LOG.debug(PrettyFormatAny.form(p_controller_obj, 'Controller'))
        l_command = bytearray(22)
        l_command[0] = 0x02
        l_command[1] = 0x62
        insteon_utils.insert_address_into_message(p_controller_obj.Family.Address, l_command, 2)
        l_command[5] = 0x13
        l_command[6] = 0x2f  #  Cmd1
        l_command[7] = 0x00  #  Cmd2
        l_command[8] = 0x00  #  D1  Unused
        l_command[9] = 0x00  #  D2  Record request
        l_command[10] = 0x00  # D3  High Byte
        l_command[11] = 0x00  # D4  Low Byte
        l_command[12] = 0x00  # D5  All Records
        insteon_utils.queue_command(p_controller_obj, l_command, 'Query ALDB')


class Decode:
    """
    """

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj

    @staticmethod
    def decode_0x53(p_pyhouse_obj, p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 247(260) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x53
        [2] = LinkCode - 0=PLM is Responder, 1=PLM is Controller, FF=Deleted
        [3] = LinkGroup
        [4-6] = from address
        [7-8] = DevCat
        [9] = Firmwear Version
        """
        l_message = p_controller_obj._Message
        l_msg = insteon_utils.decode_link_code(l_message[2])
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        l_device_obj = utilDecode().get_obj_from_message(p_pyhouse_obj, l_from_id)
        utilDecode._devcat(l_message[7:9], p_controller_obj)
        _l_version = l_message[9]
        LOG.info('All-Linking completed - Link Code:{}, Group:{}, From:{} '.format(l_msg, l_link_group, l_device_obj.Name))

    @staticmethod
    def decode_0x54(_p_pyhouse_obj, p_controller_obj):
        """Insteon Button Press event (3 bytes).
        The PLM set button was pressed.
        See p 263(276) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x54
        [2] = Button Event
        """
        l_message = p_controller_obj._Message
        l_event = l_message[2]
        LOG.info('The Set button was pressed {}'.format(l_event))

    @staticmethod
    def decode_0x55(_p_pyhouse_obj, p_controller_obj):
        """Insteon Reset Detected. (2 bytes)
        See p 256(269) of 2009 developers guide.

        Reports that the user manually put the IM into factory default state.
        Takes about 20 seconds to respond.

        [0] = 0x02
        [1] = 0x55
        """
        _l_message = p_controller_obj._Message
        LOG.info('The Set button was pressed')

    @staticmethod
    def decode_0x56(_p_pyhouse_obj, p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 243(256) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x56
        [2] = 0x01
        [3] = LinkGroup
        [4-6] = from address
        """
        l_message = p_controller_obj._Message
        l_link_code = l_message[2]
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        LOG.info('All-Linking failed {}, Group:{}, From:{} '.format(l_link_code, l_link_group, l_from_id))

    @staticmethod
    def decode_0x57(p_pyhouse_obj, p_controller_obj):
        """All-Link Record Response (10 bytes).
        See p 251(264) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x57
        [2] = AllLink Record Flags
        [3] = AllLink Group
        [4-6] = from address
        [7] = Link Data 1
        [8] = Link Data 2
        [9] = Link Data 3
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode().get_obj_from_message(p_pyhouse_obj, l_message[4:7])
        l_link_obj = LinkData()
        l_link_obj.Flag = l_flags = l_message[2]
        l_link_obj.Group = l_group = l_message[3]
        l_link_obj.InsteonAddess = l_obj.InsteonAddress
        l_link_obj.Data = l_data = [l_message[7], l_message[8], l_message[9]]
        l_flag_control = l_flags & 0x40
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
            l_link_obj.IsController = True
        LOG.info("All-Link response-0x57 - Group={:#02X}, Name={}, Flags={:#x}, Data={}, {}".format(l_group, l_obj.Name, l_flags, l_data, l_type))

        # Ask for next record
        Send().queue_0x6A_command(p_controller_obj)

        return

    @staticmethod
    def decode_0x58(_p_pyhouse_obj, p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 242(255) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Linking cleanup {}, Group:{}, From:{} '.format(l_status))

    @staticmethod
    def decode_0x64(_p_pyhouse_obj, p_controller_obj):
        """Start All-Link ACK response (5 bytes).
        See p 243(256) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_grp = l_message[2]
        l_cmd1 = l_message[3]
        l_ack = l_message[4]
        LOG.info("All-Link Ack - Group:{}, Cmd:{}, Ack:{}".format(l_grp, l_cmd1, l_ack))
        if l_ack == ACK:
            l_ret = True
        else:
            LOG.error("== 64 - No ACK - Got {:#x}".format(l_ack))
            l_ret = False
        return l_ret

    @staticmethod
    def decode_0x65(_p_pyhouse_obj, p_controller_obj):
        """All-Link Cancel response (5 bytes).
        See p 244(257) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Linking cancel {}, Group:{}, From:{} '.format(l_status))
        return False

    @staticmethod
    def decode_0x69(_p_pyhouse_obj, p_controller_obj):
        """Get All-Link First Record response (5 bytes).
        See p 248(261) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x69
        [2] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ack = 'ACK'
            Send().queue_0x6A_command(p_controller_obj)
        else:
            LOG.info("All-Link first record - NAK")
            l_ack = 'NAK'
        LOG.info("All-Link first record -{}".format(l_ack))
        return

    @staticmethod
    def decode_0x6A(_p_pyhouse_obj, p_controller_obj):
        """All-Link Next Record response (3 bytes).
        See p 249(262) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6A
        [2] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        if l_message[2] == ACK:
            l_ack = 'ACK'
            Send().queue_0x6A_command(p_controller_obj)
        else:
            l_ack = 'NAK'
        LOG.info("All-Link Next record - {}".format(l_ack))
        return

    @staticmethod
    def decode_0x6C(_p_pyhouse_obj, p_controller_obj):
        """All-Link Record for sender response (3 bytes).
        See p 250(263) of 2009 developers guide.
        [0] = 0x02
        [1] = 0x6C
        [2] = ACK/NAK
        """
        l_message = p_controller_obj._Message
        LOG.info("All-Link Record for sender record - ACK")
        if l_message[2] == ACK:
            l_ret = True
        else:
            LOG.info("All-Link Record for sender record - NAK")
            l_ret = False
        return l_ret


class InsteonAllLinks:

    def get_all_allinks(self, p_controller_obj):
        """A command to fetch the all-link database from the PLM
        """
        LOG.info("Get all All-Links from controller {}.".format(p_controller_obj.Name))
        # Send().queue_0x69_command(p_controller_obj)
        Send().read_aldb_v2(p_controller_obj)

        # Send.queue

    def add_link(self, p_link):
        """Add an all link record.
        """
        pass

    def delete_link(self, p_controller_obj, p_address, p_group, p_flag):
        """Delete an all link record.
        """
        #  p_light_obj = LightData()
        p_light_obj = InsteonData()
        p_light_obj.InsteonAddress = convert.dotted_hex2int(p_address)
        p_light_obj.GroupNumber = p_group
        #  p_code = 0x00  # Find First
        p_code = 0x00  #  Delete First Found record
        #  p_flag = 0xE2
        p_data = bytearray(b'\x00\x00\x00')
        LOG.info("Delete All-link record - Address:{}, Group:{:#02X}".format(p_light_obj.InsteonAddress, p_group))
        l_ret = Send().queue_0x6F_command(p_controller_obj, p_light_obj, p_code, p_flag, p_data)
        return l_ret

    def Xreset_plm(self, p_controller_obj):
        """This will clear out the All-Links database.
        """
        l_debug_msg = "Resetting PLM - Name:{}".format(p_controller_obj)
        Send().queue_0x67_command(p_controller_obj)
        LOG.info(l_debug_msg)


class API:
    """
    """

#  ## END DBK
