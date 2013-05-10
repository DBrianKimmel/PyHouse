#!/usr/bin/env python

"""Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.

"""

# Import system type stuff
import logging
import importlib
import xml.etree.ElementTree as ET

# Import PyHouse files
from utils import xml_tools
import lighting_buttons
import lighting_controllers
import lighting_lights
import lighting_scenes

g_debug = 0
# 0 = off
# 1 = major routine entry

g_logger = None

# These globals in the lighting singleton hold the operating data loaded at startup.
Singletons = {}

' *!* Modules and pointers to the modules'
from families import VALID_FAMILIES

m_InsteonDevice = None
m_X10Device = None
m_UpbDevice = None

class FamilyData(object):
    """A container for every family that has been defined.
    """

    def __init__(self):
        global ScheduleCount
        self.Active = False
        self.Api = None
        self.Family = ''
        self.Import = ''
        self.Key = 0
        self.Module = ''
        self.Name = ''
        self.Package = ''

    def __repr__(self):
        return "FamilyData:: Name:{0:}".format(self.Name)


class CommonInfo(object):

    def read_light_common(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        TODO: move some of lights to lighting or lighting_xxx and family stuff to Device_<family> called from lighting.
        """
        if g_debug >= 5:
            print "lighting.read_lights_common() - ", p_device_obj
        self.xml_read_common_info(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_element(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_element(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool(p_entry_xml.findtext('Dimmable'))
        p_device_obj.Family = l_fam = self.get_text_element(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.HouseName = p_entry_xml.findtext('House')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        for l_family_obj in self.m_family_data.itervalues():
            if l_family_obj.Name == l_fam:
                l_family_obj.Api.extract_device_xml(p_entry_xml, p_device_obj)
        return p_device_obj

    def write_light_common(self, p_entry, p_device_obj):
        if g_debug > 4:
            print "lighting.write_light_common()"
        ET.SubElement(p_entry, 'Comment').text = str(p_device_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_device_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_device_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_device_obj.Family
        ET.SubElement(p_entry, 'House').text = p_device_obj.HouseName
        ET.SubElement(p_entry, 'Room').text = p_device_obj.RoomName
        ET.SubElement(p_entry, 'Type').text = p_device_obj.Type
        for l_family_obj in self.m_family_data.itervalues():
            if l_family_obj.Name == p_device_obj.Family:
                l_family_obj.Api.insert_device_xml(p_entry, p_device_obj)


class ButtonData(lighting_buttons.ButtonsData): pass

class ButtonAPI(lighting_buttons.ButtonsAPI, CommonInfo):

    def read_buttons(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug > 4:
            print "lighting.read_buttons() - House:{0:}".format(p_house_obj.Name)
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Buttons')
        l_list = l_sect.iterfind('Button')
        for l_entry in l_list:
            l_obj = ButtonData()
            l_obj = self.read_light_common(l_entry, l_obj)
            # l_obj.Key = l_count
            l_dict[l_count] = l_obj
            l_count += 1
        p_house_obj.Buttons = l_dict
        if g_debug > 5:
            print "lighting.read_buttons()  loaded {0:} buttons for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_buttons(self, p_dict):
        if g_debug > 4:
            print "lighting.write_buttons()"
        l_count = 0
        l_buttons_xml = ET.Element('Buttons')
        for l_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Button', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_buttons_xml.append(l_entry)
            l_count += 1
        if g_debug > 5:
            print "lighting.write_buttons() - Wrote {0:} buttons".format(l_count)
        return l_buttons_xml


class ControllerData(lighting_controllers.ControllerData): pass

class ControllerAPI(lighting_controllers.ControllersAPI):
    pass


class LightData(lighting_lights.LightData):

    def __init__(self):
        super(LightData, self).__init__()

    def __repr__(self):
        return super(LightData, self).__repr__()


class LightingAPI(xml_tools.ConfigTools, lighting_lights.LightsAPI, CommonInfo):

    def read_lights(self, p_house_obj, p_house_xml):
        if g_debug > 4:
            print "lighting.read_lights()"
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Lights')
        l_list = l_sect.iterfind('Light')
        for l_entry in l_list:
            l_obj = LightData()
            l_obj = self.read_light_common(l_entry, l_obj)
            l_dict[l_count] = l_obj
            l_count += 1
        p_house_obj.Lights = l_dict
        if g_debug > 5:
            print "lighting.read_lights()  loaded {0:} lights for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_lights(self, p_dict):
        if g_debug > 4:
            print "lighting.write_lights()"
        l_lighting_xml = ET.Element('Lights')
        l_count = 0
        for l_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Light', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_lighting_xml.append(l_entry)
            l_count += 1
        return l_lighting_xml


class SceneData(lighting_scenes.ScenesData): pass

class SceneAPI(lighting_scenes.ScenesAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI, FamilyData):
    """
    """

    m_family_data = None

    def build_lighting_info(self, _p_house_obj):
        self.m_family_data = {}
        l_count = 0
        for l_family in VALID_FAMILIES:
            l_family_obj = FamilyData()
            l_family_obj.Active = False
            l_family_obj.Import = 'Device_' + l_family
            l_family_obj.Key = l_count
            l_family_obj.Name = l_family
            l_family_obj.Package = 'families.' + l_family
            l_module = importlib.import_module(l_family_obj.Package + '.' + l_family_obj.Import, l_family_obj.Package)
            l_family_obj.Module = l_module
            l_family_obj.Api = l_module.API()
            self.m_family_data[l_count] = l_family_obj
            if g_debug > 1:
                print "lighting.build_lighting_info - Package: {0:}, Import: {1:}".format(l_family_obj.Package, l_family_obj.Import)
                print "   from {0:} import {1:}".format(l_family_obj.Package, l_family_obj.Import)
                print "   Added {0:} to m_modules Key:{1:} -".format(l_family_obj.Import, l_count), l_family_obj
            l_count += 1

    def start_lighting_families(self, p_house_obj):
        """Load and start the family if there is a controller in the house for the family.
        """
        if g_debug > 1:
            print "lighting.start_lighting_families()"
        g_logger.info("Starting lighting families.")
        for l_family_obj in self.m_family_data.itervalues():
            l_family_obj.Api.Start(p_house_obj)
            g_logger.info("Started lighting family {0:}.".format(l_family_obj.Name))

    def stop_lighting_families(self, p_xml):
        if g_debug > 1:
            print "lighting.stop_lighting_families()"
        for l_family_obj in self.m_family_data.itervalues():
            l_family_obj.Api.Stop(p_xml)

    def test_lighting_families(self):
        if g_debug > 1:
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
        if g_debug > 1:
            print "lighting.change_light_setting() House={0:}, Light={1:}, Level={2:}, Rate:{3:}".format(p_house_obj.Name, p_light_obj.Name, p_level, p_rate)
        g_logger.info("Turn Light {0:} to level {1:} at rate {2:}.".format(p_light_obj.Name, p_level, p_rate))
        for l_family_obj in self.m_family_data.itervalues():
            if l_family_obj.Name != p_light_obj.Family:
                continue
            l_family_obj.Api.change_light_setting(p_light_obj, p_level)


class API(LightingUtility):

    def __init__(self, p_house_obj):
        if g_debug > 0:
            print "lighting.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Lighting')
        self.m_house_obj = p_house_obj
        self.build_lighting_info(p_house_obj)
        g_logger.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = p_house_obj
        if g_debug > 0:
            print "lighting.API.Start() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Starting.")
        self.read_buttons(self.m_house_obj, p_house_xml)
        self.read_controllers(self.m_house_obj, p_house_xml)
        self.read_lights(self.m_house_obj, p_house_xml)
        self.start_lighting_families(self.m_house_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml):
        """Allow cleanup of all drivers.
        """
        if g_debug > 0:
            print "lighting.API.Stop() - House:{0:} Count:{1:}".format(self.m_house_obj.Name, len(self.m_house_obj.Lights))
        g_logger.info("Stopping all lighting families.")
        l_lighting_xml = self.write_lights(self.m_house_obj.Lights)
        l_buttons_xml = self.write_buttons(self.m_house_obj.Buttons)
        l_controllers_xml = self.write_controllers(self.m_house_obj.Controllers)
        self.stop_lighting_families(p_xml)
        g_logger.info("Stopped.")
        if g_debug > 0:
            print "lighting.API.Stop() - House:{0:}, Lights:{1:}, Controllers:{2:}, Buttons:{3:}".format(self.m_house_obj.Name, len(l_lighting_xml), len(l_controllers_xml), len(l_buttons_xml))
        return l_lighting_xml, l_controllers_xml, l_buttons_xml

    def SpecialTest(self):
        if g_debug > 0:
            print "lighting.API.SpecialTest()"
        self.test_lighting_families()

# ## END
