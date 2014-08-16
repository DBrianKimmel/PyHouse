"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_rooms -*-

@name: PyHouse/src/Modules/Web/web_rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2013
@summary: Web interface to rooms for the selected house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Utilities import pyh_log
from Modules.Utilities.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webHouse    ')


class HouseElement(athena.LiveElement):
    """ a 'live' house element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseElement.html'))
    jsClass = u'house.HouseWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        if g_debug >= 2:
            print("web_house.HouseElement()")

    @athena.expose
    def getHouseData(self):
        l_house = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_house

    @athena.expose
    def saveHouseData(self, p_json):
        """House data is returned, so update the house info.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.House
            except AttributeError:
                print("web_lights - Failed to delete - JSON: {0:}".format(l_json))
            return
        PrettyPrintAny(l_json, 'WebHouse - JSON', 100)
        # if l_house_ix == -1:  # adding a new house
        #    l_house_ix = len(self.m_pyhouse_obj.House.OBJs)
        l_obj = self.m_pyhouse_obj.House.OBJs
        PrettyPrintAny(l_obj, 'WebHouse - OBJ', 100)
        # try:
        #    self.m_pyhouse_obj.House.OBJs[l_house_ix] = l_obj
        # except AttributeError:
        #    self.m_pyhouse_obj.House.OBJs = l_obj
        l_obj.Name = l_json['Name']
        l_obj.Key = int(l_json['Key'])
        l_obj.Location.Street = l_json['Street']
        l_obj.Location.City = l_json['City']
        l_obj.Location.State = l_json['State']
        l_obj.Location.ZipCode = l_json['ZipCode']
        l_obj.Location.Phone = l_json['Phone']
        l_obj.Location.Latitude = l_json['Latitude']
        l_obj.Location.Longitude = l_json['Longitude']
        l_obj.Location.TimeZone = l_json['TimeZone']
        l_obj.Location.SavingsTime = l_json['SavingsTime']
        self.m_pyhouse_obj.House.OBJs = l_obj

# ## END DBK
