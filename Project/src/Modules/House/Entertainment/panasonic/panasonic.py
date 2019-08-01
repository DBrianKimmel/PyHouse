"""
-*- _test-case-name: /home/briank/PyHouse/src/Modules/Housing/Entertainment/panasonic.py -*-

@name:      src.Modules.House.Entertainment.panasonic
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Jul 14, 2016
@license:      MIT License
@summary:

Cannon Trail Blueray Player

"""

__updated__ = '2019-06-30'
__version_info__ = (18, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceControl, EntertainmentDeviceInformation
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Panasonic   ')
SECTION = 'panasonic'


class PanasonicDeviceData(EntertainmentDeviceInformation):

    def __init__(self):
        super(PanasonicDeviceData, self).__init__()
        self.IPv4 = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None  # Default volume for initial turn on (usually low but audible)


class XML:
    """
    """

    @staticmethod
    def _read_device(p_xml):
        """ Read an entire <Device> section of XML and fill in the PanasonicDeviceData Object

        @return: a completed PanasonicDeviceData object
        """
        l_device = PanasonicDeviceData()
        XmlConfigTools.read_base_UUID_object_xml(l_device, p_xml)
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        l_device.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        l_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        l_device.Volume = PutGetXML.get_int_from_xml(p_xml, 'Volume')
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Device', p_obj)
        PutGetXML.put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML.put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML.put_text_element(l_xml, 'RoomName', p_obj.RoomName)
        PutGetXML.put_text_element(l_xml, 'RoomUUID', p_obj.RoomUUID)
        PutGetXML.put_text_element(l_xml, 'Type', p_obj.Type)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_panasonic_section_xml(p_pyhouse_obj):
        """ Get the entire PanasonicDeviceData object from the xml.
        """
        # Clear out the data sections
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/PanasonicSection')
        l_entry_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_entry_obj.Name = SECTION
        l_device_obj = PanasonicDeviceData()
        l_count = 0
        if l_xml is None:
            l_entry_obj.Name = 'Did not find xml section '
            return l_entry_obj
        try:
            l_entry_obj.Type = PutGetXML.get_text_from_xml(l_xml, 'Type')
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = XML._read_device(l_device_xml)
                l_device_obj.Key = l_count
                l_entry_obj.Devices[l_count] = l_device_obj
                l_entry_obj.DeviceCount += 1
                LOG.info('Loaded Panasonic Device {}'.format(l_entry_obj.Name))
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting Panasonic Device Data - {}'.format(e_err))
        if l_count > 0:
            l_entry_obj.Active = True
        LOG.info('Loaded {} Panasonic Devices.'.format(l_count))
        return l_entry_obj

    @staticmethod
    def write_panasonic_section_xml(p_pyhouse_obj):
        """ Create the entire PanasonicSection of the XML.
        @param p_pyhouse_obj: containing an object with panasonic
        """
        l_active = p_pyhouse_obj.House.Entertainment.Plugins[SECTION].DeviceCount > 0
        l_xml = ET.Element('PanasonicSection', attrib={'Active': str(l_active)})
        l_count = 0
        l_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        PutGetXML.put_text_element(l_xml, 'Type', l_obj.Type)
        for l_device_object in l_obj.Devices.values():
            l_device_object.Key = l_count
            l_entry = XML._write_device(l_device_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Panasonic device(s) XML'.format(l_count))
        return l_xml


class API:

    m_started = False

    def __init__(self, p_pyhouse_obj):
        self.m_started = None
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Panasonic devices.
        """
        LOG.info("Loaded Panasonic XML.")
        return

    def Start(self):
        """Start the Pandora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        # LOG.info("Starting")
        l_topic = 'house/entertainment/panasonic/control'
        l_obj = EntertainmentDeviceControl()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        """
        """
        l_xml = XML.write_panasonic_section_xml(self.m_pyhouse_obj)
        # p_xml.append(l_xml)
        LOG.info("Saved Panasonic XML.")
        return l_xml

    def Stop(self):
        """Stop the Panasonic player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        LOG.info("Stopped.")

# ## END DBK
