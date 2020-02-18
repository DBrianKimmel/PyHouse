"""
@name:      Modules/House/Lighting/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.
"""

__updated__ = '2020-02-16'
__version_info__ = (20, 1, 20)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [
    'Buttons',
    'Controllers',
    'Lights',
    'Outlets'
    ]

CONFIG_NAME = 'lighting'


class LightingInformation:
    """
    ==> PyHouse.House.Lighting.xxx as in the def below
    """

    def __init__(self):
        self.Buttons = None  # ==> ButtonInformation()
        self.Controllers = None  # ==> ControllerInformation()
        self.Lights = None  # ==> LightInformation()
        self.Outlets = None  # ==> OutletInformation
        self._Apis = {}


class LightingClass:
    """
    """

    def __init__(self):
        pass

# ## END DBK
