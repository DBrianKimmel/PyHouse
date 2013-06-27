'''
Created on Jun 13, 2013

@author: briank
'''

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from src.utils import xml_tools


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# + = NOT USED HERE


class CoreData(object):
    """Information
    """

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.Coords = ''
        self.CurLevel = 0
        self.Dimmable = False
        self.Family = ''
        self.RoomName = ''
        self.Type = ''

    def __str__(self):
        l_str = "Light:: "
        l_str += "Name:{0:}, ".format(self.Name)
        l_str += "Key:{0:}, ".format(self.Key)
        l_str += "Active:{0:}, ".format(self.Active)
        l_str += "Comment:{0:}, ".format(self.Comment)
        l_str += "Coords:{0:}, ".format(self.Coords)
        l_str += "CurLevel:{0:}, ".format(self.CurLevel)
        l_str += "Dimmable:{0:}, ".format(self.Dimmable)
        l_str += "Family:{0:}, ".format(self.Family)
        l_str += "RoomName:{0:}, ".format(self.RoomName)
        l_str += "Type:{0:};".format(self.Type)
        return l_str

    def __repr__(self):
        l_str = "{"
        l_str += '"Name":"{0:}", '.format(self.Name)
        l_str += '"Key":"{0:}", '.format(self.Key)
        l_str += '"Active":"{0:}", '.format(self.Active)
        l_str += '"Comment":"{0:}", '.format(self.Comment)
        l_str += '"Coords":"{0:}", '.format(self.Coords)
        l_str += '"CurLevel":"{0:}", '.format(self.CurLevel)
        l_str += '"Dimmable":"{0:}", '.format(self.Dimmable)
        l_str += '"Family":"{0:}", '.format(self.Family)
        l_str += '"RoomName":"{0:}", '.format(self.RoomName)
        l_str += '"Type":"{0:}"'.format(self.Type)
        l_str += "}"
        return l_str


class CoreAPI(xml_tools.ConfigTools):
    """
    """

    def read_light_common(self, p_entry_xml, p_device_obj, p_house_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        if g_debug >= 3:
            print "lighting_core.read_light_common() XML={0:}".format(p_entry_xml)
        self.xml_read_common_info(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_from_xml(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool_from_xml(p_entry_xml, 'Dimmable')
        p_device_obj.Family = l_fam = self.get_text_from_xml(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if l_family_obj.Name == l_fam:
                l_family_obj.API.extract_device_xml(p_entry_xml, p_device_obj)
        if g_debug >= 3:
            print "lighting_tools.read_light_common() - ", p_device_obj
        return p_device_obj

    def write_light_common(self, p_entry, p_device_obj, p_house_obj):
        if g_debug >= 3:
            print "lighting_tools.write_light_common()"
        self.put_text_element(p_entry, 'Comment', p_device_obj.Comment)
        self.put_text_element(p_entry, 'Coords', p_device_obj.Coords)
        self.put_bool_element(p_entry, 'Dimmable', p_device_obj.Dimmable)
        self.put_text_element(p_entry, 'Family', p_device_obj.Family)
        self.put_text_element(p_entry, 'Room', p_device_obj.RoomName)
        self.put_text_element(p_entry, 'Type', p_device_obj.Type)
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if l_family_obj.Name == p_device_obj.Family:
                l_family_obj.API.insert_device_xml(p_entry, p_device_obj)

# ## END DBK