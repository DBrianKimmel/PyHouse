'''
Created on Jun 13, 2013

@author: briank
'''

# Import system type stuff

# Import PyHouse files
from src.utils import xml_tools
# from src.utils.tools import PrintObject
from src.web import web_utils


g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE


class XXXBaseLightingData(object):
    """Information
    """

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.Coords = ''  # Room relative coords of the light switch
        self.Dimmable = False
        self.Family = ''
        self.RoomName = ''
        self.Type = ''
        self.UUID = None

    def reprJSON(self):
        """lighting_core.
        """
        l_ret = dict(
           Name = self.Name, Key = self.Key, Active = self.Active,
           Comment = self.Comment, Coords = self.Coords, Dimmable = self.Dimmable,
           Family = self.Family, RoomName = self.RoomName, Type = self.Type, UUID = self.UUID
           )
        l_attrs = filter(lambda aname: not aname.startswith('__'), dir(self))
        for l_attr in l_attrs:
            if not hasattr(l_ret, l_attr):
                l_val = getattr(self, l_attr)
                if not l_attr.startswith('_'):
                    l_ret[l_attr] = str(l_val)
                    if l_attr == 'InsteonAddress':
                        l_ret[l_attr] = web_utils.int2dotted_hex(l_val)
        return l_ret


class CoreAPI(xml_tools.ConfigTools):

    def read_light_common(self, p_entry_xml, p_device_obj, p_house_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        self.xml_read_common_info(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_from_xml(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool_from_xml(p_entry_xml, 'Dimmable')
        p_device_obj.Family = l_fam = self.get_text_from_xml(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        p_device_obj.UUID = self.get_uuid_from_xml(p_entry_xml, 'UUID')
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if l_family_obj.Name == l_fam:
                l_family_obj.API.extract_device_xml(p_entry_xml, p_device_obj)
        return p_device_obj

    def write_light_common(self, p_entry, p_device_obj, p_house_obj):
        self.put_text_element(p_entry, 'Comment', p_device_obj.Comment)
        self.put_text_element(p_entry, 'Coords', p_device_obj.Coords)
        self.put_bool_element(p_entry, 'Dimmable', p_device_obj.Dimmable)
        self.put_text_element(p_entry, 'Family', p_device_obj.Family)
        self.put_text_element(p_entry, 'Room', p_device_obj.RoomName)
        self.put_text_element(p_entry, 'Type', p_device_obj.Type)
        self.put_text_element(p_entry, 'UUID', p_device_obj.UUID)
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if l_family_obj.Name == p_device_obj.Family:
                l_family_obj.API.insert_device_xml(p_entry, p_device_obj)

# ## END DBK
