"""
@name:      Modules/House/Family/hue/hue_config.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-10-15'

# Import system type stuff

# Import PyMh files

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

# ## END DBK
