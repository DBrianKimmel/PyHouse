"""
Created on May 30, 2013

@author: briank
"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webRMenu    ')


class RootMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'rootMenuElement.html'))
    jsClass = u'rootMenu.RootMenuWidget'

    def __init__(self, p_workspace_obj):
        if g_debug >= 2:
            print("web_rootMenu.RootMenuElement()")
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj

    @athena.expose
    def doRootMenuReload(self, p_json):
        """ Process a message for a XML save/reload from the browser/client.
        """
        if g_debug >= 3:
            print("web_rootMenu.RootMenuElement.doRootMenuReload() - Json:{0:}".format(p_json))
        LOG.info("doRootMenuReload called {0:} {1:}".format(self, p_json))
        self.m_pyhouses_obj.API.Reload(self.m_pyhouses_obj)

    @athena.expose
    def doRootMenuQuit(self, p_json):
        """ Process a message for a browser logoff and quit that came from the browser/client.
        """
        if g_debug >= 3:
            print("web_rootMenu.RootMenuElement.doRootMenuQuit() - Json:{0:}".format(p_json))
        LOG.info("doRootMenuQuit called {0:} {1:}".format(self, p_json))

# ## END DBK
