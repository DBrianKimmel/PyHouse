'''
Created on Dec 20, 2012

@author: briank
'''

import array
import sys
import time
from twisted.internet import reactor
# Use USB package that was written by Wander Lairson Costa
# PYUSB_DEBUG_LEVEL=debug
# export PYUSB_DEBUG_LEVEL
import usb.core
import usb.util

import Driver_USB


callLater = reactor.callLater

g_debug = Driver_USB.g_debug

# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3
READ_TIMER = 0.100  # Every 100 miliseconds

class UsbDriverAPI(Driver_USB.UsbDriverAPI):
    """
    """

    def read_device(self):
        l_len = -1
        while l_len != 0:
            try:
                l_msg = self.m_device.read(self.m_epi_addr, self.m_epi_packet_size, timeout = 100)
                # we seem to have actual length + 240 as 1st char
                l_len = l_msg[0] - 240
                if l_len > 0:
                    if g_debug > 1:
                        print "Driver_USB.read_device() {0:} - {1:}".format(l_len, l_msg)
                    self.m_bytes += l_len
                    for l_x in range(l_len):
                        self.m_message.append(l_msg[l_x + 1])
            except usb.USBError, e:
                print "Driver_USB.read_device() got USBError", e
            except Exception, e:
                print " -- Error in Driver_USB.read_device() ", sys.exc_info(), e
            time.sleep(0.1)


def Init(p_obj):
    """
    """
    if g_debug > 0:
        print "\nDriver_USB_0403_6001.Init()"
    l_ret = Driver_USB.Init(p_obj, READ_TIMER, UsbDriverAPI())
    return l_ret

# ## END
