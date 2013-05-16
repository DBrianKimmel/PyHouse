#!/usr/bin/env python

"""Handle the controller component of the lighting system.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
import lighting_tools
from utils.tools import PrintBytes
from drivers import interface

g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = controller summary information
# 3 = controller detail information

Controller_Data = {}
ControllerCount = 0


class ControllerData(lighting_tools.CoreData):
    """This data is common to all controllers.

    There is also interface information that controllers need.
    """

    def __init__(self):
        global ControllerCount
        ControllerCount += 1
        super(ControllerData, self).__init__()  # The core data
        self.Type = 'Controller'
        self.Command = None
        self.Data = None  # Interface specific data
        self.HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        self.Interface = ''
        self.Message = ''
        self.Port = ''

    def __repr__(self):
        l_ret = "LightingController:: Name:{0:}, Family:{1:}, Interface:{2:}, Port:{3:}, Type:{4:}, Message:{5:}, ".format(
                self.Name, self.Family, self.Interface, self.Port, self.Type, PrintBytes(self.Message))
        return l_ret


class ControllersAPI(lighting_tools.CoreAPI):

    def __init__(self):
        super(ControllersAPI, self).__init__()

    def read_controllers(self, p_house_obj, p_house_xml):
        if g_debug >= 1:
            print "lighting_controller.read_controllers()", p_house_obj
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Controllers')
        l_list = l_sect.iterfind('Controller')
        for l_controller_xml in l_list:
            l_controller_obj = ControllerData()
            l_controller_obj = self.read_light_common(l_controller_xml, l_controller_obj)
            l_controller_obj.Interface = self.get_text_element(l_controller_xml, 'Interface')
            l_controller_obj.Port = self.get_text_element(l_controller_xml, 'Port')
            interface.ReadWriteConfig().extract_xml(l_controller_obj, l_controller_xml)
            l_dict[l_count] = l_controller_obj
            l_count += 1
        p_house_obj.Controllers = l_dict
        if g_debug >= 2:
            print "lighting_controller.read_controllers()  loaded {0:} controllers for house {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_controllers(self, p_dict):
        if g_debug >= 1:
            print "lighting_controller.write_controllers()"
        l_count = 0
        l_controllers_xml = ET.Element('Controllers')
        for l_controller_obj in p_dict.itervalues():
            l_entry = self.xml_create_common_element('Controller', l_controller_obj)
            self.write_light_common(l_entry, l_controller_obj)
            ET.SubElement(l_entry, 'Interface').text = l_controller_obj.Interface
            ET.SubElement(l_entry, 'Port').text = l_controller_obj.Port
            interface.ReadWriteConfig().write_xml(l_entry, l_controller_obj)
            l_controllers_xml.append(l_entry)
            l_count += 1
        if g_debug >= 2:
            print "lighting_controller.write_controllers() - Wrote {0:} controllers".format(l_count)
        return l_controllers_xml

# ## END
