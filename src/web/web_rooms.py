"""
Created on Jun 3, 2013

@author: briank
"""

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils
from src.housing import rooms

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webRooms    ')

#==============================================================================

class RoomsElement(athena.LiveElement):
    jsClass = u'rooms.RoomsWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'roomsElement.html'))

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_rooms.RoomsElement()"

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the room information for a given house.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        if g_debug >= 3:
            print "web_rooms.RoomsElement.getRoomData(1) - HouseIndex:", p_index
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        return unicode(l_json)

    @athena.expose
    def saveRoomData(self, p_json):
        """A new/changed/deleted room is returned.  Process it and update the internal data.
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        l_room_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if g_debug >= 4:
            print "web_rooms.RoomsElement.saveRoomData() - JSON:", l_json
        if l_delete:
            try:
                del self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Rooms[l_room_ix]
            except AttributeError:
                print "web_rooms - Failed to delete - JSON: ", l_json
            return
        try:
            l_obj = self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Rooms[l_room_ix]
        except KeyError:
            l_obj = rooms.RoomData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_room_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Corner = l_json['Corner']
        l_obj.Size = l_json['Size']
        l_obj.Type = 'Room'
        self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Rooms[l_room_ix] = l_obj
        self.m_pyhouses_obj.API.UpdateXml()

# ## END DBK
