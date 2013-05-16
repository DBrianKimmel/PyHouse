'''
Created on Dec 13, 2012

@author: briank

Created to handle the UPB PIM which is a HID device.

Bus xxx Device yyy: ID 17dd:5500
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               1.00
  bDeviceClass            0 (Defined at Interface level)
  bDeviceSubClass         0
  bDeviceProtocol         0
  bMaxPacketSize0         8
  idVendor           0x17dd
  idProduct          0x5500
  bcdDevice            0.00
  iManufacturer           1 Simply Automated Inc.
  iProduct                2 USB to Serial
  iSerial                 0
  bNumConfigurations      1
'''
# import array
import sys
from twisted.internet import reactor
import usb
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL

import Driver_USB

callLater = reactor.callLater

g_debug = Driver_USB.g_debug

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for polling the usb device for data to be added to the rx buffer
READ_TIMER = 0.100  # Every 100 miliseconds

class UsbDriverAPI(Driver_USB.UsbDriverAPI):

    def setup_hid_device(self):
        """Use the control endpoint to set up report descriptors for HID devices.

        Much of this was determined empirically for a smarthome UPB PIM
        """
        l_report = bytearray(b'12345')
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03
        l_requestType = 0x21  # LIBUSB_ENDPOINT_OUT (0x00) | LIBUSB_REQUEST_TYPE_CLASS (0x20) | LIBUSB_RECIPIENT_DEVICE (0x00)
        l_request = Driver_USB.HID_SET_REPORT  # 0x09
        l_value = 0x0003  # Report type & Report ID
        l_index = 0
        l_ret = (l_requestType,
                l_request,
                l_value,
                l_index,
                l_report)
        if g_debug > 1:
            print "Driver_USB_17DD_5500._setup_hid_device() ", l_ret
        return l_ret

    def read_device(self, p_usb):
        callLater(RECEIVE_TIMEOUT, lambda x = p_usb: self.read_device(x))
        if g_debug > 5:
            print "Driver_USB_17DD_5500.read_device() - usb =", p_usb
        l_len = -1
        while l_len != 0:
            try:
                l_msg = p_usb.Device.read(0x81, 8, timeout = 1000)
                # we seem to have actual length + 240 as 1st char
                l_len = l_msg[0] - 240
                if l_len > 0:
                    if g_debug > 1:
                        print "Driver_USB.read_device() {0:} - {1:}".format(l_len, l_msg)
                    for l_x in range(l_len):
                        p_usb.message.append(l_msg[l_x + 1])
            except usb.USBError, e:
                # print "Driver_USB_17DD_5500.read_device() got USBError", e
                l_len = 0
                break
            except Exception, e:
                print " -- Error in Driver_USB_17DD_5500.read_device() ", sys.exc_info(), e
                l_len = 0
                break
        if g_debug > 5:
            print "Driver_USB_17DD_5500.read_device() - exit"


class API(UsbDriverAPI):

    m_driver = None

    def __init__(self):
        """
        """
        if g_debug > 0:
            print "Driver_USB_17DD_5500.__init__() "
        self.m_driver = Driver_USB.API()

    def Start(self, p_controller_obj):
        if g_debug > 0:
            print "Driver_USB_17DD_5500.Start() - Name:{0:}".format(p_controller_obj.Name)
        self.m_driver.Start(p_controller_obj, self)

    def Stop(self, p_obj):
        if g_debug > 0:
            print "Driver_USB_17DD_5500.Start()", p_obj.Name
        self.m_driver.Start(p_obj)

# ## END
