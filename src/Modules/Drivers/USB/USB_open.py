"""
-*- test-case-name: PyHouse.src.Modules.Drivers.USB.test.test_usb_open -*-

@name:      PyHouse/src/Modules/Drivers/USB/usb_open.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2011
@summary:   This module is for communicating with USB devices.


This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

Instead of using callLater timers, it would be better to use deferred callbacks when data arrives.

"""

# Import system type stuff
import usb.core
import usb.util

# Import PyHouse modules
from Modules.Utilities.tools import PrintBytes
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.USBDriver_Open ')


# Timeouts for send/receive delays
RECEIVE_TIMEOUT = 0.3


class UsbDeviceData(object):
    """
    This is the data object for one USB controller device.
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


class Utility(object):

    @staticmethod
    def format_names(p_USB_obj):
        """
        Printable Vendor, Product and controller name
        """
        l_ret = "{0:#04x}:{1:#04x} {2:}".format(p_USB_obj.Vendor, p_USB_obj.Product, p_USB_obj.Name)
        return l_ret

    @staticmethod
    def is_hid(p_device):
        if p_device.bDeviceClass == 3:
            return True

    @staticmethod
    def setup_hid_17DD_5500(p_USB_obj):
        """
        Use the control endpoint to set up report descriptors for HID devices.
        Much of this was determined empirically for a smarthome UPB PIM
        """
        l_report = bytearray(b'12345')
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03  # len ???
        l_requestType = 0x21  # LIBUSB_ENDPOINT_OUT (0x00) | LIBUSB_REQUEST_TYPE_CLASS (0x20) | LIBUSB_RECIPIENT_DEVICE (0x00)
        l_request = 0x09  # USB_driver.HID_SET_REPORT  # 0x09
        l_value = 0x0003  # Report type & Report ID
        l_index = 0  #
        l_ret = (l_requestType, l_request, l_value, l_index, l_report)
        p_USB_obj.Device.ctrl_transfer(l_requestType, l_request, l_value, l_index, l_report)
        LOG.debug("setup_hid {}".format(PrintBytes(l_ret)))
        return l_ret



class API(UsbDeviceData):

    m_controller_obj = None

    def _save_find_device(self, p_USB_obj, p_device):
        p_USB_obj.Device = p_device
        p_USB_obj.num_configs = p_device.bNumConfigurations
        p_USB_obj.hid_device = Utility.is_hid(p_device)
        p_USB_obj.configs = {}
        return p_USB_obj

    def _open_find_device(self, p_USB_obj):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        l_vpn = Utility.format_names(p_USB_obj)
        l_device = None
        try:
            l_device = usb.core.find(idVendor = p_USB_obj.Vendor, idProduct = p_USB_obj.Product)
        except usb.USBError:
            LOG.error("ERROR no such USB device for {}".format(l_vpn))
            return None
        if l_device == None:
            LOG.error('ERROR - USB device not found  {}'.format(l_vpn))
            return None
        p_USB_obj.Device = self._save_find_device(p_USB_obj, l_device)
        LOG.info('Found a device - HID: {}'.format(l_vpn))
        return l_device

    def _setup_detach_kernel(self, p_USB_obj):
        """Get rid of any kernel device driver that is in our way.
        On a restart of PyHouse we expect no such kernel driver to exist.
        """
        try:
            if not p_USB_obj.Device.is_kernel_driver_active(0):
                return
        except usb.USBError:
            pass
        try:
            p_USB_obj.Device.detach_kernel_driver(0)
        except Exception as e:
            LOG.error("Error in detaching_kernel_driver - {0:}".format(e))

    def _setup_configurations(self, p_USB_obj):
        """Now we deal with the USB configuration

        1. get all the configs
        2. use the 'proper' config.

        @param p_usb: is the 'found' device
        """
        # TODO don't do if not needed
        p_USB_obj.Device.set_configuration()
        p_USB_obj.configs = p_USB_obj.Device.get_active_configuration()
        p_USB_obj.num_interfaces = p_USB_obj.configs.bNumInterfaces
        p_USB_obj.interfaces = {}

    def _setup_interfaces(self, p_USB_obj):
        """
        """
        l_interface_number = p_USB_obj.configs[(0, 0)].bInterfaceNumber
        l_interface_class = p_USB_obj.configs[(0, 0)].bInterfaceClass
        try:
            l_alternate_setting = usb.control.get_interface(p_USB_obj.Device, l_interface_number)
        except Exception as e:
            LOG.error("   -- Error in alt setting {0:}".format(e))
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_USB_obj.configs,
            bInterfaceNumber = l_interface_number,
            bAlternateSetting = l_alternate_setting)
        p_USB_obj.num_endpoints = l_interface.bNumEndpoints
        p_USB_obj.interface_num = l_interface.bInterfaceNumber
        p_USB_obj.interface = l_interface
        if l_interface_class == 3:
            p_USB_obj.hid_device = True
            self._setup_reports(p_USB_obj)

    def _setup_endpoints(self, p_USB_obj):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        if g_debug >= 1:
            LOG.debug("_setup_endpoints() - Name: {0:},  endpoint count: {1:}".format(p_USB_obj.Name, p_USB_obj.num_endpoints))
        p_USB_obj.ep_out = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        if g_debug >= 1:
            LOG.debug("  Ep_Out: {0:}".format(p_USB_obj.ep_out.__dict__))
        p_USB_obj.epo_addr = p_USB_obj.ep_out.bEndpointAddress
        p_USB_obj.epo_type = p_USB_obj.ep_out.bmAttributes & 0x03
        p_USB_obj.epo_packet_size = p_USB_obj.ep_out.wMaxPacketSize

        p_USB_obj.ep_in = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        if g_debug >= 1:
            LOG.debug("  Ep_In: {0:}".format(p_USB_obj.ep_in.__dict__))
        p_USB_obj.epi_addr = p_USB_obj.ep_in.bEndpointAddress
        p_USB_obj.epi_type = p_USB_obj.ep_in.bmAttributes & 0x03
        p_USB_obj.epi_packet_size = p_USB_obj.ep_in.wMaxPacketSize

    def _setup_reports(self, p_USB_obj):
        _l_reports = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

    def open_device(self, p_USB_obj):
        p_USB_obj.message = bytearray()
        l_vpn = Utility.format_names(p_USB_obj)
        LOG.info("Opening USB device - {}".format(l_vpn))
        p_USB_obj.Device = self._open_find_device(p_USB_obj)
        if p_USB_obj.Device == None:
            LOG.error('ERROR - Setup Failed')
            return False
        self._setup_detach_kernel(p_USB_obj)
        self._setup_configurations(p_USB_obj)
        self._setup_interfaces(p_USB_obj)
        self._setup_endpoints(p_USB_obj)
        _l_msg = Utility.setup_hid_17DD_5500(p_USB_obj)
        return True

    def close_device(self, p_USB_obj):
        p_USB_obj.Device.reset()

# ## END DBK
