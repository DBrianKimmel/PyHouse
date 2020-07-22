"""
@name:      Modules/Housing/Pool/pool_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2020 by D. Brian Kimmel
@note:      Created on Feb 13, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2019-12-30'

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import BaseUUIDObject


class PoolData(BaseUUIDObject):
    """ Holds information about the pool(s)

    ==> PyHouse.House.Pools.{}.
    """

    def __init__(self):
        super(PoolData, self).__init__()
        self.PoolType = None  # 'Pool', 'Pond', 'HotTub'

# ## END DBK
