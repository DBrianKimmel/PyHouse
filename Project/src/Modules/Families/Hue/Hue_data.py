"""
-*- test-case-name: PyHouse/src/Modules/Families/Hue/Hue_data.py -*-

@name:      PyHouse/src/Modules/Families/Hue/Hue_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-01-21'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import DeviceData
from Modules.Housing.Lighting.lighting_lights import LightData


class HueData(LightData):
    """
    This is known only within the Hue family package.
    """

    def __init__(self):
        super(HueData, self).__init__()
        self.DeviceFamily = 'Hue'
        self.HueLightIndex = 0


class HueHubData(DeviceData):
    """
    """

    def __init__(self):
        super(HueHubData, self).__init__()
        self.DeviceType = 4
        self.ApiKey = 'None defined'


class HueAddInData(object):
    """ This is the Hue specific data.
    It will be added into device objects that are Insteon.
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
