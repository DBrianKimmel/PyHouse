"""
@name:      Modules/Computer/Nodes/node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019  by D. Brian Kimmel
@note:      Created on Apr 2, 2014
@license:   MIT License
@summary:   Gather this node's information.

This module:
    Gathers information about the interfaces (ethernet, wifi etc.) on this node.
    Gathers information about the controller devices attached to this node.
    Gathers information about the specialized PyHouse software installed on this node.
    Saves all the gathered information in p_pyhouse_obj.
    Starts services on the local node (i.e. ir_service).

The discovered services may be fooled by non PyHouse devices plugged into the computer
  so it will be possible to override the role via configuration.
Once overridden the new role will "stick" by being written into the local XML file.
"""

__updated__ = '2019-10-31'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from datetime import datetime
import fnmatch  # Filename matching with shell patterns
import netifaces  # has gateways(), ifaddresses(). interfaces()
from netifaces import *
import os
import pyudev
import subprocess

#  Import PyMh files and modules.
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Core.Utilities.uuid_tools import Uuid as toolUuid

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeLocal      ')

__all__ = ['NODE_NOTHING', 'NODE_USB_CONTROLLER',
           'NODE_PANDORA', 'NODE_CAMERA',
           'NODE_PIFACECAD', 'NODE_V6ROUTER',
           'Api'
           ]

NODE_NOTHING = 0x0000  # a basic node with no special functions
NODE_USB_CONTROLLER = 0x0001  # Node has an attached controller for Lights (optionally other stuff)
NODE_PANDORA = 0x0002  # Node can use pianobar to receive Pandora streams
NODE_CAMERA = 0x0004  # Pi with attached camera (not USB camera)
NODE_PIFACECAD = 0x0008  #
NODE_V6ROUTER = 0x0010  # Iv6 Router node
NODE_NOT_UNIX = 0x0020  # Windows - not Linux
NODE_TUNNEL = 0x0040  # IPv6 Tunnel
NODE_IR = 0x0080  # Infrared receiver and optional transmitter
NODE_MQTT_BROKER = 0x0100


class InterfaceData():
    """
    """

    def __init__(self):
        self.InterfaceName = None


class Devices():
    """ Identify the controller devices attached to this node.

    Here we want to find out what device type controllers (eg Insteon PLM) may be attached to this node.
    We have looked at the node and select the udev characteristics that will identify the controller.
    Then we search for that signature to mark this node as having the device.
    In this way, we can get to the point where only the nodes having a control device can react and, say, turn on a light.
    """

    def _lsusb(self):
        l_ret = subprocess.check_output('lsusb')
        return l_ret

    def _find_controllers(self):
        """ Find out what controllers are attached to this node.

            DEVLINKS === /dev/serial/by-path/pci-0000:00:14.0-usb-0:3:1.0-port0 /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A403KF9V-if00-port0
            DEVNAME === /dev/ttyUSB0
            DEVPATH === /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/ttyUSB0/tty/ttyUSB0
            ID_BUS === usb
            ID_MM_CANDIDATE === 1
            ID_MODEL === FT232R_USB_UART
            ID_MODEL_ENC === FT232R\x20USB\x20UART
            ID_MODEL_FROM_DATABASE === FT232 Serial (UART) IC
            ID_MODEL_ID === 6001
            ID_PATH === pci-0000:00:14.0-usb-0:3:1.0
            ID_PATH_TAG === pci-0000_00_14_0-usb-0_3_1_0
            ID_PCI_CLASS_FROM_DATABASE === Serial bus controller
            ID_PCI_INTERFACE_FROM_DATABASE === XHCI
            ID_PCI_SUBCLASS_FROM_DATABASE === USB controller
            ID_REVISION === 0600
            ID_SERIAL === FTDI_FT232R_USB_UART_A403KF9V
            ID_SERIAL_SHORT === A403KF9V
            ID_TYPE === generic
            ID_USB_DRIVER === ftdi_sio
            ID_USB_INTERFACES === :ffffff:
            ID_USB_INTERFACE_NUM === 00
            ID_VENDOR === FTDI
            ID_VENDOR_ENC === FTDI
            ID_VENDOR_FROM_DATABASE === Future Technology Devices International, Ltd
            ID_VENDOR_ID === 0403
            MAJOR === 188
            MINOR === 0
            SUBSYSTEM === tty
            TAGS === :systemd:
            USEC_INITIALIZED === 61213086823
        """
        l_ret = ''
        l_context = pyudev.Context()
        for l_dev in l_context.list_devices(subsystem='tty'):
            if 'ID_VENDOR_ID' not in l_dev:
                continue
            l_msg = '\nDevice found: {}\n'.format(l_dev.get('DEVNAME'))
            for k, v in l_dev.items():
                l_msg += '{} === {}\n'.format(k, v)
            l_id = '{}:{}'.format(l_dev.get('ID_VENDOR_ID'), l_dev.get('ID_MODEL_ID'))
            if l_id == '0403:6001':
                l_ret = 'Insteon PLM (0403:6001)'
            elif l_id == '067b:2303':
                l_ret = 'USB Serial port (067b:2303)'
            LOG.info(l_msg)
        return l_ret

    def _add_controller(self, p_node, p_obj):
        """
        @param p_node: is the node obj for this node
        @param p_obj: is the discovered DeviceController type to be added to the list
        """
        p_node.ControllerCount += 1
        p_node.ControllerType.append(p_obj)
        return

    def find_devices(self, p_node_obj):
        """
        """
        l_controllers = {}
        self._find_controllers()
        LOG.info('NodeControllers: {}'.format(l_controllers))
        return p_node_obj


class Interfaces():
    """
    Loop thru all the interfaces of this local node and extract the info.
    """

    def _find_all_interface_names(self):
        """ Get the names of all the network interfaces on this computer.
        Linux before about 2015 returned something like eth0, wlan0, or lo0.
        Later Linuxes return a descriptive id that contains a physical slot like enp3s0, wlp2s0.

        @return: a list of interface names ['lo', 'enp3s0', 'wlp2s0', ...]
        """
        l_interface_names = netifaces.interfaces()
        return l_interface_names

    def _find_addr_family_name(self, p_ix):
        """ Returns the string of the family name for a given index.

        Linux, Kubuntu (Laptop):
        2  = AF_INET   - IPv4
        10 = AF_INET6  - IPv6
        17 = AF_PACKET - Link layer

        @param p_ix: The index of the AF Name (May be different on different computers).
        @return: a strng of the AF Name 'AF_NET' or 'AF_INET6'
        """
        l_name = netifaces.address_families[p_ix]
        return l_name

    def _find_addr_lists(self, p_interface_name):
        """
        @param p_interface_name: is the name of an interface like 'lo' or 'etp3s0' etc.
        @return:  a dict with the key = interface type (-1000 = MAC Addr, 2 = INET, 23 = INET6)
                    The values are a list of dicts of addresses for that interface.
        """
        l_ret = netifaces.ifaddresses(p_interface_name)
        return l_ret

    def _get_address_list_INET(self, p_list):
        l_list = []
        for l_ent in p_list:
            l_list.append(l_ent['addr'])
        return l_list

    def _get_one_interface(self, p_interface_name):
        """ Gather the information about a single interface given the interface name.
        Only UP interfaces return data, apparently,
        """
        l_interface = NodeInterfaceData()
        l_interface.Name = p_interface_name
        # l_interface.Active = True
        l_interface.Key = 0
        l_interface.UUID = toolUuid.create_uuid()  # We need a way to persist the UUID instead of this
        l_interface.NodeInterfaceType = 'Other'
        l_afList = Interfaces()._find_addr_lists(p_interface_name)
        for l_afID in l_afList.keys():
            l_v4 = []
            l_v6 = []
            l_afName = Interfaces()._find_addr_family_name(l_afID)
            if l_afName == 'AF_PACKET':
                l_interface.MacAddress = l_afList[l_afID]
            if l_afName == 'AF_INET':
                l_v4 = Interfaces()._get_address_list_INET(l_afList[l_afID])
                l_interface.V4Address = l_v4
            if l_afName == 'AF_INET6':
                l_v6 = Interfaces()._get_address_list_INET(l_afList[l_afID])
                l_interface.V6Address = l_v6
        return l_interface, l_v4, l_v6

    def _get_all_interfaces(self):
        """
        @return: a dict of interfaces for this node.
        """
        l_count = 0
        l_dict = {}
        l_ipv4 = []
        l_ipv6 = []
        for l_interface_name in Interfaces()._find_all_interface_names():
            #  print('\n160 All Interfaces: {}'.format(l_interface_name))
            l_iface, l_v4, l_v6 = Interfaces()._get_one_interface(l_interface_name)
            if l_v4 != []:
                l_ipv4.append(l_v4)
            if l_v6 != []:
                l_ipv6.append(l_v6)
            l_iface.Key = l_count
            l_dict[l_count] = l_iface
            l_count += 1
        LOG.info('Added {} Interfaces to local node'.format(l_count))
        return l_dict, l_ipv4, l_ipv6

    @staticmethod
    def _list_families():
        """
        @return: A dict of families for netifaces
        """
        l_ret = netifaces.address_families
        return l_ret

    @staticmethod
    def _list_gateways():
        """ netifaces.gateways()

        Obtain a list of the gateways on this machine.

        Returns a dict whose keys are equal to the address family constants,
        e.g. netifaces.AF_INET, and whose values are a list of tuples of the
        format (<address>, <interface>, <is_default>).

        There is also a special entry with the key 'default', which you can use
        to quickly obtain the default gateway for a particular address family.

        There may in general be multiple gateways; different address
        families may have different gateway settings (e.g. AF_INET vs AF_INET6)
        and on some systems it's also possible to have interface-specific
        default gateways.

        """
        l_ret = netifaces.gateways()
        return l_ret

    @staticmethod
    def _list_ifaddresses(p_if):
        """
        Obtain information about the specified network interface.

        Returns a dict whose keys are equal to the address family constants,
        e.g. netifaces.AF_INET, and whose values are a list of addresses in
        that family that are attached to the network interface.
        """
        l_ret = netifaces.ifaddresses(p_if)
        return l_ret

    @staticmethod
    def _list_interfaces():
        """
        Obtain a list of the interfaces available on this machine.
        """
        l_ret = netifaces.interfaces()
        return l_ret

    def add_interfaces(self, p_node_obj):
        """ Add the interfaces with addressing to the node object
        """
        l_interface, l_v4, l_v6 = Interfaces()._get_all_interfaces()
        p_node_obj.NodeInterfaces = l_interface
        p_node_obj.ConnectionAddr_IPv4 = l_v4
        p_node_obj.ConnectionAddr_IPv6 = l_v6
        return p_node_obj


class HandleNodeType(object):

    m_node = NODE_NOTHING

    def __init__(self, p_role):
        self.find_node_type(p_role)

    def init_node_type(self, p_pyhouse_obj):
        if self.m_node & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouse_obj)

    def _init_ir_control(self, p_pyhouse_obj):
        """This node has an IR receiver so set it up.
        """
        pass


class Util(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    @staticmethod
    def _is_camera_node():
        """
        Test to see if this node has a camera attached
        """
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _is_controller_node():
        """
        Test to see if this node has a USB/Serial controller attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            #  Test for lights
            if fnmatch.fnmatch(l_file, 'ttyUSB?'):
                l_ret |= NODE_USB_CONTROLLER
                LOG.info('USB-Controller Node')
        return l_ret

    @staticmethod
    def _is_ir_node():
        """
        Test to see if this node has an IR sensor attached.
        I only have a PiFace-CAD attached
        """
        l_ret = NODE_NOTHING
        for l_file in os.listdir('/dev'):
            if fnmatch.fnmatch(l_file, 'lirc?'):
                l_ret |= NODE_PIFACECAD
                LOG.info('Lirc Node')
        return l_ret

    @staticmethod
    def _is_pandora_node():
        """
        Test to see if this node is a Pandora player
        """
        l_ret = NODE_NOTHING
        if os.path.exists('/usr/bin/pianobar'):
            l_ret |= NODE_PANDORA
            LOG.info('This node is a Pandora Player Node')
        return l_ret

    @staticmethod
    def _is_v6_router_node():
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _is_tunnel_node():
        l_ret = NODE_NOTHING
        return l_ret

    @staticmethod
    def _unix_node_test(p_role):
        p_role |= Util._is_camera_node()
        p_role |= Util._is_controller_node()
        p_role |= Util._is_ir_node()
        p_role |= Util._is_pandora_node()
        p_role |= Util._is_v6_router_node()
        p_role |= Util._is_tunnel_node()
        return p_role

    @staticmethod
    def find_node_role():
        l_role = NODE_NOTHING
        try:
            Util._unix_node_test(l_role)
        except Exception:
            l_role |= NODE_NOT_UNIX
        LOG.info('NodeRole: {}'.format(l_role))
        return l_role

    def init_node_type(self, p_pyhouse_obj):
        l_role = p_pyhouse_obj.Computer.Nodes[p_pyhouse_obj.Computer.UUID].NodeRole
        if l_role & NODE_PIFACECAD:
            self._init_ir_control(p_pyhouse_obj)
        elif l_role & NODE_USB_CONTROLLER:
            pass
        elif l_role & NODE_CAMERA:
            pass

    def _init_ir_control(self, p_pyhouse_obj):
        """This node has an IR receiver so set it up.
        """
        pass

    def insert_node(self, p_node, p_pyhouse_obj):
        """
        """
        # l_max_key = -1
        # try:
        #    for l_node in p_pyhouse_obj.Computer.Nodes.values():
        #        # if l_node.Name == p_node.Name:
        #            p_pyhouse_obj.Computer.Nodes[p_node.Key] = p_node
        #            LOG.info('Added node {}'.format(p_node.Name))
        #        #    return
        #        # if l_node.Key > l_max_key:
        #        #    l_max_key = l_node.Key
        # except AttributeError:
        #    pass
        p_pyhouse_obj.Computer.Nodes[p_node.UUID] = p_node
        LOG.info('Nodes = {}'.format(p_pyhouse_obj.Compute.Nodes))

    def create_local_node(self):
        """ Create the local node info structure
        """
        l_node = NodeInformation()
        l_node.Name = self.m_pyhouse_obj.Computer.Name
        l_node.Key = 0
        # l_node.Active = True
        l_node.UUID = self.m_pyhouse_obj.Computer.UUID
        Interfaces().add_interfaces(l_node)
        Devices().find_devices(l_node)
        l_node.NodeRole = Util.find_node_role()
        l_node.LastUpdate = datetime.now()
        # l_topic = 'computer/local'
        # self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_node)
        return l_node


class Api(Util):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Node xml info.
        """
        pass

    def Start(self):
        l_uuid = self.m_pyhouse_obj.Computer.UUID
        l_local = Util(self.m_pyhouse_obj).create_local_node()
        self.m_pyhouse_obj.Computer.Nodes[l_uuid] = l_local
        LOG.info('Adding node  {} {}'.format(l_local.Name, l_uuid))
        self.init_node_type(self.m_pyhouse_obj)

    def SaveXml(self, p_xml):
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

#  ## END DBK
