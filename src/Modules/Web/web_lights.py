"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_lights -*-

@name:      PyHouse/src/Modules/web/web_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Handle all of the lights information for a house.

TODO: Change all references to a light if name changes.

"""

# Import system type stuff
import os
import uuid
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core import conversions
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Lighting import lighting_lights
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webLight    ')


class LightsElement(athena.LiveElement):
    """ a 'live' lights element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'lightsElement.html'))
    jsClass = u'lights.LightsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
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
                del self.m_pyhouse_obj.House.DeviceOBJs.Lights[l_light_ix]
            except AttributeError:
                LOG.error("web_lights - Failed to delete - JSON: {0:}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.House.DeviceOBJs.Lights[l_light_ix]
        except KeyError:
            LOG.warning('Creating a new light for light {0:}'.format(l_light_ix))
            l_obj = lighting_lights.LightData()
        #
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_light_ix
        l_obj.Comment = l_json['Comment']
        l_obj.RoomCoords = l_json['RoomCoords']
        l_obj.IsDimmable = l_json['IsDimmable']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.LightingType = l_json['LightingType']
        l_obj.UUID = l_json['UUID']
        if len(l_obj.UUID) < 8:
            l_obj.UUID = str(uuid.uuid1())
        if l_obj.DeviceFamily == 'Insteon':
            Insteon_utils.Util().get_json_data(l_obj, l_json)
        elif l_obj.DeviceFamily == 'UPB':
            l_obj.UPBAddress = l_json['UPBAddress']
            l_obj.UPBPassword = l_json['UPBPassword']
            l_obj.UPBNetworkID = l_json['UPBNetworkID']
        self.m_pyhouse_obj.House.DeviceOBJs.Lights[l_light_ix] = l_obj

# ## END DBK
