"""
@name:      PyHouse/src/Modules/Rules/rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 27, 2015
@Summary:

"""

__updated__ = '2017-01-20'


# Import system type stuff

# Import PyMh files and modules.
from Modules.Housing.Rules.rules_xml import Xml as rulesXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.RulesXml       ')

class API (object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        l_count = 0
        LOG.info('{} Rules were loaded'.format(l_count))

    def Stop(self):
        pass

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Mqtt xml info.
        """
        l_rules = rulesXML.read_rules_xml(self.m_pyhouse_obj)
        return l_rules

    def SaveXml(self, p_xml):
        l_xml = rulesXML.write_rules_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Rules XML.")
        return p_xml

# ## END DBK
