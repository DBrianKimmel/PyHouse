"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_thermostats -*-

@name:      PyHouse/src/Modules/Web/web_thermostats.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 1, 2014
@summary:   Handle the Thermostat information for a house.

"""


# Import system type stuff
import os
import uuid
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.Web.web_utils import JsonUnicode, GetJSONHouseInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Families.Insteon import Insteon_utils
from Modules.Utilities.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
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
        # PrettyPrintAny(l_json, "Json")
        return l_json

    @athena.expose
    def saveThermostatsData(self, p_json):
        """Thermostat data is returned, so update the info.
        """
        l_json = JsonUnicode().decode_json(p_json)
        l_delete = l_json['Delete']
        l_ix = int(l_json['Key'])
        if l_delete:
            try:
                del self.m_pyhouse_obj.House.DeviceOBJs.Thermostats[l_ix]
            except AttributeError:
                LOG.error("web_thermostats - Failed to delete - JSON: {0:}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.House.DeviceOBJs.Thermostats[l_ix]
        except KeyError:
            LOG.warning('Creating a new Thermostat for Key:{}'.format(l_ix))
            l_obj = ThermostatData()
        #
        LOG.info('JSON {}'.format(l_json))
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.UUID = l_json['UUID']
        if len(l_obj.UUID) < 8:
            l_obj.UUID = str(uuid.uuid1())
        l_obj.CoolSetPoint = l_json['CoolSetPoint']
        l_obj.ControllerFamily = l_json['ControllerFamily']
        l_obj.CurrentTemperature = 0
        l_obj.HeatSetPoint = l_json['HeatSetPoint']
        l_obj.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        l_obj.ThermostatScale = 'F'  # F | C
        if l_obj.ControllerFamily == 'Insteon':
            Insteon_utils.Util.get_json_data(l_obj, l_json)
        elif l_obj.ControllerFamily == 'UPB':
            l_obj.UPBAddress = l_json['UPBAddress']
            l_obj.UPBPassword = l_json['UPBPassword']
            l_obj.UPBNetworkID = l_json['UPBNetworkID']
        self.m_pyhouse_obj.House.DeviceOBJs.Thermostats[l_ix] = l_obj

# ## END DBK
