"""
@name:      Modules/House/Family/hue/hue_config.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-09-16'

# Import system type stuff

# Import PyMh files
from Modules.House.Family.hue.hue_data import HueAddInData

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_xml    ')


class HueInformation:
    """
    """

    def __init__(self):
        self.Family = None
        self.Address = None
        self.Host = None
        self.Port = None


class Config:
    """
    """

    def extract_family_config(self, p_config):
        """
        Device:
           Family:
              Name: hue

        @param p_config: is the yaml fragment containing the family tree.
        """
        l_obj = HueInformation()
        l_required = ['Name', 'Address']
        for l_key, l_value in p_config.items():  # A map
            print('Hue Family Config Key:{}; Value{}'.format(l_key, l_value))
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.error('Hue Family config is missing a required entry for "{}"'.format(l_key))
        return l_obj

# ## END DBK
