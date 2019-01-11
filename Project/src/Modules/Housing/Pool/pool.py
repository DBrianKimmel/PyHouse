"""
@name:      PyHouse/src/Modules/Housing/Pool/pool.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2019-01-11'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Housing.Pool.pool_data import PoolData
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Pool           ')


class Xml(object):

    @staticmethod
    def _read_base(p_pool_element):
        l_pool_obj = PoolData()
        XmlConfigTools.read_base_UUID_object_xml(l_pool_obj, p_pool_element)
        return l_pool_obj

    @staticmethod
    def _write_base(p_obj):
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Pool', p_obj)
        return l_entry

    @staticmethod
    def _read_one_pool(p_pool_element):
        l_pool_obj = Xml._read_base(p_pool_element)
        # l_pool_obj.Comment = PutGetXML.get_text_from_xml(p_pool_element, 'Comment')
        l_pool_obj.PoolType = PutGetXML.get_text_from_xml(p_pool_element, 'PoolType')
        return l_pool_obj

    @staticmethod
    def _write_one_pool(p_pool_obj):
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Pool', p_pool_obj)
        # PutGetXML().put_text_element(l_entry, 'Comment', p_pool_obj.Comment)
        PutGetXML().put_text_element(l_entry, 'PoolType', p_pool_obj.PoolType)
        return l_entry

    @staticmethod
    def read_all_pools_xml(p_pyhouse_obj):
        l_dict = {}
        l_count = 0
        l_pools_sect = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision/PoolSection')
        if l_pools_sect != None:
            for l_pool in l_pools_sect.iterfind('Pool'):
                l_one = Xml._read_one_pool(l_pool)
                l_dict[l_count] = l_one
                l_count += 1
        p_pyhouse_obj.House.Pools = l_dict
        return l_dict

    @staticmethod
    def write_all_pools_xml(p_pyhouse_obj):
        l_xml = ET.Element('PoolSection')
        l_count = 0
        l_pools_obj = p_pyhouse_obj.House.Pools
        if l_pools_obj == {}:
            return (l_xml, l_count)
        try:
            for l_obj in l_pools_obj.values():
                l_sys = Xml._write_one_pool(l_obj)
                l_count += 1
                l_xml.append(l_sys)
        except AttributeError as e_err:
            LOG.error('{}'.format(e_err))
        return (l_xml, l_count)


class API(object):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def Start(self):
        self.LoadXml(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def LoadXml(self, p_pyhouse_obj):
        l_dict = Xml.read_all_pools_xml(p_pyhouse_obj)
        # p_pyhouse_obj.House.Pools = l_dict
        return l_dict

    def SaveXml(self, p_xml):
        (l_xml, l_count) = Xml.write_all_pools_xml(self.m_pyhouse_obj)
        if l_count > 0:
            p_xml.append(l_xml)
            LOG.info("Saved {} Pools XML.".format(l_count))
        else:
            LOG.info('No Pools were defined.')
        return p_xml

# ## END DBK
