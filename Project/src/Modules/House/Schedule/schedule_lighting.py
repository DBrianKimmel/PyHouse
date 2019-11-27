"""
@name:      Modules/House/Schedules/schedule_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 13, 2019
@summary:   Schedule events

"""

__updated__ = '2019-11-26'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.House.Family.family_utils import FamUtil
from Modules.House.Lighting.lighting_utility import lightingUtility
from Modules.House.Lighting.lighting_lights import LightData

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Schedule_lightn')


class Api():

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, _p_pyhouse_obj):
        """ Load the Schedule from the XML info.
        """
        LOG.info('Loaded Schedules XML')

    def Start(self):
        """
        Extracts all from XML so an update will write correct info back out to the XML file.
        """
        LOG.info("Started.")

    def Stop(self):
        """Stop everything.
        """
        LOG.info("Stopped.")

    def SaveXml(self, _p_xml):
        """
        """
        LOG.info('Saved Schedules XML.')

    def DoSchedule(self, p_pyhouse_obj, p_schedule_obj):
        """ A schedule action has been called for on a Light

        @param p_pyhouse_obj: The entire data set.
        @param p_schedule_obj: the schedule event being executed.

        """
        l_light_name = p_schedule_obj.LightName
        l_lighting_objs = p_pyhouse_obj.House.Lighting
        l_light_obj = lightingUtility().get_object_by_id(l_lighting_objs.Lights, name=l_light_name)
        #
        l_controller_objs = lightingUtility().get_controller_objs_by_family(l_lighting_objs.Controllers, l_light_obj.Family.Name)
        l_control = LightData()
        l_control.BrightnessPct = p_schedule_obj.Level
        l_control.TransitionTime = p_schedule_obj.Rate
        if len(l_controller_objs) < 1:
            LOG.warn('No controllers on this server for Light: {}'.format(l_light_obj.Name))
            return
        for l_controller_obj in l_controller_objs:
            # if not l_controller_obj.Active:
            #    continue
            LOG.info("\n\tSchedLightName:{}; Level:{}; LightName:{}; Controller:{}".format(
                    l_light_name, l_control.BrightnessPct, l_light_obj.Name, l_controller_obj.Name))
            self.ControlLight(p_pyhouse_obj, l_light_obj, l_controller_obj, l_control)

    def ControlLight(self, p_pyhouse_obj, p_light_obj, p_controller_obj, p_control):
        """
        @param p_pyhouse_obj: The entire data set.
        @param p_light_obj: the device being controlled
        @param p_controller_obj: ==> ControllerInformation()
        @param p_control: the idealized light control params

        """
        try:
            LOG.info('Turn Light: "{}" to level: "{}", Family: "{}"; Controller: {}'.format(
                    p_light_obj.Name, p_control.BrightnessPct, p_light_obj.Family.Name, p_controller_obj.Name))
            l_family_api = FamUtil._get_family_device_api(p_pyhouse_obj, p_light_obj)
            # print(PrettyFormatAny.form(l_family_api.Control, 'Family Api'))
            l_family_api.Control(p_light_obj, p_controller_obj, p_control)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

# ## END DBK
