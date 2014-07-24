"""
-*- test-case-name: PyHouse.src.Modules.drivers.test.test_thermostat -*-

@name: PyHouse/src/Modules/drivers/Driver_USB.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 27, 2011
@summary: This module is for communicating with USB devices.


This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

Instead of using callLater timers, it would be better to use deferred callbacks when data arrives.

"""

# Import system type stuff
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util
from twisted.internet.protocol import Protocol

# Import PyHouse modules
from Modules.utils.tools import PrintBytes, PrettyPrintAny
from Modules.utils import pyh_log

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.USBDriver   ')


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


class SerialProtocol(Protocol):

    m_data = None

    def __init__(self, p_data, p_USB_obj):
        self.m_data = p_data
        self.m_controller_obj = p_USB_obj

    def connectionFailed(self):
        LOG.error("Driver_USB.connectionFailed() - {0:}".format(self))

    def connectionMade(self):
        if g_debug >= 2:
            LOG.debug('Driver_USB.connectionMade() - Connected to Serial Device')  # , dir(self), vars(self)

    def dataReceived(self, p_data):
        if g_debug >= 2:
            LOG.debug("Driver_USB.dataReceived() - {0:}".format(PrintBytes(p_data)))
        self.m_USB_obj.message += p_data


class UsbDriverAPI(UsbDeviceData):

    m_controller_obj = None

    def _setup_hid_17DD_5500(self, p_USB_obj):
        """Use the control endpoint to set up report descriptors for HID devices.

        Much of this was determined empirically for a smarthome UPB PIM
        """
        l_report = bytearray(b'12345')
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03  # len ???
        l_requestType = 0x21  # LIBUSB_ENDPOINT_OUT (0x00) | LIBUSB_REQUEST_TYPE_CLASS (0x20) | LIBUSB_RECIPIENT_DEVICE (0x00)
        l_request = 0x09  # Driver_USB.HID_SET_REPORT  # 0x09
        l_value = 0x0003  # Report type & Report ID
        l_index = 0  #
        l_ret = (l_requestType,
                l_request,
                l_value,
                l_index,
                l_report)
        p_USB_obj.Device.ctrl_transfer(l_requestType, l_request, l_value, l_index, l_report)
        if g_debug >= 2:
            l_msg = "_setup_hid_17DD_5500() ", l_ret
            LOG.debug(l_msg)
        return l_ret

    def _format_vpn(self, p_USB_obj):
        """Printable Vendor Product and controller name
        """
        l_ret = "{0:#04x}:{1:#04x} {2:}".format(p_USB_obj.Vendor, p_USB_obj.Product, p_USB_obj.Name)
        return l_ret

    def _is_hid(self, p_device):
        if p_device.bDeviceClass == 3:
            return True

    def _setup_find_device(self, p_USB_obj):
        """First step in opening a USB device.
        Get the number of configurations.

        @return:  None if no such device or a pyusb device object
        """
        l_vpn = self._format_vpn(p_USB_obj)
        try:
            l_device = usb.core.find(idVendor = p_USB_obj.Vendor, idProduct = p_USB_obj.Product)
        except usb.USBError:
            LOG.error("ERROR no such USB device for {0:}".format(l_vpn))
            return None
        if l_device == None:
            LOG.error('ERROR - USB device not found  {0:}'.format(l_vpn))
            return None
        p_USB_obj.Device = l_device
        p_USB_obj.num_configs = l_device.bNumConfigurations
        p_USB_obj.hid_device = self._is_hid(l_device)
        if g_debug >= 1:
            LOG.debug('Found a device - HID: {0:}'.format(l_vpn))
        p_USB_obj.configs = {}
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
        self.m_controller_obj = p_USB_obj
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
        self.m_controller_obj = p_USB_obj
        p_USB_obj.message = bytearray()
        l_vpn = self._format_vpn(p_USB_obj)
        LOG.info("Opening USB device - {0:}".format(l_vpn))
        p_USB_obj.Device = self._setup_find_device(p_USB_obj)
        if p_USB_obj.Device == None:
            LOG.error('ERROR - Setup Failed')
            return False
        self._setup_detach_kernel(p_USB_obj)
        self._setup_configurations(p_USB_obj)
        self._setup_interfaces(p_USB_obj)
        self._setup_endpoints(p_USB_obj)
        _l_msg = self._setup_hid_17DD_5500(p_USB_obj)
        return True

    def close_device(self, p_USB_obj):
        self.m_controller_obj = p_USB_obj
        p_USB_obj.Device.reset()

    def read_usb(self, p_pyhouse_obj):
        """Routine that reads the USB device.
        Calls either HID or Non-HID routines to fetch tha actual data.
        """
        p_pyhouse_obj.Twisted.Reactor.callLater(RECEIVE_TIMEOUT, self.read_usb, p_pyhouse_obj)
        if self.m_USB_obj.hid_device:
            l_msg = self.read_hid_report(self.m_USB_obj)
        else:
            l_msg = self.read_device(self.m_USB_obj)
        for l_ix in range(len(l_msg)):
            self.m_USB_obj.message.append(l_msg[l_ix])
        if len(l_msg) > 0:
            LOG.debug('Driver - ReadUSB  JustRead:{0:}'.format(PrintBytes(l_msg)))
        if len(self.m_USB_obj.message) > 0:
            LOG.debug('Driver - ReadUSB  Accumulated:{0:}'.format(PrintBytes(self.m_USB_obj.message)))
        return l_msg

    def read_device(self, p_USB_obj):
        """
        Get any data the USB device has and append it to the controller _Data field.
        @return: the number of bytes fetched from the controller
        """
        try:
            l_msg = p_USB_obj.Device.read(p_USB_obj.epi_addr, p_USB_obj.epi_packet_size, timeout = 100)  # Note - No device to test with
            if g_debug >= 1:
                LOG.debug("read_device() - Msg:{1:}".format(PrintBytes(l_msg)))
        except usb.USBError as e_err:
            LOG.error("ERROR - read_device() got USBError - {0:}".format(e_err))
            l_msg = bytearray(0)
        except Exception as e_err:
            LOG.error("ERROR - read_device() {0:}".format(e_err))
            l_msg = bytearray(0)
        return l_msg

    def _extract_hid_report(self, p_message):
        """
        Take a HID report and clean up the data to be useful

        @param p_message: is the data received from the USB device
        @type p_message: bytearray

        @return: a bytearray with the length byte removes and trimmed to the length
        """
        l_ret = bytearray(0)
        if len(p_message) == 0:
            return l_ret
        l_len = p_message[0] & 0x0F
        if l_len > 0:
            if g_debug >= 1:
                LOG.debug("read_hid_report() A - Msg:{0:}".format(PrintBytes(p_message)))
            l_ret = p_message[1:l_len + 1]
        return l_ret

    def read_hid_report(self, p_USB_obj):
        """This is probably not the right place to do this BUT

        The report looks like 0xF1 0x33 0x00 0x00 0x00 0x00 0x00 0x00
        with the first byte being 0xFx where x is 0-7 = length of the data
        So here we will strip off the length and append the rest of the message to the buffer

        I really think this is PIM specific but it makes sense to only pass back the real message if we can.

        When we get interrupts working (if ever) then we can pass the data to the UPB pim for cleanup but for now
        we need to do this to avoid filling up the pim buffer with an endledss string of 0xF0 bytes meaning no data
        was available.
        """
        try:
            l_msg = p_USB_obj.Device.read(p_USB_obj.epi_addr, p_USB_obj.epi_packet_size, timeout = 100)
        except usb.USBError as e_err:
            LOG.error("ERROR - read_hid_report() got USBError {0:}".format(e_err))
            l_msg = bytearray(0)
        except Exception as e_err:
            LOG.error("ERROR - read_hid_report() {0:}".format(e_err))
            l_msg = bytearray(0)
        l_ret = self._extract_hid_report(l_msg)
        return l_ret

    def fetch_read_data(self):
        l_ret = self.m_USB_obj.message
        # PrettyPrintAny(self.m_USB_obj, 'Driver_USB - FetchData ')
        self.m_USB_obj.message = bytearray()
        if len(l_ret) == 0:
            return l_ret
        if g_debug >= 1:
            LOG.debug("fetch_read_data() - Msg:{0:}".format(PrintBytes(l_ret)))
        return l_ret

    def write_usb(self, p_message):
        if self.m_USB_obj.hid_device:
            self.write_report(self.m_USB_obj, p_message)
        else:
            self.write_device(self.m_USB_obj, p_message)

    def write_report(self, p_USB_obj, p_message):
        if g_debug >= 1:
            LOG.debug("Write Report - {0:}".format(PrintBytes(p_message)))
        self._write_bis_device(p_USB_obj, p_message)

    def write_device(self, p_USB_obj, p_message):
        """Send message to the USB device.

        Sending speed is up to the controller.
        Someday we may provide notification that a command is complete.

        @return: the number of bytes written
        """
        if g_debug >= 1:
            LOG.debug("write_device() - {0:}".format(PrintBytes(p_message)))
        if p_USB_obj.epi_type == 0:
            self._write_control_device(p_USB_obj, p_message)
        else:
            self._write_bis_device(p_USB_obj, p_message)

    def _write_bis_device(self, p_USB_obj, p_message):
        """Bulk, Interrupt, isoSynchronous
        """
        l_message = p_message
        if g_debug >= 1:
            LOG.debug("write_bis_device() - Ep_out: {0:#04X}, - {1:}".format(p_USB_obj.epo_addr, PrintBytes(l_message)))
        try:
            l_len = p_USB_obj.Device.write(p_USB_obj.epo_addr, l_message)
        except Exception as e:
            LOG.error("_write_bis_device() - Error in writing to USB device {0:}".format(e))
            l_len = 0
        return l_len

    def _write_control_device(self, p_USB_obj, p_message):
        if g_debug >= 1:
            LOG.debug("_write_control_device() {0:}".format(p_USB_obj.Device))
        l_len = p_USB_obj.Device.ctrl_transfer(0, p_message, timeout = 100)
        return l_len

class API(UsbDriverAPI):

    def _get_usb_device_data(self, p_USB_obj):
        l_usb_device_obj = UsbDeviceData()
        l_usb_device_obj.Name = p_USB_obj.Name
        l_usb_device_obj.Port = p_USB_obj.Port
        l_usb_device_obj.Vendor = p_USB_obj.Vendor
        l_usb_device_obj.Product = p_USB_obj.Product
        return l_usb_device_obj

    def __init__(self):
        """
        """
        if g_debug >= 1:
            LOG.info('Initialized')

    def Start(self, p_pyhouse_obj, p_controller_obj):
        """
        @param p_controller_obj: is the Controller_Data object we are starting.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        self.m_USB_obj = self._get_usb_device_data(p_controller_obj)
        if self.open_device(self.m_USB_obj):
            self.read_usb(p_pyhouse_obj)
            LOG.info("Opened Controller:{0:}".format(self.m_USB_obj.Name))
            self.write_usb(bytearray(b'\x00\x01\x02\x03'))
            self.write_usb(bytearray(b'\xff\x01\x02\x03'))
            l_ret = True
        else:
            LOG.warning("Failed to open Controller:{0:}".format(self.m_USB_obj.Name))
            l_ret = False
        if g_debug >= 1:
            LOG.info('Started')
        return l_ret

    def Stop(self):
        self.close_device(self.m_controller_obj)

    def Read(self):
        l_ret = self.fetch_read_data()
        return l_ret

    def Write(self, p_message):
        self.write_usb(p_message)

# ## END DBK
