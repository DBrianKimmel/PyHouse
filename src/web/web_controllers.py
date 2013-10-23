'''
Created on Apr 8, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils
from src.drivers import interface
from src.lights import lighting_controllers
from src.families.Insteon import Device_Insteon

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
g_logger = logging.getLogger('PyHouse.webCntlr')


class ControllersElement(athena.LiveElement):
    """ a 'live' controllers element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'controllersElement.html'))
    jsClass = u'controllers.ControllersWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_controllers.ControllersElement()"
            #print "    self = ", self  #, vars(self)
            #print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS receiver for House information from the client.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        if g_debug >= 3:
            print "web_controllers.getHouseData() - JSON:", l_json
        return unicode(l_json)

    @athena.expose
    def getInterfaceData(self):
        """ A JS request for interface information has been received from the client.
        """
        l_interfaces = interface.VALID_INTERFACES
        l_obj = {}
        for l_int in l_interfaces:
            l_name = l_int + 'Data'
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 3:
            print "web_controllers.ControllersElement.getInterfaceData() - JSON:", l_json
        return unicode(l_json)

    @athena.expose
    def saveControllerData(self, p_json):
        """A new/changed controller is returned.  Process it and update the internal data via controller.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        l_controller_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if g_debug >= 0:
            print "web_controllers.ControllersElement.saveControllerData() - JSON:", p_json
        if l_delete:
            try:
                del self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Controllers[l_controller_ix]
            except AttributeError:
                print "web_controllers - Failed to delete - JSON: ", l_json
            return
        try:
            l_obj = self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Controllers[l_controller_ix]
        except KeyError:
            l_obj = lighting_controllers.ControllerData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_controller_ix
        l_obj.Comment = l_json['Comment']
        l_obj.Coords = l_json['Coords']
        l_obj.Dimmable = l_json['Dimmable']
        l_obj.Family = l_json['Family']
        l_obj.RoomName = l_json['RoomName']
        l_obj.Type = l_json['Type']
        l_obj.UUID = l_json['UUID']
        l_obj.Interface = l_json['Interface']
        l_obj.Port = l_json['Port']
        l_obj.InsteonAddress = l_json['InsteonAddress']

# ## END DBK
