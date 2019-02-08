"""
-*- test-case-name: PyHouse.src.Modules.Lighting.test.test_lighting_actions -*-
@name:      PyHouse/src/Modules/Lighting/lighting_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:   Handle lighting scheduled events.

This module will handle all scheduled events for the Lighting system of a house.
This is so other modules only need to dispatch to here for any lighting event - scene, theme or whatever.

"""
#  Import system type stuff

#  Import PyMh files
from Modules.Families.family_utils import FamUtil
from Modules.Housing.Lighting.lighting_utility import Utility
from Modules.Housing.Lighting.lighting_lights import LightData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.LightingAction ')


class API:
    """

2019-02-06 18:12:35,686 [INFO] PyHouse.Schedule       : dispatch_one_schedule 242: - Execute_one_schedule type = Lighting
2019-02-06 18:12:35,688 [DEBUG] PyHouse.LightingAction : DoSchedule 42: -
        SchedName:Evening-00; SchedLightName:LR Rope; Level:100; LightName:LR Rope; LightKey:4
2019-02-06 18:12:35,689 [INFO] PyHouse.LightingAction : AbstractControlLight 55: - Turn Light: "LR Rope" to level: "100", DeviceFamily: "Insteon"
2019-02-06 18:12:35,691 [DEBUG] PyHouse.Insteon_Device : AbstractControlLight 139: - Controlling Insteon device LR Rope using
2019-02-06 18:12:35,692 [ERROR] PyHouse.LightingAction : AbstractControlLight 59: - ERROR - 'API' object is not callable

    """

    def DoSchedule(self, p_pyhouse_obj, p_schedule_obj):
        """ A schedule action has been called for on a Light
        """
        l_lighting_objs = p_pyhouse_obj.House.Lighting

        l_light_obj = Utility()._get_object_by_id(l_lighting_objs.Lights, name=p_schedule_obj.LightName)
        l_controller_objs = Utility().get_controller_objs_by_family(l_lighting_objs.Controllers, l_light_obj.DeviceFamily)
        l_control = LightData()
        l_control.BrightnessPct = p_schedule_obj.Level
        l_control.TransitionTime = p_schedule_obj.Rate
        if len(l_controller_objs) < 1:
            LOG.warn('No controllers on this server for Light: {}'.format(l_light_obj.Name))
            return
        for l_controller_obj in l_controller_objs:
            LOG.info("\n\tSchedLightName:{}; Level:{}; LightName:{}; Controller:{}".format(
                    p_schedule_obj.LightName, l_control.BrightnessPct, l_light_obj.Name, l_controller_obj.Name))
            self.AbstractControlLight(p_pyhouse_obj, l_light_obj, l_controller_obj, l_control)
        # p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_schedule_obj)

    def AbstractControlLight(self, p_pyhouse_obj, p_light_obj, p_controller_obj, p_control):
        """
        @param p_pyhouse_obj: The entire data set.
        @param p_light_obj: the device being controlled
        @param p_controller_obj: ControllerData()
        @param p_control: the idealized light control params

        """
        try:
            LOG.info('Turn Light: "{}" to level: "{}", Family: "{}"; Controller: {}'.format(
                    p_light_obj.Name, p_control.BrightnessPct, p_light_obj.DeviceFamily, p_controller_obj.Name))
            l_family_api = FamUtil._get_family_device_api(p_pyhouse_obj, p_light_obj)
            l_family_api(p_pyhouse_obj).AbstractControlLight(p_light_obj, p_controller_obj, p_control)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

#  ## END DBK
