#!/usr/bin/python

"""Handle the house information.
"""

# Import system type stuff
import logging

# Import PyMh files
import configure_mh


Location_Data = {}
Room_Data = {}

m_logger = None
#g_config = None


class LocationData(object):
    Name = ''
    Active = False
    Latitude = 0.0
    Longitude = 0.0

    def __init__(self, Name):
        self.Name = Name

    def __repr__(self):
        l_ret = ' House:{0:}, Active:{1:}, Lat:{2:}, Lon:{3:}'.format(self.Name, self.Active, self.Latitude, self.Longitude)
        return l_ret

    def get_Active(self):
        return self.Active

    def get_Latitude(self):
        return self.Latitude

    def get_Longitude(self):
        return self.Longitude

    def get_Timezone(self):
        return self.Timezone


class RoomData(object):

    def __init__(self, Name):
        self.Name = Name

    def __repr__(self):
        l_ret = '** Room:{0:} \t Size:{1:} \t Corner:{2:}\n'.format(self.Name, self.Size, self.Corner)
        return l_ret


class LoadSaveConfigs(RoomData, LocationData):
    """
    """

    def load_location(self):
        #print "...House-locations loading"
        l_cfgdict = self.m_config.get_value('HouseLocation')
        for l_name, l_dict in l_cfgdict.iteritems():
            #print "...  ", l_name, l_dict
            l_entry = LocationData(l_name)
            l_entry.Name = l_name
            l_entry.Active = l_dict.get('Active', 'False') == 'True'
            l_entry.Latitude = float(l_dict.get('Latitude', 0.0))
            l_entry.Longitude = float(l_dict.get('Longitude', 0.0))
            l_entry.Timezone = float(l_dict.get('Timezone', 0.0))
            l_entry.Saving = l_dict.get('Saving', 'False') == 'True'
            Location_Data[l_name] = l_entry

    def dump_location(self):
        print "   House locations:"
        for l_name, l_obj in Location_Data.iteritems():
            print "     ", l_obj
        print

    def load_rooms(self):
        l_dict = self.m_config.get_value('Rooms')
        for l_name, l_dict in l_dict.iteritems():
            l_entry = RoomData(l_name)
            l_entry.Name = l_name
            l_entry.Size = l_dict.get('Size')
            l_entry.Corner = l_dict.get('Corner')
            Room_Data[l_name] = l_entry

    def dump_rooms(self):
        pass


class HouseMain(LoadSaveConfigs):
    """
    """

    def __init__(self):
        m_logger = logging.getLogger('PyHouse.House')
        m_logger.info("Initializing.")
        self.m_config = configure_mh.ConfigureMain()
        self.load_location()
        #self.dump_location()
        self.load_rooms()
        self.dump_rooms()

###  END
