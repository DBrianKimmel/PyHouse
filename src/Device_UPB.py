#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import logging
import time

# Import PyMh files
import configure_mh
import lighting


m_config = None
m_logger = None


class UpbLightingData(lighting.LightingData):

    Name = ''
    Family = 'UPB'
    Type = ''
    Comment = ''
    CurLevel = 0


    def __init__(self, Name):
        lighting.LightingData.__init__(self, Name)
        self.Name = Name

    def __repr__(self):
        l_str = lighting.LightingData.__str__(self)
        l_str += " \t Address: {0:}".format(self.Address)
        return l_str

    def get_Name(self):
        return self.Name


class UPBLightingStatus(lighting.LightingStatus):
    """
    """


class UPBLightingDeviceAPI(lighting.LightingAPI):
    """
    """

    def turn_light_off(self, p_name):
        print "Turning off UPB light {0:}".format(p_name)

    def turn_light_on(self, p_name):
        print "Turning on UPB light {0:}".format(p_name)

    def turn_light_dim(self, p_name, p_level):
        print "Turning UPB light {0:} to level {1:}".format(p_name, p_level)

    def XXload_all_devices(self):
        """Called from lighting.
        """
        #print "Loading all UPB devices."
        self.Light_Data = {}
        l_dict = self.m_config.get_value("UPBLights")
        for l_dev, l_vals in l_dict.iteritems():
            Name = l_vals.get('Name', 'xx')
            Address = l_vals.get('Address', 123)
            Room = l_vals.get('Room', 'no room')
            #print "Name =", Name
            lighting.Light_Data[Name] = UpbLightingData(Name)

    def dump_all_devices(self):
        #print "Dumping all UPB Devices:"
        #for l_key, l_value in lighting.Light_Data.iteritems():
        #    print "  {0:} - {1:}".format(l_key, l_value)
        print


class UPBControllerData(lighting.ControllerData):

    Port = ''


    def __init__(self, Name):
        lighting.ControllerData.__init__(self, Name)
        print " __UPBControllerData.__init__() ", Name


class UPBControllerAPI(lighting.ControllerAPI):
    """
    """

    def __init__(self, Name):
        lighting.ControllerAPI.__init__(self, Name)

    def load_controllers(self, p_dict):
        print " - UPB_Device.load_controllers ", p_dict.keys()
        for l_key, l_dict in p_dict.iteritems():
            print " - ", l_key, l_dict
            Name = l_dict.get('Name', 'InsteonLightingController')
            #l_ctlr = UPBControllerData(Name)
            l_ctlr = lighting.ControllerAPI.load_controller(self, l_dict)
            """
            l_ctlr.Family = l_dict.get('Family', 'Insteon')
            l_ctlr.Interface = l_dict.get('Interface', 'serial')
            l_ctlr.Port = l_dict.get('Port', '/dev/ttyUSB0')
            l_ctlr.BaudRate = l_dict.get('BaudRate', 19200)
            l_ctlr.ByteSize = l_dict.get('ByteSize', 8)
            l_ctlr.Parity = l_dict.get('Parity', 'None')
            l_ctlr.StopBits = l_dict.get('StopBits', 1.0)
            l_ctlr.Timeout = l_dict.get('Timeout', 0.1)
            l_ctlr.WriteTimeout = l_dict.get('WriteTimeout', 1)
            l_ctlr.InterCharTimeout = l_dict.get('InterCharTimeout', 1)
            l_ctlr.XonXoff = l_dict.get('XonXoff', False)
            l_ctlr.RtsCts = l_dict.get('RtsCts', False)
            l_ctlr.DsrDtr = l_dict.get('DsrDtr', False)
            """
            lighting.Controller_Data[Name] = l_ctlr

    def dump_controllers(self):
        for l_key, l_obj in lighting.Controller_Data.iteritems():
            print " # {0:}.dump_controllers - Key:{1:}, Object:{2:}".format(__name__, l_key, l_obj)


class UPBDeviceMain(UPBControllerAPI, UPBLightingDeviceAPI):
    """
    """

    def __init__(self, p_debug = False):
        """Constructor for the UPB .
        """
        self.m_config = configure_mh.ConfigureMain()
        self.m_logger = logging.getLogger('PyHouse.UpbDevice')
        self.load_all_UPB()
        self.dump_all_devices()
        self.m_logger.info('Initialized.')

    def start(self):
        pass

    def load_all_UPB(self):
        #self.load_all_devices()
        self.load_controllers(self.m_config.get_value('UPBControllers'))
        self.dump_controllers()

### END
