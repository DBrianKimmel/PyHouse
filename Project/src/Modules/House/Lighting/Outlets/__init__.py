"""
@name:      Modules/House/Lighting/Outlets/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb  9, 2020

"""

__updated__ = '2020-02-09'
__version_info__ = (20, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

CONFIG_NAME = 'outlets'


class OutletInformation:
    """ This is the information that the user needs to enter to uniquely define a Outlet.
    """

    def __init__(self) -> None:
        self.Name = None
        self.Comment = None  # Optional
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Outlet'
        self.LastUpdate = None  # Not user entered but maintained
        self.Uuid = None  # Not user entered but maintained
        self.Family = None
        self.Room = None

# ## END DBK
