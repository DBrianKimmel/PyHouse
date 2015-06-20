"""
-*- test-case-name: PyHouse.src.Modules.families.UPB.test.test_Device_UPB -*-

@name:      PyHouse/src/Modules/families/UPB/Device_UPB.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   This module is for communicating with UPB controllers.

Load the database with UPB devices.
Start Active UPB Controllers.
    If more than one ???

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.UPB.UPB_data import UPBData
from Modules.Utilities.xml_tools import PutGetXML, stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

g_debug = 9
LOG = Logger.getLogger('PyHouse.UPB_xml     ')



# class ReadWriteXml(xml_tools.XmlConfigTools):
#    """Interface to the lights of this module.
#    """

def ReadXml(p_device_obj, p_in_xml):
    """
    @param p_in_xml: is the e-tree XML house object
    @param p_house: is the text name of the House.
    @return: a dict of the entry to be attached to a house object.
    """
    l_obj = UPBData()
    l_obj.UPBAddress = PutGetXML().get_int_from_xml(p_in_xml, 'Address', 255)
    l_obj.UPBNetworkID = PutGetXML().get_int_from_xml(p_in_xml, 'UPBNetworkID')
    l_obj.UPBPassword = PutGetXML().get_int_from_xml(p_in_xml, 'UPBPassword')
    stuff_new_attrs(p_device_obj, l_obj)


def WriteXml(p_out_xml, p_device_obj):
    try:
        PutGetXML().put_int_element(p_out_xml, 'UPBAddress', p_device_obj.UPBAddress)
        PutGetXML().put_int_element(p_out_xml, 'UPBNetworkID', p_device_obj.UPBNetworkID)
        PutGetXML().put_int_element(p_out_xml, 'UPBPassword', p_device_obj.UPBPassword)
    except AttributeError as e_err:
        LOG.error('InsertDeviceXML ERROR {0:}'.format(e_err))

# ## END DBK
