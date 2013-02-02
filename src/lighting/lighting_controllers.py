#!/usr/bin/env python

"""Superclass

Handle the controller component of the lighting system.

"""

import lighting_tools

Controller_Data = {}
ControllerCount = 0

g_debug = 9


class ControllerData(lighting_tools.CoreData):

    def __init__(self):
        global ControllerCount
        ControllerCount += 1
        # print " C lighting_controllers.__init__()"
        super(ControllerData, self).__init__()
        self.Type = 'Controller'
        # All controllers (Common)
        self.Interface = None
        self.Port = None
        # Serial Controllers interface
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
        # USB Controllers interface
        self.Product = None
        self.Vendor = None

    def __str__(self):
        l_ret = "LightingController:: Name:{0:}, Family:{1:}, Interface:{2:}, Port:{3:}, Type:{4:}, ".format(
                self.Name, self.Family, self.Interface, self.Port, self.Type)
        l_ret += "Baud:{0:}, ByteSize:{1:}, Parity:{2:}, StopBits:{3:} ".format(self.BaudRate, self.ByteSize, self.Parity, self.StopBits)
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

    def get_network_id(self):
        return self.__NetworkID
    def set_network_id(self, value):
        self.__NetworkID = value
    def get_unit_id(self):
        return self.__UnitID
    def set_unit_id(self, value):
        self.__UnitID = value
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

    NetworkID = property(get_network_id, set_network_id, None, None)
    UnitID = property(get_unit_id, set_unit_id, None, None)
    Password = property(get_password, set_password, None, None)
    Product = property(get_product, set_product, None, None)
    Vendor = property(get_vendor, set_vendor, None, None)


class ControllersAPI(lighting_tools.CoreAPI):

    def __init__(self):
        # print " C lighting_controller.ControllerAPI.__init__()"
        super(ControllersAPI, self).__init__()

    def get_ControllerCount(self):
        return ControllerCount

    def load_controller(self, p_dict, p_ctlr):
        l_ctlr = super(ControllersAPI, self).load_core_device(p_dict, self.get_ControllerCount())
        if g_debug > 0:
            print " C lighting_controllers.load_controller() - {0:}".format(p_ctlr.Name)
        l_ctlr.Interface = self.getValue(p_dict, 'Interface')
        l_ctlr.Port = self.getValue(p_dict, 'Port')
        # Serial Data
        l_ctlr.BaudRate = self.getValue(p_dict, 'BaudRate')
        l_ctlr.ByteSize = self.getInt(p_dict, 'ByteSize')
        l_ctlr.DsrDtr = self.getBool(p_dict, 'DsrDtr')
        l_ctlr.InterCharTimeout = self.getFloat(p_dict, 'InterCharTimeout')
        l_ctlr.Parity = self.getValue(p_dict, 'Parity')
        l_ctlr.RtsCts = self.getBool(p_dict, 'RtsCts')
        l_ctlr.StopBits = self.getFloat(p_dict, 'StopBits')
        l_ctlr.Timeout = self.getFloat(p_dict, 'Timeout')
        l_ctlr.WriteTimeout = self.getFloat(p_dict, 'WriteTimeout')
        l_ctlr.XonXoff = self.getBool(p_dict, 'XonXoff')
        # USB Data
        l_ctlr.NetworkID = self.getInt(p_dict, 'Network')
        l_ctlr.UnitID = self.getInt(p_dict, 'UnitID')
        l_ctlr.Password = self.getInt(p_dict, 'Password')
        l_ctlr.Product = self.getInt(p_dict, 'Product')
        l_ctlr.Vendor = self.getInt(p_dict, 'Vendor')
        # Ethernet Data # ---None yet
        return l_ctlr

    def dump_all_controllers(self):
        print "***** All Controllers *****"
        for l_key, l_obj in Controller_Data.iteritems():
            self.dump_device(l_obj, 'Controller', l_key)
        print

    def update_all_controllers(self):
        """Write out config file
        (usually called from web-server after update/add)
        """
        pass

# ## END
