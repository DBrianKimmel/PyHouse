"""
@name:      Modules/House/Lighting/actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:   Handle lighting scheduled events.

This module will handle all scheduled events for the Lighting system of a house.

This is so other modules only need to dispatch to here for any lighting event - scene, theme or whatever.

"""

__updated__ = '2019-12-12'

#  Import system type stuff

#  Import PyMh files
from Modules.House.Lighting.utility import lightingUtility
from Modules.House.Lighting.lights import LightData

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightingAction ')


class Api:
    """
    """

    def DoSchedule(self, p_pyhouse_obj, p_schedule_obj):
        """ A schedule action has been called for on a Lighting device

        @param p_pyhouse_obj: The entire data set.
        @param p_schedule_obj: the schedule event being executed.  ==> ScheduleInformation()

        """
        l_light_name = p_schedule_obj.Sched.Name
        l_type = p_schedule_obj.Sched.Type
        l_lighting_objs = p_pyhouse_obj.House.Lighting
        LOG.debug('Lighting type {}'.format(l_type))
        if l_type == 'Light':
            l_obj = l_lighting_objs.Lights
        elif l_type == 'Outlet':
            l_obj = l_lighting_objs.Outlets
        else:
            LOG.error('Schedule type is invalid "{}"'.format(l_type))
            return
        try:
            l_light_obj = lightingUtility().get_object_by_id(l_obj, name=l_light_name)
            l_controller_objs = lightingUtility().get_controller_objs_by_family(l_lighting_objs.Controllers, l_light_obj.Family.Name)
            l_control = LightData()
            l_control.BrightnessPct = p_schedule_obj.Sched.Brightness
            l_control.TransitionTime = p_schedule_obj.Sched.Rate
            if len(l_controller_objs) < 1:
                LOG.warning('No controllers on this server for Light: {}'.format(l_light_obj.Name))
                return
            for l_controller_obj in l_controller_objs:
                if not l_controller_obj._isLocal:
                    continue
                LOG.info("\n\tSchedLightName:{}; Level:{}; LightName:{}; Controller:{}".format(
                        l_light_name, l_control.BrightnessPct, l_light_obj.Name, l_controller_obj.Name))
                self.ControlLight(l_light_obj, l_controller_obj, l_control)
        except Exception as e_err:
            LOG.debug('Something failed {}'.format(e_err))

    def ControlLight(self, p_light_obj, p_controller_obj, p_control):
        """
        @param p_pyhouse_obj: The entire data set.
        @param p_light_obj: the device being controlled
        @param p_controller_obj: ==> ControllerInformation()
        @param p_control: the idealized light control params

        """
        try:
            LOG.info('Turn Light: "{}" to level: "{}", Family: "{}"; Controller: {}'.format(
                    p_light_obj.Name, p_control.BrightnessPct, p_light_obj.Family.Name, p_controller_obj.Name))
            # l_family_api = FamUtil._get_family_device_api(p_pyhouse_obj, p_light_obj)
            l_family_api = p_controller_obj._HandlerApi
            # print(PrettyFormatAny.form(l_family_api.Control, 'Family Api'))
            l_family_api.Control(p_light_obj, p_controller_obj, p_control)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

#  ## END DBK
