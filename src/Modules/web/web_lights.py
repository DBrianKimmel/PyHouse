"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_lights -*-

@name: PyHouse/src/Modules/web/web_lights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Handle all of the lights information for a house.

"""

# Import system type stuff
import os
import uuid
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core import conversions
from Modules.web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.lights import lighting_lights
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webLight    ')


class LightsElement(athena.LiveElement):
    """ a 'live' lights element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'lightsElement.html'))
    jsClass = u'lights.LightsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        """Called when connection is made to browser.

        @param p_params: = 'dummy'
        """
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self, _p_index):
        # PrettyPrintAny(self.m_pyhouse_obj, 'Web Lights - House.OBJs ')
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        # PrettyPrintAny(l_house, 'Web Lights - Json ')
        return l_house

    @athena.expose
    def saveLightData(self, p_json):
        """A new/changed light is returned.  Process it and update the internal data via light_xxxx.py
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_light_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.OBJs.Lights[l_light_ix]
            except AttributeError:
                LOG.error("web_lights - Failed to delete - JSON: {0:}".format(l_json))
            return
        #
        # Note - we don't want a plain light here - we want a family light
        #
        try:
            l_obj = self.m_pyhouse_obj.House.OBJs.Lights[l_light_ix]
        except KeyError:
            LOG.warning('Creating a new light for light {0:}'.format(l_light_ix))
            l_obj = lighting_lights.LightData()
        #
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = int(l_json['Key'])
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.IsDimmable = l_json['IsDimmable']
        l_obj.ControllerFamily = l_json['ControllerFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.LightingType = l_json['LightingType']
        l_obj.UUID = l_json['UUID']
        if len(l_obj.UUID) < 8:
            l_obj.UUID = str(uuid.uuid1())
        if l_obj.ControllerFamily == 'Insteon':
            l_obj.InsteonAddress = conversions.dotted_hex2int(l_json['InsteonAddress'])
            l_obj.DevCat = conversions.dotted_hex2int(l_json['DevCat'])
            l_obj.GroupNumber = l_json['GroupNumber']
            l_obj.GroupList = l_json['GroupList']
            l_obj.IsMaster = l_json['IsMaster']
            l_obj.IsResponder = l_json['IsResponder']
            l_obj.ProductKey = conversions.dotted_hex2int(l_json['ProductKey'])
        self.m_pyhouse_obj.House.OBJs.Lights[l_light_ix] = l_obj

# ## END DBK
