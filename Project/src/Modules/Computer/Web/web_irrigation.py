"""
-*- _test-case-name: PyHouse/src/Modules/Computer/Web/web_irrigation.py -*-

@name:      Modules/Computer/Web/web_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@note:      Created on Aug 22, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2019-07-30'

# Import system type stuff
import os

# Import PyMh files and modules.
from Modules.Core.data_objects import IrrigationData
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Core.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.WebIrrigation  ')


class IrrigationElement(athena.LiveElement):
    """ a 'live' internet element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'irrigationElement.html'))
    jsClass = u'irrigation.IrrigationWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_computer = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_computer

    @athena.expose
    def saveIrrigationData(self, p_json):
        """Internet data is returned, so update the computer info.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_ix = int(l_json['Key'])
        _l_system = l_json['Name']
        try:
            l_obj = self.m_pyhouse_obj.House.Irrigation[l_ix]
        except KeyError:
            l_obj = IrrigationData()
            l_obj.DynDns = {}
        l_obj.Name = l_json['Name']
        l_obj.Key = 0
        l_obj.Active = True
        self.m_pyhouse_obj.House.Irrigation[l_ix] = l_obj

# ## END DBK
