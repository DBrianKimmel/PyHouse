"""
@name:      Modules/House/Family/sonoff/sonoff_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Aug 19, 2019
@license:   MIT License
@summary:   This module is for Insteon

"""

__updated__ = '2019-10-15'
__version_info__ = (19, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.sonoff_device  ')


class SonoffInformation:
    """
    """

    def __init__(self):
        """
        """
        self.Name = None


class Config:
    """
    This class and methods are pointed to by family.py and must be the same in every Device package.
    """


class Api:
    """
    These are the public methods available to use Devices from any family.
    """

    m_plm = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Created an instance of sonoff_device.')

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config')

    def Start(self):
        """
        """
        LOG.info('Starting.')

# ## END DBK
