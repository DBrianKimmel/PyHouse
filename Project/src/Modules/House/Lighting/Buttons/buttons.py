"""
@name:      Modules/House/Lighting/Buttons/buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system buttons.

Buttons may be:
    Remote = Mini remotes (Insteon)
    Slave = light switches that control another switch load
    Split = buttons (UPB)

"""
from Modules.House.Lighting import LightingClass

__updated__ = '2020-02-09'
__version_info__ = (20, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Lighting.Buttons import ButtonInformation, CONFIG_NAME

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Buttons        ')


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_remote_button(self, p_config) -> dict:
        """
        Button:
            - Name: GDO
              Comment: Garage Door Open/Close
              Group: 1
            - Name: B
              Group: 2
       """
        l_obj = ButtonInformation()
        l_required = ['Name', 'Group']
        for l_key, l_value in p_config:
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('buttons.yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted button "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_one_button_set(self, p_config) -> dict:
        """ Extract the config info for one button.
        - Name: Button 1
          Comment: This is _test button 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Dimmable: true  # Optional
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = ButtonInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
            elif l_key == 'Button':
                # l_obj.Button = self._extract_remote_button(l_value)
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('buttons.yaml is missing an entry for "{}"'.format(l_key))
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Button'))
        # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Button.Family'))
        LOG.info('Extracted button "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_button_sets(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        # for l_ix, l_button in enumerate(p_config):
        #    # print('Light: {}'.format(l_light))
        #    l_button_obj = self._extract_one_button_set(l_button)
        #    l_dict[l_ix] = l_button_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the buttons.yaml file if it exists.  No file = no buttons.
        """
        LOG.info('Load Config')
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Buttons']
        except:
            LOG.warning('The config file does not start with "Buttons:"')
            return None
        l_buttons = self._extract_all_button_sets(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Buttons = l_buttons
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'Buttons'))
        return l_buttons

    def _build_yaml(self):
        """
        """
        return self.m_config.create_yaml('Lights')


class Api:
    """
    """
    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        if not hasattr(self.m_pyhouse_obj.House, 'Lighting'):
            self.m_pyhouse_obj.House.Lighting = LightingClass()
        self.m_pyhouse_obj.House.Lighting.Buttons = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config.')
        self.m_pyhouse_obj.House.Lighting.Buttons = self.m_local_config.load_yaml_config()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'buttons.Api.LoadConfig'))
        LOG.info('Loaded {} Buttons.'.format(len(self.m_pyhouse_obj.House.Lighting.Buttons)))

    def SaveConfig(self):
        pass

    def Start(self):
        pass  # Nothing needs starting ATM

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse')

    def MqttDispatch(self, p_msg):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/house/lighting/controller/<action>

        @param p_msg.Topic: is the topic after 'controller'
        @return: a message to be logged as a Mqtt message
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += ' Buttons: {}\n\t'.format(p_msg.Topic)
        if l_topic[0] == 'control':
            p_msg.LogMessage += 'Button Control: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Controller Control'))
            LOG.debug('Control Topic:{}\n\tMsg: {}'.format(p_msg.Topic, p_msg.Payload))
        elif l_topic[0] == 'status':
            p_msg.LogMessage += 'Button Status: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Controller Status'))
            LOG.debug(' Status Topic:{}\n\tMsg: {}'.format(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Button sub-topic:{}\n\t{}'.format(p_msg.Topic, PrettyFormatAny.form(p_msg.Payload, 'Button Status'))
            LOG.warning('Unknown Button Topic: {}'.format(l_topic[0]))

#  ## END DBK
