"""
@name:      Modules/House/Family/insteon/insteon_config.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul163, 2019
@license:   MIT License
@summary:   This module is for Insteon

This module merges the Insteon specific information (InsteonData) with the generic controllerI Information (ControllerInformation)
 giving an expanded ControllerInformation.
"""

__updated__ = '2019-08-28'

#  Import system type stuff

#  Import PyMh files

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Insteon_conf')


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

# ## END DBK
