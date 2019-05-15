"""
-*- test-case-name: PyHouse.src.Modules.Computer.Nodes.test.XXtest_nodes -*-

@name:      PyHouse/Project/src/Modules/Computer/Nodes/nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 6, 2014
@summary:   This module does everything for nodes.

Nodes are read in from the config Xml file.

Then node local is run to update the local node

Finally, the nodes are synced between each other.

"""

__updated__ = '2019-05-13'
__version_info__ = (18, 10, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer.Nodes.node_local import API as localAPI
from Modules.Computer.Nodes.node_sync import API as syncAPI
from Modules.Computer.Nodes.nodes_xml import Xml as nodesXml

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Nodes          ')


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_local = localAPI(p_pyhouse_obj)
        self.m_sync = syncAPI(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized - Version:{}'.format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Node xml info.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        l_nodes = nodesXml.read_all_nodes_xml(p_pyhouse_obj)
        p_pyhouse_obj.Computer.Nodes = l_nodes
        LOG.info('Loaded XML - Version:{}'.format(__version__))
        return l_nodes

    def Start(self):
        self.m_local.Start()
        self.m_sync.Start()
        LOG.info('Started - Version:{}'.format(__version__))

    def SaveXml(self, p_xml):
        l_xml, l_count = nodesXml.write_nodes_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML for {} nodes.".format(l_count))
        return l_xml  # For testing

    def Stop(self):
        self.m_local.Stop()
        self.m_sync.Stop()

#  ## END DBK
