"""
-*- test-case-name: PyHouse.Modules.Computer.test.test_weather -*-

@name:      PyHouse/src/Modules/Computer/weather.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2015 by D. Brian Kimmel
@note:      Created on Jan 20, 2014
@license:   MIT License
@summary:


"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Weather        ')


class API(object):
    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def Start(self):
        pass

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = ET.Element('Weather')
        p_xml.append(l_xml)
        LOG.info('Saved XML.')
        return p_xml

# ## END DBK
