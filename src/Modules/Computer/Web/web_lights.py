"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_lights -*-

@name:      PyHouse/src/Modules/web/web_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Handle all of the lights information for a house.

TODO: Change all references to a light if name changes.
"""

__updated__ = '2016-10-10'

#  Import system type stuff
import os
from nevow import loaders
from nevow import athena

#  Import PyMh files and modules.
#  from Modules.Core import conversions
from Modules.Core.data_objects import CoordinateData
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Housing.Lighting import lighting_lights
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils
from Modules.Utilities import json_tools

#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

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
        l_json = json_tools.decode_json_unicode(p_json)
        l_delete = l_json['Delete']
        l_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Lighting.Lights[l_ix]
            except AttributeError:
                LOG.error("web_lights - Failed to delete - JSON: {}".format(l_json))
            return
        l_obj = lighting_lights.LightData()
        try:
            l_obj = self.m_pyhouse_obj.House.Lighting.Lights[l_ix]
        except KeyError:
            LOG.warning('Creating a new light {}'.format(l_ix))
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.Comment = l_json['Comment']
        l_coords = CoordinateData()
        l_coords.X_Easting = l_json['RoomCoords'][0]
        l_coords.Y_Northing = l_json['RoomCoords'][1]
        l_coords.Z_Height = l_json['RoomCoords'][2]
        l_obj.RoomCoords = l_coords
        l_obj.IsDimmable = l_json['IsDimmable']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 2
        l_obj.UUID = l_json['UUID']
        #  if len(l_obj.UUID) < 8:
        #    l_obj.UUID = str(uuid.uuid1())
        if l_obj.DeviceFamily == 'Insteon':
            Insteon_utils.Util().get_json_data(l_obj, l_json)
        elif l_obj.DeviceFamily == 'UPB':
            l_obj.UPBAddress = l_json['UPBAddress']
            l_obj.UPBPassword = l_json['UPBPassword']
            l_obj.UPBNetworkID = l_json['UPBNetworkID']
        self.m_pyhouse_obj.House.Lighting.Lights[l_ix] = l_obj

#  ## END DBK
