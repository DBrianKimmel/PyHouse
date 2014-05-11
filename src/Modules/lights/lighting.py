"""
-*- test-case-name: PyHouse.Modules.lights.test.test_lighting -*-

@name: PyHouse/Modules/lights/lighting.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Apr 2, 2010
@license: MIT License
@summary: Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff

# Import PyHouse files
from Modules.families import family
from Modules.lights import lighting_buttons
from Modules.lights import lighting_controllers
from Modules.lights import lighting_lights
from Modules.lights import lighting_scenes
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Lighting    ')

class ButtonData(lighting_buttons.ButtonData): pass
class ButtonAPI(lighting_buttons.ButtonsAPI): pass
class ControllerData(lighting_controllers.ControllerData): pass
class ControllerAPI(lighting_controllers.ControllersAPI): pass
class LightData(lighting_lights.LightData): pass
class LightingAPI(lighting_lights.LightingAPI): pass
class SceneData(lighting_scenes.ScenesData): pass
class SceneAPI(lighting_scenes.ScenesAPI): pass


class Utility(ButtonAPI, ControllerAPI, LightingAPI):
    """Commands we can run from high places.
    """

    m_family_data = None

    def test_lighting_families(self):
        pass


class API(Utility):

    def __init__(self, _p_house_obj):
        self.m_family = family.API()
        LOG.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = p_house_obj
        LOG.info("Starting - House:{0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.FamilyData = self.m_family.build_lighting_family_info(p_house_obj)
        self.read_button_xml(self.m_house_obj, p_house_xml)
        self.read_controller_xml(self.m_house_obj, p_house_xml)
        self.read_light_xml(self.m_house_obj, p_house_xml)
        self.m_family.start_lighting_families(self.m_house_obj)
        LOG.info("Started.")

    def Stop(self, p_xml):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_family.stop_lighting_families(p_xml, self.m_house_obj)
        p_xml.append(self.write_light_xml(self.m_house_obj))
        p_xml.append(self.write_button_xml(self.m_house_obj))
        p_xml.append(self.write_controller_xml(self.m_house_obj))
        LOG.info("Stopped.")

    def ChangeLight(self, p_light_obj, p_level):
        l_key = p_light_obj.Key
        l_light_obj = self.m_house_obj.Lights[l_key]
        LOG.info("Turn Light {0:} to level {1:}, Family:{2:}".format(l_light_obj.Name, p_level, l_light_obj.Family))
        for l_family_obj in self.m_house_obj.FamilyData.itervalues():
            if l_family_obj.Name != l_light_obj.Family:
                continue
            l_family_obj.API.ChangeLight(l_light_obj, p_level, 0)

# ## END DBK
