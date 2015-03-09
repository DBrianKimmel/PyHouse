"""
Created on May 30, 2013

@author: briank
"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webRootMenu    ')


class RootMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'rootMenuElement.html'))
    jsClass = u'rootMenu.RootMenuWidget'

    def __init__(self, p_workspace_obj):
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def doRootMenuReload(self, p_json):
        """ Process a message for a XML save/reload from the browser/client.
        """
        LOG.info("Self: {}".format(self))
        self.m_pyhouse_obj.APIs.PyHouseAPI.SaveXml(self.m_pyhouse_obj)

    @athena.expose
    def doRootMenuQuit(self, p_json):
        """ Process a message for a browser logoff and quit that came from the browser/client.
        """
        LOG.info("Self: {0:};  JSON: {1:}".format(self, p_json))

# ## END DBK
