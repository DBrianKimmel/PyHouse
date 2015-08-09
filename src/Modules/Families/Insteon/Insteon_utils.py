"""
-*- test-case-name: PyHouse/src/Modules/Families/Insteon/test/test_Insteon_utils.py -*-

@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 27, 2013
@summary:   This module is for Insteon conversion routines.

This is a bunch of routines to deal with Insteon devices.
Some convert things like addresses '14.22.A5' to a int for ease of handling.

"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon.Insteon_constants import InsteonError

LOG = Logger.getLogger('PyHouse.Insteon_Utils  ')


class Util(object):

    @staticmethod
    def int2message(p_int, p_message, p_index = 3):
        """Place an Insteon address (int internally) into a message at a given offset.
        The message must exist and be long enough to include a 3 byte area for the address.
        """
        if p_int > 16777215 or p_int < 0:
            l_msg = 'ERROR - Insteon_utils - trying to convert {} to message byte string.'.format(p_int)
            LOG.error(l_msg)
            p_int = 12245933  # 0xBADBAD
        l_ix = 256 * 256
        l_int = p_int
        while l_ix > 0:
            p_message[p_index], l_int = divmod(l_int, l_ix)
            l_ix = l_ix / 256
            p_index += 1
        return p_message

    @staticmethod
    def message2int(p_message, p_index):
        """Extract the address (3 bytes) from a response message.
        The message is a byte array returned from the PLM.
        Return a 24 bit int that is the address.
        """
        try:
            l_int = p_message[p_index] * 256 * 256 + p_message[p_index + 1] * 256 + p_message[p_index + 2]
        except IndexError:
            l_int = 0
        return l_int

    @staticmethod
    def get_json_data(l_obj, l_json):
        l_obj.DevCat = int(l_json['DevCat'])
        l_obj.GroupList = l_json['GroupList']
        l_obj.GroupNumber = l_json['GroupNumber']
        l_obj.InsteonAddress = int(l_json['InsteonAddress'])
        l_obj.IsMaster = l_json['IsMaster']
        l_obj.ProductKey = int(l_json['ProductKey'])
        return l_obj

# ## END DBK
