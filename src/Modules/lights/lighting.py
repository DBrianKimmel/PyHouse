"""
-*- test-case-name: PyHouse.Modules.lights.test.test_lighting -*-

@name: PyHouse/src/Modules/lights/lighting.py
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
# from Modules.Core.data_objects import ButtonData
from Modules.families import family
from Modules.lights import lighting_buttons
from Modules.lights.lighting_controllers import ControllersAPI
from Modules.lights import lighting_lights
from Modules.lights import lighting_scenes
from Modules.utils import pyh_log
# from src.Modules.utils.tools import PrettyPrintAny

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.Lighting    ')

class ButtonAPI(lighting_buttons.ButtonsAPI): pass
# class ControllerAPI(ControllersAPI): pass
class LightingAPI(lighting_lights.LightingAPI): pass
class SceneAPI(lighting_scenes.ScenesAPI): pass


class Utility(ControllersAPI, LightingAPI):
    """Commands we can run from high places.
    """

    m_family_data = None

    def test_lighting_families(self):
        pass


class API(Utility):

    def __init__(self):
        self.m_family = family.API()
        LOG.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = p_pyhouses_obj.HouseData
        l_house_xml = p_pyhouses_obj.XmlParsed.find('Houses/House')
        # PrettyPrintAny(l_house_xml, 'Lighting() ')
        LOG.info("Starting - House:{0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.FamilyData = self.m_family.build_lighting_family_info(self.m_house_obj)
        self.m_house_obj.Controllers = ControllersAPI().read_controllers_xml(l_house_xml)
        self.m_house_obj.Buttons = lighting_buttons.ButtonsAPI().read_buttons_xml(l_house_xml)
        self.m_house_obj.Lights = self.read_lights_xml(l_house_xml)
        self.m_family.start_lighting_families(self.m_house_obj)
        LOG.info("Started.")

    def Stop(self, p_xml):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_family.stop_lighting_families(p_xml, self.m_house_obj.FamilyData)
        p_xml.append(self.write_lights_xml(self.m_house_obj.Lights))
        p_xml.append(self.write_buttons_xml(self.m_house_obj.Buttons))
        p_xml.append(self.write_controllers_xml(self.m_house_obj.Controllers))
        LOG.info("Stopped.")

    def ChangeLight(self, p_light_obj, p_level):
        l_key = p_light_obj.Key
        l_light_obj = self.m_house_obj.Lights[l_key]
        LOG.info("Turn Light {0:} to level {1:}, Family:{2:}".format(l_light_obj.Name, p_level, l_light_obj.Family))
        for l_family_obj in self.m_house_obj.FamilyData.itervalues():
            if l_family_obj.Name != l_light_obj.Family:
                continue
            l_family_obj.ModuleAPI.ChangeLight(l_light_obj, p_level, 0)

# ## END DBK
