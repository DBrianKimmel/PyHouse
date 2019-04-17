"""

@name: PyHouse/Project/src/Modules/Housing/Entertainment/pandora/pandora_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: (c)2019-2019 by D. Brian Kimmel
@note: Created on Apr 15, 2019
@license: MIT License
@summary: Loads/Saves extra pandora info from XML file.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Housing.Entertainment.entertainment_data import EntertainmentServiceData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pandora_xml    ')

SECTION = 'pandora'


class XML:
    """ Read the XML and initialize device objects,
    Write the object to an XML structure for safekeeping
    """

    def _read_device(self, p_entry_xml):
        """
        @param p_entry_xml: Element <Device> within <PandoraSection>
        @return: a EntertainmentServiceData object
        """
        l_service = EntertainmentServiceData()
        l_obj = entertainmentXML().read_entertainment_service(p_entry_xml, l_service)
        return l_obj

    def _write_device(self, p_obj):
        """
        @param p_obj: a filled in PandorDeviceData object
        @return: An XML element for <Device> to be appended to <PandoraSection> Element
        """

        l_xml = entertainmentXML().write_entertainment_service(p_obj)
        return l_xml

    def read_pandora_section_xml(self, p_pyhouse_obj):
        """
        This has to:
            Fill in an entry in Entertainment Plugins

        @param p_pyhouse_obj: containing an XML Element for the <PandoraSection>
        @return: a EntertainmentPluginData object filled in.
        """
        l_plugin_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_plugin_obj.Name = SECTION
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/PandoraSection')
        if l_xml is None:
            return l_plugin_obj
        l_count = 0
        try:
            l_plugin_obj.Active = PutGetXML.get_bool_from_xml(l_xml, 'Active')
            l_plugin_obj.Type = PutGetXML.get_text_from_xml(l_xml, 'Type')
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = self._read_device(l_device_xml)
                l_device_obj.Key = l_count
                l_plugin_obj.Devices[l_count] = l_device_obj
                LOG.info('Loaded {} Device {}'.format(SECTION, l_plugin_obj.Name))
                l_count += 1
                l_plugin_obj.DeviceCount = l_count
        except AttributeError as e_err:
            LOG.error('ERROR if getting {} Device Data - {}'.format(SECTION, e_err))
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_plugin_obj
        LOG.info('Loaded {} {} Devices.'.format(l_count, SECTION))
        return l_plugin_obj

    def write_pandora_section_xml(self, p_pyhouse_obj):
        """ Create the <PandoraSection> portion of the <EntertainmentSection>

        @param p_pyhouse_obj: containing an object with pandora data filled in.
        @return: An Element of the tree which can be appended to the EntertainmentSection
        """
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_active = l_plugin_obj.Active
        l_xml = ET.Element('PandoraSection', attrib={'Active': str(l_active)})
        PutGetXML.put_text_element(l_xml, 'Type', l_plugin_obj.Type)
        l_count = 0
        for l_pandora_object in l_plugin_obj.Devices.values():
            l_pandora_object.Key = l_count
            l_entry = self._write_device(l_pandora_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Pandora device(s) XML'.format(l_count))
        return l_xml

# ## END DBK
