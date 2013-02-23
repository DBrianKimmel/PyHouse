#!/usr/bin/env python

"""Handle the home lighting system automation.

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional.
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)
New lighting families are added to this module.

Each family consists of four major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.

    *!* - These are the places to add new lighting family information
"""

# Import system type stuff
import logging
import importlib
import xml.etree.ElementTree as ET

# Import PyMh files
from configure import xml_tools
import lighting_buttons
import lighting_controllers
import lighting_lights
import lighting_scenes
# import lighting_status

g_debug = 3

g_logger = None

# These globals in the lighting singleton hold the operating data loaded at startup.
Light_Data = lighting_lights.Light_Data
Singletons = {}

' *!* Modules and pointers to the modules'
from families import VALID_FAMILIES
VALID_INTERFACES = ['Serial', 'USB', 'Ethernet']

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
        self.Family = None
        self.Import = None
        self.Key = 0
        self.Module = None
        self.Name = None
        self.Package = None

    def __str__(self):
        return "FamilyData:: Name:{0:}".format(self.Name)


class CommonInfo(object):

    def read_light_common(self, p_entry, p_obj):
        """
        @param p_entry: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        TODO: move some of lights to lighting or lighting_xxx and family stuff to Device_<family> called from lighting.
        """
        self.read_common(p_obj, p_entry)
        p_obj.Comment = self.get_text(p_entry, 'Comment')
        p_obj.Coords = self.get_text(p_entry, 'Coords')
        p_obj.Dimmable = self.get_bool(p_entry.findtext('Dimmable'))
        p_obj.Family = l_fam = self.get_text(p_entry, 'Family')
        p_obj.RoomName = p_entry.findtext('Room')
        p_obj.HouseName = p_entry.findtext('House')
        p_obj.Type = p_entry.findtext('Type')
        if l_fam == 'UPB':
            p_obj.NetworkID = l_fam = p_entry.findtext('NetworkID')
            p_obj.Password = p_entry.findtext('Password')
            p_obj.UnitID = p_entry.findtext('UnitID')
        elif l_fam == 'Insteon':
            p_obj.Address = p_entry.findtext('Address')
            p_obj.Controller = p_entry.findtext('Controller')
            p_obj.DevCat = p_entry.findtext('DevCat')
            p_obj.GroupList = p_entry.findtext('GroupList')
            p_obj.GroupNumber = p_entry.findtext('GroupNumber')
            p_obj.Master = p_entry.findtext('Master')
            p_obj.ProductKey = p_entry.findtext('ProductKey')
            p_obj.Responder = p_entry.findtext('Responder')
        if g_debug > 5:
            print "yyy-common ", p_obj
        return p_obj

    def write_light_common(self, p_entry, p_obj):
        if g_debug > 4:
            print "lighting.write_light_common()"
        ET.SubElement(p_entry, 'Comment').text = str(p_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_obj.Family
        ET.SubElement(p_entry, 'House').text = p_obj.HouseName
        ET.SubElement(p_entry, 'Room').text = p_obj.RoomName
        ET.SubElement(p_entry, 'Type').text = p_obj.Type
        if p_obj.Family == 'Insteon':
            if g_debug > 4:
                print "WriteLightCommon Insteon=", p_obj
            ET.SubElement(p_entry, 'Address').text = p_obj.Address
            ET.SubElement(p_entry, 'Controller').text = self.put_bool(p_obj.Controller)
            ET.SubElement(p_entry, 'DevCat').text = str(p_obj.DevCat)
            ET.SubElement(p_entry, 'GroupList').text = str(p_obj.GroupList)
            ET.SubElement(p_entry, 'GroupNumber').text = str(p_obj.GroupNumber)
            ET.SubElement(p_entry, 'Master').text = str(p_obj.Master)
            ET.SubElement(p_entry, 'ProductKey').text = str(p_obj.ProductKey)
            ET.SubElement(p_entry, 'Responder').text = self.put_bool(p_obj.Responder)
        elif p_obj.Family == 'UPB':
            if g_debug > 4:
                print "WriteLightCommon UPB=", p_obj
            try:
                ET.SubElement(p_entry, 'NetworkID').text = self.put_str(p_obj.NetworkID)
                ET.SubElement(p_entry, 'Password').text = str(p_obj.Password)
                ET.SubElement(p_entry, 'UnitID').text = str(p_obj.UnitID)
            except AttributeError:
                pass


class ButtonData(lighting_buttons.ButtonsData): pass

class ButtonAPI(lighting_buttons.ButtonsAPI, CommonInfo):

    def read_buttons(self, p_house_obj, p_house_xml):
        """
        """
        if g_debug > 4:
            print "lighting.read_buttons()"
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

    def write_buttons(self, p_parent, p_dict):
        if g_debug > 4:
            print "lighting.write_buttons()"
        l_count = 0
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(p_parent, 'Button', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_count += 1
        if g_debug > 5:
            print "lighting.write_buttons() - Wrote {0:} buttons".format(l_count)


class ControllerData(lighting_controllers.ControllerData): pass

class ControllerAPI(lighting_controllers.ControllersAPI, CommonInfo):

    def read_controllers(self, p_house_obj, p_house_xml):
        if g_debug > 4:
            print "lighting.read_controllers()"
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Controllers')
        l_list = l_sect.iterfind('Controller')
        for l_entry in l_list:
            l_obj = ControllerData()
            l_obj = self.read_light_common(l_entry, l_obj)
            l_obj.Interface = l_if = self.get_text(l_entry, 'Interface')
            l_obj.Port = self.get_text(l_entry, 'Port')
            if l_if == 'Serial':
                l_obj.BaudRate = self.get_int(l_entry, 'BaudRate')
                l_obj.ByteSize = self.get_int(l_entry, 'ByteSize')
                l_obj.DtsDtr = self.get_text(l_entry, 'DtsDtr')
                l_obj.InterCharTimeout = self.get_float(l_entry, 'InterCharTimeout')
                l_obj.Parity = self.get_text(l_entry, 'Parity')
                l_obj.RtsCts = self.get_text(l_entry, 'RtsCts')
                l_obj.StopBits = self.get_float(l_entry, 'StopBits')
                l_obj.Timeout = self.get_float(l_entry, 'Timeout')
                l_obj.WriteTimeout = self.get_float(l_entry, 'WriteTimeout')
                l_obj.XonXoff = self.get_text(l_entry, 'XonXoff')
                l_obj.Product = self.get_int(l_entry, 'Product')
                l_obj.Vendor = self.get_int(l_entry, 'Vendor')
            elif l_if == 'USB':
                l_obj.Product = self.get_int(l_entry, 'Product')
                l_obj.Vendor = self.get_int(l_entry, 'Vendor')
            elif l_if == 'Ethernet':
                pass
            # l_obj.Key = l_count
            l_dict[l_count] = l_obj
            l_count += 1
        p_house_obj.Controllers = l_dict
        if g_debug > 5:
            print "lighting.read_controllers()  loaded {0:} controllers for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_controllers(self, p_parent, p_dict):
        if g_debug > 4:
            print "lighting.write_controllers()"
        l_count = 0
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(p_parent, 'Controller', l_obj)
            self.write_light_common(l_entry, l_obj)
            ET.SubElement(l_entry, 'Interface').text = l_obj.Interface
            if l_obj.Interface == 'Serial':
                ET.SubElement(l_entry, 'Port').text = l_obj.Port
                ET.SubElement(l_entry, 'BaudRate').text = str(l_obj.BaudRate)
                ET.SubElement(l_entry, 'Parity').text = str(l_obj.Parity)
                ET.SubElement(l_entry, 'ByteSize').text = str(l_obj.ByteSize)
                ET.SubElement(l_entry, 'StopBits').text = str(l_obj.StopBits)
                ET.SubElement(l_entry, 'Timeout').text = str(l_obj.Timeout)
            elif l_obj.Interface == 'USB':
                ET.SubElement(l_entry, 'Vendor').text = str(l_obj.Vendor)
                ET.SubElement(l_entry, 'Product').text = str(l_obj.Product)
            elif l_obj.Interface == 'Ethernet':
                pass
            l_count += 1
        if g_debug > 4:
            print "lighting.write_controllers() - Wrote {0:} controllers".format(l_count)


class LightData(lighting_lights.LightData):

    def __init__(self):
        super(LightData, self).__init__()

    def __str__(self):
        return super(LightData, self).__str__()


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

    def write_lights(self, p_parent, p_dict):
        if g_debug > 4:
            print "lighting.write_lights()"
        l_count = 0
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(p_parent, 'Light', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_count += 1
        if g_debug > 5:
            print "lighting.write_lights() - Wrote {0:} lights".format(l_count)


class SceneData(lighting_scenes.ScenesData): pass

class SceneAPI(lighting_scenes.ScenesAPI): pass


class LightingUtility(ButtonAPI, ControllerAPI, LightingAPI, FamilyData):
    """
    """

    m_family_data = None

    def start_lighting_families(self, p_house_obj):
        """Load and start the family if there is a controller in the house for the family.
        """
        if g_debug > 1:
            print "lighting.start_lighting_families()"
        l_count = 0
        self.m_family_data = {}
        g_logger.info("Starting lighting families.")
        for l_family in VALID_FAMILIES:
            l_family_obj = FamilyData()
            l_family_obj.Active = False
            l_family_obj.Import = 'Device_' + l_family
            l_family_obj.Key = l_count
            l_family_obj.Name = l_family
            l_family_obj.Package = 'families.' + l_family
            if g_debug > 1:
                print "lighting.start_lighting_families - Package: {0:}, Import: {1:}".format(l_family_obj.Package, l_family_obj.Import)
                print "  from {0:} import {1:}".format(l_family_obj.Package, l_family_obj.Import)
            l_module = importlib.import_module(l_family_obj.Package + '.' + l_family_obj.Import, l_family_obj.Package)
            l_family_obj.Module = l_module
            l_family_obj.Api = l_api = l_module.API()
            if g_debug > 1:
                print "lighting.start_lighting_families() - Added {0:} to m_modules Key:{1:} -".format(l_family_obj.Import, l_count), l_family_obj
            l_api.Start(p_house_obj)
            self.m_family_data[l_count] = l_family_obj
            l_count += 1
            g_logger.info("Started lighting family {0:}.".format(l_family))
        if g_debug > 1:
            print "lighting.start_lighting_families() ", self.m_family_data

    def stop_lighting_families(self):
        if g_debug > 1:
            print "lighting.stop_lighting_families()"
        for l_obj in self.m_family_data.itervalues():
            l_obj.Api.Stop()

    def change_light_setting(self, p_house_obj, p_key, p_level):
        """
        Turn a light to a given level (0-100) off/dimmed/on.

        @param p_house_obj: is a house object
        @param p_key: is the index (Key) of the Light to be changed within the House object.
        @param p_level: is the level to set
        """
        l_light_obj = p_house_obj.Lights[p_key]
        if g_debug > 1:
            print "lighting.change_light_setting() House={0:}, Light={1:}, Level={2:}".format(p_house_obj.Name, l_light_obj.Name, p_level)
            # print "   Family_Data ", self.m_family_data
        g_logger.info("Turn Light {0:} to level {1:}.".format(p_house_obj.Lights[p_key].Name, p_level))
        for l_family_obj in self.m_family_data.itervalues():
            l_module = l_family_obj.Module
            if l_family_obj.Name != l_light_obj.Family:
                if g_debug > 1:
                    print "   Skipping Module ", l_family_obj.Name, l_family_obj.Family
                continue
            if g_debug > 1:
                print "   Processing Module ", l_family_obj.Name
            l_family_obj.Api.change_light_setting(l_light_obj, p_level)

    def update_all_lighting_families(self):
        """ *!*  API
        Update the light configs in the appropriate module.
        """
        g_logger.info("Updating all lighting families.")
        for l_obj in self.m_family_data.itervalues():
            l_obj.Module.LightingAPI().update_all_lights()

    def scan_all_lighting(self, p_lights):
        """ *!*
        """
        return
        if self.m_InsteonDevice != None:
            self.m_InsteonDevice.scan_all_lights(p_lights)
        if self.m_UpbDevice != None:
            self.m_UpbDevice.scan_all_lights(p_lights)
        if self.m_X10Device != None:
            self.m_X10Device.scan_all_lights(p_lights)

    def get_light_ref(self, p_house, p_light):
        """Return a light object reference for the given light in a house.
        """
        for l_obj in Light_Data.itervalues():
            print "get_light_ref()", l_obj.HouseName, l_obj.Name
            if l_obj.HouseName == p_house and l_obj.Name == p_light:
                return l_obj
        return None


class API(LightingUtility):

    def __init__(self):
        if g_debug > 0:
            print "lighting.__init__()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Lighting')
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
        l_lighting_xml = ET.Element('Lights')
        self.write_lights(l_lighting_xml, self.m_house_obj.Lights)
        p_xml.append(l_lighting_xml)
        l_button_xml = ET.Element('Buttons')
        self.write_buttons(l_button_xml, self.m_house_obj.Buttons)
        p_xml.append(l_button_xml)
        l_controller_xml = ET.Element('Controllers')
        self.write_controllers(l_controller_xml, self.m_house_obj.Controllers)
        p_xml.append(l_controller_xml)
        self.stop_lighting_families()
        g_logger.info("Stopped.")
        if g_debug > 0:
            print "lighting.API.Stop()"
        return p_xml


def GetLightRef(p_house, p_light):
    """Return a light object reference for the given light in a house.
    """
    for l_obj in Light_Data.itervalues():
        if l_obj.HouseName == p_house and l_obj.Name == p_light:
            return l_obj
    return None

# ## END
