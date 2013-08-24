"""
Created on May 30, 2013

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

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webRMenu')


class RootMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'rootMenuElement.html'))
    jsClass = u'rootMenu.RootMenuWidget'

    def __init__(self, p_workspace):
        if g_debug >= 2:
            print "web_rootMenu.RootMenuElement()"

    @athena.expose
    def doRootMenu(self, p_json):
        """ A JS receiver for root menu information from the client.
        """
        if g_debug >= 3:
            print "web_rootMenu.RootMenuElement.doRootMenu() - Json:{0:}".format(p_json)
        g_logger.info("doRootMenu called {0:} {1:}".format(self, p_json))



# ## END DBK
