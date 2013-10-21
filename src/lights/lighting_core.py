'''
Created on Jun 13, 2013

@author: briank
'''

# Import system type stuff
import uuid

# Import PyHouse files
from src.utils import xml_tools
#from src.families import family
#from src.families.Insteon import Device_Insteon


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Print family info
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
        #self.CurLevel = 0
        self.Dimmable = False
        self.Family = ''
        self.RoomName = ''
        self.Type = ''
        self.UUID = None

    def __str__(self):
        l_str = "Light:: "
        l_str += "Name:{0:}, ".format(self.Name)
        l_str += "Key:{0:}, ".format(self.Key)
        l_str += "Active:{0:}, ".format(self.Active)
        l_str += "Comment:{0:}, ".format(self.Comment)
        l_str += "Coords:{0:}, ".format(self.Coords)
        #l_str += "CurLevel:{0:}, ".format(self.CurLevel)
        l_str += "Dimmable:{0:}, ".format(self.Dimmable)
        l_str += "Family:{0:}, ".format(self.Family)
        l_str += "RoomName:{0:}, ".format(self.RoomName)
        l_str += "Type:{0:}, ".format(self.Type)
        l_str += "UUID:{0:};".format(self.UUID)
        return l_str

    def reprJSON(self):
        #print "lighting_core.reprJSON() - Name:{0:}, Family:{1:}".format(self.Name, self.Family)
        l_ret = dict(Name = self.Name, Active = self.Active, Key = self.Key,
                    Comment = self.Comment, Coords = self.Coords, Dimmable = self.Dimmable,
                    Family = self.Family, RoomName = self.RoomName, Type = self.Type, UUID = self.UUID)
        return l_ret


class CoreAPI(xml_tools.ConfigTools):
    """
    """

    def read_light_common(self, p_entry_xml, p_device_obj, p_house_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        self.m_house_obj = p_house_obj
        if g_debug >= 3:
            print "lighting_core.read_light_common() XML={0:}".format(p_entry_xml)
        self.xml_read_common_info(p_device_obj, p_entry_xml)
        p_device_obj.Comment = self.get_text_from_xml(p_entry_xml, 'Comment')
        p_device_obj.Coords = self.get_text_from_xml(p_entry_xml, 'Coords')
        p_device_obj.Dimmable = self.get_bool_from_xml(p_entry_xml, 'Dimmable')
        p_device_obj.Family = l_fam = self.get_text_from_xml(p_entry_xml, 'Family')
        p_device_obj.RoomName = p_entry_xml.findtext('Room')
        p_device_obj.Type = p_entry_xml.findtext('Type')
        p_device_obj.UUID = self.get_text_from_xml(p_entry_xml, 'UUID')
        if len(p_device_obj.UUID) < 8:
            p_device_obj.UUID = str(uuid.uuid1())
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if g_debug >= 4:
                print "    {0:}, {1:}".format(l_family_obj.Name, l_fam)
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
        self.put_text_element(p_entry, 'UUID', p_device_obj.UUID)
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if g_debug >= 4:
                print "    {0:}, {1:}".format(l_family_obj.Name, p_device_obj.Family)
            if l_family_obj.Name == p_device_obj.Family:
                l_family_obj.API.insert_device_xml(p_entry, p_device_obj)

    def addJSON(self):
        print "lighting_core.addJSON() - {0:}".format(self.Name)
        l_ret = dict()
        for l_family_obj in self.m_house_obj.FamilyData.itervalues():
            pass
        return l_ret

# ## END DBK
