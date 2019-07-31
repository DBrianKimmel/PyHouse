"""
-*- test-case-name: PyHouse.src.Modules.Drivers.USB.test.test_usb_open -*-

@name:      PyHouse/src/Modules/Drivers/USB/usb_open.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2011
@summary:   This module is for communicating with USB devices.


This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

Instead of using callLater timers, it would be better to use deferred callbacks when data arrives.

"""

__updated__ = '2017-04-26'

# Import system type stuff
import usb.core
import usb.util

# Import PyHouse modules
from Modules.Drivers.USB.Driver_USB_17DD_5500 import API as usb5500API
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.USBDriver_Open ')


# Timeouts for send/receive delays
RECEIVE_TIMEOUT = 0.3


class Utility(object):

    @staticmethod
    def format_names(p_USB_obj):
        """
        Printable Vendor, Product and controller name
        """
        l_ret = "{:#04x}:{:#04x} {}".format(p_USB_obj.Vendor, p_USB_obj.Product, p_USB_obj.Name)
        return l_ret

    @staticmethod
    def is_hid(p_device):
        if p_device.bUsbDeviceClass == 3:
            return True


class API(object):

    m_controller_obj = None

    @staticmethod
    def _save_find_device(p_USB_obj, p_device):
        p_USB_obj.UsbDevice = p_device
        p_USB_obj.num_configs = p_device.bNumConfigurations
        p_USB_obj.hid_device = True  # Utility.is_hid(p_device)
        p_USB_obj.configs = {}
        return p_USB_obj

    @staticmethod
    def _open_find_device(p_USB_obj):
        """First step in opening a USB device.
        @return:  None if no such device or a pyusb device object
        """
        l_vpn = Utility.format_names(p_USB_obj)
        l_device = None
        try:
            l_device = usb.core.find(idVendor=p_USB_obj.Vendor, idProduct=p_USB_obj.Product)
        except (usb.USBError, ValueError):
            LOG.error("ERROR no such USB device for {}".format(l_vpn))
            return None
        if l_device == None:
            LOG.error('ERROR - USB device not found  {}'.format(l_vpn))
            return None
        LOG.debug(PrettyFormatAny.form(l_device, 'Device'))
        LOG.debug(PrettyFormatAny.form(p_USB_obj, 'pUSB_obj'))
        p_USB_obj.UsbDevice = API._save_find_device(p_USB_obj, l_device)
        LOG.info('Found a device - HID: {}'.format(l_vpn))
        return l_device

    @staticmethod
    def _setup_detach_kernel(p_USB_obj):
        """Get rid of any kernel device driver that is in our way.
        On a restart of PyHouse we expect no such kernel driver to exist.
        """
        try:
            if not p_USB_obj.UsbDevice.is_kernel_driver_active(0):
                return
        except usb.USBError:
            pass
        try:
            p_USB_obj.UsbDevice.detach_kernel_driver(0)
        except Exception as e:
            LOG.error("ERROR in detaching_kernel_driver - {}".format(e))

    @staticmethod
    def _setup_configurations(p_USB_obj):
        """Now we deal with the USB configuration

        1. get all the configs
        2. use the 'proper' config.

        @param p_usb: is the 'found' device
        """
        # TODO don't do if not needed
        p_USB_obj.UsbDevice.set_configuration()
        p_USB_obj.configs = p_USB_obj.UsbDevice.get_active_configuration()
        p_USB_obj.num_interfaces = p_USB_obj.configs.bNumInterfaces
        p_USB_obj.interfaces = {}

    @staticmethod
    def _setup_interfaces(p_USB_obj):
        """
        """
        l_interface_number = p_USB_obj.configs[(0, 0)].bInterfaceNumber
        l_interface_class = p_USB_obj.configs[(0, 0)].bInterfaceClass
        try:
            l_alternate_setting = usb.control.get_interface(p_USB_obj.UsbDevice, l_interface_number)
        except Exception as e:
            LOG.error("   -- Error in alt setting {}".format(e))
            l_alternate_setting = 0
        l_interface = usb.util.find_descriptor(
            p_USB_obj.configs,
            bInterfaceNumber=l_interface_number,
            bAlternateSetting=l_alternate_setting)
        p_USB_obj.num_endpoints = l_interface.bNumEndpoints
        p_USB_obj.interface_num = l_interface.bInterfaceNumber
        p_USB_obj.interface = l_interface
        if l_interface_class == 3:
            p_USB_obj.hid_device = True
            API._setup_reports(p_USB_obj)

    @staticmethod
    def _setup_endpoints(p_USB_obj):
        """We will deal with 2 endpoints here - as that is what I expect a controller to have.
        No use in be too general if no device exists that is more complex.
        """
        LOG.debug("_setup_endpoints() - Name: {},  endpoint count: {}".format(p_USB_obj.Name, p_USB_obj.num_endpoints))
        p_USB_obj.ep_out = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
        LOG.debug("  Ep_Out: {}".format(p_USB_obj.ep_out.__dict__))
        p_USB_obj.epo_addr = p_USB_obj.ep_out.bEndpointAddress
        p_USB_obj.epo_type = p_USB_obj.ep_out.bmAttributes & 0x03
        p_USB_obj.epo_packet_size = p_USB_obj.ep_out.wMaxPacketSize

        p_USB_obj.ep_in = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        LOG.debug("  Ep_In: {}".format(p_USB_obj.ep_in.__dict__))
        p_USB_obj.epi_addr = p_USB_obj.ep_in.bEndpointAddress
        p_USB_obj.epi_type = p_USB_obj.ep_in.bmAttributes & 0x03
        p_USB_obj.epi_packet_size = p_USB_obj.ep_in.wMaxPacketSize

    @staticmethod
    def _setup_reports(p_USB_obj):
        _l_reports = usb.util.find_descriptor(
            p_USB_obj.interface,
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)

    @staticmethod
    def open_device(p_USB_obj):
        p_USB_obj.message = bytearray()
        l_vpn = Utility.format_names(p_USB_obj)
        LOG.info("Opening USB device - {}".format(l_vpn))
        p_USB_obj.UsbDevice = API._open_find_device(p_USB_obj)
        if p_USB_obj.UsbDevice == None:
            LOG.error('ERROR - Setup Failed')
            return False
        API._setup_detach_kernel(p_USB_obj)
        API._setup_configurations(p_USB_obj)
        API._setup_interfaces(p_USB_obj)
        API._setup_endpoints(p_USB_obj)
        _l_control = usb5500API.Setup()
        # _l_msg = Utility.setup_hid_17DD_5500(p_USB_obj)
        return True

    @staticmethod
    def Setup(p_USB_obj):
        l_control = usb5500API.Setup()
        return l_control

    @staticmethod
    def close_device(p_USB_obj):
        p_USB_obj.UsbDevice.reset()

# ## END DBK
