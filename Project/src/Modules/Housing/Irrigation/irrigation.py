"""
-*- test-case-name: PyHouse.src.Modules.Irrigation.test.test_irrigation -*-

@name:      PyHouse/src/Modules/Irrigation/irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

"""

__updated__ = '2019-05-28'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
# from Modules.Core.Utilities import extract_tools
from Modules.Housing.Irrigation.irrigation_data import IrrigationData
from Modules.Housing.Irrigation.irrigation_xml import Xml as irrigationXml

from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.Irrigation     ')


class MqttActions():
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

    def decode(self, p_topic, p_message, p_logmsg):
        """ pyhouse/<HouseName>/irrigation/<action>
        where <action> is control, status
        """
        l_logmsg = ' Irrigation '
        if p_topic[0].lower() == 'control':
            l_logmsg += '\tControl: {}\n'.format(self._decode_control(p_topic, p_message))
        elif p_topic[0].lower() == 'status':
            l_logmsg += '\tStatus: {}\n'.format(self._decode_status(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown irrigation sub-topic {}'.format(p_message)
            LOG.warn('Unknown Topic: {}'.format(p_topic[0]))
        return l_logmsg


class Utility(object):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Irrigation = IrrigationData()

    def add_api_references(self, p_pyhouse_obj):
        pass


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Irrigations xml info.
        """
        l_obj = irrigationXml.read_irrigation_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Irrigation = l_obj
        LOG.info('Loaded XML')
        return l_obj

    def Start(self):
        LOG.info('Started Irrigation')

    def SaveXml(self, p_xml):
        (l_xml, l_count) = irrigationXml.write_irrigation_xml(self.m_pyhouse_obj.House.Irrigation)
        p_xml.append(l_xml)
        LOG.info("Saved {} Irrigation XML.".format(l_count))
        return p_xml

    def Stop(self):
        LOG.info('Stopped Irrigation')

#  ## END DBK
