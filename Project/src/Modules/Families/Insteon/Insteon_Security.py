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

__updated__ = '2019-06-24'

#  Import system type stuff

#  Import PyMh files
from Modules.Families.Insteon import Insteon_utils
from Modules.Families.Insteon.Insteon_utils import Decode as utilDecode
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Secure ')


class SensorMessage(object):
    """ This is what will be sent in the mqtt message.
    """

    def __init__(self, p_name, p_room, p_type):
        self.Name = p_name
        self.RoomName = p_room
        self.Type = p_type
        self.Status = None


class DecodeResponses(object):

    m_idex = 0

    def decode_0x50(self, p_pyhouse_obj, p_device_obj, p_controller_obj):
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
        l_message = p_controller_obj._Message

        l_device = SensorMessage(p_device_obj.Name, p_device_obj.RoomName, 'Generic ')
        l_topic = 'houe/security/'
        l_mqtt_msg = 'security '
        if p_device_obj.DeviceSubType == 1:
            l_mqtt_msg += 'Garage Door: '
            l_device.Type = 'Garage Door'
            l_topic += 'garage_door'
        elif p_device_obj.DeviceSubType == 2:
            l_mqtt_msg += 'Motion Sensor: '
            l_device.Type = 'Motion Sensor'
            l_topic += 'motion_sensor'
        #
        l_firmware = l_message[7]
        l_flags = utilDecode._decode_message_flag(l_message[8])
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_data = [l_cmd1, l_cmd2]
        l_mqtt_msg += 'Fm:"{}"; Flg:{}; C1:{:#x},{:#x}; '.format(p_device_obj.Name, l_flags, l_cmd1, l_cmd2)

        if l_message[8] & 0xE0 == 0x80:  #  100 - SB [Broadcast]
            l_mqtt_msg += utilDecode._devcat(l_message[5:7], p_device_obj)
        elif l_message[8] & 0xE0 == 0xC0:  #  110 - SA Broadcast = all link broadcast of group id
            l_group = l_message[7]
            l_mqtt_msg += 'A-L-brdcst-Gp:"{}","{}"; '.format(l_group, l_data)

        if l_cmd1 == MESSAGE_TYPES['cleanup_success']:  #  0x06
            l_mqtt_msg += 'CleanupSuccess with {} failures; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['engine_version']:  #  0x0D
            p_device_obj.EngineVersion = l_cmd2
            l_mqtt_msg += 'Engine-version:"{}"; '.format(l_cmd2)
        elif l_cmd1 == MESSAGE_TYPES['id_request']:  #  0x10
            p_device_obj.FirmwareVersion = l_firmware
            l_mqtt_msg += 'Request-ID-From:"{}"; '.format(p_device_obj.Name)

        elif l_cmd1 == MESSAGE_TYPES['on']:  #  0x11
            if p_device_obj.DeviceSubType == 1:  # The status turns on when the Garage Door goes closed
                l_mqtt_msg += 'Garage Door Closed; '.format(p_device_obj.Name)
                p_device_obj.Status = 'Close'
                l_device.Status = 'Garage Door Closed.'
            elif p_device_obj.DeviceSubType == 2:
                l_mqtt_msg += 'Motion Detected; '.format(p_device_obj.Name)
                l_device.Status = 'Motion Detected.'
            else:
                l_mqtt_msg += 'Unknown SubType {} for Device; '.format(p_device_obj.DeviceSubType, p_device_obj.Name)
            if ((l_message[8] & 0xE0) >> 5) == 6:
                p_pyhouse_obj._APIs.Computer.MqttAPI.MqttPublish(l_topic, l_device)  #  /security

        elif l_cmd1 == MESSAGE_TYPES['off']:  #  0x13
            if p_device_obj.DeviceSubType == 1:
                l_mqtt_msg += 'Garage Door Opened; '.format(p_device_obj.Name)
                p_device_obj.Status = 'Opened'
                l_device.Status = 'Garage Door Opened.'
            elif p_device_obj.DeviceSubType == 2:
                l_mqtt_msg += 'NO Motion; '.format(p_device_obj.Name)
                l_device.Status = 'Motion Stopped.'
            else:
                l_mqtt_msg += 'Unknown SubType {} for Device; '.format(p_device_obj.DeviceSubType, p_device_obj.Name)
            if ((l_message[8] & 0xE0) >> 5) == 6:
                p_pyhouse_obj._APIs.Computer.MqttAPI.MqttPublish(l_topic, l_device)  #  /security

        LOG.info('Security {}'.format(l_mqtt_msg))
        Insteon_utils.update_insteon_obj(p_pyhouse_obj, p_device_obj)
        return

# ## END DBK
