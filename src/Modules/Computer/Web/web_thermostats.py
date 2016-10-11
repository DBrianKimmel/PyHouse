"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_thermostats -*-

@name:      PyHouse/src/Modules/Web/web_thermostats.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 1, 2014
@summary:   Handle the Thermostat information for a house.

"""

__updated__ = '2016-10-10'

#  Import system type stuff
import os
from nevow import athena
from nevow import loaders

#  Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.Computer.Web.web_utils import GetJSONHouseInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils
from Modules.Utilities import json_tools

#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webThermost ')



class ThermostatsElement(athena.LiveElement):
    """ a 'live' thermostat element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'thermostatElement.html'))
    jsClass = u'thermostats.ThermostatsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHouseData(self):
        l_json = GetJSONHouseInfo(self.m_pyhouse_obj)
        return l_json

    @athena.expose
    def saveThermostatsData(self, p_json):
        """Thermostat data is returned, so update the info.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_delete = l_json['Delete']
        l_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.Hvac.Thermostats[l_ix]
            except AttributeError:
                LOG.error("web_thermostats - Failed to delete - JSON: {}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.House.Hvac.Thermostats[l_ix]
        except KeyError:
            LOG.warning('Creating a new Thermostat for Key:{}'.format(l_ix))
            l_obj = ThermostatData()
        #
        LOG.info('JSON {}'.format(l_json))
        l_obj.Active = l_json['Active']
        l_obj.Comment = l_json['Comment']
        l_obj.CoolSetPoint = l_json['CoolSetPoint']
        l_obj.CurrentTemperature = 0
        l_obj.DeviceFamily = l_json['DeviceFamily']
        l_obj.DeviceSubType = 1
        l_obj.DeviceType = 2
        l_obj.HeatSetPoint = l_json['HeatSetPoint']
        l_obj.Key = l_ix
        l_obj.Name = l_json['Name']
        l_obj.RoomCoords = [0.0, 0.0, 0.0]
        l_obj.RoomName = l_json['RoomName']
        l_obj.ThermostatMode = 'Cool'  #  Cool | Heat | Auto | EHeat
        l_obj.ThermostatScale = 'F'  #  F | C
        l_obj.ThermostatStatus = 'Off'
        l_obj.UUID = l_json['UUID']
        if l_obj.DeviceFamily == 'Insteon':
            Insteon_utils.Util.get_json_data(l_obj, l_json)
        elif l_obj.DeviceFamily == 'UPB':
            l_obj.UPBAddress = l_json['UPBAddress']
            l_obj.UPBPassword = l_json['UPBPassword']
            l_obj.UPBNetworkID = l_json['UPBNetworkID']
        self.m_pyhouse_obj.House.Hvac.Thermostats[l_ix] = l_obj  #  Put into internal data store

#  ## END DBK
