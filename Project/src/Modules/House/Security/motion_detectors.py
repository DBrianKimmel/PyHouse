"""
@name:      Modules/House/Security/motion_sensor.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on aug 26, 2019
@Summary:

"""

__updated__ = '2019-12-29'
__version_info__ = (19, 8, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.MotionSensor   ')

CONFIG_NAME = 'motiondetectors'


class MotionDetectorInformation:
    """ This is the motion detector data

    ==> PyHouse.House.Security.MotionDetector.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Security'
        self.DeviceSubType = 'MotionDetector'
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()
        self.Motion = None
        self.Timeout = 0


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_motion_detector(self, p_config) -> dict:
        """ Extract the config info for one button.
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = MotionDetectorInformation()
        l_required = ['Name', 'Family']
        l_allowed = ['Room']
        l_groupfields = ['Family', 'Room']
        for l_key, l_value in p_config.items():
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted Motion Detector "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_motion_detectors(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_sensor in enumerate(p_config):
            l_sensor_obj = self._extract_one_motion_detector(l_sensor)
            l_dict[l_ix] = l_sensor_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Motion_Detectors']
        except:
            LOG.warning('The config file does not start with "Motion_Detectors:"')
            return None
        l_motion = self._extract_all_motion_detectors(l_yaml)
        return l_motion


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
        self.m_pyhouse_obj.House.Security.MotionDetectors = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_pyhouse_obj.House.Security.MotionDetectors = self.m_local_config.load_yaml_config()

    def SaveConfig(self):
        """
        """
        pass

    def Start(self):
        """
        """

    def Stop(self):
        """
        """

# ## END DBK
