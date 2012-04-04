#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""


Controller_Data = {}


class ControllerData(object):
    """
    """

    def __init__(self, Name):
        #print " --lighting.Controller_Data.__init__() ", Name
        self.Name = Name

    def X__repr__(self):
        l_ret = "Lighting Controller Name:{0:}, Family:{1:} ".format(self.Name, self.Family)
        return l_ret

    def get_Port(self):
        return self.Port

    def get_BaudRate(self):
        return int(self.BaudRate)

    def get_Family(self):
        return self.Family

    def get_Interface(self):
        return self.Interface


class ControllerAPI(ControllerData):
    """
    """

    def load_controller(self, p_dict):
        """Load the common part of the controller.
        """
        print "## lighting.load_controller ", p_dict.keys()
        Name = p_dict.get('Name', 'LightingController')
        l_ctlr = ControllerData(Name)
        # Common Data
        l_ctlr.Active = p_dict.get('Active', 'False')
        l_ctlr.Family = p_dict.get('Family', 'None')
        l_ctlr.Interface = p_dict.get('Interface', 'None')
        l_ctlr.Port = p_dict.get('Port', 'None')
        l_ctlr.Type = p_dict.get('Type', None)
        # Serial Data
        l_ctlr.BaudRate = p_dict.get('BaudRate', None)
        l_ctlr.ByteSize = p_dict.get('ByteSize', None)
        l_ctlr.DsrDtr = p_dict.get('DsrDtr', None)
        l_ctlr.InterCharTimeout = p_dict.get('InterCharTimeout', None)
        l_ctlr.Parity = p_dict.get('Parity', None)
        l_ctlr.RtsCts = p_dict.get('RtsCts', None)
        l_ctlr.StopBits = p_dict.get('StopBits', None)
        l_ctlr.Timeout = p_dict.get('Timeout', None)
        l_ctlr.WriteTimeout = p_dict.get('WriteTimeout', None)
        l_ctlr.XonXoff = p_dict.get('XonXoff', None)
        # USB Data
        l_ctlr.Product = p_dict.get('Product', None)
        l_ctlr.Vendor = p_dict.get('Vendor', None)
        # Ethernet Data
        # ---None yet
        #
        Controller_Data[Name] = l_ctlr
        return l_ctlr

    def dump_all_controllers(self):
        pass


### END
