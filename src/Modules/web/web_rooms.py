"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_rooms -*-

@name: PyHouse/src/Modules/web/web_rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Web interface to rooms for the selected house.

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.housing import rooms
from Modules.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webRooms    ')

#==============================================================================

class RoomsElement(athena.LiveElement):
    jsClass = u'rooms.RoomsWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'roomsElement.html'))

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self, _p_index):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj.HouseData)
        return l_house

    @athena.expose
    def saveRoomData(self, p_json):
        """A new/changed/deleted room is returned.  Process it and update the internal data.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_room_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.HouseData.Rooms[l_room_ix]
            except AttributeError:
                print("web_rooms - Failed to delete - JSON: {0:}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.HouseData.Rooms[l_room_ix]
        except KeyError:
            l_obj = rooms.RoomData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_room_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Corner = l_json['Corner']
        l_obj.Size = l_json['Size']
        l_obj.RoomType = 'Room'
        self.m_pyhouse_obj.HouseData.Rooms[l_room_ix] = l_obj

# ## END DBK
