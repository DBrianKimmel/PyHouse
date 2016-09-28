"""

@name:      PyHouse/src/Modules/Web/web_rootMenu.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 30, 2013
@summary:   Handle the Main menu.

"""

__updated__ = '2016-09-23'

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
        self.m_pyhouse_obj.APIs.PyHouseMainAPI.SaveXml(self.m_pyhouse_obj)

    @athena.expose
    def doRootMenuQuit(self, p_json):
        """ Process a message for a browser logoff and quit that came from the browser/client.
        """
        LOG.info("Self: {};  JSON: {}".format(self, p_json))

# ## END DBK
