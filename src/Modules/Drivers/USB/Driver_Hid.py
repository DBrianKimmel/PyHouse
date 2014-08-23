"""
Created on Apr 8, 2013

@author: briank

Driver_USB.py - USB Driver module.

This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

This should also allow control of many different houses.
"""

__author__ = 'D. Brian Kimmel'

# Import system type stuff
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util
from twisted.internet import reactor

# Import PyHouse modules
from Modules.Utilities.tools import PrintBytes
from Modules.Computer import logging_pyh as Logger

callLater = reactor.callLater

g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Startup Details
# 3 = Read / write details

LOG = Logger.getLogger('PyHouse.USBHIDDriver ')
g_usb = None


# Timeouts for send/receive delays
RECEIVE_TIMEOUT = 0.3

HID_GET_REPORT = 0x01
HID_GET_IDLE = 0x02
HID_GET_PROTOCOL = 0x03
HID_SET_REPORT = 0x09
HID_SET_IDLE = 0x0A
HID_SET_PROTOCOL = 0x0B



class UsbDeviceData(object):
    """This is the data object for one USB controller device.
    """

    def __init__(self):
        self.Device = None
        self.Name = None
        self.Port = None
        self.Product = None
        self.Vendor = None
        self.ep_in = None
        self.epi_addr = 0
        self.epi_type = 0
        self.epi_packet_size = 0
        self.ep_out = None
        self.epo_addr = 0
        self.hid_device = False
        self.message = ''

    def __str__(self):
        l_ret = "Driver_USB.UsbDeviceData: Name: {0:}, Vendor: {1:#04x}, Product: {2:#04x}, Device: {3:}, Port: {4:}".format(self.Name, self.Vendor, self.Product, self.Device, self.Port)
        return l_ret

class UsbDriverAPI(UsbDeviceData):

    def _setup_find_device(self, p_usb):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        try:
            l_device = usb.core.find(idVendor = p_usb.Vendor, idProduct = p_usb.Product)
        except usb.USBError:
            LOG.error("ERROR no such USB device")
            return None
        if l_device == None:
            LOG.error('USB device not found  {0:X}:{1:X}, {2:}'.format(p_usb.Vendor, p_usb.Product, p_usb.Name))
            return None
        p_usb.Device = l_device
        p_usb.num_configs = l_device.bNumConfigurations
        if p_usb.Device.bDeviceClass == 3:
            p_usb.hid_device = True
        p_usb.configs = {}
        return l_device

    def _setup_detach_kernel(self, p_usb):
        """Get rid of any kernel device driver that is in our way.
        On a restart of PyHouse we expect no such kernel driver to exist.
        """
        try:
            if not p_usb.Device.is_kernel_driver_active(0):
                return
        except usb.USBError:
            pass
        try:
            p_usb.Device.detach_kernel_driver(0)
        except Exception as e:
            LOG.error("Driver_USB - Error in detaching_kernel_driver {0:} ".format(e))

    def _setup_configurations(self, p_usb):
        """Now we deal with the USB configuration

        1. get all the configs
        2. use the 'proper' config.

        @param p_usb: is the 'found' device
        """
        p_usb.Device.set_configuration()
        p_usb.configs = p_usb.Device.get_active_configuration()
        p_usb.num_interfaces = p_usb.configs.bNumInterfaces
        p_usb.interfaces = {}

    def _setup_interfaces(self, p_usb):
        """
        """
        l_interface_number = p_usb.configs[(0, 0)].bInterfaceNumber
        l_interface_class = p_usb.configs[(0, 0)].bInterfaceClass
        if l_interface_class == 3:
            p_usb.hid_device = True
        try:
            l_alternate_setting = usb.control.get_interface(p_usb.Device, l_interface_number)
        except Exception as e:
            LOG.error("Error in alt setting {0:}".format(e))
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_usb.configs, bInterfaceNumber = l_interface_number,
            bAlternateSetting = l_alternate_setting)
        p_usb.num_endpoints = l_interface.bNumEndpoints
        p_usb.interface_num = l_interface.bInterfaceNumber
        p_usb.interface = l_interface
        # return l_interface

    def _setup_endpoints(self, p_usb):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        p_usb.ep_out = usb.util.find_descriptor(
            p_usb.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        p_usb.epo_addr = p_usb.ep_out.bEndpointAddress
        p_usb.epo_type = p_usb.ep_out.bmAttributes & 0x03
        p_usb.epo_packet_size = p_usb.ep_out.wMaxPacketSize

        p_usb.ep_in = usb.util.find_descriptor(
            p_usb.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        p_usb.epi_addr = p_usb.ep_in.bEndpointAddress
        p_usb.epi_type = p_usb.ep_in.bmAttributes & 0x03
        p_usb.epi_packet_size = p_usb.ep_in.wMaxPacketSize

    def _setup_control_transfer(self, p_usb):
        l_par = p_usb.Parent.setup_hid_device()
        return
        l_ret = p_usb.Device.ctrl_transfer(
                                 l_par[0],
                                 l_par[1],
                                 l_par[2],
                                 l_par[3],
                                 l_par[4],
                                 timeout = 100)
        if l_ret < 0:
            return -1
        return

    def open_device(self, p_controller_obj, p_usb):
        p_usb.Name = p_controller_obj.Name
        p_usb.Port = p_controller_obj.Port
        p_usb.Product = p_controller_obj.Product
        p_usb.Vendor = p_controller_obj.Vendor
        p_usb.message = bytearray()
        LOG.info(" Initializing USB port - {0:#04X}:{1:#04X} - {2:} on port {3:}".format(
            p_usb.Vendor, p_usb.Product, p_usb.Name, p_usb.Port))
        p_usb.Device = self._setup_find_device(p_usb)
        if p_usb.Device == None:
            return None
        self._setup_detach_kernel(p_usb)
        self._setup_configurations(p_usb)
        self._setup_interfaces(p_usb)
        self._setup_endpoints(p_usb)
        if p_usb.hid_device:
            self._setup_control_transfer(p_usb)
        return p_usb

    def close_device(self, p_usb):
        p_usb.Device.reset()

    def read_device(self, p_usb):
        """
        """
        p_usb.Parent.read_device(p_usb)

    def fetch_read_data(self, p_controller_obj):
        l_ret = g_usb.message
        g_usb.message = bytearray()
        return l_ret

    def write_device(self, p_message):
        """Send message to the USB device.

        Sending speed is up to the controller.
        Someday we may provide notification that a command is complete.

        @return: the number of bytes written
        """
        if g_usb.epi_type == 0:
            self._write_control_device(p_message)
        else:
            self._write_bis_device(p_message)

    def _write_bis_device(self, p_message):
        """Bulk, Interrupt, isoSynchronous
        """
        l_message = p_message
        try:
            l_len = g_usb.Device.write(g_usb.epo_addr, l_message)
        except Exception as e:
            LOG.error("Driver_USB._write_bis_device() - Error in writing to USB device {0:}".format(e))
            l_len = 0
        return l_len

    def _write_control_device(self, p_message):
        l_len = g_usb.Device.write(0, p_message, timeout = 100)
        return l_len

class API(UsbDriverAPI):

    def __init__(self):
        """
        """
        pass

    def Start(self, p_controller_obj, p_parent):
        """
        @param p_controller_obj: is the Controller_Data object we are starting.
        @param p_parent: is the address of the caller USB device driver
        """
        global g_usb
        g_usb = UsbDeviceData()
        g_usb.Parent = p_parent
        if self.open_device(p_controller_obj, g_usb) != None:
            callLater(RECEIVE_TIMEOUT, lambda x = g_usb: self.read_device(x))

    def Stop(self):
        self.close_device(g_usb)

# ## END DBK
