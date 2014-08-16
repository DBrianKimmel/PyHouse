"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_utils -*-

@name: PyHouse/src/Modules/web/web_utils.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 30, 2013
@summary: Test handling the information for a house.

"""

# Import system type stuff
import jsonpickle
import json

# Import PyMh files and modules.
from Modules.Core.data_objects import JsonHouseData, ComputerInformation
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0

# Web States defined
#-------------------
WS_IDLE = 0  # Starting state
WS_LOGGED_IN = 1  # Successful login completed
WS_ROOTMENU = 2
WS_HOUSE_SELECTED = 3
# global things
WS_SERVER = 101
WS_LOGS = 102
# House things
WS_HOUSE = 201
WS_LOCATION = 202
WS_ROOMS = 203
WS_INTERNET = 204
# Light things
WS_BUTTONS = 501
WS_CONTROLLERS = 502
WS_LIGHTS = 503


def GetJSONHouseInfo(p_pyhouse_obj):
    """Get house info for the browser.
    This is simplified and customized so JSON encoding works.

    @param p_house_obj: is the complete information
    """
    l_ret = JsonHouseData()
    l_ret.Name = p_pyhouse_obj.House.Name
    l_ret.Key = p_pyhouse_obj.House.Key
    l_ret.Active = p_pyhouse_obj.House.Active
    l_ret.Buttons = p_pyhouse_obj.House.OBJs.Buttons
    l_ret.Controllers = p_pyhouse_obj.House.OBJs.Controllers
    l_ret.Lights = p_pyhouse_obj.House.OBJs.Lights
    l_ret.Location = p_pyhouse_obj.House.OBJs.Location
    l_ret.Rooms = p_pyhouse_obj.House.OBJs.Rooms
    l_ret.Schedules = p_pyhouse_obj.House.OBJs.Schedules
    l_json = unicode(JsonUnicode().encode_json(l_ret))
    return l_json

def GetJSONComputerInfo(p_pyhouse_obj):
    """Get house info for the browser.
    This is simplified and customized so JSON encoding works.

    @param p_house_obj: is the complete information
    """
    l_ret = ComputerInformation()
    l_ret.InternetConnection = p_pyhouse_obj.Computer.InternetConnection
    l_ret.Logs = p_pyhouse_obj.Computer.Logs
    l_ret.Nodes = p_pyhouse_obj.Computer.Nodes
    l_ret.Web = p_pyhouse_obj.Computer.Web
    l_json = unicode(JsonUnicode().encode_json(l_ret))
    return l_json


class State(object):
    """Used by various web_ modules to keep the state of the web server.
    """
    def __init__(self):
        self.State = WS_IDLE


class JsonUnicode(object):
    """Utilities for handling unicode and json
    """

    def convert_from_unicode(self, p_input):
        """Convert unicode strings to python 2 strings.
        """
        if isinstance(p_input, dict):
            return {self.convert_from_unicode(key): self.convert_from_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_from_unicode(element) for element in p_input]
        elif isinstance(p_input, unicode):
            return p_input.encode('ascii')
        else:
            return p_input

    def convert_to_unicode(self, p_input):
        if isinstance(p_input, dict):
            return {self.convert_to_unicode(key): self.convert_to_unicode(value) for key, value in p_input.iteritems()}
        elif isinstance(p_input, list):
            return [self.convert_to_unicode(element) for element in p_input]
        elif isinstance(p_input, (int, bool)):
            return unicode(str(p_input), 'iso-8859-1')
        elif isinstance(p_input, unicode):
            return p_input
        else:
            return unicode(p_input, 'iso-8859-1')

    def decode_json(self, p_json):
        """Convert a json object to a python object
        """
        try:
            l_obj = self.convert_from_unicode(json.loads(p_json))
        except (TypeError, ValueError):
            l_obj = None
        return l_obj

    def encode_json(self, p_obj):
        """Convert a python object to a valid json object.
        """
        try:
            l_json = jsonpickle.encode(p_obj, unpicklable = False, max_depth = 5)
        except (TypeError, ValueError) as l_error:
            print('web_utils.encode_json ERROR {0:}'.format(l_error))
            l_json = u'{}'
        return l_json

# ## END DBK
