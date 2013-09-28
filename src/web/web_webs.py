'''
Created on Sep 27, 2013

@author: briank
'''
'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from src.web import web_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data
g_logger = logging.getLogger('PyHouse.webWebs')


class WebsElement(athena.LiveElement):
    """ a 'live' webs element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'websElement.html'))
    jsClass = u'webs.WebsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_webs.WebsElement()"


# ## END DBK
