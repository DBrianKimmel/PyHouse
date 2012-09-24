#!/usr/bin/env python

"""Handle the scenes component of the lighting system.
"""


Scene_Data = {}

class ScenesData(object):
    """
    """

    def __init__(self):
        self.Active = None
        self.Name = None
        self.Light = None
        self.Controller = None
        self.Level = None
        self.Rate = None

    def get_active(self):
        return self.__Active
    def get_name(self):
        return self.__Name
    def get_light(self):
        return self.__Light
    def get_controller(self):
        return self.__Controller
    def get_level(self):
        return self.__Level
    def get_rate(self):
        return self.__Rate
    def set_active(self, value):
        self.__Active = value
    def set_name(self, value):
        self.__Name = value
    def set_light(self, value):
        self.__Light = value
    def set_controller(self, value):
        self.__Controller = value
    def set_level(self, value):
        self.__Level = value
    def set_rate(self, value):
        self.__Rate = value

    def __str__(self):
        l_ret = "Scene Name:{0:} - Light:{1:}".format(self.Name, self.Light)
        return l_ret
    Active = property(get_active, set_active, None, None)
    Name = property(get_name, set_name, None, None)
    Light = property(get_light, set_light, None, None)
    Controller = property(get_controller, set_controller, None, None)
    Level = property(get_level, set_level, None, None)
    Rate = property(get_rate, set_rate, None, None)


class ScenesAPI(ScenesData):
    """
    """

    def load_all_scenes(self, p_dict):
        return
        #for l_value in p_dict.itervalues():
        #    self.load_scene(l_value)

    def load_scene(self, p_dict):
        l_scene = ScenesData()
        l_scene.Active = p_dict.get('Active', None)
        Name = l_scene.Name = p_dict.get('Name', None)
        Scene_Data[Name] = l_scene
        return l_scene

    def dump_all_scenes(self):
        print "***** All Scenes *****"
        for l_key, l_obj in Scene_Data.iteritems():
            print "~~~Scene: {0:}".format(l_key)
            print "     ", l_obj
        print



### END
