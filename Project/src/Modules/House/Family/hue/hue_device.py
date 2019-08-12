"""
@name:      Modules/House/Family/Hue/Hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-08-10'

# Import system type stuff

# Import PyMh files
from Modules.House.Family.hue.hue_hub import HueHub

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_device     ')


class API(object):
    """
    """

    m_pyhouse_obj = None
    m_hue_hub = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_hue_hub = HueHub(p_pyhouse_obj)
        LOG.info('Initialized')

    def LoadConfig(self):
        """
        """
        LOG.info('Loading')
        # HueHub(self.m_pyhouse_obj).Start(p_pyhouse_obj)

    def Start(self):
        """
        """
        # if self.m_pyhouse_obj.Computer != {}:
        # self.m_hue_hub.Start()
        LOG.info('Started')

    def SaveConfig(self):
        """ Handled by Bridges
        """
        return

    def ControlDevice(self, p_device_obj, p_bridge_obj, p_control):
        """ Control some device using the Philips Hue HUB.
        @param p_device_obj: is the device being controlled.
        @param p_bridge_obj: is the HUB
        @param p_control: is the generic control actions to be performed on the device
        """
        pass

# ## END DBK
