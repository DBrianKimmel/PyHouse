#!/usr/bin/env python

"""Handle the light status component of the lighting system.

    Status is the light level - 0 100%
    
    Future additions include button led status etc.
"""


Light_Status = {}

class LightingStatusData(object):
    """
    """
    CurLevel = 0

    def __init__(self):
        self.CurLevel = 0
        self.Name = None
        self.Family = None

    def get_cur_level(self):
        return self.__CurLevel
    def set_cur_level(self, value):
        self.__CurLevel = value
    def get_name(self):
        return self.__Name
    def set_name(self, value):
        self.__Name = value

    CurLevel = property(get_cur_level, set_cur_level, None, None)
    Name = property(get_name, set_name, None, None)

class LightingStatusAPI(LightingStatusData):

    def __init__(self):
        pass

    def load_all_status(self, p_dict):
        for _l_key, l_obj in p_dict.iteritems():
            self.load_status(l_obj)

    def load_status(self, p_obj):
        l_status = LightingStatusData()
        Name = l_status.Name = p_obj.get('Name', 'NoName')
        l_status.Family = p_obj.get('Family', None)
        Light_Status[Name] = l_status
        return l_status

    def update_status_by_name(self, p_name, p_family, p_level):
        for l_key, l_obj in Light_Status.iteritems():
            if l_obj.Name != p_name: continue
            if l_obj.Family != p_family: continue
            l_obj.CurLevel = p_level
            Light_Status[l_key] = l_obj
            #print " && Updated light status for {0:} {1:} to {2:}".format(p_family, p_name, p_level)
            return True
        return False

### END
