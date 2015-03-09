"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_buttons -*-

@name: PyHouse/src/Modules/web/web_buttons.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Web interface to buttons for the selected house.

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Lighting import lighting_buttons
from Modules.Computer import logging_pyh as Logger

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webButton   ')


class ButtonsElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'buttonsElement.html'))
    jsClass = u'buttons.ButtonsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        if g_debug >= 2:
            print("web_buttons.ButtonsElement()")

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveButtonData(self, p_json):
        """A new/changed button is returned.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_obj = lighting_buttons.ButtonData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Level = l_json['Level']
        if l_obj.ControllerFamily == 'Insteon':
            Insteon_utils.Util().get_jaon_data(l_obj, l_json)

# ## END DBK
