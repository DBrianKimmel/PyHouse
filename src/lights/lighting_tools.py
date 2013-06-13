#!/usr/bin/env python

"""Tools for use in all lighting component files.
"""

# Import system type stuff

# Import PyHouse files


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 =
# 3 =


class LightingTools(object):

    def getBool(self, p_dict, p_field, p_default = 'False'):
        """Get field and return a bool as the value of the field.
        """
        l_field = p_dict.get(p_field, p_default)
        if l_field == 'False':
            return False
        if l_field == 'True':
            return True
        return False

    def getInt(self, p_dict, p_field):
        """Get a field and return as an int.
        """
        l_field = p_dict.get(p_field, 0)
        try:
            l_field = int(l_field, 0)
        except TypeError:
            l_field = int(l_field)
        return l_field

    def getFloat(self, p_dict, p_field):
        """Get field as a number - floating point is ok.
        """
        try:
            l_field = float(p_dict.get(p_field, 0.0))
        except TypeError:
            l_field = 0.0
        return l_field

    def getText(self, p_dict, p_field):
        l_field = p_dict.get(p_field, '')
        return l_field

    def getValue(self, p_dict, p_field):
        """Return None if config value is 'None'
        """
        l_field = p_dict.get(p_field, None)
        if l_field == 'None': l_field = None
        return l_field

# ## END DBK
