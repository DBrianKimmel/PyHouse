"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/bridges.py -*-

@name:      PyHouse/src/Modules/Computer/Bridges/bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:   The entry point for dealing with bridges.

Bridges may be attached locally (USB) or via the network (Ethernet, WiFi).

Locally attached are generally controllers.

"""

__updated__ = '2017-12-27'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Bridges.bridges_xml import Xml as bridgesXML
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
        bridgesXML().read_bridges_xml(p_pyhouse_obj, self)
        LOG.info("Loaded XML")

    def Start(self):
        LOG.info("Starting Bridges")
        pass

    def SaveXml(self, p_xml):
        """ Generate the Bridges XML branch, Append it to the PyHouse XML tree.

        @param p_xml: the XML tree that we will eventually write to disk.
        """
        l_xml = bridgesXML().write_bridges_xml(self.m_pyhouse_obj, self)
        p_xml.append(l_xml)  # Add the bridges branch to the tree,
        LOG.info("Saved XML")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
