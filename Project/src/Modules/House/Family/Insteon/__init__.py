"""
@name:      Modules/House/Family/Insteon/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This interfaces PyHouse to the Insteon family of products.
This includes light switches, thermostats and a number of other devices.
"""

__updated__ = '2020-02-18'
__version_info__ = (20, 1, 31)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [
    'Lighting',
    'Hvac',
    'Security'
    ]


class InsteonInformation:
    """
    """

    def __init__(self) -> None:
        self.Family: str = 'insteon'
        self.Address: str = '00.00.00'
        self._Private: InsteonPrivateInformation = InsteonPrivateInformation()
        self._Links = {}


class InsteonPrivateInformation:
    """
    """

    def __init__(self) -> None:
        self._DevCat: int = 0  # Dev-Cat and Sub-Cat (2 bytes)
        self._EngineVersion: int = 2
        self._FirmwareVersion: int = 0
        self._ProductKey: str = '00.00.00'

# ## END DBK
