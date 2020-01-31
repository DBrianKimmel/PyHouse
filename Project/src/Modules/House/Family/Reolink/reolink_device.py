"""
@name:      /home/briank/workspace/PyHouse/Project/src/Modules/House/Family/Reolink/reolink_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 26, 2020
@summary:

"""

__updated__ = '2020-01-26'
__version_info__ = (20, 1, 26)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.reolink_device ')


class Api:
    """
    These are the public methods available to use Devices from any family.
    """

    m_plm_list = []
    m_hub_list = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        # p_pyhouse_obj.House._Commands['insteon'] = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadConfig(self):
        """
        """

    def Start(self):
        """
        """

    def SaveConfig(self):
        """
        """

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'pyhouse')

# ## END DBK
