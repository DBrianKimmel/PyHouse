"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_data -*-

@name: PyHouse/src/Modules/families/Null/Null_data.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 10, 2014
@summary: This module is for invalid families.

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightData


class NullData(LightData):
    """
    This is known only within the Null family package.
    """

    def __init__(self):
        super(NullData, self).__init__()
        self.ControllerFamily = 'Null'

# ## END DBK
