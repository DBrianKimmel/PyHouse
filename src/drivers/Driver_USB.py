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
import logging
import sys
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util
from twisted.internet import reactor

# Import PyHouse modules
from src.utils.tools import PrintBytes


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Startup Details
# 3 = Read / write details

g_logger = logging.getLogger('PyHouse.USBDriver')

callLater = reactor.callLater


# Timeouts for send/receive delays
RECEIVE_TIMEOUT = 0.3


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
        l_ret = "UsbDevice:: Name:{0:}, Vendor: {1:#04x}, Product: {2:#04x}, Device: {3:}, Port: {4:}".format(self.Name, self.Vendor, self.Product, self.Device, self.Port)
        return l_ret


class UsbDriverAPI(UsbDeviceData):

    def _setup_find_device(self, p_controller_obj):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        if g_debug >= 2:
            print "Driver_USB._setup_find_device() - Name: {0:},   Vendor: {1:#x}, Product: {2:#x}".format(p_controller_obj.Name, p_controller_obj.Vendor, p_controller_obj.Product)
        try:
            l_device = usb.core.find(idVendor = p_controller_obj.Vendor, idProduct = p_controller_obj.Product)
        except usb.USBError:
            l_msg = "ERROR no such USB device for {0:}".format(p_controller_obj.Name)
            print l_msg
            g_logger.error(l_msg)
            return None
        if l_device == None:
            g_logger.error('USB device not found  {0:X}:{1:X}, {2:}'.format(p_controller_obj.Vendor, p_controller_obj.Product, p_controller_obj.Name))
            return None
        if g_debug >= 8:
            print "  Device =", l_device.__dict__
        p_controller_obj.Data.Device = l_device
        p_controller_obj.Data.num_configs = l_device.bNumConfigurations
        if p_controller_obj.Data.Device.bDeviceClass == 3:
            p_controller_obj.Data.hid_device = True
        p_controller_obj.Data.configs = {}
        return l_device

    def _setup_detach_kernel(self, p_controller_obj):
        """Get rid of any kernel device driver that is in our way.
        On a restart of PyHouse we expect no such kernel driver to exist.
        """
        try:
            if not p_controller_obj.Data.Device.is_kernel_driver_active(0):
                return
        except usb.USBError:
            pass
        if g_debug >= 2:
            print "Driver_USB._setup_detach_kernel()"
        try:
            p_controller_obj.Data.Device.detach_kernel_driver(0)
        except Exception, e:
            print "Driver_USB - Error in detaching_kernel_driver ", sys.exc_info()[0], e

    def _setup_configurations(self, p_controller_obj):
        """Now we deal with the USB configuration

        1. get all the configs
        2. use the 'proper' config.

        @param p_usb: is the 'found' device
        """
        # TODO don't do if not needed
        if g_debug >= 2:
            print "Driver_USB._setup_configurations() - Name: {0:},   configuration count: {1:}".format(p_controller_obj.Name, p_controller_obj.Data.num_configs)
        for l_ix in range(p_controller_obj.Data.Device.bNumConfigurations):
            if g_debug >= 2:
                print " -- get config #", l_ix
            # p_usb.configs[l_ix] = p_usb.Device.Configuration(l_ix)
            pass
        p_controller_obj.Data.Device.set_configuration()
        p_controller_obj.Data.configs = p_controller_obj.Data.Device.get_active_configuration()
        if g_debug >= 8:
            print "  Config:", p_controller_obj.Data.configs.__dict__
        p_controller_obj.Data.num_interfaces = p_controller_obj.Data.configs.bNumInterfaces
        p_controller_obj.Data.interfaces = {}

    def _setup_interfaces(self, p_controller_obj):
        """
        """
        if g_debug >= 2:
            print "Driver_USB._setup_interfaces() - Name: {0:},   interface count: {1:}".format(p_controller_obj.Name, p_controller_obj.Data.num_interfaces)
        l_interface_number = p_controller_obj.Data.configs[(0, 0)].bInterfaceNumber
        l_interface_class = p_controller_obj.Data.configs[(0, 0)].bInterfaceClass
        if l_interface_class == 3:
            p_controller_obj.Data.hid_device = True
        if g_debug >= 6:
            print "  Interface_number: {0:}, Class: {1:}".format(l_interface_number, l_interface_class)
        try:
            l_alternate_setting = usb.control.get_interface(p_controller_obj.Data.Device, l_interface_number)
            if g_debug >= 6:
                print "  Alternate_setting:", l_alternate_setting
        except Exception, e:
            print "   -- Error in alt setting ", sys.exc_info()[0], e
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_controller_obj.Data.configs, bInterfaceNumber = l_interface_number,
            bAlternateSetting = l_alternate_setting)
        if g_debug >= 8:
            print "  Interface:", l_interface.__dict__
        p_controller_obj.Data.num_endpoints = l_interface.bNumEndpoints
        p_controller_obj.Data.interface_num = l_interface.bInterfaceNumber
        p_controller_obj.Data.interface = l_interface
        # return l_interface

    def _setup_endpoints(self, p_controller_obj):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        if g_debug >= 2:
            print "Driver_USB._setup_endpoints() - Name: {0:},  endpoint count: {1:}".format(p_controller_obj.Name, p_controller_obj.Data.num_endpoints)
        p_controller_obj.Data.ep_out = usb.util.find_descriptor(
            p_controller_obj.Data.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        if g_debug >= 8:
            print "  Ep_Out:", p_controller_obj.Data.ep_out.__dict__
        p_controller_obj.Data.epo_addr = p_controller_obj.Data.ep_out.bEndpointAddress
        p_controller_obj.Data.epo_type = p_controller_obj.Data.ep_out.bmAttributes & 0x03
        p_controller_obj.Data.epo_packet_size = p_controller_obj.Data.ep_out.wMaxPacketSize

        p_controller_obj.Data.ep_in = usb.util.find_descriptor(
            p_controller_obj.Data.interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        if g_debug >= 8:
            print "  Ep_In: ", p_controller_obj.Data.ep_in.__dict__
        p_controller_obj.Data.epi_addr = p_controller_obj.Data.ep_in.bEndpointAddress
        p_controller_obj.Data.epi_type = p_controller_obj.Data.ep_in.bmAttributes & 0x03
        p_controller_obj.Data.epi_packet_size = p_controller_obj.Data.ep_in.wMaxPacketSize

    def open_device(self, p_controller_obj):
        if g_debug >= 2:
            print "Driver_USB.open_device() - Name:{0:}".format(p_controller_obj.Name)
        p_controller_obj.Message = bytearray()
        g_logger.info(" Initializing USB port - {0:#04X}:{1:#04X} - {2:} on port {3:}".format(
            p_controller_obj.Vendor, p_controller_obj.Product, p_controller_obj.Name, p_controller_obj.Port))
        p_controller_obj.Data.Device = self._setup_find_device(p_controller_obj)
        if p_controller_obj.Data.Device == None:
            return None
        self._setup_detach_kernel(p_controller_obj)
        self._setup_configurations(p_controller_obj)
        self._setup_interfaces(p_controller_obj)
        self._setup_endpoints(p_controller_obj)
        return p_controller_obj.Active

    def close_device(self, p_controller_obj):
        p_controller_obj.Data.Device.reset()

    def read_device(self, p_controller_obj):
        """
        """
        callLater(RECEIVE_TIMEOUT, lambda x = p_controller_obj: self.read_device(x))
        if g_debug >= 6:
            print "Driver_USB.read_device_1() A - Name:{0:}, Endpoint:{1:#02x}, Size:{2:}".format(p_controller_obj.Name, p_controller_obj.Data.epi_addr, p_controller_obj.Data.epi_packet_size)
        try:
            l_msg = p_controller_obj.Data.Device.read(p_controller_obj.Data.epi_addr, p_controller_obj.Data.epi_packet_size, timeout = 100)
            l_len = len(l_msg)
            if l_len > 0:
                if g_debug >= 5:
                    print "Driver_USB.read_device_1() B - Len:{0:}, Msg:{1:}".format(l_len, PrintBytes(l_msg))
                for l_x in range(l_len):
                    p_controller_obj.Message.append(l_msg[l_x])
            elif g_debug >= 6:
                print "Driver_USB.read_device_1() C - len was 0 ", l_msg
        except usb.USBError, e:
            print "Driver_USB.read_device_1() got USBError", e
            l_len = 0
            # break
        except Exception, e:
            print " -- Error in Driver_USB.read_device_1() ", sys.exc_info(), e
            l_len = 0
            # break
        if g_debug >= 6:
            print "Driver_USB.read_device_1() - exit Message:{0:}".format(PrintBytes(p_controller_obj.Message))

    def fetch_read_data(self, p_controller_obj):
        l_ret = p_controller_obj.Message
        p_controller_obj.Message = bytearray()
        if g_debug >= 3:
            print "Driver_USB.fetch_read_data() - Msg:{0:}".format(PrintBytes(l_ret))
        return l_ret

    def write_device(self, p_message):
        """Send message to the USB device.

        Sending speed is up to the controller.
        Someday we may provide notification that a command is complete.

        @return: the number of bytes written
        """
        if g_debug >= 4:
            print "Driver_USB.write_device() - {0:}".format(PrintBytes(p_message)), self.m_controller_obj.Data.epi_type
        if self.m_controller_obj.Data.epi_type == 0:
            self._write_control_device(p_message)
        else:
            self._write_bis_device(p_message)

    def _write_bis_device(self, p_message):
        """Bulk, Interrupt, isoSynchronous
        """
        l_message = p_message
        if g_debug >= 4:
            print "Driver_USB._write_bis_device() - Ep_out: {0:#04X}, - {1:}".format(self.m_controller_obj.Data.epo_addr, PrintBytes(l_message))
        try:
            l_len = self.m_controller_obj.Data.Device.write(self.m_controller_obj.Data.epo_addr, l_message)
        except Exception, e:
            print "Driver_USB._write_bis_device() - Error in writing to USB device ", sys.exc_info()[0], e
            l_len = 0
        return l_len

    def _write_control_device(self, p_message):
        if g_debug >= 4:
            print "Driver_USB._write_control_device() ", self.m_controller_obj.Data.Device
        l_len = self.m_controller_obj.Data.Device.write(0, p_message, timeout = 100)
        return l_len

class API(UsbDriverAPI):

    def __init__(self):
        """
        """
        if g_debug >= 1:
            print "Driver_USB.API.__init__()"

    def Start(self, p_controller_obj):
        """
        @param p_controller_obj: is the Controller_Data object we are starting.
        @param p_parent: is the address of the caller USB device driver
        """
        self.m_controller_obj = p_controller_obj
        if g_debug >= 1:
            print "Driver_USB.Start() - Name:{0:}".format(p_controller_obj.Name)
        p_controller_obj.Data = self.m_usb = UsbDeviceData()
        if self.open_device(p_controller_obj) == True:
            self.read_device(p_controller_obj)
            if g_debug >= 1:
                print "Driver_USB opened Controller:{0:}".format(p_controller_obj.Name)
                self.write_device(bytearray(b'\x00\x01\x02\x03'))
                self.write_device(bytearray(b'\xff\x01\x02\x03'))
            return True
        else:
            print "Driver_USB failed to open Controller:{0:}".format(p_controller_obj.Name)
            return False

    def Stop(self):
        if g_debug >= 1:
            print "Driver_USB.Stop()"
        self.close_device(self.m_controller_obj)

# ## END DBK
