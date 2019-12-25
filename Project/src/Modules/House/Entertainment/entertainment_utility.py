"""
@name:      /home/briank/workspace/PyHouse/Project/src/Modules/House/Entertainment/entertainment_util.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 23, 2019
@summary:

"""

#  Import system type stuff
from ruamel.yaml.comments import CommentedSeq, CommentedMap

#  Import PyMh files and modules.

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.EntertainConfig')


def _extract_list(p_config):
    """
    """
    l_list = []
    for l_value in p_config:
        l_list.append(l_value)
    return l_list


def extract_device_config_file(p_config):
    """
    """
    l_dict = {}
    for l_key, l_value in p_config.items():
        # LOG.debug('Key: "{}"\tType: {}'.format(l_key, type(l_value)))
        if isinstance(l_value, (int, str)):
            l_scalar = l_value
            l_dict[l_key] = l_scalar
        if isinstance(l_value, CommentedSeq):
            l_list = '**List**'  # self._extract_model_config_list(l_value)
            # l_dict[l_key] = l_list
            l_dict[l_key] = _extract_list(l_value)
        elif isinstance(l_value, CommentedMap):
            l_map = 'Mapping'  # self._extract_model_config_key(l_value)
            l_dict[l_key] = extract_device_config_file(l_value)
        else:
            # l_dict[l_key] = '** DBK Unknown type **: {}   {}'.format(type(l_value), l_value)
            l_dict[l_key] = l_value
    # LOG.debug(PrettyFormatAny.form(l_dict, 'extract key/Val'))
    return l_dict


def extract_zone(p_config):
    """ Zone is an output area.
    Each zone has a set of speakers that are driven by an A/V device.

    Zones:
        0: Main
        1: Lanai
    """
    l_required = ['Name', 'Type', 'Host']
    l_obj = {}
    for l_key, l_value in p_config.items():
        setattr(l_obj, l_key, l_value)
    return l_obj  # For testing.

# ## END DBK
