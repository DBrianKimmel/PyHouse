"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_controlLights -*-

@name: PyHouse/src/Modules/web/web_controlLights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Web interface to control lights for the selected house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webCtlLigt  ')


class ControlLightsElement(athena.LiveElement):
    """ a 'live' controlLights element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controlLightsElement.html'))
    jsClass = u'controlLights.ControlLightsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        """ A JS client has requested all the information for a given house.

        @param p_index: is the house index number.
        """
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveControlLightData(self, p_json):
        """A changed Light is returned.  Process it and update the light level
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_light_ix = int(l_json['Key'])
        l_light_obj = LightData()
        l_light_obj.Name = l_json['Name']
        l_light_obj.Key = l_light_ix
        l_light_obj.CurLevel = l_level = l_json['Level']
        l_light_obj.UUID = l_json['UUID']
        LOG.info('Control Light via Web - Change {0:} device to level {1:}'.format(l_light_obj.Name, l_light_obj.CurLevel))
        self.m_pyhouse_obj.APIs.LightingAPI.ChangeLight(l_light_obj, l_level)

# ## END DBK
