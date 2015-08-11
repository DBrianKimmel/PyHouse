"""
-*- test-case-name: PyHouse.src.Modules.families.UPB.test.test_UPB_device -*-

@name:      PyHouse/src/Modules/families/UPB/UPB_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2011
@summary:   This module is for communicating with UPB controllers.

Load the database with UPB devices.
Start Active UPB Controllers.
    If more than one ???

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.UPB.UPB_Pim import API as upbPimAPI
from Modules.Computer.Mqtt.mqtt_client import API as mqttAPI
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UPB_device     ')


class Utility(object):

    @staticmethod
    def _is_upb_active(p_controller_obj):
        if p_controller_obj.DeviceFamily != 'UPB':
            return False
        if p_controller_obj.Active:
            return True


class API(object):

    def __init__(self, p_pyhouse_obj):
        """Constructor for the UPB.
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        """For the given house, this will start all the controllers for family = UPB in that house.
        """
        l_count = 0
        for l_controller_obj in self.m_pyhouse_obj.House.Controllers.itervalues():
            if Utility._is_upb_active(l_controller_obj):
                l_controller_prefix = 'lighting/controller/{}'.format(l_controller_obj.Name)
                l_controller_obj._HandlerAPI = upbPimAPI(self.m_pyhouse_obj)
                if l_controller_obj._HandlerAPI.Start(self.m_pyhouse_obj, l_controller_obj):
                    LOG.info('Controller {} Started.'.format(l_controller_obj.Name))
                    l_count += 1
                    l_topic = l_controller_prefix + '/start'
                    l_message = ''
                    # mqttAPI(self.m_pyhouse_obj).MqttPublish(l_topic, l_message)
                    self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_message)
                else:
                    LOG.error('Controller {} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        LOG.info('Started {} UPB Controllers.'.format(l_count))

    def Stop(self):
        try:
            for l_controller_obj in self.m_pyhouse_obj.House.Controllers.itervalues():
                if Utility._is_upb_active(l_controller_obj):
                    l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError as e_err:
            LOG.error('Stop ERROR {}'.format(e_err))

    def SaveXml(self, p_xml):
        """
        Not needed since the xml is taken care as a part of the device.
        """
        return p_xml

    def ChangeLight(self, p_light_obj, p_source, p_level, _p_rate = 0):
        LOG.debug('Change light Name:{}, DeviceFamily:{}'.format(p_light_obj.Name, p_light_obj.DeviceFamily))
        self.m_plm.ChangeLight(p_light_obj, p_source, p_level)

# ## END
