"""
-*- test-case-name: PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py -*-

@name:      PyHouse/src/Modules/Housing/Entertainment/entertainment_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Mar 18, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-08-08'


class EntertainmentData:
    """

    ==> PyHouse.House.Entertainment.xxx as in the def below.
    """

    def __init__(self):
        self.Onkyo = None
        self.Panasonic = None
        self.Pandora = None
        self.Pioneer = None
        self.Samsung = None
        self.Sharp = None
        self.Sony = None


class EntertainmentDeviceControl:
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        self.Channel = None  # '01'
        self.Direction = None  # 'F'  # F or R
        self.Input = None  # '01'  # Input ID
        self.Power = None  # 'Off'  # On or Off which is standby
        self.Volume = None  # '0'  # 0-100 - Percent
        self.Zone = None  # '1'  # For multi zone output

# ## END DBK
