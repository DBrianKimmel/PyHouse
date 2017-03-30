"""
@name:      PyHouse/src/Modules/Lighting/lighting_scenes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:

Handle the scenes component of the lighting system.

"""

__updated__ = '2017-03-26'


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

    def __str__(self):
        l_ret = "Scene Name:{} - Light:{}".format(self.Name, self.Light)
        return l_ret


class ScenesAPI(ScenesData):
    """
    """

    def load_all_scenes(self, p_dict):
        return
        # for l_value in p_dict.values():
        #    self.load_scene(l_value)

    def load_scene(self, p_dict):
        l_scene = ScenesData()
        l_scene.Active = p_dict.get('Active', None)
        Name = l_scene.Name = p_dict.get('Name', None)
        Scene_Data[Name] = l_scene
        return l_scene

    def dump_all_scenes(self):
        pass

# ## END DBK
