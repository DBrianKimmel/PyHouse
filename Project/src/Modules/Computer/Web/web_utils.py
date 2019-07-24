"""
@name:      PyHouse/src/Modules/Computer/Web/web_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 30, 2013
@summary:   Test handling the information for a house.

"""

__updated__ = '2019-07-15'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import JsonHouseData
from Modules.Core.Utilities import json_tools
from Modules.Housing.Lighting.lighting import LightingInformation
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webUtils       ')

#  Web States defined
#-------------------
WS_IDLE = 0  #  Starting state
WS_LOGGED_IN = 1  #  Successful login completed
WS_ROOTMENU = 2
WS_HOUSE_SELECTED = 3
#  global things
WS_SERVER = 101
WS_LOGS = 102
#  House things
WS_HOUSE = 201
WS_LOCATION = 202
WS_ROOMS = 203
WS_INTERNET = 204
#  Light things
WS_BUTTONS = 501
WS_CONTROLLERS = 502
WS_LIGHTS = 503


class UtilJson(object):
    """
    """

    @staticmethod
    def _get_Lighting(p_pyhouse_obj):
        l_ret = LightingInformation()
        l_ret.Buttons = p_pyhouse_obj.House.Lighting.Buttons
        l_ret.Controllers = p_pyhouse_obj.House.Lighting.Controllers
        l_ret.GarageDoors = p_pyhouse_obj.House.Security.GarageDoors
        l_ret.Lights = p_pyhouse_obj.House.Lighting.Lights
        l_ret.Motion = p_pyhouse_obj.House.Security.MotionSensors
        return l_ret


def GetJSONHouseInfo(p_pyhouse_obj):
    """
    Get house info for the browser.

    This is simplified and customized so JSON encoding works.
    """
    l_ret = JsonHouseData()
    l_ret.Name = p_pyhouse_obj.House.Name
    l_ret.Key = p_pyhouse_obj.House.Key
    l_ret.Active = p_pyhouse_obj.House.Active
    l_ret.Hvac = p_pyhouse_obj.House.Hvac
    l_ret.Irrigation = p_pyhouse_obj.House.Irrigation
    l_ret.Lighting = UtilJson._get_Lighting(p_pyhouse_obj)
    l_ret.Location = p_pyhouse_obj.House.Location
    l_ret.Rooms = p_pyhouse_obj.House.Rooms
    l_ret.Schedules = p_pyhouse_obj.House.Schedules
    l_ret.Security = p_pyhouse_obj.House.Security
    l_json = unicode(json_tools.encode_json(l_ret))
    return l_json


def GetJSONComputerInfo(p_pyhouse_obj):
    """Get house info for the browser.
    This is simplified and customized so JSON encoding works.

    @param p_house_obj: is the complete information
    """
    l_ret = p_pyhouse_obj.Computer
    l_json = unicode(json_tools.encode_json(l_ret))
    return l_json


class State(object):
    """Used by various web_ modules to keep the state of the web server.
    """

    def __init__(self):
        self.State = WS_IDLE


def get_base_info(p_obj, p_json_decoded):
        p_obj.Name = p_json_decoded['Name']
        p_obj.Active = p_json_decoded['Active']
        p_obj.Key = p_json_decoded['Key']
        p_obj.UUID = p_json_decoded['UUID']
        return p_obj


def get_room_info(p_obj, p_json_decoded):
        # l_coords = CoordinateInformation()
        # l_coords.X_Easting = p_json_decoded['RoomCoords'][0]
        # l_coords.Y_Northing = p_json_decoded['RoomCoords'][1]
        # l_coords.Z_Height = p_json_decoded['RoomCoords'][2]
        # p_obj.RoomCoords = l_coords
        p_obj.RoomName = p_json_decoded['RoomName']
        p_obj.RoomUUID = p_json_decoded['RoomUUID']
        return p_obj

#  ## END DBK
