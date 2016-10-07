"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_webs -*-

@name:      PyHouse/src/Modules/web/web_webs.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 27, 2013
@summary:   Handle all of the information for a house.

"""

__updated__ = '2016-10-06'

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import WebData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webWebs    ')


class WebsElement(athena.LiveElement):
    """ a 'live' webs element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'websElement.html'))
    jsClass = u'webs.WebsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getWebsData(self):
        """ A JS client has requested all the webs information.
        """
        l_obj = self.m_pyhouse_obj.Computer.Web
        l_json = unicode(json_tools.encode_json(l_obj))
        return l_json

    @athena.expose
    def saveWebData(self, p_json):
        """A new/changed web is returned.  Process it and update the internal data via ???.py
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_obj = WebData()
        l_obj.Port = l_json['Port']
        self.m_pyhouse_obj.APIs.Computer.WebAPI.SaveXml(l_obj)

# ## END DBK
