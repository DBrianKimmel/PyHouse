"""
@name:      PyHouse/src/Modules/Drivers/USB/Driver_USB_17DD_5500.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 13, 2012
@summary:   This module is for


Created to handle the UPB PIM which is a HID device.

Bus xxx Device yyy: ID 17dd:5500
Device Descriptor:
  bLength                18  [0]
  bDescriptorType         1  [1]
  bcdUSB               1.00  [2:4]
  bDeviceClass            0  [4] - (Defined at Interface level)
  bDeviceSubClass         0  [5]
  bDeviceProtocol         0  [6]
  bMaxPacketSize0         8  [7]
  idVendor           0x17dd  [8:10]
  idProduct          0x5500  [10:12]
  bcdDevice            0.00  [12:14]
  iManufacturer           1  [14] - Simply Automated Inc.
  iProduct                2  [15] - USB to Serial
  iSerial                 0  [16]
  bNumConfigurations      1  [17]

    Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength           41
    bNumInterfaces          1
    bConfigurationValue     1
    iConfiguration          4 Sample HID
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              100mA

    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           2
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      0 No Subclass
      bInterfaceProtocol      0 None
      iInterface              0

        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.00
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 Report
          wDescriptorLength      37

         Report Descriptors:
           ** UNAVAILABLE **

      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              10

      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x02  EP 2 OUT
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              10

"""

__updated__ = '2019-10-06'

# import array
import usb

# Import PyMh files
# from Modules.Drivers.USB import USB_driver
from Modules.Core import logging_pyh as Logger
from _ctypes import Array
from array import array

LOG = Logger.getLogger('PyHouse.UPB_17DD_5500  ')


class Api(object):

    @staticmethod
    def Setup():
        """Use the control endpoint to set up report descriptors for HID devices.

        Much of this was determined empirically for a smarthome UPB PIM
        """
        l_requestType = 0x21  # LIBUSB_ENDPOINT_OUT (0x00) | LIBUSB_REQUEST_TYPE_CLASS (0x20) | LIBUSB_RECIPIENT_DEVICE (0x00)
        l_request = 0x09  #
        l_value = 0x0003  # Report type & Report ID
        l_index = 0
        l_report = bytearray(b'12345')
        # l_report = array.array('B', '\x00'.encode('utf-8') * 5)
        l_report[0] = 0xc0
        l_report[1] = 0x12
        l_report[2] = 0x00
        l_report[3] = 0x00
        l_report[4] = 0x03
        l_ret = (l_requestType,
                l_request,
                l_value,
                l_index,
                l_report)
        LOG.info("USB_driver_17DD_5500._setup_hid_device() {}".format(l_ret))
        return l_ret

    @staticmethod
    def Read(self, p_usb):
        print("USB_driver_17DD_5500.read_device() - usb ={}".format(p_usb))
        l_len = -1
        while l_len != 0:
            try:
                l_msg = p_usb.Device.read(0x81, 8, timeout=1000)
                # we seem to have actual length + 240 as 1st char
                l_len = l_msg[0] - 240
                if l_len > 0:
                    LOG.info("USB_driver.read_device() {} - {}".format(l_len, l_msg))
                    for l_x in range(l_len):
                        p_usb.message.append(l_msg[l_x + 1])
            except usb.USBError as e:
                l_len = 0
                break
            except Exception as e:
                LOG.info(" -- Error in USB_driver_17DD_5500.read_device() ".format(e))
                l_len = 0
                break

# ## END DBK
