"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Computer/Web/web_family.py -*-

@name:      /home/briank/PyHouse/src/Modules/Computer/Web/web_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Nov 8, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-11-08'


def _get_insteon_json_data(p_obj, p_json):
    try:
        p_obj.DevCat = int(p_json['DevCat'])
    except KeyError:
        p_obj.DevCat = 0
    try:
        p_obj.GroupList = p_json['GroupList']
    except KeyError:
        p_obj.GroupList = 'Bad insteon_utils.get_json_data()'
    try:
        p_obj.GroupNumber = p_json['GroupNumber']
    except KeyError:
        p_obj.GroupNumber = 0
    try:
        p_obj.InsteonAddress = int(p_json['InsteonAddress'])
    except KeyError:
        p_obj.InsteonAddress = 1
    try:
        p_obj.ProductKey = int(p_json['ProductKey'])
    except KeyError:
        p_obj.ProductKey = 0
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

# ## END DBK
