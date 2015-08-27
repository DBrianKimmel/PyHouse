"""
@name:      PyHouse/src/Modules/Web/web_users.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 23, 2015
@Summary:

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Housing import rooms
from Modules.Computer import logging_pyh as Logger

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webUsers       ')



#==============================================================================

class UsersElement(athena.LiveElement):
    jsClass = u'users.UsersWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'usersElement.html'))

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getServerData(self):
        """
        Get a lot of server JSON data and pass it to the client browser.
        """
        l_users = self.m_pyhouse_obj.Computer.Web.Logins
        l_json = unicode(JsonUnicode().encode_json(l_users))
        LOG.info('Fetched {}'.format(l_json))
        return l_json

    @athena.expose
    def saveData(self, p_json):
        """A new/changed/deleted user is returned.  Process it and update the internal data.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_room_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Rooms[l_room_ix]
            except AttributeError:
                print("web_rooms - Failed to delete - JSON: {0:}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.House.Rooms[l_room_ix]
        except KeyError:
            l_obj = rooms.RoomData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_room_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Corner = l_json['Corner']
        l_obj.Size = l_json['Size']
        l_obj.RoomType = 'Room'
        self.m_pyhouse_obj.House.Rooms[l_room_ix] = l_obj

# ## END DBK