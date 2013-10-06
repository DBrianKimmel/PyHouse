'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

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
g_logger = logging.getLogger('PyHouse.webLight')


class LightsElement(athena.LiveElement):
    """ a 'live' lights element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'lightsElement.html'))
    jsClass = u'lights.LightsWidget'

    def __init__(self, p_workspace_obj, p_params):
        """Called when connection is made to browser.

        @param p_params: = 'dummy'
        """
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_lights.LightsElement()"

    @athena.expose
    def getLightData(self, p_index):
        """ A JS client has requested all the lights information for a given house.

        Return the information via callback to the client.

        @param p_index: is the house index number.
        """
        if g_debug >= 3:
            print "web_lights.LightsElement.getLightData() - HouseIndex:", p_index
        l_lights = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Lights
        l_obj = {}
        for l_key, l_val in l_lights.iteritems():
            l_obj[l_key] = l_val
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        if g_debug >= 4:
            print "web_lights.LightsElement.getLightsEntries() - JSON:", l_json
        return l_json

    @athena.expose
    def doLightSubmit(self, p_json):
        """A new/changed Light is returned.  Process it and update the internal data via Light.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_lights.LightsElement.doLightSubmit() - JSON:", l_json
            #print "    ", type(l_json)
            #print "  1 ", str(self.m_pyhouses_obj.HousesData)
            #print "  2 ", str(self.m_pyhouses_obj.HousesData[l_ix])
            #print "  3 ", str(self.m_pyhouses_obj.HousesData[l_ix].HouseObject)
            #print "  4 ", dir(self.m_pyhouses_obj.HousesData[l_ix].HouseObject)
        l_obj = lighting_lights.LightData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Level = l_json['Level']
        l_obj.LightName = l_json['LightName']
        l_obj.Rate = l_json['Rate']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Time = l_json['Time']
        l_obj.Type = l_json['Type']
        self.m_pyhouses_obj.HousesData[l_ix].HouseObject.LightingAPI.update_data(l_obj)

# ## END DBK
