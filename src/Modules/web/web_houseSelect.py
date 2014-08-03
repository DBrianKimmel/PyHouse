"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_houseSelect -*-

@name: PyHouse/src/Modules/web/web_houseSelect.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 1, 2013
@summary: Handle all of the information for a house.

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.utils import pyh_log


# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webHouseSel ')


class HouseSelectElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseSelectElement.html'))
    jsClass = u'houseSelect.HouseSelectWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHousesToSelect(self, _p_dummy):
        """This is called from the client when the widget is activated by selecting the select house button on the root menu.

        Gather the top level data for houses and send it back to the client for building a house select page.
        """
        l_house = self.m_pyhouse_obj.House
        l_obj = {}
        l_obj[0] = {}
        l_obj[0]['Name'] = l_house.Name
        l_obj[0]['Key'] = l_house.Key
        l_obj[0]['Active'] = l_house.Active
        l_json = JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    @athena.expose
    def getSelectedHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

# ## END DBK
