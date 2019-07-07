"""
-*- test-case-name: PyHouse/src/Modules/Computer/Bridges/bridges_data.py -*-

@name:      PyHouse/src/Modules/Computer/Bridges/bridges_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 23, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-07-05'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges_Data   ')


class BridgesInformation(object):
    """
    ==> PyHouse.Computer.Bridges.
    """

    def __init__(self):
        super(BridgesInformation, self).__init__()
        self.Bridges = {}


class BridgeData(BaseUUIDObject):
    """
    ==> PyHouse.Computer.Bridges[x].xxx as below
    """

    def __init__(self):
        super(BridgeData, self).__init__()
        self.Connection = None  # 'Ethernet, Serial, USB
        self.Type = None  # Insteon, Hue
        self.IPv4Address = '9.8.7.6'
        self.Tcp_port = None
        self.UserName = None
        self.Password = None
        self._Queue = None

# ## END DBK
