"""
@name:      PyHouse/src/Modules/Drivers/USB/USB_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 29, 2015
@Summary:

"""

class UsbData(object):
    """
    This is the data object for one USB controller device.

    Instance
    """

    def __init__(self):
        self.UsbDevice = None
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

# ## END DBK
