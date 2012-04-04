#!/usr/bin/python

"""Driver_USB.py - USB Driver module. 

This will interface various PyHouse modules to a USB device.

This may be instanced as many times as there are USB devices to control.

This should also allow control of many different houses.
"""

# Import system type stuff
import logging
import usb.core
import usb.util


# Import PyHouse modules
#from tools import Lister


class UsbDeviceData(object):

    def __init__(self):
        pass


class UsbDriverAPI(UsbDeviceData):
    """
    """

    def open_device(self):
        pass

    def close_device(self):
        pass

    def read_device(self):
        pass

    def write_device(self):
        pass


class UsbUtility(UsbDriverAPI):
    """
    """

    def extract_usb(self, p_obj):
        self.m_device_data = UsbDeviceData()
        self.m_device_data.Vendor = int(p_obj.Vendor, 0)
        self.m_device_data.Product = int(p_obj.Product, 0)
        print "!  Driver_USB.extract_usb {0:X} {1:X}".format(self.m_device_data.Vendor, self.m_device_data.Product)

    def usb_open(self):
        self.m_device_data.Device = usb.core.find(idVendor = self.m_device_data.Vendor, idProduct = self.m_device_data.Product)
        if self.m_device_data.Device is None:
            self.m_logger.error('USB device not found ')
            print "!  Driver_USB.usb_open - Device not found."
            return False
        self.dump_usb_info_for_debugging()
        print "!  Driver_USB.usb_open - about to set_configuration"
        try:
            self.m_device_data.Device.set_configuration()
        except:
           print "!  Driver_USB.usb_open - Set config error."
        print "!  Driver_USB.usb_open - about to get_active_configuration"
        self.m_device_data.m_endpoint_cfg = self.m_device_data.Device.get_active_configuration()

    def dump_usb_info_for_debugging(self):
        Vend = self.m_device_data.Device.idVendor
        Prod = self.m_device_data.Device.idProduct
        Cfgs = self.m_device_data.Device.bNumConfigurations
        print "! !Driver_USB.usb_open"
        print "   Vendor:{0:X}:{1:X}, Configs:{2:}".format(Vend, Prod, Cfgs)
        print


class USBDriverMain(UsbUtility):
    """
    """

    def __init__(self, p_obj):
        print "!  USBDriverMain.__init__()", p_obj
        self.m_logger = logging.getLogger('PyHouse.USBDriver')
        self.m_logger.info(" Initializing USB port")
        self.extract_usb(p_obj)
        self.usb_open()

### END
