"""
@name:      PyHouse/src/Modules.Core.Utilities.obj_defs.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 7, 2015
@Summary:

"""

class GetPyhouse(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def House(self):
        return self.m_pyhouse_obj.House

    def Schedules(self):
        return self.m_pyhouse_obj.House.Schedules

    def Location(self):
        return self.m_pyhouse_obj.House.Location

# ## END DBK
