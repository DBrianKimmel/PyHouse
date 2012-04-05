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

    def dump_all_devices(self):
        #print "Dumping all UPB Devices:"
        #for l_key, l_value in lighting.Light_Data.iteritems():
        #    print "  {0:} - {1:}".format(l_key, l_value)
        print


class UPBControllerData(lighting.ControllerData): pass
class UPBControllerAPI(lighting.ControllerAPI): pass
class UPBButtonData(lighting.ButtonData): pass
class UPBButtonAPI(lighting.ButtonAPI, UPBButtonData): pass


class UPBDeviceMain(UPBControllerAPI, UPBLightingDeviceAPI, UPBButtonAPI):
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
        self.load_all_controllers(self.m_config.get_value('UPBControllers'))
        self.dump_all_controllers()
        self.load_all_buttons(self.m_config.get_value('UPBButtons'))
        self.dump_all_buttons()

### END
