"""
@name:      Modules/House/Irrigation/irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

"""

__updated__ = '2019-12-02'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
# from Modules.Core.Utilities import extract_tools
from Modules.House.Irrigation.irrigation_data import IrrigationData
from Modules.House.Irrigation.irrigation_xml import Xml as irrigationXml

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Irrigation     ')


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, _p_topic, _p_message):
        l_logmsg = '\tIrrigation Control'
        return l_logmsg

    def _decode_status(self, _p_topic, _p_message):
        l_logmsg = '\tIrrigation Status'
        return l_logmsg

    def decode(self, p_msg):
        """ pyhouse/<HouseName>/irrigation/<action>
        where <action> is control, status
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        l_logmsg = ' Irrigation '
        if l_topic[0].lower() == 'control':
            l_logmsg += '\tControl: {}\n'.format(self._decode_control(p_msg.Topic, p_msg.Payload))
        elif l_topic[0].lower() == 'status':
            l_logmsg += '\tStatus: {}\n'.format(self._decode_status(p_msg.Topic, p_msg.Payload))
        else:
            l_logmsg += '\tUnknown irrigation sub-topic {}'.format(p_msg.Payload)
            LOG.warn('Unknown Irrigation Topic: {}'.format(l_topic[0]))
        return l_logmsg


class lightingUtilityIrr:
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Irrigation = IrrigationData()

    def add_api_references(self, p_pyhouse_obj):
        pass


class Api(lightingUtilityIrr):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadConfig(self):
        """ Load the Irrigations config info.
        """
        l_obj = irrigationXml.read_irrigation_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Irrigation = l_obj
        LOG.info('Loaded XML')
        return l_obj

    def Start(self):
        LOG.info('Started Irrigation')

    def SaveConfig(self):
        irrigationXml.write_irrigation_xml(self.m_pyhouse_obj.House.Irrigation)
        LOG.info("Saved Irrigation XML.")

    def Stop(self):
        LOG.info('Stopped Irrigation')

#  ## END DBK
