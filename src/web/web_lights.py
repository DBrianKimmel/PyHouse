'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
import uuid
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
g_logger = logging.getLogger('PyHouse.webLight    ')


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
    def getHouseData(self, p_index):
        """ A JS client has requested all the lights information for a given house.

        Return the information via callback to the client.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        return l_json

    @athena.expose
    def saveLightData(self, p_json):
        """A new/changed light is returned.  Process it and update the internal data via light_xxxx.py
        """
        # print "saveLightData ", p_json
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_house_ix = int(l_json['HouseIx'])
        l_light_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Lights[l_light_ix]
            except AttributeError:
                print "web_lights - Failed to delete - JSON: ", l_json
            return
        #
        # Note - we don't want a plain light here - we want a family light
        #
        try:
            l_obj = self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Lights[l_light_ix]
        except KeyError:
            g_logger.warning('Creating a new light for house {0:} and light {1:}'.format(l_house_ix, l_light_ix))
            l_obj = lighting_lights.LightData()
        #
        # print "web_lights.saveLightData(1) ", l_json
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = int(l_json['Key'])
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.Dimmable = l_json['Dimmable']
        l_obj.Family = l_json['Family']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Type = l_json['Type']
        l_obj.UUID = l_json['UUID']
        if len(l_obj.UUID) < 8:
            l_obj.UUID = str(uuid.uuid1())
        if l_obj.Family == 'Insteon':
            # print "saving insteon light..", l_json
            l_obj.InsteonAddress = web_utils.dotted_hex2int(l_json['InsteonAddress'])
            l_obj.DevCat = l_json['DevCat']
            l_obj.GroupNumber = l_json['GroupNumber']
            l_obj.GroupList = l_json['GroupList']
            l_obj.Master = l_json['Master']
            l_obj.Responder = l_json['Responder']
            l_obj.ProductKey = l_json['ProductKey']
        self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Lights[l_light_ix] = l_obj
        self.m_pyhouses_obj.API.UpdateXml()

# ## END DBK
