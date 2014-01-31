'''
Created on Dec 20, 2012

@author: briank

Created to handle the Insteon PLM controller:

'''

# Import system type stuff
import sys
from twisted.internet import reactor
import usb

# Import PyMh files
from src.drivers import Driver_USB

callLater = reactor.callLater


g_debug = Driver_USB.g_debug

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for polling the usb device for data to be added to the rx buffer
READ_TIMER = 0.100  # Every 100 miliseconds

class UsbDriverAPI(Driver_USB.UsbDriverAPI):
    """
    """

    def read_device(self, p_usb):
        callLater(RECEIVE_TIMEOUT, lambda x = p_usb: self.read_device(x))
        if g_debug > 5:
            print "Driver_USB_0403_6001.read_device() A - Name:{0:}, Endpoint:{1:#02x}, Size:{2:}".format(p_usb.Name, p_usb.epi_addr, p_usb.epi_packet_size)
        try:
            l_msg = p_usb.Device.read(p_usb.epi_addr, p_usb.epi_packet_size, timeout = 400)
            l_len = len(l_msg)
            if l_len > 0:
                if g_debug > 4:
                    print "Driver_USB_0403_6001.read_device() B - Len:{0:}, Msg:{1:}".format(l_len, l_msg)
                for l_x in range(l_len):
                    p_usb.message.append(l_msg[l_x])
            elif g_debug > 5:
                print "Driver_USB_0403_6001.read_device() C - len was 0 ", l_msg
        except usb.USBError as e:
            print "Driver_USB_0403_6001.read_device() got USBError", e
            l_len = 0
            # break
        except Exception as e:
            print " -- Error in Driver_USB_0403_6001.read_device() ", sys.exc_info(), e
            l_len = 0
            # break
        if g_debug > 5:
            print "Driver_USB_0403_6001.read_device() - exit"


class API(UsbDriverAPI):

    m_driver = None

    def __init__(self):
        """
        """
        if g_debug > 0:
            print "Driver_USB_0403_6001.__init__() "
        self.m_driver = Driver_USB.API()

    def Start(self, p_controller_obj):
        if g_debug > 0:
            print "Driver_USB_0403_6001.Start() - Name:{0:}".format(p_controller_obj.Name)
        self.m_driver.Start(p_controller_obj, self)

    def Stop(self):
        if g_debug > 0:
            print "Driver_USB_0403_6001.Stop() "
        self.m_driver.Stop()

# ## END DBK
