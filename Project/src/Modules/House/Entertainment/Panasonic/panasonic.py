"""
@name:      Modules.House.Entertainment.Panasonic
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Jul 14, 2016
@license:      MIT License
@summary:

Cannon Trail Blueray Player

"""

__updated__ = '2020-02-14'
__version_info__ = (18, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

#  Import PyMh files and modules.
from Modules.House.Entertainment.entertainment_data import EntertainmentDeviceControl, EntertainmentDeviceInformation
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
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = None
        return l_xml

    @staticmethod
    def read_panasonic_section_xml(p_pyhouse_obj):
        """ Get the entire PanasonicDeviceData object from the xml.
        """
        # Clear out the data sections
        l_xml = None
        l_entry_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_entry_obj.Name = SECTION
        l_device_obj = PanasonicDeviceData()
        l_count = 0
        if l_xml is None:
            l_entry_obj.Name = 'Did not find xml section '
            return l_entry_obj
        if l_count > 0:
            l_entry_obj.Active = True
        LOG.info('Loaded {} Panasonic Devices.'.format(l_count))
        return l_entry_obj

    @staticmethod
    def write_panasonic_section_xml(p_pyhouse_obj):
        """ Create the entire PanasonicSection of the XML.
        @param p_pyhouse_obj: containing an object with panasonic
        """


class Api:

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
