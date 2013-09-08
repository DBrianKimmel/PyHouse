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

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
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
            print "    self = ", self  #, vars(self)
            print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)


    @athena.expose
    def getRooms(self):
        if g_debug >= 2:
            print "web_rooms.Room.getTimeOfDay() - called from browser"
        return uc('abc')

def uc(msg):
    if type(msg) == type(''):
        return unicode(msg, 'iso-8859-1')
    else:
        return msg

# ## END DBK
