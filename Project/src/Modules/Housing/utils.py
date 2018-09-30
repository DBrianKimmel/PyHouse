"""
-*- test-case-name: PyHouse.src.Modules.Housing.utils.py -*-

@name:      PyHouse/src/Modules/Housing/utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Nov 23, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-11-23'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.xml_tools import PutGetXML

class Utility (object):
    """
    """

def read_room_reference_xml(p_obj, p_xml):
    """ Since many different XML routines need this - it is factored out here.
    It will use the XML in a configuration file to gather the room information.
    @param p_obj: is the object that will have the room information from the XML added.
    @param p_xml: is the XML that has the room information as sub elements
    """
    p_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_xml, 'RoomCoords')
    p_obj.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
    p_obj.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
    return p_obj

def write_room_reference_xml(p_obj, p_xml):
    PutGetXML.put_coords_element(p_xml, 'RoomCoords', p_obj.RoomCoords)
    PutGetXML.put_text_element(p_xml, 'RoomName', p_obj.RoomName)
    PutGetXML.put_text_element(p_xml, 'RoomUUID', p_obj.RoomUUID)
    return p_xml

# ## END DBK
