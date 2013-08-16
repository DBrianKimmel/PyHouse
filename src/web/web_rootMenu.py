"""
Created on May 30, 2013

@author: briank
"""

# Import system type stuff
from nevow import loaders
from nevow import athena
from twisted.python.filepath import FilePath

# Import PyMh files and modules.
from src import web


# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class Username(object):
    """
    """


class RootMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(webdir('template/rootMenuElement.html').path)
    jsClass = u'rootMenu.RootMenuWidget'

    def __init__(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 2:
            print "web_rootMenu.RootMenuElement() ", p_pyhouses_obj
        pass

    @athena.expose
    def rootMenu(self, p_json):
        """ A JS receiver for root menu information from the client.
        """
        if g_debug >= 3:
            print "web_rootMenu.RootMenuElement.rootMenu() - Json:{0:}".format(p_json)



# ## END DBK
