"""
Created on Mar 1, 2014

@author: briank

This will set up this node and then find all other nodes in the same cluster (House).

Then start the House and all the sub systems.
"""


# Import system type stuff
import logging
import netifaces
import os

from src.entertain import entertainment
from src.communication import ir_control

g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


NODE_NOTHING = 0x0000
NODE_LIGHTS = 0x0001
NODE_PANDORA = 0x0002
NODE_CAMERA = 0x0004
NODE_PIFACECAD = 0x0008
NODE_V6ROUTER = 0x0010

InterfacesData = {}

class InterfaceData(object):
    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = False
        self.MacAddress = ''
        self.V4Address = ''
        self.V6Address = ''


class NodeRoleData(object):
    def __init__(self):
        self.CameraNode = False
        self.LightingNode = False
        self.PifaceCadNode = False
        self.PandoraNode = False


class FindAllInterfaceData(object):
    """Loop thru all the interfaces and extract the info
    """
    def __init__(self):
        l_interfaces = netifaces.interfaces()
        l_count = 0
        for l_interface in l_interfaces:
            if l_interface == 'lo':
                continue
# TODO: this only allows for one address per interface dur to the [0] below
            m_interface = InterfaceData()
            m_interface.Name = l_interface
            m_interface.Key = l_count
            for l_af in netifaces.ifaddresses(l_interface):
                # print "     Link ", l_interface, netifaces.address_families[l_af], netifaces.ifaddresses(l_interface)[l_af]
                if netifaces.address_families[l_af] == 'AF_PACKET':
                    m_interface.MacAddress = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
                if netifaces.address_families[l_af] == 'AF_INET':
                    m_interface.V4Address = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
                if netifaces.address_families[l_af] == 'AF_INET6':
                    m_interface.V6Address = netifaces.ifaddresses(l_interface)[l_af][0]['addr']
            g_logger.info("Interface:{0}, Mac:{1:}, V4:{2:}, V6:{3:}".format(m_interface.Name, m_interface.MacAddress, m_interface.V4Address, m_interface.V6Address))
            InterfacesData[l_count] = m_interface
            l_count += 1
        pass


class HandleNodeType(object):

    def __init__(self):
        self.find_node_type()
        self.init_node_type()

    def find_node_type(self):
        self.m_node = NODE_NOTHING
        # Test for lights
        if os.path.exists('/dev/ttyUSB0'):
            self.m_node |= NODE_LIGHTS
        # Test for Pandora
        if os.path.exists('/usr/bin/pianobar'):
            self.m_node |= NODE_PANDORA
        # Test for camera
        # Test for PifaceCAD
        if os.path.exists('/dev/lirc0'):
            self.m_node |= NODE_PIFACECAD

    def init_node_type(self):
        if self.m_node & NODE_PIFACECAD:
            self.init_ir_control()

    def init_ir_control(self, p_pyhouses_obj):
        """This node has an IR receiver so set it up.
        """
        pass


class FindRouter(object):
    pass


class LocateLocalNodes(object):
    """Find nodes in this house
    """
    def __init__(self):
        pass


class API(object):

    m_entertainment = None
    m_node = None

    def __init__(self):
        self.m_node = HandleNodeType()
        self.m_entertainment = entertainment.API()
        FindAllInterfaceData()
        LocateLocalNodes()
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        self.m_node.init_node_type(p_pyhouses_obj)
        # House
        # SubSystems
        self.m_entertainment.Start(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self):
        # SubSystems
        _l_entertainment_xml = self.m_entertainment.Stop()
        # House
        g_logger.info("Stopped.")

    def _UpdateXml (self, p_xml):
        pass


# ## END DBK
