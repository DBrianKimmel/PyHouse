'''
Created on Sep 27, 2013

@author: briank
'''
'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from src.utils import pyh_log
from src.web import web_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data
# 3 = Detail data
# 4 = Dump JSON
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webWebs    ')


class WebsElement(athena.LiveElement):
    """ a 'live' webs element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'websElement.html'))
    jsClass = u'webs.WebsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj

    @athena.expose
    def getWebsData(self):
        """ A JS client has requested all the webs information.
        """
        l_obj = self.m_pyhouses_obj.WebData
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        return l_json

    @athena.expose
    def saveWebData(self, p_json):
        """A new/changed web is returned.  Process it and update the internal data via ???.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)

# ## END DBK
