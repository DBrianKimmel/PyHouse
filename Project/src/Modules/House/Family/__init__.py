"""
@name:      Modules/House/Family/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:

To add a family named 'NewFamily', do the following:
    * Add a package named 'New_Family'.
    * Add the family name (Capitalized) to the list MODULES below.
    * Add a module named <NewFamily>_device.py
    * Add any other modules needed by the Device module.
        <Newfamily>_xml
        <NewFamily>_data
        ...
    * A module to interface with the controller is recommended.
        <NewFamily>_pim

"""

__updated__ = '2020-02-21'
__version_info__ = (20, 2, 21)
__version__ = '.'.join(map(str, __version_info__))

CONFIG_NAME = 'families'

MODULES = [
    'Acurite',
    'Hue',
    'Insteon',
    'Lutron',
    'Sonoff',
    'Upb',
    'X10',
    'Zwave',
    'Null'
    ]


class FamilyInformation:
    """ Info about a family
    This points to the
    ==> PyHouse_obj.House.Family[<familyname>]
    indexed by lowercased family name "insteon"
    """

    def __init__(self):
        self.Name = None  # Family Name
        self.Module = None  # FamilyModuleInformation()
        self._Api = None  # of the family_device.py file


class DeviceFamilyInformation:
    """ This is used for things like Lights
    """

    def __init__(self):
        self.Name = None
        self.Type = None
        self.Address = None

# ## END DBK
