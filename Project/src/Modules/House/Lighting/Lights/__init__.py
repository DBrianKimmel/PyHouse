"""
@name:      Modules/House/Lighting/Lights/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb  5, 2020

"""

__updated__ = '2020-02-09'
__version_info__ = (20, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

CONFIG_NAME = 'lights'


class LightInformation:
    """ This is the information that the user needs to enter to uniquely define a light.
    """
    yaml_tag = u'!light'

    def __init__(self, Name=None) -> None:
        self.Name: Union[str, None] = Name
        self.Comment: Union[str, None] = None
        self.DeviceType: str = 'Lighting'
        self.DeviceSubType: str = 'Light'
        self.Family = None
        self.Room = None

    def __repr__(self):
        """
        """
        l_ret = ''
        l_ret += '{}'.format(self.Name)
        l_ret += '; {}/{}'.format(str(self.DeviceType), str(self.DeviceSubType))
        l_ret += '; Family: {}'.format(self.Family.Name)
        return l_ret

# ## END DBK
