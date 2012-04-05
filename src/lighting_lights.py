#!/usr/bin/env python

"""Handle the controller component of the lighting system.
    Static data we wish to export/share.
    
    This is the base data for all sub-classed lighting data
    
    Each entry should contain enough information to allow functionality of various family of
    lighting controllers.  Insteon is the first type coded and UPB is to follow.
    
    The real work of controlling the devices is delegated to the modules for that family of devices.
    
    Standard characteristics for each light / switch button:
"""


Light_Data = {}


class LightingData(object):

    def __init__(self, Name):
        self.Name = Name

    def __repr__(self):
        l_str = "Light Name:{0:20.20s} Family: {1:10.10s} Type: {2:10.10s} Comment: {3:40.40s} Room: {4:} Coords: {5:}".format(
                            self.Family, self.Name, self.Type, self.Comment, self.Room, self.Coords)
        return l_str

    def get_Name(self):
        return self.Name

    def get_Type(self):
        return self.Type

    def get_Family(self):
        return self.Family

    def get_Comment(self):
        return self.Comment

    def get_Room(self):
        return self.Room

    def get_Coords(self):
        return self.Coords


class LightingAPI(LightingData):
    """
    """

    def load_all_lights(self, p_dict):
        for l_key, l_dict in p_dict.iteritems():
            self.load_light(l_dict)

    def load_light(self, p_dict):
        """Load the light information.
        """
        print "$$ lighting.load_button ", p_dict.keys()
        Name = p_dict.get('Name', 'NoName')
        l_light = LightingData(Name)
        # Common Data
        l_light.Active = p_dict.get('Active', 'False')
        l_light.Comment = p_dict.get('Comment', None)
        l_light.Coords = p_dict.get('Coords', (0, 0))
        l_light.Dimmable = p_dict.get('Dimmable', False)
        l_light.Family = p_dict.get('Family', None)
        l_light.Name = Name
        l_light.Room = p_dict.get('Room', None)
        l_light.Type = p_dict.get('Type', None)
        # Insteon Data
        l_light.Address = p_dict.get('Address', '01.23.45')
        l_light.GroupList = p_dict.get('GroupList', '')
        l_light.GroupNumber = p_dict.get('GroupNumber', 0)
        l_light.Controller = p_dict.get('Controller', False)
        l_light.Responder = p_dict.get('Responder', False)
        l_light.DevCat = p_dict.get('DevCat', 0)
        l_light.Master = p_dict.get('Master', True)
        l_light.Code = p_dict.get('Code', '')
        l_light.Responder = p_dict.get('Responder', False)
        # UPB Data
        Light_Data[Name] = l_light
        return l_light

    def dump_all_lights(self):
        print "***** All Lights *****"
        for l_key, l_obj in Light_Data.iteritems():
            print "~~~Light: {0:}".format(l_key)
            print "     ", l_obj
        print

    def turn_light_off(self, _p_name):
        assert 0, "Turn light off must be subclassed."

    def turn_light_on(self, _p_name):
        assert 0, "Turn light on must be subclassed."

    def turn_light_dim(self, _p_name, _p_level):
        assert 0, "Turn light dim must be subclassed."

    def load_all_devices(self):
        assert 0, "Load all devices must be subclassed."

    def dump_all_devices(self):
        assert 0, "dump all devices must be subclassed."

    def update_all_devices(self):
        assert 0, "update all devices must be subclassed."

    def update_all_statuses(self):
        assert 0, "dump all statuses must be subclassed."

### END
