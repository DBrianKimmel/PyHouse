"""
@name:      Modules/Core/Drivers/Ethernet/Ethernet_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Feb 18, 2010
@license:   MIT License
@summary:   This module is for driving ethernet devices

This will interface various PyHouse modules to an ethernet connected controller device.
"""

# Import system type stuff

# Import PyHouse modules
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.EthernetDriver ')


class SerialPortInformation:
    """ These have defaults values if not overridden.
    """

    def __init__(self):
        self.Type = 'Serial'
        self.Baud = 9600
        self.ByteSize = 8
        self.Parity = 'N'
        self.StopBits = 1.0
        #
        self.DsrDtr = False
        self.RtsCts = False
        self.Timeout = 1.0
        self.XonXoff = False


class Api(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info(" Initializing Ethernet Driver.")

    def Start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        LOG.info("Starting Ethernet port.")
        return None

    def Stop(self):
        pass

# ## END
