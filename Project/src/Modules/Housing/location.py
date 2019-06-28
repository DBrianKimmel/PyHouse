"""
@name:      PyHouse/Project/src/Modules/Housing/location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the location information for a house.

There is location information for the house.
This is for calculating the time of sunrise and sunset.
Additional calculations may be added such things as moon rise, tides, etc.
"""
from Modules.Core.Utilities.config_tools import ConfigYamlNodeInformation
from Modules.Families.Insteon.test.xml_insteon import L_INSTEON_GROUP_LIST_0

__updated__ = '2019-06-25'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import xml.etree.ElementTree as ET
from mypy.main import config_types

#  Import PyMh files
from Modules.Core.data_objects import RiseSetData
from Modules.Core.Utilities import config_tools
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Housing.house_data import LocationInformationPrivate

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Location       ')

CONFIG_FILE_NAME = 'location.yaml'


class Xml:
    """ Use the internal data to read / write an updated XML config file.
    """

    def LoadXmlConfig(self, p_pyhouse_obj):
        """
        @param p_house_xml: is the config file xml for a house.
        """
        l_obj = LocationInformationPrivate()
        l_obj._RiseSet = RiseSetData()
        p_pyhouse_obj.House.Location = l_obj
        try:
            l_xml = p_pyhouse_obj._Config.XmlRoot.find('HouseDivision')
            if l_xml is None:
                return l_obj
            l_xml = l_xml.find('LocationSection')
            if l_xml is None:
                return l_obj
            l_obj.Street = PutGetXML.get_text_from_xml(l_xml, 'Street', 'Main')
            l_obj.City = PutGetXML.get_text_from_xml(l_xml, 'City', 'Gotham')
            l_obj.State = PutGetXML.get_text_from_xml(l_xml, 'State', 'Confusion')
            l_obj.ZipCode = PutGetXML.get_text_from_xml(l_xml, 'ZipCode', '99999')
            # l_obj.Region = PutGetXML.get_text_from_xml(l_xml, 'Region', 'America')
            l_obj.Phone = PutGetXML.get_text_from_xml(l_xml, 'Phone', '800-555-1212')
            l_obj.Latitude = PutGetXML.get_float_from_xml(l_xml, 'Latitude', 40.0)
            l_obj.Longitude = PutGetXML.get_float_from_xml(l_xml, 'Longitude', 100.0)
            l_obj.Elevation = PutGetXML.get_float_from_xml(l_xml, 'Elevation', 10.0)
            l_obj.TimeZoneName = PutGetXML.get_text_from_xml(l_xml, 'TimeZoneName', 'America/New_York')
        except AttributeError as e_err:
            LOG.error('ERROR getting location Data - {}'.format(e_err))
        # ##p_pyhouse_obj.House.Location = l_obj
        LOG.info('Loaded location information.')
        return l_obj

    @staticmethod
    def SaveXmlConfig(p_pyhouse_obj):
        """ Replace the data in the 'House/Location' section with the current data.
        """
        l_location = p_pyhouse_obj.House.Location
        l_entry = ET.Element('LocationSection')
        PutGetXML.put_text_element(l_entry, 'Street', l_location.Street)
        PutGetXML.put_text_element(l_entry, 'City', l_location.City)
        PutGetXML.put_text_element(l_entry, 'State', l_location.State)
        PutGetXML.put_text_element(l_entry, 'ZipCode', l_location.ZipCode)
        # PutGetXML.put_text_element(l_entry, 'Region', l_location.Region)
        PutGetXML.put_text_element(l_entry, 'Phone', l_location.Phone)
        PutGetXML.put_float_element(l_entry, 'Latitude', l_location.Latitude)
        PutGetXML.put_float_element(l_entry, 'Longitude', l_location.Longitude)
        PutGetXML.put_float_element(l_entry, 'Elevation', l_location.Elevation)
        PutGetXML.put_text_element(l_entry, 'TimeZoneName', l_location.TimeZoneName)
        LOG.info('Saved Location XML')
        return l_entry


class Yaml:
    """ Update the Yaml config files.
    This will handle the location.yaml file
    ==> PyHouseObj._Config.YamlTree{'location.yaml'}.xxx
    --> xxx = {Yaml, YamlPath, Filename}
    """

    def _extract_location_config(self, p_yaml) -> dict:
        """ Extract the config info for location.
        Warn if there are extra attributes in the config.
        Warn if there are missing attributes in the config.

        @param p_yaml: is the config fragment containing location information.
        @return: a LocattionInformation() obj filled in.
        """
        l_obj = LocationInformationPrivate()
        for l_key, l_val in p_yaml.items():
            # Check for extra attributes in the config file.
            try:
                _l_x = getattr(l_obj, l_key)
            except AttributeError:
                LOG.warn('location.yaml contains a bad entry "{}" = {} - Ignored.'.format(l_key, l_val))
                continue
            # setattr(l_obj, l_key, l_val)
            l_obj.update({l_key: l_val})
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    """ Use the internal data to read / write an updated YAML config file.
    """

    def _update_location_from_yaml(self, p_pyhouse_obj, p_yaml):
        """ Copies the data from the yaml config file to the Location part of the PyHouse obj.
        """
        try:
            l_yaml = p_yaml['Location']
        except:
            LOG.error('The "Location" tag is missing in the "location.yaml" file!')
            return None
        LOG.debug('location.yaml {}'.format(l_yaml))
        l_loc = p_pyhouse_obj.House.Location
        for l_key, l_val in l_yaml.items():
            if l_key not in l_yaml:
                LOG.warn('Location Yaml contains a bad item "{}" = {} - Ignored.'.format(l_key, l_val))
                continue
            setattr(l_loc, l_key, l_val)
        for l_key in [l_attr for l_attr in dir(l_loc) if not callable(getattr(l_loc, l_attr)) and not l_attr.startswith('_')]:
            l_val = getattr(l_loc, l_key)
            if l_val == None:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        return l_loc  # For testing.

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the location.yaml file.
        It contains Location data for the house.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_locat = self._update_location_from_yaml(p_pyhouse_obj, l_node.Yaml)
        p_pyhouse_obj.House.Location = l_locat
        return l_locat  # for testing purposes

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['Location']
        # LOG.debug(PrettyFormatAny.form(l_config, 'Location', 190))
        l_working = p_pyhouse_obj.House.Location
        # LOG.debug(PrettyFormatAny.form(l_working, 'House', 190))
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            l_config[l_key] = l_val
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Location'] = l_config
        # LOG.debug(PrettyFormatAny.form(l_node, 'Updated', 190))
        l_ret = {'Location': l_config}
        return l_ret

    def SaveYamlConfig(self, p_pyhouse_obj):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml(p_pyhouse_obj)
        config_tools.Yaml(p_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class Api:
    """ Location sub-module of a house.
    """

    def __init__(self, p_pyhouse_obj):
        """ Set up the location info.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.Location = LocationInformationPrivate()
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME] = ConfigYamlNodeInformation()

    def LoadConfig(self):
        """ Load the Yaml config file into the system.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        Yaml().LoadYamlConfig(self.m_pyhouse_obj)
        # Xml().LoadXmlConfig(self.m_pyhouse_obj)

    def SaveConfig(self):
        """ Take a snapshot of the running system and save it in Yaml to be loaded on restart.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        Yaml().SaveYamlConfig(self.m_pyhouse_obj)
        Xml().SaveXmlConfig(self.m_pyhouse_obj)

#  ## END DBK
