"""
-*- test-case-name: PyHouse.src.Modules.Housing.Sync.test.test-sync -*-

@name:      PyHouse/src/Modules/Housing/Sync/sync.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Mar 24, 2018
@license:   MIT License
@summary:   Sync the house info

Send a Mqtt message asking for all house info
Try to tell what version is the master (Latest?)
If multiple house UUISs match - one of them is master and any/all different ones should update to master

"""

__updated__ = '2018-10-01'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Sync           ')


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the XML.
        """
        LOG.info("Loading XML")
        LOG.info("Loaded XML")

    def Start(self):
        """
        """
        LOG.info("Start")
        pass

    def SaveXml(self, p_xml):
        LOG.info("Saved Mqtt XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
