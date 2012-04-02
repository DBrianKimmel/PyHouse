#!/usr/bin/python

"""Load the database with X10 devices.
"""

# Import system type stuff
import logging
import time

# Import PyMh files
import configure_mh
import lighting


m_config = None
m_logger = None


class X10LightingData(lighting.LightingData):

    Family = 'X10'
    Type = None
    Comment = ''
    Room = ''
    CurLevel = 0


    def __init__(self, Name):
        lighting.LightingData.__init__(self, Name)
        self.Family = "X10"
        self.Address = 'asdf'

    def __str__(self):
        l_str = lighting.LightingData.__str__(self)
        l_str += " \t Address: {0:}".format(self.Address)
        return l_str

    def get_Name(self):
        return self.Name

class X10DeviceAPI(lighting.LightingAPI):
    """Overload the base methods with specific ones here.
    """

    def turn_light_off(self, p_name):
        print "Turning off X10 light {0:}".format(p_name)

    def turn_light_on(self, p_name):
        print "Turning on X10 light {0:}".format(p_name)

    def turn_light_dim(self, p_name, p_level):
        print "Turning X10 light {0:} to level {1:}".format(p_name, p_level)

    def load_all_devices(self):
        """Called from lighting.
        """
        #print "Loading all X10 devices."
        #self.Light_Data = {}
        l_dict = self.m_config.get_value("X10Lights")
        for _l_dev, l_vals in l_dict.iteritems():
            Name = l_vals.get('Name', 'xx')
            #print "Name =", Name
            lighting.Light_Data[Name] = X10LightingData(Name)
        #return self.Light_Data

    def dump_all_devices(self):
        print "Dumping all X10 Devices:"
        for l_key, l_value in lighting.Light_Data.iteritems():
            print "  {0:} - {1:}".format(l_key, l_value)
        print


class X10DeviceMain(X10DeviceAPI):
    """
    """

    def __init__(self):
        """Constructor for the PLM.
        """
        self.m_config = configure_mh.ConfigureMain()
        self.m_logger = logging.getLogger('PyMh.X10Device')
        self.load_all_devices()
        #self.dump_all_devices()
        self.m_logger.info('Initialized.')

    def start(self):
        pass

### END
