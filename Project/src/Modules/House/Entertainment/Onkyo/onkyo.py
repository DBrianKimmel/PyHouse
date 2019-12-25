"""
@name:      Modules/House/Entertainment/Onkyo/onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)2016-2019 by D. Brian Kimmel
@note:      Created on Jul 9, 2016
@license:   MIT License
@summary:   Connects to and controls Onkyo devices.

"""

__updated__ = '2019-12-25'
__version_info__ = (19, 11, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools
from Modules.House.Entertainment import entertainment_utility as E_U
from Modules.House.Entertainment.entertainment_data import \
    EntertainmentDeviceInformation, EntertainmentDeviceControl, EntertainmentDeviceStatus, \
    EntertainmentPluginInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')

CONFIG_NAME = 'onkyo'


class OnkyoPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(OnkyoPluginInformation, self).__init__()


class OnkyoDeviceInformation(EntertainmentDeviceInformation):
    """ A super that contains some onkyo specific fields
    """

    def __init__(self):
        super(OnkyoDeviceInformation, self).__init__()
        self.Commands = None
        self.Type = None
        self.Volume = None
        self.Zone = None


class OnkyoDeviceControl(EntertainmentDeviceControl):
    """ Used to control a device.
    All defaults are None - Only fill in what you need so inadvertent controls are not done.
    """

    def __init__(self):
        super(OnkyoDeviceControl, self).__init__()
        pass


class OnkyoDeviceStatus(EntertainmentDeviceStatus):
    """
    The device family is part of the topic.
    """

    def __init__(self):
        super(OnkyoDeviceStatus, self).__init__()
        pass


class OnkyoZoneStatus():
    """ The status of each zone.
    """

    def __init__(self):
        self.Name = None
        self.Power = None
        self.Input = None
        self.Volume = 0


class OnkyoQueueData:
    """
    """

    def __init__(self):
        self.Command = 'PWR'
        self.Args = 'QSTN'
        self.Zone = 1


class OnkyoCommandSet:
    """
    """

    def __init__(self):
        self.Arguments = None
        self.UnitType = None


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _find_model(self, p_family, p_model):
        l_devices = self.m_pyhouse_obj.House.Entertainment['onkyo'].Devices
        for l_device in l_devices.values():
            if l_device.Name.lower() == p_model.lower():
                LOG.info("found device - {} {}".format(p_family, p_model))
                return l_device
        LOG.error('No such device as {}'.format(p_model))
        return None

    def _get_power(self, p_message):
        """
        force power to be None, 'On' or 'Off'
        """
        l_ret = extract_tools.get_mqtt_field(p_message, 'Power')
        if l_ret == None:
            return l_ret
        if l_ret == 'On':
            return 'On'
        return 'Off'

    def _decode_control(self, p_topic, p_message):
        """ Decode the control message.

        @param p_message: is the payload used to control
        """
        LOG.debug('Decode-Control called:\n\tTopic:{}\n\tMessage:{}'.format(p_topic, p_message))
        l_sender = extract_tools.get_mqtt_field(p_message, 'Sender')
        l_family = extract_tools.get_mqtt_field(p_message, 'Family')
        l_model = extract_tools.get_mqtt_field(p_message, 'Model')
        if l_family == None:
            l_family = 'onkyo'
        l_device_obj = self._find_model(l_family, l_model)
        #
        l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        l_power = self._get_power(p_message)
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_logmsg = 'Control from: {}; '.format(l_sender)
        if l_power != None:
            l_queue = OnkyoQueueData()
            l_queue.Command = 'Power'
            l_queue.Args = l_power
            l_queue.Zone = l_zone
            l_device_obj._Queue.put(l_queue)
            l_logmsg += ' Turn power {} to {}.'.format(l_power, l_model)
        if l_input != None:
            l_queue = OnkyoQueueData()
            l_queue.Command = 'InputSelections'
            l_queue.Args = l_input
            l_queue.Zone = l_zone
            l_device_obj._Queue.put(l_queue)
            l_logmsg += ' Turn input to {}.'.format(l_input)
        if l_volume != None:
            l_queue = OnkyoQueueData()
            l_queue.Command = 'Volume'
            l_queue.Args = l_volume
            l_queue.Zone = l_zone
            l_device_obj._Queue.put(l_queue)
            l_logmsg += ' Turn volume to {}.'.format(l_volume)
        self.run_queue(l_device_obj)
        #
        LOG.info('Decode-Control 2 called:\n\tTopic:{}\n\tMessage:{}'.format(p_topic, p_message))
        return l_logmsg

    def _decode_status(self, p_topic, p_message):
        """ Decode the control message.

        @param p_message: is the payload used to control
        """
        LOG.info('Decode_status called:\n\tTopic:{}\n\tMessage:{}'.format(p_topic, p_message))
        l_node_name = self.m_pyhouse_obj.Computer.Name
        if self.m_sender == l_node_name:
            return ''
        #    self.m_device._isControlling = True
        # else:
        #    self.m_device._isControlling = False

    def decode(self, p_msg):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/house/entertainment/onkyo/<type>
        <type> = control, status

        @param p_topic: is the topic with pyhouse/housename/entertainment/onkyo stripped off.
        @param p_message: is the body of the json message string.
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        LOG.debug('Decode called:\n\tTopic:{}\n\tMessage:{}'.format(p_msg.Topic, p_msg.Payload))
        p_msg.LogMessage += ' Onkyo-{}'.format(l_topic[0])
        self.m_sender = extract_tools.get_mqtt_field(p_msg.Payload, 'Sender')
        self.m_model = extract_tools.get_mqtt_field(p_msg.Payload, 'Model')
        # self.m_device = self._find_model(SECTION, self.m_model)

        if l_topic[0].lower() == 'control':
            p_msg.LogMessage += '\tControl: {}\n'.format(self._decode_control(p_msg.Topic, p_msg.Payload))
        elif l_topic[0].lower() == 'status':
            p_msg.LogMessage += '\tStatus: {}\n'.format(self._decode_status(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Onkyo sub-topic: {}  Message: {}'.format(p_msg.Topic, PrettyFormatAny.form(p_msg.Payload, 'Entertainment msg', 160))
            LOG.warning('Unknown Onkyo Topic: {}'.format(l_topic[0]))


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def dump_struct(self):
        """
        """
        l_entertain = self.m_pyhouse_obj.House.Entertainment
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'Pyhouse'))
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'House'))
        LOG.debug(PrettyFormatAny.form(l_entertain, 'Entertainment'))
        l_onkyo = l_entertain['onkyo']
        LOG.debug(PrettyFormatAny.form(l_onkyo, 'Onkyo'))
        LOG.debug(PrettyFormatAny.form(l_onkyo.Devices, 'Devices'))
        #
        for _l_key, l_service in l_onkyo.Services.items():
            LOG.debug(PrettyFormatAny.form(l_service, 'Service'))
            if hasattr(l_service, 'Connection'):
                LOG.debug(PrettyFormatAny.form(l_service.Connection, 'Connection'))
            if hasattr(l_service, 'Host'):
                LOG.debug(PrettyFormatAny.form(l_service.Host, 'Host'))
            if hasattr(l_service, 'Access'):
                LOG.debug(PrettyFormatAny.form(l_service.Access, 'Access'))

    def _get_model_config(self, p_config):
        """
        """
        l_filename = 'onkyo_' + p_config
        l_yaml = self.m_config.read_config(l_filename)
        return l_yaml

    def _extract_one_device(self, p_config):
        """ Extract one device from the onkyo.yaml file and call the routine to extract the command .yaml file for that device.
        """
        # self.dump_struct()
        l_required = ['Name', 'Type', 'Host']
        l_obj = OnkyoDeviceInformation()
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Obj'))
        for l_key, l_value in p_config.items():
            if l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            elif l_key == 'Model':
                setattr(l_obj, l_key, l_value)
                l_yaml = self._get_model_config(l_value)
                l_obj.Commands = E_U.extract_device_config_file(l_yaml)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Onkyo Yaml is missing an entry for "{}"'.format(l_key))
        LOG.debug(PrettyFormatAny.form(l_obj, 'Obj'))
        LOG.info('Extracted device "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_devices(self, p_config):
        """ Extract all of the one or more onkyo devices from the onkyo.yaml file.
        """
        l_dict = {}
        for l_ix, l_value in enumerate(p_config):
            l_device = self._extract_one_device(l_value)
            l_dict[l_ix] = l_device
        return l_dict

    def _extract_all_onkyo(self, p_config, p_api):
        """ extract the contents of the onkyo.yaml file.
        """
        # self.dump_struct()
        l_required = ['Name', 'Device']
        l_obj = OnkyoPluginInformation()
        l_obj._Api = p_api
        for l_key, l_value in p_config.items():
            if l_key == 'Device':
                l_devices = self._extract_all_devices(l_value)
                l_obj.Devices = l_devices
                l_obj.DeviceCount = len(l_devices)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Onkyo Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def load_yaml_config(self, p_api):
        """ Read the onkyo.yaml file.
        """
        # LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Onkyo']
        except:
            LOG.warning('The config file does not start with "Onkyo:"')
            return None
        l_onkyo = self._extract_all_onkyo(l_yaml, p_api)
        # self.dump_struct()
        return l_onkyo


class Api(MqttActions):
    """This interfaces to all of PyHouse.
    """

    m_device_lst = []
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self):
        self.m_pyhouse_obj.House.Entertainment['onkyo'] = {}
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'HouseZZZ'))

    def LoadConfig(self):
        """ Read the Config for all Onkyo devices.
        """
        LOG.info("Loading Config - Version:{}".format(__version__))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'HouseZZZ'))
        self.m_pyhouse_obj.House.Entertainment['onkyo'] = self.m_local_config.load_yaml_config(self)

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.

        We have one or more Onkyo devices in this house to use/control.
        Connect to all of them.

        OnkyoDeviceInformation()

        """
        LOG.info('Start Onkyo.')
        l_devices = self.m_pyhouse_obj.House.Entertainment['onkyo'].Devices
        l_count = 0

        return

        for l_device_obj in l_devices.values():
            if l_device_obj._isRunning:
                LOG.info('Onkyo device {} is already running.'.format(l_device_obj.Name))
                continue
            l_count += 1
            self.onkyo_start_connecting(self.m_pyhouse_obj, l_device_obj)
            self.m_device_lst.append(l_device_obj)
        LOG.info("Started {} Onkyo devices".format(l_count))

    def SaveConfig(self):
        # LOG.info("Saved Onkyo XML.")
        return

    def Stop(self):
        LOG.info("Stopped.")

    def run_queue(self, p_device_obj):
        """
        """
        # LOG.debug('Started to run_queue. {}'.format(PrettyFormatAny.form(p_device_obj, 'Device', 180)))
        # LOG.debug('Started to run_queue. {}'.format(PrettyFormatAny.form(p_device_obj._Queue, 'Queue', 180)))
        if p_device_obj._Queue.empty():
            # LOG.debug('Queue is empty')
            _l_runID = self.m_pyhouse_obj._Twisted.Reactor.callLater(60.0, self.run_queue, p_device_obj)
        else:
            l_queue = p_device_obj._Queue.get()
            LOG.debug(PrettyFormatAny.form(l_queue, 'Queue', 190))
            self.send_command(p_device_obj, l_queue)
            _l_runID = self.m_pyhouse_obj._Twisted.Reactor.callLater(0.5, self.run_queue, p_device_obj)

# ## END DBK
