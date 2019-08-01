"""

@name:      PyHouse/src/Modules/Families/Insteon/_test/test_Insteon_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 20, 2012
@summary:   TCreated to handle the Insteon PLM controller

"""

__updated__ = '2016-09-23'

# Import system type stuff
from twisted.internet import reactor
import usb

# Import PyMh files
from Modules.Drivers.USB import USB_driver

callLater = reactor.callLater


# Timeouts for send/receive delays
SEND_TIMEOUT = 0.8
RECEIVE_TIMEOUT = 0.3  # this is for polling the usb device for data to be added to the rx buffer
READ_TIMER = 0.100  # Every 100 miliseconds

class UsbDriverAPI(USB_driver.UsbDriverAPI):
    """
    """

    def read_device(self, p_usb):
        callLater(RECEIVE_TIMEOUT, lambda x=p_usb: self.read_device(x))
        print("USB_driver_0403_6001.read_device() A - Name:{}, Endpoint:{:#02x}, Size:{}".format(p_usb.Name, p_usb.epi_addr, p_usb.epi_packet_size))
        try:
            l_msg = p_usb.Device.read(p_usb.epi_addr, p_usb.epi_packet_size, timeout=400)
            l_len = len(l_msg)
            if l_len > 0:
                if g_debug > 4:
                    print("USB_driver_0403_6001.read_device() B - Len:{}, Msg:{}".format(l_len, l_msg))
                for l_x in range(l_len):
                    p_usb.message.append(l_msg[l_x])
            elif g_debug > 5:
                print("USB_driver_0403_6001.read_device() C - len was 0  {}".format(l_msg))
        except usb.USBError as e:
            print("USB_driver_0403_6001.read_device() got USBError {}".format(e))
            l_len = 0
            # break
        except Exception as e:
            print(" -- Error in USB_driver_0403_6001.read_device() {}".format(e))
            l_len = 0
            # break


class API(UsbDriverAPI):

    m_driver = None

    def __init__(self):
        """
        """
        self.m_driver = USB_driver.API()

    def Start(self, p_controller_obj):
        self.m_driver.Start(p_controller_obj, self)

    def Stop(self):
        self.m_driver.Stop()

# ## END DBK
