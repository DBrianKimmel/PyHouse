"""
@name:      Modules/House/Family/insteon/insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This is the main module for the Insteon family of device controllers.
It is imported once and instantiates insteon_plm for each local controller and insteon_hub one time for each hub.

"""

__updated__ = '2019-11-28'
__version_info__ = (19, 10, 15)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_device ')

CONFIG_NAME = 'insteon'


class InsteonInformation:
    """
    """

    def __init__(self):
        self.Family = None
        self.Address = None  # '1A.B2.3C'
        self._DevCat = 0  # Dev-Cat and Sub-Cat (2 bytes)
        self._EngineVersion = 2
        self._FirmwareVersion = 0
        self._ProductKey = ''  # 3 bytes
        self._Links = {}


class InsteonCommandData:
    """ This holds the outstanding Insteon commands.
    """

    def __init__(self):
        """
        """
        self.Device = None  # InsteonID as a key


class Utility:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _is_valid_controller(self, p_controller_obj):
        if p_controller_obj.Family.Name.lower() == 'insteon':
            # LOG.debug('Insteon')
            return True
        else:
            LOG.debug(PrettyFormatAny.form(p_controller_obj.Family, 'Family'))
            LOG.debug('Not Insteon')
            return False

    def _start_one_plm(self, p_controller_obj):
        """
        import PLM module when we run this otherwise we will get a circular import
        @param p_controller_obj: ==> ControllerInformation(CoreLightingData)
        @return: None if no PLM, Api Pointer if OK
        """
        from Modules.House.Family.insteon import insteon_plm
        l_plmApi = insteon_plm.Api(self.m_pyhouse_obj, p_controller_obj)
        p_controller_obj._HandlerApi = l_plmApi
        if l_plmApi.Start():
            LOG.info('Successfully started Insteon controller "{}"'.format(p_controller_obj.Name))
            # p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerCount += 1
            # p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerTypes.append('insteon')
            return l_plmApi
        else:
            LOG.error('Controller {} failed to start.'.format(p_controller_obj.Name))
            p_controller_obj._isFunctional = False
            return None

    def start_all_hubs(self):
        """
        Run thru all the controllers and find all active Insteon Hubs.
        Start the controller and its driver.

        @return: a list of the Insteon_PLM Api references
        """
        l_list = []
        return l_list

    def start_all_plms(self):
        """
        Run thru all the controllers and find the first active Insteon controller.
        Start the controller and its driver.

        @return: a list of the Insteon_PLM Api references
        """
        l_list = []
        l_controllers = self.m_pyhouse_obj.House.Lighting.Controllers
        # LOG.debug(PrettyFormatAny.form(l_controllers, 'Controllers'))
        if l_controllers == None:
            return l_list
        for l_controller_obj in l_controllers.values():
            if l_controller_obj == None:
                LOG.error('Something is wrong with config.  Device is missing all information.')
                continue
            # LOG.debug(PrettyFormatAny.form(l_controller_obj, 'Controller'))
            if not l_controller_obj._isLocal:
                LOG.info('Controller "{}" is not local'.format(l_controller_obj.Name))
                continue
            LOG.info('Checking Controller "{}"'.format(l_controller_obj.Name))
            if self._is_valid_controller(l_controller_obj):
                # LOG.debug('Insteon Controller: "{}" - will be started.'.format(l_controller_obj.Name))
                l_ret = self._start_one_plm(l_controller_obj)
                if l_ret != None:
                    l_list.append(l_ret)
                else:
                    LOG.error('Could not start PLM')
            else:
                LOG.warn('Not an insteon controller "{}"'.format(l_controller_obj.Name))
                pass  #  Not interested in this controller. (Non-Insteon)
        LOG.info('Found the following insteon PLMs: {}'.format(l_list))
        return l_list

    def stop_all_controllers(self):
        l_controllers = self.m_pyhouse_obj.House.Lighting.Controllers
        if l_controllers == None:
            return
        for l_controller_obj in l_controllers.values():
            if self._is_valid_controller(l_controller_obj):
                l_controller_obj._HandlerApi.Stop(l_controller_obj)


class LocalConfig:
    """
    """

    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_modules_info(self, p_yaml):
        """
        """
        _l_required = ['Name']
        l_obj = InsteonInformation()
        try:
            l_modules = p_yaml['Modules']
        except:
            LOG.warn('No "Modules" list in "house.yaml"')
            return
        for l_module in l_modules:
            LOG.debug('found Module "{}" in house config file.'.format(l_module))
        return l_obj

    def _extract_one_insteon(self, p_config):
        """
        """
        # LOG.debug('Config: {}'.format(p_config))
        l_required = ['Name', 'Family', 'Host', 'Access']
        l_obj = InsteonInformation()
        for l_key, l_value in p_config.items():
            LOG.debug('Key: {}; Value: {}'.format(l_key, l_value))
            if l_key == 'Access':
                l_obj.Access = self.m_config.extract_access_group(l_value)
            elif l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Insteon config is missing an entry for "{}"'.format(l_key))
        LOG.debug(PrettyFormatAny.form(l_obj, 'Insteon'))
        return l_obj

    def _extract_all_devices(self, p_config):
        """
        """
        _l_insteon = {}
        # LOG.debug('Insteon Config: {}'.format(p_config))
        for _l_ix, l_value in enumerate(p_config):
            _l_obj = self._extract_one_insteon(l_value)

    def load_yaml_config(self):
        """ Read the Rooms.Yaml file.
        It contains Rooms data for all rooms in the house.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        # self.m_pyhouse_obj.House.Family
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Insteon']
        except:
            LOG.warn('The config file does not start with "Insteon:"')
            return None
        l_hue = self._extract_all_devices(l_yaml)
        # self.m_pyhouse_obj.House.Name = l_house.Name
        return l_hue  # for testing purposes


class Api:
    """
    These are the public methods available to use Devices from any family.
    """

    m_plm_list = []
    m_hub_list = []
    m_local_config = None
    m_pyhouse_obj = None
    m_utility = None

    def __init__(self, p_pyhouse_obj):
        # p_pyhouse_obj.House._Commands['insteon'] = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_utility = Utility(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info('Initialized')

    def LoadConfig(self):
        """
        """
        self.m_local_config.load_yaml_config()

    def Start(self):
        """
        Note that some controllers may not be available on this node.
        """
        LOG.info('Starting the Insteon Device.')
        self.m_plm_list = self.m_utility.start_all_plms()
        self.m_hub_list = self.m_utility.start_all_hubs()
        LOG.info('Started {} Insteon Devices.'.format(len(self.m_plm_list)))

    def SaveConfig(self):
        """
        """

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'pyhouse')
        try:
            self.m_utility.stop_all_controllers()
        except AttributeError as e_err:
            LOG.info('Stop Warning - {}'.format(e_err))  #  no controllers for house(House is being added)

    def Control(self, _p_pyhouse_obj, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj:  ==> ControllerInformation()
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params
        """
        LOG.debug('Controlling Insteon device "{}" using "{}"'.format(p_device_obj.Name, p_controller_obj.Name))
        # if not p_controller_obj._isFunctional:
        #    return
        # l_plm = p_controller_obj._HandlerApi  # (self.m_pyhouse_obj)
        # [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]
        for l_ctlr in self.m_plm_list:
            l_ctlr.Control(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
