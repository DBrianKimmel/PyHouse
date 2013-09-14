'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
#from src.web import web_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 5
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detailed Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webHSel ')


class HouseSelectElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseSelectElement.html'))
    jsClass = u'houseSelect.HouseSelectWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_houseSelect.houseSelectElement()"

    @athena.expose
    def houseSelect(self, p_params):
        if g_debug >= 3:
            print "web_houseSelect.HouseSelectElement.houseSelect() - called from browser ", self, p_params

    @athena.expose
    def doSelect(self, p_json):
        """ A JS receiver for houseSelect information from the client.
        """
        if g_debug >= 3:
            print "web_login.HouseSelectElement.doSelect() - Json:{0:}".format(p_json)
        pass

    @athena.expose
    def getHousesToSelect(self, p_dummy):
        l_houses = self.m_pyhouses_obj.HousesData
        if g_debug >= 3:
            print "web_login.HouseSelectElement.getHousesToSelect()"
            print "    ", l_houses
        pass

# ## END DBK
