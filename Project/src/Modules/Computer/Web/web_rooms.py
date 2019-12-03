"""
-*- _test-case-name: PyHouse.src.Modules.web._test.test_web_rooms -*-

@name:      PyHouse/Project/src/Modules/Computer/web/web_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Web interface to rooms for the selected house.

"""

__updated__ = '2019-12-02'

# Import system type stuff
import os
from twisted.web.template import Element, XMLString, renderer

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webRooms       ')

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

# class RoomsElement(athena.LiveElement):
#    jsClass = u'rooms.RoomsWidget'
#    docFactory = loaders.xmlfile(os.path.join(templatepath, 'roomsElement.html'))

#    def __init__(self, p_workspace_obj, p_params):
#        self.m_workspace_obj = p_workspace_obj
#        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
#        self.m_params = p_params

#    @athena.expose
#    def getServerData(self):
#        """
#        Get a lot of server JSON data and pass it to the client browser.
#        """
#        l_json = GetJSONHouseInfo(self.m_pyhouse_obj)
#        # LOG.warning('Fetched {}'.format(l_json))
#        return l_json

#    @athena.expose
#    def saveRoomData(self, p_json):
#        """A new/changed/deleted room is returned.  Process it and update the internal data.
#        """
#        l_json = json_tools.decode_json_unicode(p_json)
#        roomMaint().from_web(self.m_pyhouse_obj, l_json)


class RoomsElement(Element):

    loader = XMLString((
        '<h1 '
        'xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1"'
        '>Hello, <span t:render="name"></span>!</h1>'))

    def __init__(self, name):
        self.m_name = name

    @renderer
    def name(self, _request, _tag):
        return self.m_name

# ## END DBK
