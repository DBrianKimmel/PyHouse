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
g_logger = logging.getLogger('PyHouse.webClLgt')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE

class ControlLightsElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controlLightsElement.html'))
    jsClass = u'controlLights.ControlLightsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_controlLights.ControlLightsElement()"

    @athena.expose
    def getControlLightData(self, p_index):
        """ A JS client has requested all the lights information for a given house.

        Return the information via a remote call to the client.

        @param p_index: is the house index number.
        """
        if g_debug >= 3:
            print "web_controlLights.ControlLightsElement.getControlLightEntries() - HouseIndex:", p_index
        l_lights = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Lights
        l_obj = {}
        for l_key, l_val in l_lights.iteritems():
            l_obj[l_key] = l_val
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        if g_debug >= 3:
            print "web_controlLights.ControlLightsElement.getControlLightsEntries() - JSON:", l_json
        return unicode(l_json)

    @athena.expose
    def saveControlLightData(self, p_json):
        """A changed Light is returned.  Process it and update the light level
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_controlLights.ControlLightsElement.doControlLightSubmit() - JSON:", l_json
        l_obj = lighting_lights.LightData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = int(l_json['Key'])
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.Dimmable = l_json['Dimmable']
        l_obj.Family = l_json['Family']
        l_obj.Level = l_json['Level']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Type = l_json['Type']
        l_obj.UUID = l_json['UUID']
        l_obj.DeleteFlag = l_json['Delete']
        l_obj.HouseIx = l_house_ix
        self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.LightingAPI.Update(l_obj)

# ## END DBK
