'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import os
import uuid
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.lights import lighting_lights
from Modules.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webLight    ')


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
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the lights information for a given house.

        Return the information via callback to the client.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouse_obj.HouseData
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        return l_json

    @athena.expose
    def saveLightData(self, p_json):
        """A new/changed light is returned.  Process it and update the internal data via light_xxxx.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_house_ix = int(l_json['HouseIx'])
        l_light_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.HouseData.Lights[l_light_ix]
            except AttributeError:
                LOG.error("web_lights - Failed to delete - JSON: {0:}".format(l_json))
            return
        #
        # Note - we don't want a plain light here - we want a family light
        #
        try:
            l_obj = self.m_pyhouse_obj.HouseData.Lights[l_light_ix]
        except KeyError:
            LOG.warning('Creating a new light for house {0:} and light {1:}'.format(l_house_ix, l_light_ix))
            l_obj = lighting_lights.LightData()
        #
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = int(l_json['Key'])
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.Dimmable = l_json['Dimmable']
        l_obj.LightingFamily = l_json['LightingFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.LightingType = l_json['Type']
        l_obj.UUID = l_json['UUID']
        if len(l_obj.UUID) < 8:
            l_obj.UUID = str(uuid.uuid1())
        if l_obj.LightingFamily == 'Insteon':
            l_obj.InsteonAddress = web_utils.dotted_hex2int(l_json['InsteonAddress'])
            l_obj.DevCat = l_json['DevCat']
            l_obj.GroupNumber = l_json['GroupNumber']
            l_obj.GroupList = l_json['GroupList']
            l_obj.Master = l_json['Master']
            l_obj.Responder = l_json['Responder']
            l_obj.ProductKey = l_json['ProductKey']
        self.m_pyhouse_obj.HouseData.Lights[l_light_ix] = l_obj

# ## END DBK
