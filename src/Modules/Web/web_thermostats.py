"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_thermostats -*-

@name: PyHouse/src/Modules/Web/web_thermostats.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 1, 2014
@summary: Handle the Thermostat information for a house.

"""


# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Web.web_utils import JsonUnicode
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webThermost ')


class ThermostatsElement(athena.LiveElement):
    """ a 'live' internet element.
    """
    # print('ThermostatElement')
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'thermostatElement.html'))
    jsClass = u'thermostats.ThermostatsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        # print('thermostat.ThermostatElement.__init__()')

    @athena.expose
    def getHouseData(self):
        # print('thermostat.ThermostatElement.getHouseData')
        l_computer = JsonUnicode().encode_json(self.m_pyhouse_obj.House.OBJs.Thermostats)
        return l_computer

    @athena.expose
    def saveThermostatsData(self, p_json):
        """Thermostat data is returned, so update the computer info.
        """
        # print('thermostat.saveThermostatData')
        l_json = JsonUnicode().decode_json(p_json)
        print('JSON: {}'.format(l_json))

# ## END DBK
