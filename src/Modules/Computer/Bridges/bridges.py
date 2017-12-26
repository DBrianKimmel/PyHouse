"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/bridges.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Bridges/bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-26'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges        ')


class Xml(object):
    """
    """

    def read_xml(self):
        l_dict = {}
        l_count = 0
        try:
            l_section = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            if l_section == None:
                return l_dict
            l_section = l_section.find('BridgesSection')
            if l_section == None:
                return l_dict
        except AttributeError as e_err:
            LOG.error('Reading Bridges Configuration information - {}'.format(e_err))
            l_section = None
        try:
            for l_xml in l_section.iterfind('Bridge'):
                l_broker = Xml._read_one_broker(l_xml)
                l_broker.Key = l_count
                l_broker._ClientAPI = p_api
                l_dict[l_count] = l_broker
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Mqtt Errors: {}'.format(e_err))
        return l_dict

    def write_xml(self):
        pass


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the xml info.
        """
        LOG.info("Loading XML")

    def Start(self):
        LOG.info("Starting Bridges")
        pass

    def SaveXml(self, p_xml):
        LOG.info("Saved XML")
        l_xml = ET.Element('BridgesSection')
        p_xml.append(l_xml)
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
