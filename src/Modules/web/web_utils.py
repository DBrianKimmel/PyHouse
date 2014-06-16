"""
-*- test-case-name: PyHouse.Modules.web.test.test_web_utils -*-

@name: PyHouse/src/Modules/web/web_utils.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 30, 2013
@summary: Test handling the information for a house.

"""

# Import system type stuff
# import datetime
import jsonpickle
# import random
# import twisted.python.components as tpc
# from nevow import flat
# from nevow import inevow
# from nevow import rend
# from nevow import static
# from nevow import url
# from nevow import util
# from nevow.rend import _CARRYOVER
# from formless import iformless
import json

# Import PyMh files and modules.
from Modules.Core.data_objects import JsonHouseData
# from Modules.utils.tools import PrettyPrintAny


g_debug = 0


# Web States defined
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

SUBMIT = '_submit'
BUTTON = 'post_btn'

def GetJSONHouseInfo(p_house_obj):
    """Get house info for the browser.
    This is simplified so JSON encoding works.
    Perhaps we should split the HouseData object and do it that way.

    @param p_house_obj: is the complete information
    """
    l_ret = JsonHouseData()
    l_ret.Buttons = p_house_obj.Buttons
    l_ret.Controllers = p_house_obj.Controllers
    l_ret.Lights = p_house_obj.Lights
    l_ret.Rooms = p_house_obj.Rooms
    l_ret.Schedules = p_house_obj.Schedules
    # PrettyPrintAny(l_ret, 'web_utils house data')
    l_json = unicode(JsonUnicode().encode_json(l_ret))
    # PrettyPrintAny(l_json, 'web_utils to browser JSON')
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
            # l_json = json.dumps(p_obj, cls = ComplexHandler)
            l_json = jsonpickle.encode(p_obj, unpicklable = False, max_depth = 150)
        except (TypeError, ValueError) as l_error:
            print('web_utils.encode_json ERROR {0:}'.format(l_error))
            l_json = '{}'
        return l_json


def dotted_hex2int(p_addr):
    """Convert A1.B2.C3 to int
    """
    l_hexn = ''.join(["%02X" % int(l_ix, 16) for l_ix in p_addr.split('.')])
    return int(l_hexn, 16)

def int2dotted_hex(p_int):
    """Convert 24 bit int to Dotted hex Insteon Address
    """
    l_ix = 256 * 256
    l_hex = []
    while l_ix > 0:
        l_byte, p_int = divmod(p_int, l_ix)
        l_hex.append("{0:02X}".format(l_byte))
        l_ix = l_ix / 256
    return '.'.join(l_hex)

# ## END DBK
