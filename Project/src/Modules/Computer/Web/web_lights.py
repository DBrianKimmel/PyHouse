"""
-*- _test-case-name: PyHouse.src.Modules.web._test.test_web_lights -*-

@name:      PyHouse/src/Modules/web/web_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Handle all of the lights information for a house.

TODO: Change all references to a light if name changes.
"""

__updated__ = '2017-01-19'

#  Import system type stuff
import os
from nevow import loaders
from nevow import athena

#  Import PyMh files and modules.
from Modules.Computer.Web import web_family, web_utils
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Housing.Lighting import lighting_lights
from Modules.Core.Utilities import json_tools
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webLight    ')
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


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
            l_obj = lighting_lights.LightData()
            LOG.warning('Creating a new light {}'.format(l_ix))
        # LOG.debug(PrettyFormatAny.form(l_json, 'json'))
        web_utils.get_base_info(l_obj, l_json)
        l_obj.Comment = l_json['Comment']
        l_obj.IsDimmable = l_json['IsDimmable']
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.DeviceType = 1
        l_obj.DeviceSubType = 3
        web_family.get_family_json_data(l_obj, l_json)
        web_utils.get_room_info(l_obj, l_json)
        self.m_pyhouse_obj.House.Lighting.Lights[l_ix] = l_obj
        LOG.info('Light Added - {}'.format(l_obj.Name))

#  ## END DBK
