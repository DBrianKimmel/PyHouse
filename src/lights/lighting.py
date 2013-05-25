#!/usr/bin/env python

"""Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyHouse files
from src.families import family
from src.lights import lighting_buttons
from src.lights import lighting_controllers
from src.lights import lighting_lights
from src.lights import lighting_scenes
from src.utils import xml_tools

g_debug = 9
# 0 = off
# 1 = major routine entry
# 2 = xml read / write

g_logger = None


class CommonInfo(object):

    def read_light_common(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        self.xml_read_common_info(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_element(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_element(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool(p_entry_xml.findtext('Dimmable'))
        p_device_obj.Family = l_fam = self.get_text_element(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        for l_family_obj in family.g_family_data.itervalues():
            if l_family_obj.Name == l_fam:
                l_family_obj.Api.extract_device_xml(p_entry_xml, p_device_obj)
        if g_debug >= 2:
            print "lighting.read_light_common() - ", p_device_obj
        return p_device_obj

    def write_light_common(self, p_entry, p_device_obj):
        if g_debug >= 2:
            print "lighting.write_light_common()"
        ET.SubElement(p_entry, 'Comment').text = str(p_device_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_device_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_device_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_device_obj.Family
        ET.SubElement(p_entry, 'Room').text = p_device_obj.RoomName
        ET.SubElement(p_entry, 'Type').text = p_device_obj.Type
        for l_family_obj in family.g_family_data.itervalues():
            if l_family_obj.Name == p_device_obj.Family:
                l_family_obj.Api.insert_device_xml(p_entry, p_device_obj)


class ButtonData(lighting_buttons.ButtonsData): pass

class ButtonAPI(lighting_buttons.ButtonsAPI, CommonInfo):

    def read_button_xml(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug >= 2:
            print "lighting.read_button_xml() - House:{0:}".format(p_house_obj.Name)
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Buttons')
        l_list = l_sect.iterfind('Button')
        for l_entry in l_list:
            l_button_obj = ButtonData()
            l_button_obj = self.read_light_common(l_entry, l_button_obj)
            # l_button_obj.Key = l_count
            l_dict[l_count] = l_button_obj
            l_count += 1
        p_house_obj.Buttons = l_dict
        if g_debug >= 6:
            print "lighting.read_button_xml()  loaded {0:} buttons for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_button_xml(self, p_dict):
        if g_debug >= 2:
            print "lighting.write_button+xml()"
        l_count = 0
        l_buttons_xml = ET.Element('Buttons')
        for l_button_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Button', l_button_obj)
            self.write_light_common(l_entry, l_button_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        if g_debug >= 6:
            print "lighting.write_button_xml() - Wrote {0:} buttons".format(l_count)
        return l_buttons_xml


class ControllerData(lighting_controllers.ControllerData):
    pass

class ControllerAPI(lighting_controllers.ControllersAPI):
    pass


class LightData(lighting_lights.LightData):

    def __init__(self):
        super(LightData, self).__init__()

    def __repr__(self):
        return super(LightData, self).__repr__()


class LightingAPI(xml_tools.ConfigTools, CommonInfo):

    def read_light_xml(self, p_house_obj, p_house_xml):
        if g_debug >= 2:
            print "lighting.read_light_xml()"
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Lights')
        l_list = l_sect.iterfind('Light')
        for l_entry in l_list:
            l_light_obj = LightData()
            l_light_obj = self.read_light_common(l_entry, l_light_obj)
            l_dict[l_count] = l_light_obj
            l_count += 1
        p_house_obj.Lights = l_dict
        if g_debug >= 4:
            print "lighting.read_light_xml()  loaded {0:} lights for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_light_xml(self, p_dict):
        if g_debug >= 2:
            print "lighting.write_light_xml()"
        l_lighting_xml = ET.Element('Lights')
        l_count = 0
        for l_light_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Light', l_light_obj)
            self.write_light_common(l_entry, l_light_obj)
            l_lighting_xml.append(l_entry)
            l_count += 1
        return l_lighting_xml


class SceneData(lighting_scenes.ScenesData): pass

class SceneAPI(lighting_scenes.ScenesAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI):
    """
    """

    m_family_data = None

    def test_lighting_families(self):
        if g_debug >= 2:
            print "lighting.test_lighting_families()"
        for l_family_obj in self.m_family_data.itervalues():
            l_family_obj.Api.SpecialTest()

    def change_light_setting(self, p_house_obj, p_light_obj, p_level, p_rate = 0):
        """Called from several places (schedle, Gui, Web etc.) to change a light level.
        Turn a light to a given level (0-100) off/dimmed/on.

        @param p_house_obj: is a house object
        @param p_light_obj: is the index (Key) of the Light to be changed within the House object.
        @param p_level: is the level to set
        TODO: add rate to family routines and pass along.
        """
        if g_debug >= 2:
            print "lighting.change_light_setting() House={0:}, Light={1:}, Level={2:}, Rate:{3:}".format(p_house_obj.Name, p_light_obj.Name, p_level, p_rate)
        g_logger.info("Turn Light {0:} to level {1:} at rate {2:}.".format(p_light_obj.Name, p_level, p_rate))
        for l_family_obj in self.m_family_data.itervalues():
            if l_family_obj.Name != p_light_obj.Family:
                continue
            l_family_obj.Api.change_light_setting(p_light_obj, p_level)


class API(LightingUtility):

    def __init__(self, p_house_obj):
        if g_debug >= 1:
            print "lighting.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Lighting')
        self.m_house_obj = p_house_obj
        self.m_family = family.LightingUtility()
        self.m_family.build_lighting_family_info(p_house_obj)
        g_logger.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "lighting.API.Start() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Starting.")
        self.read_button_xml(self.m_house_obj, p_house_xml)
        self.read_controller_xml(self.m_house_obj, p_house_xml)
        self.read_light_xml(self.m_house_obj, p_house_xml)
        self.m_family.start_lighting_families(self.m_house_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml):
        """Allow cleanup of all drivers.
        """
        if g_debug >= 1:
            print "lighting.API.Stop() - House:{0:} Count:{1:}".format(self.m_house_obj.Name, len(self.m_house_obj.Lights))
        g_logger.info("Stopping all lighting families.")
        l_lighting_xml = self.write_light_xml(self.m_house_obj.Lights)
        l_buttons_xml = self.write_button_xml(self.m_house_obj.Buttons)
        l_controllers_xml = self.write_controller_xml(self.m_house_obj.Controllers)
        self.m_family.stop_lighting_families(p_xml)
        g_logger.info("Stopped.")
        if g_debug >= 1:
            print "lighting.API.Stop() - House:{0:}, Lights:{1:}, Controllers:{2:}, Buttons:{3:}".format(self.m_house_obj.Name, len(l_lighting_xml), len(l_controllers_xml), len(l_buttons_xml))
        return l_lighting_xml, l_controllers_xml, l_buttons_xml

    def SpecialTest(self):
        if g_debug >= 1:
            print "lighting.API.SpecialTest()"
        self.test_lighting_families()

# ## END DBK
