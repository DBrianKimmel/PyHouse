"""
@name:      Modules/families/UPB/UPB_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2011
@summary:   This module is for communicating with UPB controllers.

Load the database with UPB devices.
Start Active UPB Controllers.
    If more than one ???

"""

__updated__ = '2019-12-30'

# Import system type stuff

# Import PyMh files
from Modules.Families.UPB.UPB_Pim import Api as upbPimApi
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UPB_device     ')


class lightingUtility(object):

    @staticmethod
    def _is_upb_active(p_controller_obj):
        if p_controller_obj.Family.Name != 'UPB':
            return False
        # if p_controller_obj.Active:
        #    return True


class Api(object):

    def __init__(self, p_pyhouse_obj):
        """Constructor for the UPB.
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        """For the given house, this will start all the controllers for family = UPB in that house.
        """
        l_count = 0
        for l_controller_obj in self.m_pyhouse_obj.House.Lighting.Controllers.values():
            if lightingUtility._is_upb_active(l_controller_obj):
                l_controller_prefix = 'house/lighting/controller/{}'.format(l_controller_obj.Name)
                l_controller_obj._HandlerApi = upbPimApi(self.m_pyhouse_obj)
                if l_controller_obj._HandlerApi.Start(self.m_pyhouse_obj, l_controller_obj):
                    LOG.info('Controller {} Started.'.format(l_controller_obj.Name))
                    l_count += 1
                    # l_topic = 'house/lighting/controller/' + l_controller_prefix + '/start'
                    # self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_controller_obj)  # /start
                else:
                    LOG.error('Controller {} failed to start.'.format(l_controller_obj.Name))
                    # l_controller_obj.Active = False
        LOG.info('Started {} UPB Controllers.'.format(l_count))

    def Stop(self):
        try:
            for l_controller_obj in self.m_pyhouse_obj.House.Lighting.Controllers.values():
                if lightingUtility._is_upb_active(l_controller_obj):
                    l_controller_obj._HandlerApi.Stop(l_controller_obj)
        except AttributeError as e_err:
            LOG.error('Stop ERROR {}'.format(e_err))

    def SaveXml(self, p_xml):
        """
        Not needed since the xml is taken care as a part of the device.
        """
        return p_xml

    def Control(self, p_device_obj, p_controller_obj, p_control):
        LOG.debug('Change light Name:{}, Family.Name:{}'.format(p_light_obj.Name, p_light_obj.Family.Name))
        self.m_plm.Control(p_light_obj, p_source, p_level)

# ## END
