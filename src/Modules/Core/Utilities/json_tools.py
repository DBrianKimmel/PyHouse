"""
-*- test-case-name: PyHouse.src.Modules.Core.Utilities.test.test_json_tools -*-

@name:      PyHouse/src/Modules.Core.Utilities.json_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 6, 2013
@Summary:   This module is being phased in and web json is being phased out.

Json is now used for Mqtt messages in addition to web browser.

"""
from Modules.Core.Utilities.debug_tools import FormatBytes

__updated__ = '2017-04-30'


# Import system type stuff
import jsonpickle

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Json_Tools     ')


def encode_json(p_obj):
    """Convert a python object to a valid json object.
    """
    try:
        l_json = jsonpickle.encode(p_obj, unpicklable=False, max_depth=5)
    except (TypeError, ValueError) as l_error:
        LOG.error('ERROR encode_json{}'.format(l_error))
        l_json = u'{}'
    return l_json

def decode_json_unicode(p_json):
    """Convert a json object to a valid python object.
    The object keys and values are all encoded in unicode
    """
    # l_json = convert_from_unicode(p_json)
    try:
        l_json = jsonpickle.decode(p_json)
    except (TypeError, ValueError) as e_err:
        LOG.error('ERROR {}  {}'.format(e_err, FormatBytes(p_json)[:30]))
        l_json = u'{}'
    return l_json

def convert_from_unicode(p_input):
    """Convert unicode strings to python 2.7 strings.
    """
    if isinstance(p_input, dict):
        return {convert_from_unicode(key): convert_from_unicode(value) for key, value in p_input.items()}
    elif isinstance(p_input, list):
        return [convert_from_unicode(element) for element in p_input]
    elif isinstance(p_input, type('utf-8')):
        return p_input.encode('ascii')
    else:
        return p_input

# ## END DBK
