"""
@name:      Modules/Computer/weather.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2019 by D. Brian Kimmel
@note:      Created on Jan 20, 2014
@license:   MIT License
@summary:
"""

__updated__ = '2019-10-06'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Weather        ')


class Api:

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadConfig(self):
        pass

    def Start(self):
        pass

    def Stop(self):
        pass

    def SaveConfig(self):
        LOG.info('Saved XML.')

#  ## END DBK
