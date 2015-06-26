"""
-*- test-case-name: PyHouse.src.Modules.Utilities.test.test_json_tools -*-

@name:      PyHouse/src/Modules/Utilities/json_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 6, 2013
@Summary:   This module is being phased in and web json is being phased out.

Json is now used for Mqtt messages in addition to web browser.

"""


# Import system type stuff
import jsonpickle

# Import PyMh files


def encode_json(p_obj):
    """Convert a python object to a valid json object.
    """
    try:
        l_json = jsonpickle.encode(p_obj, unpicklable = False, max_depth = 5)
    except (TypeError, ValueError) as l_error:
        print('web_utils.encode_json ERROR {0:}'.format(l_error))
        l_json = u'{}'
    return l_json

def decode_json_unicode(p_json):
    """Convert a json object to a valid object.
    The object keys and values are all encoded in unicode
    """
    try:
        l_json = jsonpickle.decode(p_json)
    except (TypeError, ValueError) as l_error:
        print('web_utils.encode_json ERROR {0:}'.format(l_error))
        l_json = u'{}'
    return l_json

def convert_from_unicode(p_input):
    """Convert unicode strings to python 2.7 strings.
    """
    if isinstance(p_input, dict):
        return {convert_from_unicode(key): convert_from_unicode(value) for key, value in p_input.iteritems()}
    elif isinstance(p_input, list):
        return [convert_from_unicode(element) for element in p_input]
    elif isinstance(p_input, unicode):
        return p_input.encode('ascii')
    else:
        return p_input

# ## END DBK
