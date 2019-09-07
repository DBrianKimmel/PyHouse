"""
@name:      Modules/Houe/Family/abstract_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 19, 2014
@Summary:

"""

__updated__ = '2019-07-31'


class API:

    def Start(self, _p_pyhouse_obj):
        assert('Must be defined')

    def Stop(self):
        assert('Must be defined')

    def LoadConfig(self):
        assert('Must be defined')

    def SaveConfig(self):
        assert('Must be defined')

# ## END DBK
