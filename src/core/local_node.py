"""
@name: PyHouse/src/core/local_node.py

# -*- test-case-name: PyHouse.src.core.test.test_local_node -*-

Created on Apr 2, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: Gather this nodes information.

This module:
    Gathers the information about this node and saves it in PyHousesData.
"""


# Import system type stuff
import logging
import netifaces
import platform

from src.core.nodes import NodeData


g_debug = 0
g_logger = logging.getLogger('PyHouse.LocalNode   ')


class InterfaceData(object):
    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = True
        self.MacAddress = ''
        self.V4Address = []
        self.V6Address = []


class GetNodeInfo(object):
    """Get the information about this node and stick it in NodeData
    """
    def __init__(self, p_node):
        p_node.Name = platform.node()


class GetAllInterfaceData(object):
    """Loop thru all the interfaces and extract the info
    """
    def __init__(self, p_node):
        """
        @type p_node: C{NodeData}
        @param p_node: the node information
        """
        l_interfaces = netifaces.interfaces()
        l_count = 0
        global InterfacesData
        for l_ix in l_interfaces:
            l_interface = InterfaceData()
            l_interface.Name = l_ix
            l_interface.Key = l_count
            for l_af in netifaces.ifaddresses(l_ix):
                if netifaces.address_families[l_af] == 'AF_PACKET':
                    l_interface.MacAddress = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET':
                    l_interface.V4Address = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
                if netifaces.address_families[l_af] == 'AF_INET6':
                    l_interface.V6Address = self._get_list(netifaces.ifaddresses(l_ix)[l_af])
            if l_interface.V4Address == [] and l_interface.V6Address == []:
                continue
            g_logger.info("Interface:{0:}, Mac:{1:}, V4:{2:}, V6:{3:} - {4:}".format(l_interface.Name, l_interface.MacAddress, l_interface.V4Address, l_interface.V6Address, l_count))
            p_node.Interfaces[l_count] = l_interface
            l_count += 1

    def _get_list(self, p_list):
        l_list = []
        for l_ent in p_list:
            l_list.append(l_ent['addr'])
        return l_list


class Utility(object):

    def insert_node(self, p_node, p_pyhouses_obj):
        """The local node should always be node 0 - Do I want to force it ???
        """
        l_max_key = -1
        try:
            for l_node in p_pyhouses_obj.Nodes.itervalues():
                if l_node.Name == p_node.Name:
                    p_pyhouses_obj.Nodes[l_node.Key] = p_node
                    return
                if l_node.Key > l_max_key:
                    l_max_key = l_node.Key
        except AttributeError:
            pass
        p_pyhouses_obj.Nodes[l_max_key + 1] = p_node

        g_logger.debug('Nodes = {0:}'.format(p_pyhouses_obj.Nodes))


class API(Utility):

    m_node = None

    def __init__(self):
        self.m_node = NodeData()
        GetNodeInfo(self.m_node)
        GetAllInterfaceData(self.m_node)

    def Start(self, p_pyhouses_obj):
        self.insert_node(self.m_node, p_pyhouses_obj)

    def Stop(self):
        pass

# ## END DBK
