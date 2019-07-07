"""
-*- test-case-name: PyHouse/Project/src/Modules/Families/Insteon/Insteon_Light.py -*-

@name:      PyHouse/Project/src/Modules/Families/Insteon/Insteon_Light.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Dec 4, 2018
@license:   MIT License
@summary:

We get these only if a controller is attached.

"""

__updated__ = '2019-07-07'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Families.Insteon import Insteon_utils
from Modules.Families.Insteon.Insteon_constants import MESSAGE_TYPES
from Modules.Families.Insteon.Insteon_utils import Decode as utilDecode

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Light  ')


class InsteonLightStatus:

    def __init__(self):
        self.Name = None
        self.Family = 'Insteon'
        self.Type = 1  # 1 = Lighting
        self.SubType = 1  # 1 = Button
        self.BrightnessPct = None
        self.RoomName = None


class DecodeResponses:

    def decode_0x50(self, p_pyhouse_obj, p_controller_obj, p_device_obj):
        """
        There are 2 types of responses here.
        One is from a request for information from the light type device.
        The other is a change of status from a light type device.

        @param p_controller_obj: is the controller that received the message
        @param p_device_obj: is

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

        l_mqtt_publish = False
        p_device_obj.BrightnessPct = '?'
        p_device_obj.ControllerNode = p_pyhouse_obj.Computer.Name
        p_device_obj.ControllerName = p_controller_obj.Name
        l_flags = utilDecode._decode_message_flag(l_message[8])
        l_cmd1 = l_message[9]
        l_cmd2 = l_message[10]
        l_data = [l_cmd1, l_cmd2]
        l_debug_msg = 'Fm:"{}"; Flg:{}; C1:{:#x},{:#x}; '.format(p_device_obj.Name, l_flags, l_cmd1, l_cmd2)
        #
        #  Break down bits 7(msb), 6, 5 into message type
        #
        if l_message[8] & 0xE0 == 0x80:  #  100 - SB [Broadcast]
            l_debug_msg += utilDecode._devcat(l_message[5:7], p_device_obj)
        elif l_message[8] & 0xE0 == 0xC0:  #  110 - SA Broadcast = all link broadcast of group id
            l_group = l_message[7]
            l_debug_msg += 'A-L-brdcst-Gp:"{}","{}"; '.format(l_group, l_data)
        try:
            # Query responses
            if l_cmd1 == MESSAGE_TYPES['assign_to_group'] and l_message[8] & 0xE0 == 0x80:  # 0x01
                l_debug_msg += ' Device-Set-Button-Pressed '
            elif l_cmd1 == MESSAGE_TYPES['delete_from_group'] and l_message[8] & 0xE0 == 0x80:  # 0x02
                l_debug_msg += ' Controller-Set-Button-Pressed '
            elif l_cmd1 == MESSAGE_TYPES['product_data_request']:  #  0x03
                l_debug_msg += " Product-data-request."
            elif l_cmd1 == MESSAGE_TYPES['cleanup_success']:  #  0x06
                l_debug_msg += 'CleanupSuccess with {} failures; '.format(l_cmd2)
            elif l_cmd1 == MESSAGE_TYPES['engine_version']:  #  0x0D
                p_device_obj.EngineVersion = l_cmd2
                l_debug_msg += 'Engine-version:"{}(i-{})"; '.format(l_cmd2, l_cmd2 + 1)
            elif l_cmd1 == MESSAGE_TYPES['id_request']:  #  0x10
                p_device_obj.FirmwareVersion = l_cmd2
                l_debug_msg += 'Request-ID:"{}"; '.format(p_device_obj.FirmwareVersion)

            elif l_cmd1 == MESSAGE_TYPES['on']:  #  0x11
                p_device_obj.BrightnessPct = 100
                l_mqtt_publish = True
                l_debug_msg += 'Turn ON; '.format(p_device_obj.Name)
            elif l_cmd1 == MESSAGE_TYPES['off']:  #  0x13
                p_device_obj.BrightnessPct = 0
                l_mqtt_publish = True
                l_debug_msg += 'Turn OFF; '.format(p_device_obj.Name)
            elif l_cmd1 == MESSAGE_TYPES['status_request']:  #  0x19
                p_device_obj.BrightnessPct = l_level = utilDecode.decode_light_brightness(l_cmd2)
                l_mqtt_publish = True
                l_debug_msg += 'Status of light:"{}"-level:"{}"; '.format(p_device_obj.Name, l_level)
            else:
                l_debug_msg += '\n\tUnknown-type:{} - "{}"; '.format(l_cmd1, FormatBytes(l_message))
                p_device_obj.BrightnessPct = utilDecode.decode_light_brightness(l_cmd2)
                l_mqtt_publish = True
        except AttributeError as e_err:
            LOG.error('ERROR decoding 0x50 record {}'.format(e_err))

        Insteon_utils.update_insteon_obj(p_pyhouse_obj, p_device_obj)
        p_controller_obj.Ret = True
        LOG.debug('Light Response {}'.format(l_debug_msg))
        LOG.info('Light: {}, Brightness: {}'.format(p_device_obj.Name, p_device_obj.BrightnessPct))
        if l_mqtt_publish:
            l_topic = 'house/lighting/light/status'
            p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, p_device_obj)
            pass
        return l_debug_msg

# ## END DBK
