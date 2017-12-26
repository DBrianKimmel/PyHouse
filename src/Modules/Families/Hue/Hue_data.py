"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_data.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-23'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightData


class HueData(LightData):
    """
    This is known only within the hUE family package.
    """

    def __init__(self):
        super(HueData, self).__init__()
        self.DeviceFamily = 'Hue'

# ## END DBK
