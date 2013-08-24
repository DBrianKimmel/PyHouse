'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
from twisted.python.filepath import FilePath
from nevow import loaders
from nevow import athena
#from nevow import rend

# Import PyMh files and modules.
from src import web
#from src.web.web_tagdefs import *
#from src.web import web_utils
#from src.web import web_houseMenu

# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class HouseSelectElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(webdir('template/houseSelectElement.html').path)
    jsClass = u'houseSelect.HouseSelectWidget'

    def __init__(self, p_workspace_obj):
        self.m_pyhouses_obj = p_workspace_obj
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

# ## END DBK
