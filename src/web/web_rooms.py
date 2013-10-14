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

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webRooms')

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
    def getRoomData(self, p_index):
        """ A JS client has requested all the room information for a given house.

        @param p_index: is the house index number.
        """
        if g_debug >= 3:
            print "web_rooms.EoomsElement.getRoomData(1) - HouseIndex:", p_index
        g_logger.info("getRoomData called {0:}".format(self))
        l_rooms = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Rooms
        l_obj = {}
        for l_key, l_val in l_rooms.iteritems():
            l_obj[l_key] = l_val
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 4:
            print "web_rooms.RoomsElement.getRoomData(2) - JSON:", l_json
        return unicode(l_json)

    @athena.expose
    def saveRoomData(self, p_json):
        """A new/changed/deleted room is returned.  Process it and update the internal data via ???
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_rooms.RoomsElement.saveRoomData() - JSON:", l_json
        l_obj = rooms.RoomData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Comment = l_json['Comment']
        l_obj.Corner = l_json['Corner']
        l_obj.Size = l_json['Size']
        l_obj.Type = 'Room'
        self.m_pyhouses_obj.HousesData[l_ix].HouseAPI.Update(l_obj)

# ## END DBK
