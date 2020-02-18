"""
@name:      Modules/House/Security/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__version_info__ = (19, 12, 20)
__version__ = '.'.join(map(str, __version_info__))

MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'Cameras',
    'Doorbells',
    'Garagedoors',
    'Motiondetectors'
    ]


class SecurityClass:
    """
    """

    def __init__(self):
        pass


class SecurityInformation:
    """
    DeviceType = 3
    ==> PyHouse.House.Security.xxx as in the def below
    """

    def __init__(self):
        self.Cameras = {}
        self.Doorbells = {}
        self.Garagedoors = {}
        self.Motiondetectors = {}

# ## END DBK
