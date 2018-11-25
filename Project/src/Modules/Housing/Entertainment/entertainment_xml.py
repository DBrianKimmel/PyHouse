"""
-*- test-case-name: PyHouse/Project/src/Modules/Housing/Entertainment/entertainment_xml.py -*-

@name:      PyHouse/Project/src/Modules/Housing/Entertainment/entertainment_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Oct 17, 2018
@license:   MIT License
@summary:   Load / Save all the entertainment XML

"""

__updated__ = '2018-11-25'
__version_info__ = (18, 10, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import importlib
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData, \
        EntertainmentDeviceData, \
        EntertainmentServiceData
from Modules.Core.Utilities.xml_tools import XmlConfigTools  # , PutGetXML
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.EntertainXML   ')


class XML:
    """
    Devices all have the same basic part
    @return: EntertainmentDeviceData object
    """

    def read_entertainment_device(self, p_xml, p_device):
        XmlConfigTools().read_base_UUID_object_xml(p_device, p_xml)
        p_device.CommandSet = PutGetXML.get_text_from_xml(p_xml, 'CommandSet')
        p_device.Host = PutGetXML.get_text_from_xml(p_xml, 'Host')
        p_device.Installed = PutGetXML.get_date_time_from_xml(p_xml, 'Installed')
        p_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4', '1.2.3.4')
        p_device.IPv6 = PutGetXML.get_ip_from_xml(p_xml, 'IPv6', 'f800::1')
        p_device.Model = PutGetXML.get_text_from_xml(p_xml, 'Model')
        p_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        p_device.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        p_device.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        p_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        p_device.Volume = PutGetXML.get_int_from_xml(p_xml, 'Volume')
        return p_device

    def write_entertainment_device(self, p_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Device', p_obj)
        PutGetXML.put_text_element(l_xml, 'CommandSet', p_obj.CommandSet)
        PutGetXML.put_text_element(l_xml, 'Host', p_obj.Host)
        PutGetXML.put_date_time_element(l_xml, 'Installed', p_obj.Installed)
        PutGetXML.put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML.put_ip_element(l_xml, 'IPv6', p_obj.IPv6)
        PutGetXML.put_text_element(l_xml, 'Model', p_obj.Model)
        PutGetXML.put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML.put_text_element(l_xml, 'RoomName', p_obj.RoomName)
        PutGetXML.put_text_element(l_xml, 'RoomUUID', p_obj.RoomUUID)
        PutGetXML.put_text_element(l_xml, 'Type', p_obj.Type)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    def read_entertainment_service(self, p_entry_xml, p_service):
        """
        @param p_entry_xml: Element <Device> within <PandoraSection>
        @return: a EntertainmentServiceData object
        """
        XmlConfigTools.read_base_object_xml(p_service, p_entry_xml)
        p_service.Host = PutGetXML.get_ip_from_xml(p_entry_xml, 'Host', 'None')
        p_service.ConnectionFamily = PutGetXML.get_text_from_xml(p_entry_xml, 'ConnectionFamily')
        p_service.ConnectionName = PutGetXML.get_text_from_xml(p_entry_xml, 'ConnectionName').lower()
        p_service.InputName = PutGetXML.get_text_from_xml(p_entry_xml, 'InputName')
        p_service.InputCode = PutGetXML.get_text_from_xml(p_entry_xml, 'InputCode')
        p_service.MaxPlayTime = PutGetXML.get_int_from_xml(p_entry_xml, 'MaxPlayTime')
        p_service.Type = PutGetXML.get_text_from_xml(p_entry_xml, 'Type')
        p_service.Volume = PutGetXML.get_int_from_xml(p_entry_xml, 'Volume')
        return p_service

    def write_entertainment_service(self, p_obj):
        """
        @param p_obj: a filled in PandorDeviceData object
        @return: An XML element for <Device> to be appended to <PandoraSection> Element
        """

        l_xml = XmlConfigTools.write_base_object_xml('Device', p_obj)
        PutGetXML.put_ip_element(l_xml, 'Host', p_obj.Host)
        PutGetXML.put_text_element(l_xml, 'ConnectionFamily', p_obj.ConnectionFamily)
        PutGetXML.put_text_element(l_xml, 'ConnectionName', p_obj.ConnectionName)
        PutGetXML.put_text_element(l_xml, 'InputName', p_obj.InputName)
        PutGetXML.put_text_element(l_xml, 'InputCode', p_obj.InputCode)
        PutGetXML.put_text_element(l_xml, 'MaxPlayTime', p_obj.MaxPlayTime)
        PutGetXML.put_text_element(l_xml, 'Type', p_obj.Type)
        PutGetXML.put_int_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    def XXX_active_section(self, p_plugin_data, p_pyhouse_obj):
        """ Fill in module data if an active section
        """
        l_name = p_plugin_data.Name
        LOG.debug('Working on {}'.format(l_name))
        # Create the module plugin
        l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
        l_module = importlib.import_module(l_module_name)
        p_plugin_data._Module = l_module
        # Initialize Plugin
        p_plugin_data._API = l_module.API(p_pyhouse_obj)
        LOG.info('Created Entertainment Plugin "{}".'.format(l_name))
        # Load XML for Plugin
        l_devices = p_plugin_data._API.LoadXml(p_pyhouse_obj)
        p_plugin_data.Devices = l_devices.Devices

    def _XXX_module_load_loop(self, p_pyhouse_obj, p_section_element):
        """
        """
        l_active = True
        l_plugin_data = EntertainmentPluginData()
        l_plugin_data.Name = l_name = XmlConfigTools.extract_section_name(p_section_element)
        l_plugin_data.Active = l_active  # = PutGetXML.get_bool_from_xml(p_section_element, 'Active', True)
        LOG.debug('Working on {}'.format(l_name))
        if l_active:
            # Create the module plugin
            l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_module_name)
            l_plugin_data._Module = l_module
            # Initialize Plugin
            l_plugin_data._API = l_module.API(self.m_pyhouse_obj)
            p_pyhouse_obj.House.Entertainment.Plugins[l_name] = l_plugin_data
            LOG.info('Created Entertainment Plugin "{}".'.format(l_name))
            # Load XML for Plugin
            l_devices = l_plugin_data._API.LoadXml(p_pyhouse_obj)
            l_plugin_data.Devices = l_devices.Devices

    def read_entertainment_subsection(self, p_pyhouse_obj, p_xml):
        """ Read one complete subsection (pioneer, onkyo, pandora, ...
        The subsection must have a valid Type element
        @param p_xml: points to a XxxSectionElement
        @return: EntertainmentPluginData - ready to add into EntertainmentData['name'].
        """
        l_xml = p_xml
        l_plugin = EntertainmentPluginData()
        l_name = l_xml.tag
        l_plugin.Name = l_name
        l_plugin.Active = l_active = PutGetXML.get_text_from_xml(l_xml, 'Active')
        l_count = 0
        l_module_name = None
        if l_xml.find('Type') is None:
            LOG.warn('Entertainment subsection {} must have a "Type" element'.format(l_name))
            return l_plugin
        l_type = PutGetXML.get_text_from_xml(l_xml, 'Type')
        if l_type is not None:
            l_plugin.Type = l_type
            l_plugin.Name = l_name.lower()[:-7]
            l_module_name = 'Modules.Housing.Entertainment.' + l_plugin.Name + '.' + l_plugin.Name
        if l_type == 'Component':
            for l_xml in l_xml.findall('Device'):
                l_ret = self.read_entertainment_device(l_xml, EntertainmentDeviceData())
                l_plugin.Devices[l_count] = l_ret
                l_count += 1
        elif l_type == 'Service':
            for l_xml in l_xml.findall('Device'):
                l_ret = self.read_entertainment_service(l_xml, EntertainmentServiceData())
                l_plugin.Services[l_count] = l_ret
                l_count += 1
        else:
            # l_name = PutGetXML.get_text_from_xml(p_xml, 'Name')
            LOG.warn('Entertainment subsection {} type was illegal {}'.format(l_name, l_type))
        l_plugin.DeviceCount = l_count
        if l_active:
            # Create the module plugin
            # l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_module_name)
            l_plugin._Module = l_module
            # Initialize Plugin
            l_plugin._API = l_module.API(p_pyhouse_obj)
            LOG.info('Loaded Entertainment Plugin "{}".'.format(l_name))
        return l_plugin

    def write_entertainment_subsection(self, p_obj):
        """
        @param p_obj: a filled in PandorDeviceData object
        @return: An XML element for <Device> to be appended to <PandoraSection> Element
        """
        l_name = p_obj.Name.capitalize() + 'Section'
        l_xml = ET.Element(l_name)
        PutGetXML.put_bool_attribute(l_xml, 'Active', p_obj.Active)
        PutGetXML.put_text_element(l_xml, 'Type', p_obj.Type)
        LOG.debug('Saving Section:{}; Type:{}'.format(p_obj.Name, p_obj.Type))
        if p_obj.Type == 'Component':
            for l_obj in p_obj.Devices.values():
                LOG.debug('Saving Component {}'.format(l_obj.Name))
                # print(PrettyFormatAny.form(l_obj, ' Ret'))
                l_xml.append(self.write_entertainment_device(l_obj))
        else:
            for l_obj in p_obj.Services.values():
                LOG.debug('Saving Service {}'.format(l_obj.Name))
                l_xml.append(self.write_entertainment_service(l_obj))
        return l_xml

    def read_entertainment_all(self, p_pyhouse_obj):
        """ Read one complete subsection (pioneer, onkyo, pandora, ...
        Place all the plugins into the PyHouse Object structure
        """
        l_plugins = EntertainmentData()
        l_count = 0
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        for l_sect in l_xml:
            l_sub = self.read_entertainment_subsection(p_pyhouse_obj, l_sect)
            l_name = l_sub.Name.lower()
            l_plugins.Plugins[l_name] = l_sub
            l_count += 1
        if l_count > 0:
            l_plugins.Active = True
        l_plugins.PluginCount = l_count
        p_pyhouse_obj.House.Entertainment = l_plugins
        return l_plugins

    def write_entertainment_all(self, p_pyhouse_obj):
        """ Read one complete subsection (pioneer, onkyo, pandora, ...
        """
        l_entertainment_obj = p_pyhouse_obj.House.Entertainment.Plugins
        l_xml = ET.Element('EntertainmentSection')
        for l_plugin_obj in l_entertainment_obj.values():
            LOG.debug('Saving {} section'.format(l_plugin_obj.Name))
            l_xml.append(self.write_entertainment_subsection(l_plugin_obj))
        return l_xml

# ## END DBK
