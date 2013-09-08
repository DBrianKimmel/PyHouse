"""
Created on Jun 3, 2013

@author: briank

Web interface to control lights for the selected house.
"""

# Import system type stuff
import logging
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')
g_logger = logging.getLogger('PyHouse.webClLgt')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE

class ControlLightsElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controlLightsElement.html'))
    jsClass = u'controlLights.ControlLightsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_controlLights.SchedulesElement()"
            print "    self = ", self  #, vars(self)
            print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def getControlLights(self):
        """ A JS receiver for controlling lights from the client.
        """
        if g_debug >= 3:
            print "web_controlLights.ControlLightsElement.doSchedules()"
        g_logger.info("doControlLights called {0:}".format(self))


# ## END DBK
