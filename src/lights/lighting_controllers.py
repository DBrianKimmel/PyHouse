#!/usr/bin/env python

"""Handle the controller component of the lighting system.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from src.lights import lighting_core
from src.utils.tools import PrintBytes
from src.drivers import interface
from src.families import family
#
from src.utils.tools import PrintObject
from src.families.Insteon import Insteon_utils


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = controller summary information
# 3 = controller detail information


class ControllerData(lighting_core.CoreData):
    """This data is common to all controllers.

    There is also interface information that controllers need.
    """

    def __init__(self):
        super(ControllerData, self).__init__()  # The core data
        self.Type = 'Controller'
        self.Interface = ''
        self.Port = ''
        #
        self.DriverAPI = None
        self.HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self.Command = None
        self.Data = None  # Interface specific data
        self.Message = ''
        self.Queue = None

    def XX__str__(self):
        l_ret = "LightingController:: "
        l_ret += "Name:{0:}, ".format(self.Name)
        l_ret += "Family:{0:}, ".format(self.Family)
        l_ret += "Interface:{0:}, ".format(self.Interface)
        l_ret += "Port:{0:}, ".format(self.Port)
        l_ret += "Type:{0:}, ".format(self.Type)
        return l_ret

    def reprJSON(self):
        l_ret = super(ControllerData, self).reprJSON()  # lighting_core data
        l_ret.update(dict(
            Interface = self.Interface, Port = self.Port
        ))
        if self.Family == 'Insteon':
            from src.families.Insteon import Insteon_utils
            l_ret.update(dict(
                InsteonAddress = Insteon_utils.int2dotted_hex(self.InsteonAddress),
                DevCat = self.DevCat
            ))
        return l_ret


class ControllersAPI(lighting_core.CoreAPI):

    def __init__(self):
        super(ControllersAPI, self).__init__()

    def read_controller_xml(self, p_house_obj, p_house_xml):
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Controllers')
        try:
            l_list = l_sect.iterfind('Controller')
            for l_controller_xml in l_list:
                l_controller_obj = ControllerData()
                l_controller_obj = self.read_light_common(l_controller_xml, l_controller_obj, p_house_obj)
                l_controller_obj.Key = l_count  # Renumber
                l_controller_obj.Interface = self.get_text_from_xml(l_controller_xml, 'Interface')
                l_controller_obj.Port = self.get_text_from_xml(l_controller_xml, 'Port')
                interface.ReadWriteConfig().extract_xml(l_controller_obj, l_controller_xml)
                l_dict[l_count] = l_controller_obj
                l_count += 1
        except AttributeError:  # No Controller section
            l_dict = {}
        p_house_obj.Controllers = l_dict
        return l_dict

    def write_controller_xml(self, p_house_obj):
        l_count = 0
        l_controllers_xml = ET.Element('Controllers')
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            l_entry = self.xml_create_common_element('Controller', l_controller_obj)
            self.write_light_common(l_entry, l_controller_obj, p_house_obj)
            ET.SubElement(l_entry, 'Interface').text = l_controller_obj.Interface
            ET.SubElement(l_entry, 'Port').text = l_controller_obj.Port
            interface.ReadWriteConfig().write_xml(l_entry, l_controller_obj)
            l_controllers_xml.append(l_entry)
            l_count += 1
        return l_controllers_xml

# ## END DBK
