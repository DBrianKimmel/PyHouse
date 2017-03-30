"""
@name:      PyHouse/src/Modules/Rules/rules_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 27, 2015
@Summary:

"""

__updated__ = '2017-03-26'


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.RulesXml       ')

class Xml (object):

    @staticmethod
    def _read_one_rule():
        pass

    @staticmethod
    def _write_one_rule():
        pass

    @staticmethod
    def read_rules_xml(p_pyhouse_obj):
        l_count = 0
        l_dict = {}
        p_pyhouse_obj.House.Rules = l_dict
        return l_dict, l_count

    @staticmethod
    def write_rules_xml(p_pyhouse_obj):
        l_xml = ET.Element('RulesSection')
        l_count = 0
        for l_light_obj in p_pyhouse_obj.House.Rules.values():
            l_one = Xml._write_one_rule(p_pyhouse_obj, l_light_obj)
            l_xml.append(l_one)
            l_count += 1
        LOG.info('Saved {} Rules XML'.format(l_count))
        return l_xml, l_count

# ## END DBK
