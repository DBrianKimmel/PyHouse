'''
Created on Apr 8, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils

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
g_logger = logging.getLogger('PyHouse.webCntlr')


class ControllersElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controllersElement.html'))
    jsClass = u'controllers.ControllersWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_controllers.ControllersElement()"
            print "    self = ", self  #, vars(self)
            print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def doControllers(self, p_json):
        """ A JS receiver for controllers information from the client.
        """
        if g_debug >= 3:
            print "web_controllers.ControllersElement.doControllers()"
        g_logger.info("doControllers called {0:} {1:}".format(self, p_json))

    @athena.expose
    def getControllerEntries(self, p_index):
        """ A JS receiver for controllers information from the client.
        """
        if g_debug >= 3:
            print "web_controllers.ControllersElement.getControllerEntries() - HouseIndex:", p_index
        g_logger.info("getControllers called {0:}".format(self))
        l_controllers = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Controllers
        l_obj = {}
        for l_key, l_val in l_controllers.iteritems():
            l_obj[l_key] = l_val
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 3:
            print "web_controllers.ControllersElement.getControllerEntries() - JSON:", l_json
        self.callRemote('displayControllerButtons', unicode(l_json))  # call client @ controllers.js

    @athena.expose
    def doControllerSubmit(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        if g_debug >= 3:
            print "web_controllers.ControllersElement.doControllerSubmit() - JSON:", p_json

# ## END DBK
