"""
@name:      PyHouse/Project/src/Modules/Core/Mqtt/state.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created Jul 23, 2018
@Summary:

"""

__updated__ = '2019-01-07'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.State          ')


class State(object):
    UNKNOWN = 'unknown'
    OCCUPIED = 'occupied'
    VACANT = 'vacant'
    ON = 'on'
    OFF = 'off'
    MOTION = 'motion'
    STILL = 'still'
    OPEN = 'open'
    CLOSED = 'closed'

# ## END DBK
