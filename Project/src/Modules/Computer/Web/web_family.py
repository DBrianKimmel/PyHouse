"""
@name:      Modules/Computer/Web/web_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2020 by D. Brian Kimmel
@note:      Created on Nov 8, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2020-01-05'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webFamily   ')


def _get_insteon_json_data(p_obj, p_json):
    try:
        p_obj.Address = int(p_json['InsteonAddress'])
    except:
        p_obj.Address = 17
    try:
        p_obj.GroupList = p_json['GroupList']
    except:
        p_obj.GroupList = 'Bad insteon_utils.get_json_data()'
    try:
        p_obj.GroupNumber = p_json['GroupNumber']
    except:
        p_obj.GroupNumber = 0
    try:
        p_obj.ProductKey = int(p_json['ProductKey'])
    except:
        p_obj.ProductKey = 0
    try:
        p_obj.EngineVersion = int(p_json['EngineVersion'])
        p_obj.FirmwareVersion = int(p_json['FirmwareVersion'])
    except:
        p_obj.EngineVersion = 0
        p_obj.FirmwareVersion = 0
    return p_obj


def _get_upb_json_data(p_obj, p_json):
    p_obj.UPBAddress = p_json['UPBAddress']
    p_obj.UPBPassword = p_json['UPBPassword']
    p_obj.UPBNetworkID = p_json['UPBNetworkID']
    return p_obj


def get_family_json_data(p_obj, p_json):
    if p_obj.DeviceFamily == 'Insteon':
        _get_insteon_json_data(p_obj, p_json)
    elif p_obj.DeviceFamily == 'UPB':
        _get_upb_json_data(p_obj, p_json)
    else:
        LOG.error('Invalid Family :{}.'.format(p_obj.DeviceFamily))
    return p_obj

# ## END DBK
