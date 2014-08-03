"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_internet -*-

@name: PyHouse/src/Modules/web/web_internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Handle all of the information for a house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import InternetConnectionData
from Modules.web.web_utils import JsonUnicode
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webInternet ')


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
        l_computer = JsonUnicode().encode_json(self.m_pyhouse_obj.Computer.InternetConnection)
        PrettyPrintAny(l_computer, 'WebInternet - GetData', 100)
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
        l_obj.ExternalDelay = l_json['ExternalDelay']
        l_obj.ExternalUrl = l_json['ExternalUrl']
        l_obj.DynDns[l_dyndns_ix].Name = l_json['Name']
        l_obj.DynDns[l_dyndns_ix].Key = l_dyndns_ix
        l_obj.DynDns[l_dyndns_ix].Active = l_json['Active']
        l_obj.DynDns[l_dyndns_ix].UpdateInterval = l_json['UpdateInterval']
        l_obj.DynDns[l_dyndns_ix].UpdateUrl = l_json['UpdateUrl']
        self.m_pyhouse_obj.Computer.InternetConnection = l_obj

# ## END DBK
