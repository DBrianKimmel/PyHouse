"""
-*- _test-case-name: PyHouse.src.Modules.families.UPB._test.test_Device_UPB -*-

@name:      PyHouse/Project/src/Modules/families/UPB/UPB_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-201 by9 D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module is for communicating with UPB controllers.

"""

__updated__ = '2019-01-22'

# Import system type stuff

# Import PyMh files
from Modules.Families.UPB.UPB_data import UPBData
from Modules.Core.Utilities.xml_tools import PutGetXML, stuff_new_attrs
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.UPB_xml     ')


class Xml(object):

    @staticmethod
    def ReadXml(p_device_obj, p_in_xml):
        """
        @param p_in_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        l_obj = UPBData()
        l_obj.UPBAddress = PutGetXML.get_int_from_xml(p_in_xml, 'UPBAddress', 255)
        l_obj.UPBNetworkID = PutGetXML.get_int_from_xml(p_in_xml, 'UPBNetworkID')
        l_obj.UPBPassword = PutGetXML.get_int_from_xml(p_in_xml, 'UPBPassword')
        stuff_new_attrs(p_device_obj, l_obj)
        return l_obj  # for testing

    @staticmethod
    def WriteXml(p_out_xml, p_device_obj):
        try:
            PutGetXML.put_int_element(p_out_xml, 'UPBAddress', p_device_obj.UPBAddress)
            PutGetXML.put_int_element(p_out_xml, 'UPBNetworkID', p_device_obj.UPBNetworkID)
            PutGetXML.put_int_element(p_out_xml, 'UPBPassword', p_device_obj.UPBPassword)
        except AttributeError as e_err:
            LOG.error('InsertDeviceXML ERROR {}'.format(e_err))

# ## END DBK
