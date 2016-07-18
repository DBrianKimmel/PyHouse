"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_Link -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_Link.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2016 by D. Brian Kimmel
@note:      Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license:   MIT License
@summary:   Handle the all-link database(s) in Insteon devices.

This will maintain the all-link database in all Insteon devices.

Invoked periodically and when any Insteon device changes.
"""

__updated__ = '2016-07-17'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon.Insteon_constants import ACK
from Modules.Families.Insteon.Insteon_utils import Decode as utilDecode
LOG = Logger.getLogger('PyHouse.Insteon_Link   ')


class LinkData(object):
    """
    """

    def __init__(self):
        self.Addess = 12345  #  3 bytes
        self.Control = 0x0000  #  2 Bytes
        self.Data = '00.00.00'  #  3 bytes
        self.Flag = 0xC2
        self.Group = 0


class Send(object):
    """
    """


class Decode(object):
    """
    """

    @staticmethod
    def decode_53(p_controller_obj):
        """Insteon All-Linking completed (10 bytes).
        See p 245(258) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_link_code = l_message[2]
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        utilDecode._devcat(l_message[7:9], p_controller_obj)
        LOG.info('All-Linking completed {}, Group:{}, From:{} '.format(l_link_code, l_link_group, l_from_id))
        return False

    @staticmethod
    def decode_54(p_controller_obj):
        """Insteon Button Press event (3 bytes).
        The PLM set button was pressed.
        See p 260(273 of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_event = l_message[2]
        LOG.info('The Set button was pressed {}'.format(l_event))
        return False

    @staticmethod
    def decode_56(p_controller_obj):
        """Insteon All-Link cleanup failure report (7 bytes).
        See p 241(254 of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_link_code = l_message[2]
        l_link_group = l_message[3]
        l_from_id = l_message[4:7]
        LOG.info('All-Linking failed {}, Group:{}, From:{} '.format(l_link_code, l_link_group, l_from_id))
        return False

    @staticmethod
    def decode_57(p_pyhouse_obj, p_controller_obj):
        """All-Link Record Response (10 bytes).
        See p 249)(262 of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_obj = utilDecode.get_obj_from_message(p_pyhouse_obj, l_message[4:7])
        l_link_obj = LinkData()
        l_link_obj.Flag = l_flags = l_message[2]
        l_link_obj.Group = l_group = l_message[3]
        l_link_obj.InsteonAddess = l_obj.InsteonAddress
        l_link_obj.Data = l_data = [l_message[7], l_message[8], l_message[9]]
        l_flag_control = l_flags & 0x40
        l_type = 'Responder'
        if l_flag_control != 0:
            l_type = 'Controller'
        LOG.info("All-Link response-57 - Group={:#02X}, Name={}, Flags={:#x}, Data={}, {}".format(l_group, l_obj.Name, l_flags, l_data, l_type))
        l_ret = True
        return l_ret

    @staticmethod
    def decode_58(p_controller_obj):
        """Insteon All-Link cleanup status report (3 bytes).
        See p 242(255) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Linking cleanup {}, Group:{}, From:{} '.format(l_status))
        return False

    @staticmethod
    def decode_64(p_controller_obj):
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
    def decode_65(p_controller_obj):
        """All-Link Cancel response (5 bytes).
        See p 244(257) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        l_status = l_message[2]
        LOG.info('All-Linking cancel {}, Group:{}, From:{} '.format(l_status))
        return False

    @staticmethod
    def decode_69(p_controller_obj):
        """Get All-Link First Record response (5 bytes).
        See p 244(257) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        LOG.info("All-Link first record - ACK")
        if l_message[2] == ACK:
            l_ret = True
            Send.queue_6A_command(p_controller_obj)
        else:
            LOG.info("All-Link first record - NAK")
            l_ret = False
        return l_ret

    @staticmethod
    def decode_6A(p_controller_obj):
        """All-Link Next Record response (3 bytes).
        See p 247(260) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        LOG.info("All-Link Next record - ACK")
        if l_message[2] == ACK:
            l_ret = True
            Send.queue_6A_command()
        else:
            LOG.info("All-Link Next record - NAK")
            l_ret = False
        return l_ret

    @staticmethod
    def decode_6C(p_controller_obj):
        """All-Link Record For Sender  response (3 bytes).
        See p 248(261) of 2007 developers guide.
        """
        l_message = p_controller_obj._Message
        LOG.info("All-Link Record for sender record - ACK")
        if l_message[2] == ACK:
            l_ret = True
        else:
            LOG.info("All-Link Record for sender record - NAK")
            l_ret = False
        return l_ret


class API(object):
    """
    """


#  ## END DBK
