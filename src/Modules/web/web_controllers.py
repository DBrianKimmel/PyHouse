'''
Created on Apr 8, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.drivers import interface
from Modules.lights import lighting_controllers
from Modules.utils import pyh_log


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
LOG = pyh_log.getLogger('PyHouse.webCntlr    ')


class ControllersElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controllersElement.html'))
    jsClass = u'controllers.ControllersWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        if g_debug >= 2:
            print("web_controllers.ControllersElement()")

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS receiver for House information from the client.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouse_obj.HouseData
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        return unicode(l_json)

    @athena.expose
    def getInterfaceData(self):
        """ A JS request for interface information has been received from the client.
        """
        l_interfaces = interface.VALID_INTERFACES
        l_obj = {}
        for l_interface in l_interfaces:
            l_name = l_interface + 'Data'
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    @athena.expose
    def saveControllerData(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        l_controller_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.HouseData.Controllers[l_controller_ix]
            except AttributeError:
                print("web_controllers - Failed to delete - JSON: {0:}".FORMAT(l_json))
            return
        #
        # Note - we don't want a plain controller here - we want a family controller with the proper interface.
        #
        try:
            l_obj = self.m_pyhouse_obj.HouseData.Controllers[l_controller_ix]
        except KeyError:
            l_obj = lighting_controllers.ControllerData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_controller_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.Dimmable = l_json['Dimmable']
        l_obj.LightingFamily = l_json['LightingFamily']
        l_obj.RoomName = l_json['RoomName']
        l_obj.LightingType = l_json['Type']
        l_obj.UUID = l_json['UUID']
        l_obj.Interface = l_json['Interface']
        l_obj.Port = l_json['Port']
        if l_obj.LightingFamily == 'Insteon':
            l_obj.InsteonAddress = web_utils.dotted_hex2int(l_json['InsteonAddress'])
            l_obj.DevCat = l_json['DevCat']
            l_obj.GroupNumber = l_json['GroupNumber']
            l_obj.GroupList = l_json['GroupList']
            l_obj.Master = l_json['Master']
            l_obj.Responder = l_json['Responder']
            l_obj.ProductKey = l_json['ProductKey']
        self.m_pyhouse_obj.HouseData.Controllers[l_controller_ix] = l_obj

# ## END DBK
