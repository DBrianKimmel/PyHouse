"""
@name:      Modules/House/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2019-10-16'
__version_info__ = (19, 10, 4)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities.extract_tools import get_mqtt_field
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
# from Modules.House.Security.cameras import Api as cameraApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')

CONFIG_NAME = 'security'
# LOCATION = House.Security

MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'Cameras',
    'Door_Bells',
    'Garage_Doors',
    'Motion_Sensors'
    ]


class SecurityData:
    """
    DeviceType = 3
    ==> PyHouse.House.Security.xxx as in the def below
    """

    def __init__(self):
        self.GarageDoors = {}  # DeviceSubtype = 1
        self.MotionSensors = {}  # DeviceSubtype = 2


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/security/<type>/<Name>
        <type> = garage door, motion sensor, camera
        """
        l_logmsg = '\tSecurity:\n'
        if p_topic[0] == 'garage_door':
            l_logmsg += '\tGarage Door: {}\n'.format(get_mqtt_field(p_message, 'Name'))
        elif p_topic[0] == 'motion_sensor':
            l_logmsg += '\tMotion Sensor:{}\n\t{}'.format(get_mqtt_field(p_message, 'Name'), get_mqtt_field(p_message, 'Status'))
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Security msg', 160))
        return l_logmsg


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def import_modules(self):
        """
        """
        self.m_config.import_modules(MODULES, 'Modules.House.Security')
        pass


class Api:
    """ Called from house.
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        # self.m_api = cameraApi(p_pyhouse_obj)
        LOG.info('Initialized')

    def LoadConfig(self):
        """ Load the Security Information
        """
        LOG.info('Loading Config')
        self.m_pyhouse_obj.House.Security = SecurityData()  # Clear before loading
        self.m_local_config.import_modules()
        LOG.info('Loaded Config')
        return self.m_pyhouse_obj.House.Security

    def Start(self):
        # self.m_api.Start()
        LOG.info("Started.")

    def SaveConfig(self):
        LOG.info("Saved Config.")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
