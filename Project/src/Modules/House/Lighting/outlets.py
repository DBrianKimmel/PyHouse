"""
@name:      Modules/House/Lighting/outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul 18, 2019
@license:   MIT License
@summary:   Handle the home lighting system automation.


"""

__updated__ = '2019-08-17'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.OutletControl  ')

CONFIG_FILE_NAME = 'outlets.yaml'


class OutletInformation:
    """ This is the information that the user needs to enter to uniquely define a Outlet.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Outlet'
        self.LastUpdate = None  # Not user entered but maintained
        self.Uuid = None  # Not user entered but maintained
        self.Family = None  # LightFamilyInformation()
        self.Room = None  # LightRoomInformation() Optional


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message, p_logmsg):
        """
        --> pyhouse/<housename>/house/outlet/<name>/...
        """
        p_logmsg += ''
        # l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        if len(p_topic) > 0:
            l_name = p_topic[0]
            p_topic = p_topic[1:]
            if len(p_topic) > 0:
                if p_topic[0] == 'STATE':
                    p_logmsg += '\tState:\n'
                elif p_topic[0] == 'RESULT':
                    p_logmsg += '\tResult:\n'
                elif p_topic[0] == 'POWER':
                    p_logmsg += '\tResult:\n'
                else:
                    p_logmsg += '\tUnknown house/outlet sub-topic: {}; - {}'.format(p_topic, p_message)
                    LOG.warn('Unknown "house/outlet" sub-topic: {}\n\tTopic: {}\n\tMessge: {}'.format(p_topic[0], p_topic, p_message))
        return p_logmsg


class API:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadConfig(self):
        """
        """

    def SaveConfig(self):
        """
        """

# ## END DBK
