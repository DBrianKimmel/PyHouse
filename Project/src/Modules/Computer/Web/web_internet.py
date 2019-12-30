"""
@name:      Modules/Web/web_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Handle the "Internet" information for a house.

"""

__updated__ = '2019-12-30'

# Import system type stuff
from datetime import datetime
from nevow import athena
from nevow import loaders
import os

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionInformation
from Modules.Computer.Web.web_utils import GetJSONComputerInfo
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webInternet ')


class InternetElement(athena.LiveElement):
    """ a 'live' internet element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'internetElement.html'))
    jsClass = u'internet.InternetWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getInternetData(self):
        l_computer = GetJSONComputerInfo(self.m_pyhouse_obj)
        return l_computer

    @athena.expose
    def saveInternetData(self, p_json):
        """Internet data is returned, so update the computer info.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        # l_ix = int(l_json['Key'])
        try:
            l_obj = self.m_pyhouse_obj.Computer.InternetConnection
        except KeyError:
            l_obj = InternetConnectionInformation()
        l_obj.LastChanged = datetime.now()
        l_obj.LocateUrls = l_json['LocateUrls']
        l_obj.UpdateUrls = l_json['UpdateUrls']
        l_obj.UpdateInterval = l_json['UpdateInterval']
        self.m_pyhouse_obj.Computer.InternetConnection = l_obj

# ## END DBK
