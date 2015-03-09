"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Families/abstract_device.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 19, 2014
@Summary:

"""

class API(object):

    def Start(self, p_pyhouse_obj):
        assert('Must be defined')

    def Stop(self):
        assert('Must be defined')

    def ReadXml(self, p_pyhouse_obj):
        assert('Must be defined')

    def WriteXml(self, p_pyhouse_obj):
        assert('Must be defined')


# ## END DBK
