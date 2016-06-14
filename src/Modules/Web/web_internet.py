"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_internet -*-

@name:      PyHouse/src/Modules/Web/web_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Handle the Internet information for a house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData
from Modules.Web.web_utils import JsonUnicode, GetJSONComputerInfo
from Modules.Computer import logging_pyh as Logger

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
    def getHouseData(self):
        l_computer = GetJSONComputerInfo(self.m_pyhouse_obj)
        return l_computer

    @athena.expose
    def saveInternetData(self, p_json):
        """Internet data is returned, so update the computer info.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_dyndns_ix = int(l_json['Key'])
        try:
            l_obj = self.m_pyhouse_obj.Computer.InternetConnection
        except KeyError:
            l_obj = InternetConnectionData()
            l_obj.DynDns = {}
        l_obj.Name = l_json['Name']
        l_obj.Key = 0
        l_obj.Active = True
        # l_obj.ExternalDelay = l_json['ExternalDelay']
        l_obj.ExternalUrl = l_json['ExternalUrl']
        l_obj.DynDns[l_dyndns_ix].Name = l_json['Name']
        l_obj.DynDns[l_dyndns_ix].Key = l_dyndns_ix
        l_obj.DynDns[l_dyndns_ix].Active = l_json['Active']
        l_obj.DynDns[l_dyndns_ix].UpdateInterval = l_json['UpdateInterval']
        l_obj.DynDns[l_dyndns_ix].UpdateUrl = l_json['UpdateUrl']
        self.m_pyhouse_obj.Computer.InternetConnection = l_obj

# ## END DBK
