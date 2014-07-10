"""
-*- test-case-name: PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py -*-

@name: PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 27, 2013
@summary: This module is for Insteon conversion routines.

This is a bunch of routines to deal with Insteon devices.
Some convert things like addresses '14.22.A5' to a int for ease of handling.

"""

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

def int2message(p_int, p_message, p_index):
    """Place an Insteon address (int internally) into a message at a given offset.
    The message must exist and be long enough to include a 3 byte area for the address.
    """
    l_ix = 256 * 256
    while l_ix > 0:
        p_message[p_index], p_int = divmod(p_int, l_ix)
        l_ix = l_ix / 256
        p_index += 1
    return p_message

def dotted_hex2int(p_addr):
    """
    Convert A1.B2.C3 to int
    @param p_addr: is a 3 byte string with a format of 'A1.B2.3F'

    In case users get confused and use ':' as a separator, handle that too.
    """
    p_addr.replace(':', '.')
    l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_addr.split('.')])
    return int(l_hexn, 16)

def int2dotted_hex(p_int):
    """Convert 24 bit int to Dotted hex Insteon Address
    """
    l_ix = 256 * 256
    l_hex = []
    while l_ix > 0:
        l_byte, p_int = divmod(p_int, l_ix)
        l_hex.append("{0:02X}".format(l_byte))
        l_ix = l_ix / 256
    return '.'.join(l_hex)

# ## END DBK
