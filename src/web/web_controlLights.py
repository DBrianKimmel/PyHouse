"""
Created on Jun 3, 2013

@author: briank

Web interface to control lights for the selected house.
"""

# Import system type stuff
import logging
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from src.web import web_utils
from src.lights import lighting_lights

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webClLgt    ')

class ControlLightsElement(athena.LiveElement):
    """ a 'live' controlLights element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controlLightsElement.html'))
    jsClass = u'controlLights.ControlLightsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_controlLights.ControlLightsElement()"

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the information for a given house.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        if g_debug >= 3:
            print "web_controlLights.getHouseData() - HouseIndex:", p_index
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        return l_json

    @athena.expose
    def saveControlLightData(self, p_json):
        """A changed Light is returned.  Process it and update the light level
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_controlLights.saveControlLightData() - JSON:", l_json
        l_light_obj = lighting_lights.LightData()
        l_light_obj.Name = l_json['Name']
        l_light_obj.Key = int(l_json['Key'])
        l_light_obj.CurLevel = l_level = l_json['Level']
        l_light_obj.UUID = l_json['UUID']
        l_light_obj.HouseIx = l_house_ix
        self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.LightingAPI.ChangeLight(l_light_obj, l_level)

# ## END DBK
