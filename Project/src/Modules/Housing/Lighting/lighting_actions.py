"""
-*- test-case-name: PyHouse.src.Modules.Lighting.test.test_lighting_actions -*-
@name:      PyHouse/Project/src/Modules/Lighting/lighting_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:   Handle lighting scheduled events.

This module will handle all scheduled events for the Lighting system of a house.

This is so other modules only need to dispatch to here for any lighting event - scene, theme or whatever.

"""

__updated__ = '2019-07-22'

#  Import system type stuff

#  Import PyMh files
from Modules.Families.family_utils import FamUtil
from Modules.Housing.Lighting.lighting_utility import Utility
from Modules.Housing.Lighting.lighting_lights import LightData
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightingAction ')


class API:
    """
    """

    def DoSchedule(self, p_pyhouse_obj, p_schedule_obj):
        """ A schedule action has been called for on a Light

        @param p_pyhouse_obj: The entire data set.
        @param p_schedule_obj: the schedule event being executed.

        """
        l_light_name = p_schedule_obj.LightName
        l_lighting_objs = p_pyhouse_obj.House.Lighting
        l_light_obj = Utility().get_object_by_id(l_lighting_objs.Lights, name=l_light_name)
        #
        l_controller_objs = Utility().get_controller_objs_by_family(l_lighting_objs.Controllers, l_light_obj.Family.Name)
        l_control = LightData()
        l_control.BrightnessPct = p_schedule_obj.Level
        l_control.TransitionTime = p_schedule_obj.Rate
        if len(l_controller_objs) < 1:
            LOG.warn('No controllers on this server for Light: {}'.format(l_light_obj.Name))
            return
        for l_controller_obj in l_controller_objs:
            if not l_controller_obj.Active:
                continue
            LOG.info("\n\tSchedLightName:{}; Level:{}; LightName:{}; Controller:{}".format(
                    l_light_name, l_control.BrightnessPct, l_light_obj.Name, l_controller_obj.Name))
            self.ControlLight(p_pyhouse_obj, l_light_obj, l_controller_obj, l_control)

    def ControlLight(self, p_pyhouse_obj, p_light_obj, p_controller_obj, p_control):
        """
        @param p_pyhouse_obj: The entire data set.
        @param p_light_obj: the device being controlled
        @param p_controller_obj: ControllerInformation()
        @param p_control: the idealized light control params

        """
        try:
            LOG.info('Turn Light: "{}" to level: "{}", Family: "{}"; Controller: {}'.format(
                    p_light_obj.Name, p_control.BrightnessPct, p_light_obj.Family.Name, p_controller_obj.Name))
            l_family_api = FamUtil._get_family_device_api(p_pyhouse_obj, p_light_obj)
            # print(PrettyFormatAny.form(l_family_api.AbstractControlLight, 'Family API'))
            l_family_api.AbstractControlLight(p_pyhouse_obj, p_light_obj, p_controller_obj, p_control)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

#  ## END DBK
