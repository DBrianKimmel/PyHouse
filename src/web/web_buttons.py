'''
Created on Jun 3, 2013

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
g_logger = logging.getLogger('PyHouse.webButtn')


class ButtonsElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'buttonsElement.html'))
    jsClass = u'buttons.ButtonsWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_buttons.ButtonsElement()"
            #print "    self = ", vars(self)
            #print "    workspace_obj = ", vars(p_workspace_obj)

    @athena.expose
    def getButtons(self):
        """ A JS receiver for button information from the client.
        """
        if g_debug >= 3:
            print "web_buttons.ButtonsElement.getButtons()"
        g_logger.info("getButtons called {0:}".format(self))


# ## END DBK
