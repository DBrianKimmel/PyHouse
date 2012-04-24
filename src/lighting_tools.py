#!/usr/bin/env python

"""Tools for use in all lighting component files.
"""


# Import system type stuff
import inspect
from inspect import getmembers


class LightingTools(object):

    def getInt(self, p_dict, p_field):
        l_field = p_dict.get(p_field, 0)
        try:
            l_field = int(l_field, 0)
        except:
            l_field = int(l_field)
        return l_field

    def getBool(self, p_dict, p_field):
        l_field = p_dict.get(p_field, 0)
        if l_field == 0:
            return False
        if l_field.lower() == 'true':
            return True
        return False

    def getValue(self, p_dict, p_field):
        """Return None if config value is 'None'
        """
        l_field = p_dict.get(p_field, None)
        if l_field == 'None': l_field = None
        return l_field

    def convert_to_dict(self, p_obj):
        l_dict = {}
        l_list = getmembers(p_obj)
        for l_pair in l_list:
            l_ix = l_list[0].find('__')
            if l_ix > 0:
                l_pair[0] = l_pair[0][(l_ix + 2):]
            l_dict[l_pair[0]] = l_pair[1]
        return l_dict

### END
