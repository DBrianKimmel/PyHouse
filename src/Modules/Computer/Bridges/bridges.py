"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/bridges.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-22'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges        ')


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the xml info.
        """
        LOG.info("Loading XML")

    def Start(self):
        LOG.info("Starting Bridges")
        pass

    def SaveXml(self, p_xml):
        LOG.info("Saved XML")
        l_xml = ET.Element('BridgesSection')
        p_xml.append(l_xml)
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
