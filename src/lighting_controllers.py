#!/usr/bin/env python

"""Superclass

Handle the controller component of the lighting system.

"""

import lighting_tools
import pprint

Controller_Data = {}


class ControllerData(lighting_tools.LightingTools):

    def __init__(self):
        lighting_tools.LightingTools.__init__(self)
        # All controlers (Common)
        self.Interface = None
        self.Port = None
        self.Type = 'Controller'
        # Serial Controllers
        self.BaudRate = None
        self.ByteSize = 8
        self.DsrDtr = None
        self.InterCharTimeout = None
        self.Parity = None
        self.RtsCts = None
        self.StopBits = None
        self.Timeout = None
        self.WriteTimeout = None
        self.XonXoff = None
        # USB Data
        self.Network = None
        self.Password = None
        self.Product = None
        self.Vendor = None

        #self.Address = None

    def __repr__(self):
        l_ret = "Lighting Controller Name:{0:}, Family:{1:}, Interface:{2:}, Port:{3:}, Type:{4:} ".format(
                self.Name, self.Family, self.Interface, self.Port, self.Type)
        return l_ret

    def get_interface(self):
        return self.__Interface
    def set_interface(self, value):
        self.__Interface = value
    def get_port(self):
        return self.__Port
    def set_port(self, value):
        self.__Port = value

    def get_baud_rate(self):
        return self.__BaudRate
    def set_baud_rate(self, value):
        self.__BaudRate = value
    def get_byte_size(self):
        return self.__ByteSize
    def set_byte_size(self, value):
        self.__ByteSize = value
    def get_dsr_dtr(self):
        return self.__DsrDtr
    def set_dsr_dtr(self, value):
        self.__DsrDtr = value
    def get_inter_char_timeout(self):
        return self.__InterCharTimeout
    def set_inter_char_timeout(self, value):
        self.__InterCharTimeout = value
    def get_parity(self):
        return self.__Parity
    def set_parity(self, value):
        self.__Parity = value
    def get_rts_cts(self):
        return self.__RtsCts
    def set_rts_cts(self, value):
        self.__RtsCts = value
    def get_stop_bits(self):
        return self.__StopBits
    def set_stop_bits(self, value):
        self.__StopBits = value
    def get_timeout(self):
        return self.__Timeout
    def set_timeout(self, value):
        self.__Timeout = value
    def get_write_timeout(self):
        return self.__WriteTimeout
    def set_write_timeout(self, value):
        self.__WriteTimeout = value
    def get_xon_xoff(self):
        return self.__XonXoff
    def set_xon_xoff(self, value):
        self.__XonXoff = value

    def get_network(self):
        return self.__Network
    def set_network(self, value):
        self.__Network = value
    def get_password(self):
        return self.__Password
    def set_password(self, value):
        self.__Password = value
    def get_product(self):
        return self.__Product
    def set_product(self, value):
        self.__Product = value
    def get_vendor(self):
        return self.__Vendor
    def set_vendor(self, value):
        self.__Vendor = value

    Interface = property(get_interface, set_interface, None, "Interface's docstring")
    Port = property(get_port, set_port, None, "Port's docstring")

    BaudRate = property(get_baud_rate, set_baud_rate, None, "BaudRate's docstring")
    ByteSize = property(get_byte_size, set_byte_size, None, "ByteSize's docstring")
    DsrDtr = property(get_dsr_dtr, set_dsr_dtr, None, "DsrDtr's docstring")
    InterCharTimeout = property(get_inter_char_timeout, set_inter_char_timeout, None, "InterCharTimeout's docstring")
    Parity = property(get_parity, set_parity, None, "Parity's docstring")
    RtsCts = property(get_rts_cts, set_rts_cts, None, "RtsCts's docstring")
    StopBits = property(get_stop_bits, set_stop_bits, None, None)
    Timeout = property(get_timeout, set_timeout, None, None)
    WriteTimeout = property(get_write_timeout, set_write_timeout, None, None)
    XonXoff = property(get_xon_xoff, set_xon_xoff, None, None)

    Network = property(get_network, set_network, None, None)
    Password = property(get_password, set_password, None, None)
    Product = property(get_product, set_product, None, None)
    Vendor = property(get_vendor, set_vendor, None, None)


class ControllerAPI(ControllerData):

    def load_all_controllers(self, p_dict):
        """Each family controller section of the family config file is processed here.
        """
        for l_key, l_dict in p_dict.iteritems():
            l_ctlr = self.load_controller(l_dict)
            Controller_Data[l_key] = l_ctlr

    def load_controller(self, p_dict):
        Name = p_dict.get('Name', 'LightingController')
        l_ctlr = ControllerData()
        # Common Data
        l_ctlr.Active = self.getBool(p_dict, 'Active')
        l_ctlr.Comment = self.getValue(p_dict, 'Comment')
        l_ctlr.Family = self.getValue(p_dict, 'Family')
        l_ctlr.Interface = self.getValue(p_dict, 'Interface')
        l_ctlr.Name = self.getValue(p_dict, 'Name')
        l_ctlr.Port = self.getValue(p_dict, 'Port')
        l_ctlr.Type = self.getValue(p_dict, 'Type')
        # Serial Data
        l_ctlr.BaudRate = self.getValue(p_dict, 'BaudRate')
        l_ctlr.ByteSize = self.getInt(p_dict, 'ByteSize')
        l_ctlr.DsrDtr = self.getBool(p_dict, 'DsrDtr')
        l_ctlr.InterCharTimeout = p_dict.get('InterCharTimeout', None)
        l_ctlr.Parity = p_dict.get('Parity', None)
        l_ctlr.RtsCts = self.getBool(p_dict, 'RtsCts')
        l_ctlr.StopBits = p_dict.get('StopBits', None)
        l_ctlr.Timeout = p_dict.get('Timeout', None)
        l_ctlr.WriteTimeout = p_dict.get('WriteTimeout', None)
        l_ctlr.XonXoff = self.getBool(p_dict, 'XonXoff')
        # USB Data
        l_ctlr.Network = self.getInt(p_dict, 'Network')
        l_ctlr.Password = self.getInt(p_dict, 'Password')
        l_ctlr.Product = self.getInt(p_dict, 'Product')
        l_ctlr.Vendor = self.getInt(p_dict, 'Vendor')
        # Ethernet Data # ---None yet
        return l_ctlr

    def dump_all_controllers(self):
        print "***** All Controllers *****"
        for l_key, l_obj in Controller_Data.iteritems():
            print "~~~Controller: {0:}".format(l_key)
            print "     ", l_obj
            print
            pprint.pprint(vars(l_obj))
            print "--------------------"
        print

    def update_all_controllers(self):
        """Write out config file
        (usually called from web-server after update/add)
        """
        pass

### END
