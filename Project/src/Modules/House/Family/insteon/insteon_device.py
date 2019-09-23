"""
@name:      Modules/House/Family/insteon/insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This is the main module for the Insteon family of device controllers.
It is imported once and instantiated for each local controller

"""

__updated__ = '2019-09-22'
__version_info__ = (19, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.insteon_device ')


class InsteonCommandData:
    """ This holds the outstanding Insteon commands.
    """

    def __init__(self):
        """
        """
        self.Device = None  # InsteonID as a key


class InsteonInformation:
    """
    """

    def __init__(self):
        self.Family = None
        self.Address = None  # '1A.B3.3C'
        self._DevCat = 0  # DevCat and SubCat (2 bytes)
        self._EngineVersion = 2
        self._FirmwareVersion = 0
        self._GroupList = ''
        self._GroupNumber = 0
        self._ProductKey = ''  # 3 bytes
        self._Links = {}


class Config:
    """
    This class and methods are pointed to by family.py and must be the same in every Device package.
    """

    def extract_family_config(self, p_config):
        """
        Device:
           Family:
              Name: Insteon
              Address: 12.34.56

        @param p_config: is the yaml fragment containing the family tree.
        """
        l_obj = InsteonInformation()
        l_required = ['Name', 'Address']
        for l_key, l_value in p_config.items():  # A map
            print('Insteon Family Config Key:{}; Value{}'.format(l_key, l_value))
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.error('Insteon Family config is missing a required entry for "{}"'.format(l_key))
        return l_obj


class lightingUtility:
    """
    """

    @staticmethod
    def _is_valid_controller(p_controller_obj):
        if p_controller_obj.Family.Name.lower() == 'insteon':
            LOG.debug('Insteon')
            return True
        else:
            LOG.debug(PrettyFormatAny.form(p_controller_obj.Family, 'Family'))
            LOG.debug('Not Insteon')
            return False

    @staticmethod
    def _start_one_plm(p_pyhouse_obj, p_controller_obj):
        """
        import PLM module when we run this otherwise we will get a circular import
        @param p_controller_obj: ==> ControllerInformation(CoreLightingData)
        @return: None if no PLM, API Pointer if OK
        """
        from Modules.House.Family.insteon import insteon_plm
        l_plmAPI = insteon_plm.API(p_pyhouse_obj, p_controller_obj)
        p_controller_obj._HandlerAPI = l_plmAPI
        if l_plmAPI.Start():
            LOG.info('Successfully started Insteon controller "{}"'.format(p_controller_obj.Name))
            # p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerCount += 1
            # p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerTypes.append('insteon')
            return l_plmAPI
        else:
            LOG.error('Controller {} failed to start.'.format(p_controller_obj.Name))
            p_controller_obj._isFunctional = False
            return None

    def _start_all_controllers(self, p_pyhouse_obj):
        """
        Run thru all the controllers and find the first active Insteon controller.
        Start the controller and its driver.

        @return: a list of the Insteon_PLM API references
        """
        l_list = []
        l_controllers = p_pyhouse_obj.House.Lighting.Controllers
        LOG.debug(PrettyFormatAny.form(l_controllers, 'Controllers'))
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
            LOG.info('Starting Controller "{}"'.format(l_controller_obj.Name))
            if lightingUtility._is_valid_controller(l_controller_obj):
                LOG.debug('Insteon Controller: "{}" - will be started.'.format(l_controller_obj.Name))
                l_ret = lightingUtility._start_one_plm(p_pyhouse_obj, l_controller_obj)
                l_list.append(l_ret)
            else:
                LOG.warn('Not an insteon controller "{}"'.format(l_controller_obj.Name))
                pass  #  Not interested in this controller. (Non-Insteon)
        LOG.info('Found the following insteon controllers: {}'.format(l_list))
        return l_list

    @staticmethod
    def _stop_all_controllers(p_pyhouse_obj):
        l_controllers = p_pyhouse_obj.House.Lighting.Controllers
        if l_controllers == None:
            return
        for l_controller_obj in l_controllers.values():
            if lightingUtility._is_valid_controller(l_controller_obj):
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)


class API:
    """
    These are the public methods available to use Devices from any family.
    """

    m_plm_list = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        # p_pyhouse_obj.House._Commands['insteon'] = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Created an instance of Insteon_device.')

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config')

    def Start(self):
        """ Note that some controllers may not be available on this node.
        """
        LOG.info('Starting the Insteon Controller.')
        self.m_plm_list = lightingUtility()._start_all_controllers(self.m_pyhouse_obj)
        LOG.info('Started {} Insteon Controllers.'.format(len(self.m_plm_list)))

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config')

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'pyhouse')
        try:
            lightingUtility._stop_all_controllers(self.m_pyhouse_obj)
        except AttributeError as e_err:
            LOG.info('Stop Warning - {}'.format(e_err))  #  no controllers for house(House is being added)

    def AbstractControlLight(self, _p_pyhouse_obj, p_device_obj, p_controller_obj, p_control):
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
        # l_plm = p_controller_obj._HandlerAPI  # (self.m_pyhouse_obj)
        # [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]
        for l_ctlr in self.m_plm_list:
            l_ctlr.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
