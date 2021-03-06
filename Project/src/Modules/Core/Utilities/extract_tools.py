"""
@name:      Modules/Core/Utilities/extract_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Oct 3, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-08-20'

# Import system type stuff


def extract_quoted(p_string, p_delim=b'"'):
    """
    Used by play list extracting in pandora module.

    Discard characters before first p_delim
    extract chars between p_delim chars
    return all chars after second p_delim
    """
    l_string = p_string
    l_1st = l_string.find(p_delim)
    l_2nd = l_string.find(p_delim, l_1st + 1)
    l_string = p_string[l_1st + 1:l_2nd].decode('utf-8')
    l_rest = p_string[l_2nd + 1:]
    return l_string, l_rest


def get_mqtt_field(p_message, p_field):
    """ Get the given field from a JSON message.
    @param p_message: The json message
    @param p_field: the 'field_name' to extract
    @return: the value of the field or None if missing.
    """
    try:
        l_ret = p_message[p_field]
    except (KeyError, TypeError):
        l_ret = None
    return l_ret


def get_required_mqtt_field(p_message, p_field):
    """ Get the given field from a JSON message.
    """
    try:
        l_ret = p_message[p_field]
    except (KeyError, TypeError):
        l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
    return l_ret

# ## END DBK
