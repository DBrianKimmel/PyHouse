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


class UsbUtility(UsbDeviceData):
    """
    """

    def extract_usb(self, p_obj):
        self.m_device_data = UsbDeviceData()
        self.m_device_data.Vendor = p_obj.Vendor
        self.m_device_data.Product = p_obj.Product
        print "!  Driver_USB.extract_usb ", self.m_device_data.Vendor, self.m_device_data.Product

    def usb_open(self):
        self.m_device_data.Device = usb.core.find(idVendor = self.m_device_data.Vendor, idProduct = self.m_device_data.Product)
        if self.m_device_data.Device is None:
            self.m_logger.error('USB device not found ')
            print "!  Driver_USB.usb_open - Device not found."
            return False
        #self.m_device_data.Device.set_configuration()
        self.m_device_data.m_endpoint_cfg = self.m_device_data.Device.get_active_configuration()



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
