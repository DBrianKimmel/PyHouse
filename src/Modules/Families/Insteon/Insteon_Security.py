"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_Security.py -*-

@name:      /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_Security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Nov 2, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-11-02'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_decode ')


class DecodeResponses(object):

    m_pyhouse_obj = None
    m_idex = 0

    def decode_50(self, p_pyhouse_obj, p_device_obj, p_controller_obj):
        """
        @param p_device_obj: is the Device (light, thermostat...) we are decoding.
        """
        l_mqtt_topic = 'hvac/{}'.format(p_device_obj.Name)
        l_mqtt_message = "Thermostat: "
        l_message = p_controller_obj._Message
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_mqtt_message += ' Command1: {:#X},  Command2:{:#X}({:d})'.format(l_cmd1, l_cmd2, l_cmd2)
        LOG.info('Security {}'.format(l_mqtt_message))
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_mqtt_topic, p_device_obj)  #  /temperature
        return

# ## END DBK
