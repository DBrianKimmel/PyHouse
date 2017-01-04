"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_Security.py -*-

@name:      /home/briank/PyHouse/src/Modules/Families/Insteon/Insteon_Security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Nov 2, 2016
@license:   MIT License
@summary:

"""
from Modules.Families.Insteon.Insteon_constants import MESSAGE_TYPES

__updated__ = '2017-01-04'

#  Import system type stuff

#  Import PyMh files
from Modules.Families.Insteon.Insteon_utils import Decode as utilDecode
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Secure ')


class DecodeResponses(object):

    m_pyhouse_obj = None
    m_idex = 0

    def decode_50(self, p_pyhouse_obj, p_device_obj, p_controller_obj):
        """
        @param p_device_obj: is the Device (GDO, Motion...) we are decoding.

        A Standard-length INSTEON message is received from either a Controller or Responder that you are ALL-Linked to.
        See p 233(246) of 2009 developers guide.
        [0] = x02
        [1] = 0x50
        [2-4] = from address
        [5-7] = to address / group
        [8] = message flags
        [9] = command 1
        [10] = command 2
        """
        l_mqtt_topic = 'security/'
        l_mqtt_msg = 'security '
        if p_device_obj.DeviceSubType == 1:
            l_mqtt_msg += 'Garage Door: '
            l_mqtt_topic += 'garage_door'
        elif p_device_obj.DeviceSubType == 2:
            l_mqtt_msg += 'Motion Sensor: '
            l_mqtt_topic += 'motion_sensor'
        l_mqtt_topic += '/{}'.format(p_device_obj.Name)
        #
        l_message = p_controller_obj._Message
        l_firmware = l_message[7]
        _l_flags = utilDecode._decode_message_flag(l_message[8])
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_mqtt_msg += ' Cmd1/2:{:#02X}/{:#02X} ({:d})'.format(l_cmd1, l_cmd2, l_cmd2)

        if l_cmd1 == MESSAGE_TYPES['engine_version']:  #  0x0D
            p_device_obj.EngineVersion = l_cmd2
            l_mqtt_msg += 'Engine-version:"{}"; '.format(l_cmd2)
            # self._publish(self.m_pyhouse_obj, l_device_obj)

        elif l_cmd1 == MESSAGE_TYPES['id_request']:  #  0x10
            p_device_obj.FirmwareVersion = l_firmware
            l_mqtt_msg += 'Request-ID-From:"{}"; '.format(p_device_obj.Name)

        LOG.info('Security {}'.format(l_mqtt_msg))
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_mqtt_topic, p_device_obj)  #  /security
        return

# ## END DBK
