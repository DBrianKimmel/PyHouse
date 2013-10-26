#!/usr/bin/env python

"""Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff
import logging

# Import PyHouse files
from src.families import family
from src.lights import lighting_buttons
from src.lights import lighting_controllers
from src.lights import lighting_lights
from src.lights import lighting_scenes


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.Lighting    ')


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
        if g_debug >= 2:
            print "lighting.test_lighting_families()"

    def change_light_setting(self, p_house_obj, p_light_obj, p_level, p_rate = 0):
        """Called from several places (schedle, Gui, Web etc.) to change a light level.
        Turn a light to a given level (0-100) off/dimmed/on.

        @param p_house_obj: is a house object
        @param p_light_obj: is the index (Key) of the Light to be changed within the House object.
        @param p_level: is the level to set
        TODO: add rate to family routines and pass along.
        """
        if g_debug >= 2:
            # print "lighting.change_light_setting() House={0:}, Light={1:}, Level={2:}, Rate:{3:}".format(p_house_obj.Name, p_light_obj.Name, p_level, p_rate)
            print "lighting.change_light_setting()"
            print "    House:", p_house_obj
            print "    Light:", p_light_obj
            print "    Level:", p_level
            print "    Rate:", p_rate
            print "    Family:", p_house_obj.FamilyData
        g_logger.info("Turn Light {0:} to level {1:} at rate {2:}.".format(p_light_obj.Name, p_level, p_rate))
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if l_family_obj.Name != p_light_obj.Family:
                continue
            l_family_obj.API.change_light_setting(p_light_obj, p_level, p_house_obj)


class API(Utility):

    def __init__(self, p_house_obj):
        if g_debug >= 2:
            print "lighting.API() - House:{0:}".format(p_house_obj.Name)
        self.m_family = family.LightingUtility()
        g_logger.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "lighting.API.Start() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Starting - House:{0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.FamilyData = self.m_family.build_lighting_family_info(p_house_obj)
        self.read_button_xml(self.m_house_obj, p_house_xml)
        self.read_controller_xml(self.m_house_obj, p_house_xml)
        self.read_light_xml(self.m_house_obj, p_house_xml)
        self.m_family.start_lighting_families(self.m_house_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml, p_house_obj):
        """Allow cleanup of all drivers.
        """
        if g_debug >= 2:
            print "lighting.API.Stop() - House:{0:} Count:{1:}".format(self.m_house_obj.Name, len(self.m_house_obj.Lights))
        g_logger.info("Stopping all lighting families.")
        l_lighting_xml = self.write_light_xml(self.m_house_obj)
        l_buttons_xml = self.write_button_xml(self.m_house_obj)
        l_controllers_xml = self.write_controller_xml(self.m_house_obj)
        self.m_family.stop_lighting_families(p_xml, p_house_obj)
        g_logger.info("Stopped.")
        if g_debug >= 2:
            print "lighting.API.Stop() - House:{0:}, Lights:{1:}, Controllers:{2:}, Buttons:{3:}".format(self.m_house_obj.Name, len(l_lighting_xml), len(l_controllers_xml), len(l_buttons_xml))
        return l_lighting_xml, l_controllers_xml, l_buttons_xml

    def UpdateXml(self, p_xml):
        p_xml.append(self.write_light_xml(self.m_house_obj))
        p_xml.append(self.write_button_xml(self.m_house_obj))
        p_xml.append(self.write_controller_xml(self.m_house_obj))
        return p_xml

    def ChangeLight(self, p_entry):
        if g_debug >= 0:
            print 'lighting.API.ChangeLight({0:}'.format(p_entry)
            l_key = p_entry.Key
            l_level = p_entry.CurLevel
            l_obj = self.m_house_obj.Lights[l_key]
            self.change_light_setting(self.m_house_obj, l_obj, l_level)

# ## END DBK
