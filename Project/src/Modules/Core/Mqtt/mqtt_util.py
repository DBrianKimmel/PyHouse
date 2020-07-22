"""
@name:      Modules/Core/Mqtt/mqtt_util.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 13, 2015
@Summary:

"""

__updated__ = '2020-01-19'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.mqtt_util      ')


class EncodeDecode:
    """
    Encode and decode portions of the message.
    Part of the MQTT Protocol.
    """

    @staticmethod
    def _encodeString(p_string):
        """ Convert a string(UTF) into bytes with encoded length
        """
        # LOG.debug('Encoding "{}"'.format(p_string))
        l_len = len(p_string)
        l_str = p_string.encode('utf-8')
        l_encoded = bytearray()
        l_encoded.append(l_len >> 8)
        l_encoded.append(l_len & 0xFF)
        l_encoded += l_str
        return l_encoded

    @staticmethod
    def _decodeString(p_encodedString):
        """ Convert a lengh-encoded entry into a string
        """
        l_length = 256 * p_encodedString[0] + p_encodedString[1]
        l_ret = p_encodedString[2:2 + l_length].decode('utf-8')
        return l_ret

    @staticmethod
    def _put_string(p_string):
        """ Convert a string(utf) into bytes
        """
        l_str = p_string.encode('utf-8')
        return l_str

    @staticmethod
    def _get_string(p_string):
        """ Convert bytes into a string(utf).
        """
        l_ret = p_string.decode('utf-8')
        return l_ret

    @staticmethod
    def _encodeLength(p_length):
        l_encoded = bytearray()
        while True:
            l_digit = p_length % 128
            p_length //= 128
            if p_length > 0:
                l_digit |= 128
            l_encoded.append(l_digit)
            if p_length <= 0:
                break
        return l_encoded

    @staticmethod
    def _decodeLength(p_lengthArray):
        l_length = 0
        l_multiplier = 1
        for i in p_lengthArray:
            l_length += (i & 0x7F) * l_multiplier
            l_multiplier *= 0x80
            if (i & 0x80) != 0x80:
                break
        return l_length

    @staticmethod
    def _encodeValue(p_value):
        l_encoded = bytearray()
        l_encoded.append(p_value >> 8)
        l_encoded.append(p_value & 0xFF)
        return l_encoded

    @staticmethod
    def _decodeValue(p_valueArray):
        l_value = 0
        l_multiplier = 1
        for i in p_valueArray[::-1]:
            l_value += i * l_multiplier
            multiplier = l_multiplier << 8
        return l_value


def decode_variable_byte_integer(p_bytes):
    """
    1    0 (0x00)                            127 (0x7F)
    2    128 (0x80, 0x01)                    16,383 (0xFF, 0x7F)
    3    16,384 (0x80, 0x80, 0x01)           2,097,151 (0xFF, 0xFF, 0x7F)
    4    2,097,152 (0x80, 0x80, 0x80, 0x01)  268,435,455 (0xFF, 0xFF, 0xFF, 0x7F)
    """
    l_multiplier = 1
    l_value = 0
    for l_next_byte in p_bytes[::-1]:
        l_value += (l_next_byte & 127) * l_multiplier
        if l_multiplier > 128 * 128 * 128:
            LOG.error('Malformed Variable Byte Integer')
        l_multiplier *= 128
        return l_value

#  ## END DBK
