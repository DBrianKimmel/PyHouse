#!/usr/bin/python

# Copyright (C) 2012 by D. Brian Kimmel
#
# The following terms apply to all files associated
# with the software unless explicitly disclaimed in individual files.
#
# The authors hereby grant permission to use, copy, modify, distribute,
# and license this software and its documentation for any purpose, provided
# that existing copyright notices are retained in all copies and that this
# notice is included verbatim in any distributions. No written agreement,
# license, or royalty fee is required for any of the authorized uses.
# Modifications to this software may be copyrighted by their authors
# and need not follow the licensing terms described here, provided that
# the new terms are clearly indicated on the first page of each file where
# they apply.
#
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.

"""
Driver_USB.py - USB Driver module.

This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

This should also allow control of many different houses.
"""

__author__ = 'D. Brian Kimmel'

# Import system type stuff
import array
import logging
import sys
import time
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

# Import PyHouse modules
from tools import PrintBytes

callLater = reactor.callLater

g_debug = 8
g_logger = None
g_usb = None
g_api = None


# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
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
        self.hid_device = False
    def get_device(self):
        return self.__Device
    def set_device(self, value):
        self.__Device = value
    def get_name(self):
        return self.__Name
    def set_name(self, value):
        self.__Name = value
    def get_port(self):
        return self.__Port
    def set_port(self, value):
        self.__Port = value
    def get_product(self):
        return self.__Product
    def set_product(self, value):
        self.__Product = value
    def get_vendor(self):
        return self.__Vendor
    def set_vendor(self, value):
        self.__Vendor = value
    Device = property(get_device, set_device, None, "The USB device object returned by libusb find.")
    Name = property(get_name, set_name, None, "The configuration name for the device.")
    Port = property(get_port, set_port, None, "The name of the USB port to which the device is attached.")
    Product = property(get_product, set_product, None, "The device's assigned Product (idProduct).")
    Vendor = property(get_vendor, set_vendor, None, "The devices assigned Vendor number (idVendor).")

class UsbUtility(object):
    """
    """

    def _serialLoop(self):
        """This is invoked every 1 second.
        """
        self.read_device()

    def extract_usb(self, p_obj):
        """We are passed the Controller_Data dictionary entry for the device.
        Extract the USB info we will need and store it in this module.
        """
        self.m_ddata = UsbDeviceData()
        self.m_ddata.set_name(p_obj.Name)
        self.m_ddata.set_port(p_obj.Port)
        self.m_ddata.set_product(p_obj.Product)
        self.m_ddata.set_vendor(p_obj.Vendor)
        return self.m_ddata

    def dump_usb_info_for_debugging(self):
        Vend = self.m_ddata.get_vendor()
        Prod = self.m_ddata.Device.idProduct
        Cfgs = self.m_ddata.Device.bNumConfigurations
        if g_debug > 0:
            print "Driver_USB.usb_open"
            print "  !Vendor:{0:X}:{1:X}, Configs:{2:}".format(Vend, Prod, Cfgs)
            for attr in self.m_ddata.Device.__dict__.keys():
                if attr[:2] == '__':
                    print "\tName: {0:}=<built-in>".format(attr)
                else:
                    print "\tName: {0:}={1:}".format(attr, self.m_ddata.Device.__dict__ [attr])
            print

class UsbDriverAPI(UsbUtility):

    m_message = bytearray()
    m_ddata = None
    m_ep_in = None
    m_epi_addr = 0
    m_ep_out = None
    m_epo_addr = 0

    def _setup_find_device(self, p_usb):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        if g_debug > 0:
            print "Driver_USB._setup_find_device() - Name: {0:},   Vendor: {1:#x}, Product: {2:#x}".format(p_usb.Name, p_usb.Vendor, p_usb.Product)
        try:
            l_device = usb.core.find(idVendor = p_usb.Vendor, idProduct = p_usb.Product)
        except:
            print "ERROR no such USB device"
            return None
        if l_device == None:
            g_logger.error('USB device not found  {0:X}:{1:X}, {2:}'.format(p_usb.Vendor, p_usb.Product, p_usb.Name))
            return None
        if g_debug > 7:
            print "  Device =", l_device.__dict__
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
        except:
            pass
        if g_debug > 0:
            print "Driver_USB._setup_detach_kernel()"
        try:
            p_usb.Device.detach_kernel_driver(0)
        except Exception, e:
            print "Driver_USB - Error in detaching_kernel_driver ", sys.exc_info()[0], e

    def _setup_configurations(self, p_usb):
        """Now we deal with the USB configuration

        1. get all the configs
        2. use the 'proper' config.

        @param p_usb: is the 'found' device
        """
        # TODO don't do if not needed
        if g_debug > 0:
            print "Driver_USB._setup_configurations() - Name: {0:},   configuration count: {1:}".format(p_usb.Name, p_usb.num_configs)
        for l_ix in range(p_usb.Device.bNumConfigurations):
            print " -- get config ", l_ix
            # p_usb.configs[l_ix] = p_usb.Device.Configuration(l_ix)
            pass
        p_usb.Device.set_configuration()
        p_usb.configs = p_usb.Device.get_active_configuration()
        if g_debug > 7:
            print "  Config:", p_usb.configs.__dict__
        p_usb.num_interfaces = p_usb.configs.bNumInterfaces
        p_usb.interfaces = {}

    def _setup_interfaces(self, p_usb):
        """
        """
        if g_debug > 0:
            print "Driver_USB._setup_interfaces() - Name: {0:},   interface count: {1:}".format(p_usb.Name, p_usb.num_interfaces)
        l_interface_number = p_usb.configs[(0, 0)].bInterfaceNumber
        l_interface_class = p_usb.configs[(0, 0)].bInterfaceClass
        if l_interface_class == 3:
            p_usb.hid_device = True
        if g_debug > 5:
            print "  Interface_number: {0:}, Class: {1:}".format(l_interface_number, l_interface_class)
        try:
            l_alternate_setting = usb.control.get_interface(p_usb.Device, l_interface_number)
            if g_debug > 5:
                print "  Alternate_setting:", l_alternate_setting
        except Exception, e:
            print "   -- Error in alt setting ", sys.exc_info()[0], e
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_usb.configs, bInterfaceNumber = l_interface_number,
            bAlternateSetting = l_alternate_setting)
        if g_debug > 5:
            print "  Interface:", l_interface.__dict__
        p_usb.num_endpoints = l_interface.bNumEndpoints
        p_usb.interface_num = l_interface.bInterfaceNumber
        p_usb.interface = l_interface
        # return l_interface

    def _setup_endpoints(self, p_usb):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        if g_debug > 0:
            print "Driver_USB._setup_endpoints() - Name: {0:},  endpoint count: {1:}".format(p_usb.Name, p_usb.num_endpoints), p_usb.__dict__
        self.m_ep_out = usb.util.find_descriptor(
            p_usb.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        if g_debug > 1:
            print "  Ep_Out:", self.m_ep_out.__dict__
        self.m_epo_addr = self.m_ep_out.bEndpointAddress
        self.m_epo_type = self.m_ep_out.bmAttributes & 0x03
        self.m_epo_packet_size = self.m_ep_out.wMaxPacketSize

        self.m_ep_in = usb.util.find_descriptor(
            p_usb.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        if g_debug > 1:
            print "  Ep_In: ", self.m_ep_in.__dict__
        self.m_epi_addr = self.m_ep_in.bEndpointAddress
        self.m_epi_type = self.m_ep_in.bmAttributes & 0x03
        self.m_epi_packet_size = self.m_ep_in.wMaxPacketSize

    def _setup_control_transfer(self, p_usb):
        l_par = p_usb.Parent.setup_hid_device()
        if g_debug > 0:
            print "Driver_USB._setup_control_transfer() ", l_par
        l_ret = p_usb.Device.ctrl_transfer(
                                 l_par[0],
                                 l_par[1],
                                 l_par[2],
                                 l_par[3],
                                 l_par[4],
                                 timeout = 100)
        if l_ret < 0:
            print "Driver_USB._setup_control_transfer() = ERROR returned=", l_ret
            return -1
        if g_debug > 0:
            print "Driver_USB._setup_control_transfer() - Exit OK - Bytes=", l_ret
        return

    def open_device(self, p_obj, p_usb):
        if g_debug > 0:
            print "Driver_USB.open_device() {0:}".format(p_obj.Name)
        # self.extract_usb(p_obj)
        # self.m_bytes = 0
        p_usb.msg_len = 0
        # self.m_message = bytearray()
        p_usb.message = bytearray()
        self.m_device = self._setup_find_device(p_usb)
        if self.m_device == None:
            return None
        self._setup_detach_kernel(p_usb)
        self._setup_configurations(p_usb)
        self._setup_interfaces(p_usb)
        self._setup_endpoints(p_usb)
        if p_usb.hid_device:
            self._setup_control_transfer(p_usb)
        return self.m_device

    def close_device(self, _p_dev):
        self.m_device.reset()

    def read_device(self):
        callLater(RECEIVE_TIMEOUT, self.read_device)
        g_usb.Parent.read_device(g_usb)

    def fetch_read_data(self):
        if g_debug > 5:
            print "Driver_USB.fetch_read_data() "
        l_ret = (len(g_usb.message), g_usb.message)
        g_usb.message = bytearray()
        return (l_ret)

    def write_device(self, p_message):
        """Send message to the USB device.

        Sending speed is up to the controller.
        Someday we may provide notification that a command is complete.

        @return: the number of bytes written
        """
        if self.m_epi_type == 0:
            self.write_control_device(p_message)
        else:
            self.write_bis_device(p_message)

    def write_bis_device(self, p_message):
        """Bulk, Interrupt, isoSynchronous
        """
        l_message = array.array('B', p_message)
        if g_debug > 3:
            print "Driver_USB.write_bis_device() - Ep_out: {0:#04X}, - {1:}".format(self.m_epo_addr, PrintBytes(l_message))
        try:
            # l_len = self.m_ddata.Device.write(self.m_epo_addr, l_message)  # self.m_ddata.interface_num)
            # l_len = self.m_ep_out.write(l_message)
            for l_char in p_message:
                l_len = self.m_ddata.Device.write(2, l_char, timeout = 100)  # self.m_ddata.interface_num)
                # l_len = self.m_ddata.Device.write(self.m_ep_out, l_char, timeout = 5000)  # self.m_ddata.interface_num)
                # l_len = self.m_ep_out.write(l_char, timeout = 5000)
        except Exception, e:
            print " -- Error in writing to USB device ", sys.exc_info()[0], e
            l_len = 0
        return l_len

    def write_control_device(self, p_message):
        l_len = self.m_ddata.Device.write(0, p_message, timeout = 100)
        return l_len


def Init(p_obj, p_read_timer, p_parent):
    if g_debug > 0:
        print "Driver_USB.Init() - Name: {0:}".format(p_obj.Name)
    global g_logger, g_api, g_usb
    g_logger = logging.getLogger('PyHouse.USBDriver')
    g_usb = UsbUtility().extract_usb(p_obj)
    g_usb.Parent = p_parent
    g_api = UsbDriverAPI()
    g_logger.info(" Initializing USB port - {0:#04X}:{1:#04X} - {2:} on port {3:}".format(
        g_usb.get_vendor(), g_usb.get_product(), g_usb.get_name(), g_usb.get_port()))
    if g_api.open_device(p_obj, g_usb) != None:
        callLater(RECEIVE_TIMEOUT, g_api.read_device)
    return g_api

# ## END
