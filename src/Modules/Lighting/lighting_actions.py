"""
-*- test-case-name: PyHouse.src.Modules.Lighting.test.test_lighting_actions -*-
@name:      PyHouse/src/Modules/Lighting/lighting_actions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:   Handle lighting scheduled events.

This module will handle all scheduled events for the Lighting system of a house.
This is so other modules only need to dispatch to here for any lighting event - scene, theme or whatever.

"""

#  Import system type stuff

#  Import PyMh files
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities import tools, json_tools

LOG = Logger.getLogger('PyHouse.LightAction    ')

SECONDS_IN_WEEK = 604800  #  7 * 24 * 60 * 60


class Utility(object):
    """
    """

    @staticmethod
    def _find_full_obj(p_pyhouse_obj, p_web_obj):
        """ Given the limited information from the web browser, look up and return the full object.
        If more than one device has the same name, return the first one found.
        """
        for l_light in p_pyhouse_obj.House.Lighting.Lights.itervalues():
            if p_web_obj.Name == l_light.Name:
                return l_light
        LOG.error('ERROR - no light with name {} was found.'.format(p_web_obj.Name))
        return None

    @staticmethod
    def get_light_object(p_pyhouse_obj, name = None, key = None):
        """ Return the light object for a house using the given value.
        Either a name or a key may be used to identify the light.

        TODO: switch from key to UUID.
        Add other devices

        @return: the Light object found or None.
        """
        l_lights = p_pyhouse_obj.House.Lighting.Lights
        if name != None:
            for l_obj in l_lights.itervalues():
                if l_obj.Name == name:
                    return l_obj
            LOG.error('Using Name:{} - lookup failed'.format(name))
        elif key != None:
            for l_obj in l_lights.itervalues():
                if l_obj.Key == key:
                    return l_obj
            LOG.error('Using Key:{} - lookup failed'.format(key))
        LOG.error('Lookup failed - arg error Name:{}, Key:{}'.format(name, key))
        return None


class API(object):
    """
    """

    @staticmethod
    def DoSchedule(p_pyhouse_obj, p_schedule_obj):
        """
        """
        l_light_obj = Utility.get_light_object(p_pyhouse_obj, name = p_schedule_obj.LightName)
        LOG.info("Name:{}, Light:{}, Level:{}  {}  {}".format(p_schedule_obj.Name, p_schedule_obj.LightName,
                p_schedule_obj.Level, l_light_obj.Name, l_light_obj.Key))
        API.ChangeLight(p_pyhouse_obj, l_light_obj, 'shedule', p_schedule_obj.Level)
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("schedule/execute", p_schedule_obj)

    @staticmethod
    def ChangeLight(p_pyhouse_obj, p_light_obj, p_source, p_new_level, _p_rate = None):
        """ Set a light to a value - On, Off, or Dimmed.
        Called by:
            web_controlLights
            schedule
            @param p_pyhouse_obj: The entire data set.
            @param p_light_obj: is the partial obj of the particular light we are changing
            @param p_source: is a string denoting the source of the change.
            @param p_new_level: is the percent of light we are changing to
            @param p_rate: is the rate the change will ramp to.
        """
        l_light_obj = Utility.get_light_object(p_pyhouse_obj, name = p_light_obj.Name)  #  web has some info missing - get all the object
        try:
            LOG.info('Turn Light: "{}" to level: "{}", DeviceFamily: "{}"'.format(l_light_obj.Name, p_new_level, l_light_obj.DeviceFamily))
            l_family_api = FamUtil._get_family_device_api(p_pyhouse_obj, l_light_obj)
            l_family_api.ChangeLight(l_light_obj, p_source, p_new_level)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

#  ## END DBK
