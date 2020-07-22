"""
@name:      Modules/House/Family/insteon/insteon_button.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2020 by D. Brian Kimmel
@note:      Created on Aug 18, 2019
@license:   MIT License
@summary:

We get these .

"""

__updated__ = '2020-02-18'

#  Import system type stuff

#  Import PyMh files

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_Button ')


class LocalConfig:
    """
    """


class Discovery:
    """
    """


class ButtonActions:
    """
    """

    def initial_button_load(self):
        """
        """
        if p_obj.Family.Name.lower() == 'insteon':
            self._get_engine_version(p_controller_obj, p_obj)
            self._get_id_request(p_controller_obj, p_obj)
            self._get_one_device_status(p_controller_obj, p_obj)
        else:
            LOG.warning('Skipping "{}" "{}" device "{}"'.format(p_obj.DeviceType, p_obj.DeviceSubType, p_obj.Name))
            pass

# ## END DBK
