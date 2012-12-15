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

# Import PyHouse modules
from tools import PrintBytes

g_debug = 2
g_logger = None


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
    m_ep_in = None
    m_epi_addr = 0
    m_ep_out = None
    m_epo_addr = 0

    def _setup_find_device(self):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        if g_debug > 0:
            print "Driver_USB._setup_find_device() - Name: {0:}, Vendor: {1:#X}, Product: {2:#X}".format(self.m_ddata.get_name(), self.m_ddata.Vendor, self.m_ddata.Product)
        try:
            l_device = usb.core.find(idVendor = self.m_ddata.get_vendor(), idProduct = self.m_ddata.get_product())
        except:
            print "no such device"
            return None
        if l_device == None:
            g_logger.error('USB device not found  {0:X}:{1:X}, {2:}'.format(self.m_ddata.get_vendor(), self.m_ddata.get_product(), self.m_ddata.get_name()))
            return None
        if g_debug > 7:
            print "  Device =", l_device.__dict__
        self.m_ddata.set_device(l_device)
        self.m_ddata.num_configs = l_num_cfg = l_device.bNumConfigurations
        self.m_ddata.configs = {}
        if g_debug > 1:
            print "  Configuration count: {0:}".format(l_num_cfg)
        return l_device

    def _setup_detach_kernel(self, p_driver):
        """Get rid of any kernel device driver that is in our way.
        On a restart of PyHouse we expect no such kernel driver to exist.
        """
        if not p_driver.is_kernel_driver_active(0):
            return
        if g_debug > 0:
            print "Driver_USB._setup_detach_kernel()"
        try:
            p_driver.detach_kernel_driver(0)
        except Exception, e:
            print "Driver_USB - Error in detaching_kernel_driver ", sys.exc_info()[0], e

    def _setup_configurations(self, p_device):
        """Now we deal with the USB configuration - use the 'proper' config.

        NOTE - We should not have to do this; the device should already be in the proper config.

        @param p_device: is the 'found' device
        @return: the active configuration object.
        """
        # TODO don't do if not needed
        if g_debug > 0:
            print "Driver_USB._setup_configurations() - count: {0:}".format(self.m_ddata.num_configs)
        p_device.set_configuration()
        l_config = p_device.get_active_configuration()
        if g_debug > 7:
            print "  Config:", l_config.__dict__
        self.m_ddata.num_interfaces = l_num_int = l_config.bNumInterfaces
        self.m_ddata.interfaces = {}
        if g_debug > 1:
            print "  Interface count: {0:}".format(l_num_int)
        return l_config

    def _setup_interfaces(self, p_config):
        """
        """
        if g_debug > 0:
            print "Driver_USB._setup_interfaces() - count: {0:}".format(self.m_ddata.num_interfaces)
        l_interface_number = p_config[(0, 0)].bInterfaceNumber
        l_interface_class = p_config[(0, 0)].bInterfaceClass
        if l_interface_class == 3:
            self.setup_hid_device()
        if g_debug > 5:
            print "  Interface_number: {0:}, Class: {1:}".format(l_interface_number, l_interface_class)
        try:
            l_alternate_setting = usb.control.get_interface(self.m_ddata.get_device(), l_interface_number)
            if g_debug > 5:
                print "  Alternate_setting:", l_alternate_setting
        except Exception, e:
            print "   -- Error in alt setting ", sys.exc_info()[0], e
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_config, bInterfaceNumber = l_interface_number,
            bAlternateSetting = l_alternate_setting)
        if g_debug > 5:
            print "  Interface:", l_interface.__dict__
        self.m_ddata.num_endpoints = l_interface.bNumEndpoints
        self.m_ddata.interface_num = l_interface.bInterfaceNumber
        if g_debug > 1:
            print "  Endpoint count: {0:} for interface {1:}".format(self.m_ddata.num_endpoints, self.m_ddata.interface_num)
        return l_interface

    def _setup_endpoints(self, p_interface):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        if g_debug > 0:
            print "Driver_USB._setup_endpoints() - count: {0:}".format(self.m_ddata.num_endpoints)
        self.m_ep_out = usb.util.find_descriptor(
            p_interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        if g_debug > 1:
            print "  Ep_Out:", self.m_ep_out.__dict__
        self.m_epo_addr = self.m_ep_out.bEndpointAddress
        self.m_epo_type = self.m_ep_out.bmAttributes & 0x03
        self.m_epo_packet_size = self.m_ep_out.wMaxPacketSize

        self.m_ep_in = usb.util.find_descriptor(
            p_interface, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        if g_debug > 1:
            print "  Ep_In: ", self.m_ep_in.__dict__
        self.m_epi_addr = self.m_ep_in.bEndpointAddress
        self.m_epi_type = self.m_ep_in.bmAttributes & 0x03
        self.m_epi_packet_size = self.m_ep_in.wMaxPacketSize

    def setup_hid_device(self):
        """Use the control endpoint to set up report descriptors for HID devices.

        Much of this was determined empirically for a smarthome UPB PIM
        """
        if g_debug > 0:
            print "Driver_USB._setup_hid_device()"
        l_report = array.array('B', "12345")
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03
        # l_requestType = LIBUSB_ENDPOINT_OUT | LIBUSB_REQUEST_TYPE_CLASS | LIBUSB_RECIPIENT_DEVICE; // 0x21
        l_requestType = 0x21
        l_request = HID_SET_REPORT  # ; // 0x09
        l_value = 0x0003  # ; // Report type & Report ID
        l_index = 0
        l_ret = self.m_ddata.Device.ctrl_transfer(
                                 l_requestType,
                                 l_request,
                                 l_value,
                                 l_index,
                                 l_report,
                                 timeout = 100)
        if l_ret < 0:
            print("UsbHidSerial::InitializeHID = ERROR returned=", l_ret)
            return -1
        if g_debug > 5:
            print("Driver_USB._setup_hid_device() - Exit OK - Bytes=", l_ret)
        return 1
        pass

    def open_device(self):
        if g_debug > 0:
            print "\nDriver_USB.open_device()"
        self.m_bytes = 0
        self.m_message = bytearray()
        self.m_device = self._setup_find_device()
        if self.m_device == None:
            return None
        # self.m_device.baudrate = 19200
        self._setup_detach_kernel(self.m_device)
        l_config = self._setup_configurations(self.m_device)
        l_interface = self._setup_interfaces(l_config)
        self._setup_endpoints(l_interface)
        return self.m_device

    def close_device(self, _p_dev):
        self.m_device.reset()

    def XXXread_device(self):
        l_len = -1
        while l_len != 0:
            try:
                l_msg = self.m_device.read(self.m_epi_addr, self.m_epi_packet_size, timeout = 100)
                # we seem to have actual length + 240 as 1st char
                l_len = l_msg[0] - 240
                if g_debug > 8 or (g_debug > 1 and l_len > 0):
                    print "Driver_USB.read_device() {0:} - {1:}".format(l_len, l_msg)
                if l_len > 0:
                    self.m_bytes += l_len
                    for l_x in range(l_len):
                        self.m_message.append(l_msg[l_x + 1])
            except usb.USBError, e:
                print "Driver_USB.read_device() got USBError", e
            except Exception, e:
                print " -- Error in Driver_USB.read_device() ", sys.exc_info(), e
            time.sleep(0.1)

    def fetch_read_data(self):
        if g_debug > 5:
            print "Driver_USB.fetch_read_data() "
        l_ret = (len(self.m_message), self.m_message)
        self.m_message = bytearray()
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


class USBDriverMain(UsbDriverAPI):

    def __init__(self, p_obj, p_read_time = 1.0):
        """
        @param p_obj:is the Controller_Data object for a USB device to open.
        """
        if g_debug > 0:
            print "Driver_USB.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.USBDriver')
        l_dev = self.extract_usb(p_obj)
        g_logger.info(" Initializing USB port - {0:#04X}:{1:#04X} - {2:} on port {3:}".format(
            l_dev.get_vendor(), l_dev.get_product(), l_dev.get_name(), l_dev.get_port()))
        if self.open_device() != None:
            LoopingCall(self._serialLoop).start(0.08)


# ## END
