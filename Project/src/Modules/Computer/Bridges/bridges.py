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

__updated__ = '2018-01-05'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Bridges.bridges_xml import Xml as bridgesXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges        ')


class API(object):
    """This interfaces to all of PyHouse.
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the xml info.
        """
        l_bridges = bridgesXML().read_bridges_xml(p_pyhouse_obj, self)
        p_pyhouse_obj.Computer.Bridges = l_bridges
        LOG.info("Loaded XML")

    def Start(self):
        l_count = 0
        LOG.info("Starting Bridges")
        for l_bridge in self.m_pyhouse_obj.Computer.Bridges.values():
            if not l_bridge.Active:
                LOG.info('Skipping not active bridge: {}'.format(l_bridge.Name))
                continue
            if l_bridge.Type == 'Hue':
                # Atempt to not load unless used
                from Modules.Families.Hue.Hue_hub import HueHub
                LOG.info('Hue Bridge Active: {}'.format(l_bridge.Name))
                HueHub(self.m_pyhouse_obj).HubStart(l_bridge)
            else:
                LOG.info('Other Bridge Active: {}'.format(l_bridge.Name))
            l_count += 1

    def SaveXml(self, p_xml):
        """ Generate the Bridges XML branch, Append it to the PyHouse XML tree.

        @param p_xml: the XML tree that we will eventually write to disk.
        """
        l_xml = bridgesXML().write_bridges_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)  # Add the bridges branch to the tree,
        LOG.info("Saved XML")
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
