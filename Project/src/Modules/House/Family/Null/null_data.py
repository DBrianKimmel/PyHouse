"""
@name:      Modules/House/Family/Null/Null_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 10, 2014
@summary:   This module is for invalid families.

"""

__updated__ = '2020-01-20'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import LightControlInformation


class NullData(LightControlInformation):
    """
    This is known only within the Null family package.
    """

    def __init__(self):
        super(NullData, self).__init__()
        self.Family.Name = 'Null'

# ## END DBK
