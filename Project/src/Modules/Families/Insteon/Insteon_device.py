"""
@name:      Modules/Families/Insteon/Insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This is the main module for the Insteon family of devices.
It provides the single interface into the family.
Several other Insteon modules are included by this and are invisible to the other families.

This module loads the information about all the Insteon devices.

InsteonControllers
serial_port

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-07-21'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Device ')


class InsteonCommandData():
    """ This holds the outstanding Insteon commands.
    """

    def __init__(self):
        """
        """
        self.Device = None  # InsteonID as a key


class Utility(object):
    """
    """

    @staticmethod
    def _is_insteon(p_controller_obj):
        try:
            return p_controller_obj.Family.Name == 'Insteon'
        except AttributeError:
            return False

    @staticmethod
    def _is_active(p_controller_obj):
        try:
            return p_controller_obj.Active == True
        except AttributeError:
            return False

    @staticmethod
    def _is_valid_controller(p_controller_obj):
        return Utility._is_insteon(p_controller_obj)  # and Utility._is_active(p_controller_obj)

    @staticmethod
    def _start_plm(p_pyhouse_obj, p_controller_obj):
        """
        import PLM module when we run this otherwise we will get a circular import
        @param p_controller_obj: ==> ControllerInformation(CoreLightingData)
        @return: None if no PLM, API Pointer if OK
        """
        from Modules.Families.Insteon import Insteon_PLM
        l_plmAPI = Insteon_PLM.API()
        l_uuid = p_pyhouse_obj.Computer.UUID
        p_controller_obj._HandlerAPI = l_plmAPI
        if l_plmAPI.Start(p_pyhouse_obj, p_controller_obj):
            LOG.info('Successfully started Insteon controller {}'.format(p_controller_obj.Name))
            p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerCount += 1
            p_pyhouse_obj.Computer.Nodes[l_uuid].ControllerTypes.append('Insteon')
            return l_plmAPI
        else:
            LOG.error('Controller {} failed to start.'.format(p_controller_obj.Name))
            p_controller_obj._isFunctional = False
            return None

    def _start_all_controllers(self, p_pyhouse_obj):
        """
        Run thru all the controllers and find the first active Insteon controller.
        Start the controller and its driver.

        Return the Insteon_PLM API reference if one is found:
        """
        #  l_count = 0
        LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House.Lighting.Controllers, 'Lighting.API.Controllers', 190))
        for l_controller_obj in p_pyhouse_obj.House.Lighting.Controllers.values():
            if l_controller_obj == None:
                continue
            LOG.debug('Trying to start controller "{}"'.format(l_controller_obj.Name))
            LOG.debug(PrettyFormatAny.form(l_controller_obj, 'Controller', 190))
            if Utility._is_valid_controller(l_controller_obj):
                LOG.debug('Insteon Controller: {} - will be started.'.format(l_controller_obj.Name))
                l_ret = Utility._start_plm(p_pyhouse_obj, l_controller_obj)
                return l_ret
            elif Utility._is_insteon(l_controller_obj):
                LOG.debug('Insteon Controller: {} - will NOT be started per config file.'.format(l_controller_obj.Name))
            else:
                LOG.debug('Not an insteon controller')
                pass  #  Not interested in this controller. (Non-Insteon)
        return None

    @staticmethod
    def _stop_all_controllers(p_pyhouse_obj):
        for l_controller_obj in p_pyhouse_obj.House.Lighting.Controllers.values():
            if Utility._is_valid_controller(l_controller_obj):
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)


class API:
    """
    These are the public methods available to use Devices from any family.
    """

    m_plm = None

    def __init__(self, p_pyhouse_obj):
        p_pyhouse_obj.House._Commands['Insteon'] = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_plm = None
        LOG.info('Created an instance of Insteon_device.')

    def LoadConfig(self):
        """
        """

    def Start(self):
        """ Note that the controller may not be available on this node.
        """
        self.m_plm = Utility()._start_all_controllers(self.m_pyhouse_obj)
        LOG.info('Started the Insteon Controllers.')

    def Stop(self):
        try:
            Utility._stop_all_controllers(self.m_pyhouse_obj)
        except AttributeError as e_err:
            LOG.info('Stop Warning - {}'.format(e_err))  #  no controllers for house(House is being added)

    def AbstractControlLight(self, _p_pyhouse_obj, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj: ControllerInformation()
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params
        """
        LOG.debug('Controlling Insteon device "{}" using "{}"'.format(p_device_obj.Name, p_controller_obj.Name))
        if not p_controller_obj._isFunctional:
            return
        # l_plm = p_controller_obj._HandlerAPI  # (self.m_pyhouse_obj)
        self.m_plm.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
