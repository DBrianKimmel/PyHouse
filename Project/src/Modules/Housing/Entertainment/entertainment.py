"""
@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Start up entertainment systems.

Listen to Mqtt message to control things...
==> pyhouse/<house name>/entertainment/<thing>

where <thing> is:
    onkyo          to control the Onkyo A/V devices
    pandora        to control the pandora player
    pioneer        to control the Pioneer A/V devices
    samsung        to control the Samsung A/V devices


House.Entertainment.Plugins{}.API
                             .Devices{}

"""

__updated__ = '2019-05-23'
__version_info__ = (18, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
# import importlib
# import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentDeviceControl
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Core.Utilities.xml_tools import XmlConfigTools  # , PutGetXML

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')


class Ent:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/entertainment/<device-or-service>/...

        <device-or-service> = one of the VALID_ENTERTAINMENT_MFGRS

        These messages probably come from some external source such as node-red or alexa.

        @param p_topic: is the topic after 'entertainment'
        @return: a message to be logged as a Mqtt message
        """
        l_module = p_topic[0].lower()
        l_logmsg = '\tEntertainment: '
        LOG.debug('MqttEntertainmentDispatch Topic:{}'.format(p_topic))
        try:
            if not self.m_pyhouse_obj.House.Entertainment.Plugins[l_module].Active:
                l_logmsg += ' Module: {} is not active - skipping'.format(l_module)
                return l_logmsg
        except KeyError:
            l_logmsg += ' {} not defined here.'.format(l_module)
            return l_logmsg
        try:
            l_module_api = self.m_pyhouse_obj.House.Entertainment.Plugins[l_module]._API
            l_logmsg += l_module_api.decode(p_topic[1:], p_message)
            # LOG.debug('{} {}'.format(l_module_api, l_logmsg))
        except (KeyError, AttributeError) as e_err:
            l_module_api = None
            l_logmsg += 'Module {} not defined here -ignored.'.format(l_module)
            LOG.error('Error {}'.format(e_err))
            return l_logmsg
        return l_logmsg


class API(Ent):
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        p_pyhouse_obj.House.Entertainment = EntertainmentData()  # Create empty entertainment plugin section
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def _module_start_loop(self, p_pyhouse_obj, p_plugin):
        """
        """
        l_name = p_plugin.Name
        # Start Plugin
        p_plugin._API.Start()
        l_topic = 'house/entertainment/{}/status'.format(l_name)
        l_obj = EntertainmentDeviceControl()
        l_obj.Model = l_name
        l_obj.HostName = p_pyhouse_obj.Computer.Name
        LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}\n\tAPI:{}'.format(
            l_topic, l_obj, PrettyFormatAny.form(p_pyhouse_obj.APIs.Computer.MqttAPI, 'API', 180)))
        # p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

    def LoadXml(self, p_pyhouse_obj):
        """ Read the entertainment section.
        Everything present in the XML must be read into the pyhouse_obj structure.

        SubSections not active will not be loaded or instantiated.

        If a subsection is available, load its module and let it read the xml for itself.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("XML Loading - Version:{}".format(__version__))
        _l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')

        """
        if l_xml == None:
            l_entertain.Active = False
            return l_entertain
        l_count = 0
        for _section_element in l_xml:
            # self._module_load_loop(p_pyhouse_obj, l_section_element)
            l_count += 1
        l_entertain.Active = True
        l_entertain.PluginCount = l_count
        LOG.info('XML Loaded {} Entertainment Sections'.format(l_count))
        return l_entertain
        """

        l_entertainment_obj = entertainmentXML().read_entertainment_all(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment = l_entertainment_obj
        return l_entertainment_obj

    def Start(self):
        LOG.info("Starting - Version:{}".format(__version__))
        l_count = 0
        for l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
            self._module_start_loop(self.m_pyhouse_obj, l_plugin)
            l_count += 1
        LOG.info("Started {} plugin(s)- Version:{}".format(l_count, __version__))

    def SaveXml(self, p_xml):
        """ Stick in the entertainment section
        """
        LOG.info("Saving XML.")
        l_entertainment_xml = entertainmentXML().write_entertainment_all(self.m_pyhouse_obj)
        p_xml.append(l_entertainment_xml)
        LOG.info("Saved XML.")
        return l_entertainment_xml  # For debugging

    def Stop(self):
        LOG.info("Stopped.")

    def XXXDecodeMqtt(self, p_topic, p_message):
        """ Decode messages sent to the house module.
        """
        l_logmsg = MqttActions(self.m_pyhouse_obj).decode(p_topic, p_message)
        return l_logmsg

# ## END DBK
