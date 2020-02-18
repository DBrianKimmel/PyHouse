"""
@name:      Modules/Core/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@note:      Created on Mar 1, 2014
@license:   MIT License

Core is the main portion of every PyHouse node.
It is always present.
"""

__updated__ = '2020-02-13'
__version_info__ = (20, 2, 10)
__version__ = '.'.join(map(str, __version_info__))


class ConfigInformation:
    """ A collection of Yaml data used for Configuration

    ==> PyHouse._Config.xxx
    """

    def __init__(self):
        self.YamlFileName = None
        # self.YamlTree = {}  # ConfigFileInformation()


class ConfigFileInformation:
    """ ==? pyhouse_obj._Config {}

    Used to record where each confile is located so it can be updated.
    """

    def __init__(self) -> None:
        self.Name: Union[str, None] = None  # LowerCase filemane without .yaml
        self.Path: Union[str, None] = None  # Full path to file


class AccessInformation:
    """
    """

    def __init__(self):
        """
        """
        self.Name = None  # Username
        self.Password = None
        self.ApiKey = None
        self.AccessKey = None


class HostInformation:
    """ Used for all host related information
    This is usually not completely filled in.
    Twisted kinda likes hostnames instead of IP addresses.
    """

    def __init__(self):
        self.Name = None
        self.Port = None
        self.IPv4 = None
        self.IPv6 = None


class RoomLocationInformation:
    """
    """

    def __init__(self):
        self.Name = None

# ## END DBK
