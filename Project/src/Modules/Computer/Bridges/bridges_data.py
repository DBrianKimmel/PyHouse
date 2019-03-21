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

__updated__ = '2019-03-20'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges_Data   ')


class BridgesData(object):
    """
    ==> PyHouse.Computer.Bridges.
    """

    def __init__(self):
        super(BridgesData, self).__init__()
        Bridges = {}


class BridgeData(BaseUUIDObject):
    """
    ==> PyHouse.Computer.Bridges[x].xxx as below
    """

    def __init__(self):
        super(BridgeData, self).__init__()
        Connection = None  # 'Ethernet, Serial, USB
        Type = None  # Insteon, Hue
        IPv4Address = '9.8.7.6'
        Tcp_port = None
        UserName = None
        Password = None
        _Queue = None

# ## END DBK
