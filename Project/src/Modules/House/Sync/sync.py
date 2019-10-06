"""
@name:      Modules/House/Sync/sync.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Mar 24, 2018
@license:   MIT License
@summary:   Sync the house info

Send a Mqtt message asking for all house info
Try to tell what version is the master (Latest?)
If multiple house UUISs match - one of them is master and any/all different ones should update to master

"""

__updated__ = '2019-10-06'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Sync           ')


class Api(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadConfig(self):
        """ Load the XML.
        """
        LOG.info("Loaded Config")

    def Start(self):
        """
        """
        LOG.info("Start")
        pass

    def SaveConfig(self):
        LOG.info("Saved Sync Config.")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
