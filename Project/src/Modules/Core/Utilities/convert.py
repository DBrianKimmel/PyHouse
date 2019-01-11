"""
-*- test-case-name: PyHouse.src.Modules.Utility.test.test_convert -*-

@Name:      PyHouse/Project/src/Modules.Core.Utilities.convert.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 3, 2013
@summary:   This module determines the IP address of the ISP connection.


Utility routines to convert external readable numbers to integers for ease in comparing.
"""

__updated__ = '2019-01-11'

# Import system type stuff
import re
import netaddr
import ipaddress

"""
Handle IP V-4 32 bit numbers or V6 128 bit numbers
'192.168.1.54' == 3232235830L
'2001:db8::1' == 42540857365213159232363542340108812289L
"""


def str_to_long(p_str):
    """ If we get an error - just return a None
    """
    try:
        l_long = int(netaddr.IPAddress(p_str))
    except:
        l_long = None
    return l_long


def long_to_str(p_int):
    try:
        l_str = str(netaddr.IPAddress(p_int))
    except:
        l_str = None
    return l_str

# ## END DBK
