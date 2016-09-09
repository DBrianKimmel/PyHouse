"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_rooms -*-

@name:      PyHouse/src/Modules/web/web_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Web interface to rooms for the selected house.

"""

__updated__ = '2016-09-04'

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Computer.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Housing.rooms import Maint as roomMaint
from Modules.Computer import logging_pyh as Logger

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

LOG = Logger.getLogger('PyHouse.webRooms       ')


class RoomsElement(athena.LiveElement):
    jsClass = u'rooms.RoomsWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'roomsElement.html'))

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        self.m_params = p_params

    @athena.expose
    def getServerData(self):
        """
        Get a lot of server JSON data and pass it to the client browser.
        """
        l_json = GetJSONHouseInfo(self.m_pyhouse_obj)
        # LOG.warn('Fetched {}'.format(l_json))
        return l_json

    @athena.expose
    def saveRoomData(self, p_json):
        """A new/changed/deleted room is returned.  Process it and update the internal data.
        """
        l_json = JsonUnicode().decode_json(p_json)
        roomMaint().from_web(self.m_pyhouse_obj, l_json)

# ## END DBK
