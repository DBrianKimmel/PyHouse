"""
@name:      Modules/House/Family/Insteon/Insteon_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module contains data definition for Insteon devices.

"""

__updated__ = '2019-09-07'

#  Import system type stuff

#  Import PyMh files


class InsteonData(object):
    """ This is the Insteon specific data.
    It will be added into device objects that are Insteon.
    """

    def __init__(self):
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.EngineVersion = 2
        self.FirmwareVersion = 0
        self.GroupList = ''
        self.GroupNumber = 0
        self.InsteonAddress = 0  # Long integer internally - '1A.B3.3C' for external reaability
        self.ProductKey = ''  # 3 bytes
        self.Links = {}


class InsteonQueueInformation:

    def __init__(self):
        self.Command = None
        self.Text = None

#  ## END DBK
