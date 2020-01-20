"""
@name:      Modules/House/Family/Hue/Hue_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-08-01'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import DeviceInformation
from Modules.House.Lighting.lights import LightControlInformation


class HueLightData(LightControlInformation):
    """
    This is known only within the Hue family package.
    """

    def __init__(self):
        super(HueLightData, self).__init__()
        self.DeviceFamily = 'Hue'
        self.HueLightIndex = 0  # The key number used by the hue hub to identify the light
        self.HueUniqueId = None


class HueHubData(DeviceInformation):
    """
    """

    def __init__(self):
        super(HueHubData, self).__init__()
        self.DeviceType = 'Bridge'
        self.ApiKey = 'None defined'


class HueAddInData(object):
    """ This is the Hue specific data.
    It will be added into device objects that are Hue.
    """

    def __init__(self):
        self.ApiKey = None


class HueueQueue(object):
    """ This is the contents of a Queue Entry
    """

    def __init__(self):
        self.Uri = None
        self.Command = None  # for convenience
        self.Headers = None
        self.Payload = None

# ## END DBK
