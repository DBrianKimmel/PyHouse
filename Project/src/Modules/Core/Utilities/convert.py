"""
-*- test-case-name: PyHouse.Project.src.Modules.Utility.test.test_convert -*-

@Name:      PyHouse/Project/src/Modules.Core.Utilities.convert.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 3, 2013
@summary:   This module determines the IP address of the ISP connection.


Utility routines to convert external readable numbers to integers for ease in comparing.
"""

__updated__ = '2019-01-29'

# Import system type stuff
import datetime
import math
import netaddr
# import ipaddress

# Import PyMh files and modules.


def _makeHex(p_int):
    """ convert an int to 2 hex digits
    """
    l_int = p_int & 0xff
    l_hex = "{:02X}".format(l_int)
    return l_hex


def str_to_long(p_str):
    """ If we get an error - just return a None
    Handle IP V-4 32 bit numbers or V6 128 bit numbers
    '192.168.1.54' == 3232235830L
    '2001:db8::1' == 42540857365213159232363542340108812289L
    """
    try:
        l_long = int(netaddr.IPAddress(p_str))
    except:
        l_long = None
    return l_long


def long_to_str(p_int):
    """ If we get an error - just return a None
    Handle IP V-4 32 bit numbers or V6 128 bit numbers
    '192.168.1.54' == 3232235830L
    '2001:db8::1' == 42540857365213159232363542340108812289L
    """
    try:
        l_str = str(netaddr.IPAddress(p_int))
    except:
        l_str = None
    return l_str


def datetime_to_seconds(p_datetime):
    """ Converts a datetime to seconds
    @param p_datetime: is a datetime.datetime object
    @return: an int of the time portion of the datetime
    """
    return (((p_datetime.hour * 60) + p_datetime.minute) * 60 + p_datetime.second)


def _get_factor(p_size):
    """Internal utility to get a power of 256 (1 byte)
    """
    if p_size <= 1:
        return 0
    return int(math.pow(256, (p_size - 1)))


def _get_int(p_str):
    """ Internal utility to convert 2 hex chars into a 1 byte int.
    a3 --> 163
    """
    l_int = 0
    try:
        l_int = int(p_str, 16)
    except:
        l_int = 0
    return l_int


def dotted_hex2int(p_hex):
    """
    @param p_hex: is a str like 'A1.B2.C3'
    @return: an int

    Routine for taking a readable insteon type address and converting it to a Long int for internal use.
    """
    # print(p_hex)
    p_hex = p_hex.replace(':', '.')
    # print(p_hex)
    l_ary = p_hex.split('.')
    l_hexn = ''.join(["%02X" % _get_int(l_ix) for l_ix in l_ary])
    return int(l_hexn, 16)


def int2dotted_hex(p_int, p_size):
    """
    @param p_int: is the integer to convert to a dotted hex string such as 'A1.B2' or 'C4.D3.E2'
    @param p_size: is the number of bytes to convert - either 2 or 3
    """
    l_ix = _get_factor(p_size)

    l_hex = []
    l_int = int(p_int)
    try:
        while l_ix > 0:
            l_byte, l_int = divmod(l_int, l_ix)
            l_hex.append("{:02X}".format(l_byte))
            l_ix = int(l_ix / 256)
        return str('.'.join(l_hex))
    except (TypeError, ValueError) as e_err:
        LOG.error('ERROR in converting int to dotted Hex {} {} - Type:{} - {}'.format(p_int, l_ix, type(p_int), e_err))

# ## END DBK
