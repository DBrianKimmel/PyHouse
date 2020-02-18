"""
@name:      Modules/House/Family/insteon/insteon_hub.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2020 by D. Brian Kimmel
@note:      Created on Oct 27, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2020-02-17'

#  Import system type stuff

#  Import PyMh files

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_hub    ')


class Api:

    m_controller_obj = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj

    def LoadConfig(self):
        LOG.info('Loaded.')

    def Start(self):
        LOG.info('Started.')

    def SaveConfig(self):
        LOG.info('Saved Config')

    def Stop(self):
        LOG.info('Stopped.')

    def Control(self, p_device_obj, p_controller_obj, p_control):
        """
        @param p_controller_obj: optional
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params ==> Modules.House.Lighting.Lights.lights.Light Data()
        """
        LOG.info('Controlled.')

# ## END DBK
