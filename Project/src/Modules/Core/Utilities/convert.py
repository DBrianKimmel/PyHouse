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

__updated__ = '2019-01-13'

# Import system type stuff
import datetime
import netaddr
# import ipaddress

# Import PyMh files and modules.


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

# ## END DBK
