"""
-*- test-case-name: PyHouse/Project/src/Modules/Housing/Lighting/lighting_utility.py -*-

@name:      PyHouse/Project/src/Modules/Housing/Lighting/lighting_utility.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jan 20, 2019
@license:   MIT License
@summary:

"""

__updated__ = '2019-05-08'

#  Import system type stuff

#  Import PyMh files
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.LightUtility   ')


class Utility:
    """
    """

    def _test_object_by_id(self, p_obj, name=None, key=None, UUID=None):
        """
        Return the device object for a house using the given value.
        A name, key or UUID may be used to identify the device.

        @return: the Device object found or None.
        """
        if name != None and p_obj.Name == name:
            return p_obj
        elif key != None and p_obj.Key == key:
            return p_obj
        elif UUID != None and p_obj.UUID == UUID:
            return p_obj
        elif UUID != None and p_obj.UUID == UUID:
            return p_obj
        return None

    def get_object_by_id(self, p_objs, name=None, key=None, UUID=None):
        """
        Return the device object from a dict of objects using the given value.
        one of several things may be used for the lookup, a name,a key, or a UUID may be used to identify the object.
        Only one object is returned.

        @param p_objs: is the tree of lighting objects such as lights, buttons or controllers
        @return: the object found or None.
        """
        for l_obj in p_objs.values():
            l_ret = self._test_object_by_id(l_obj, name, key, UUID)
            if l_ret != None:
                return l_obj
        LOG.error('Light Lookup failed - arg error Name:{}, Key:{}, UUID:{}'.format(name, key, UUID))
        return None

    def get_controller_objs_by_family(self, p_objs, p_family):
        """ Gets a controller for a device.

        @param p_objs: a dict f objects to search - such as p_pyhouse_obj.House.Lighting.Controllers{}
        @param p_family: the family to search for - 'Insteon'
        @return: a list of controller objs that match the family
        """
        l_ret = []
        for l_obj in p_objs.values():
            if l_obj.Active != True:  # Skip inactive devices.
                continue
            l_family = l_obj.DeviceFamily
            if l_family == p_family:
                l_ret.append(l_obj)
        if l_ret == []:
            LOG.error('Controller Lookup failed - arg error Family:{}'.format(p_family))
        else:
            LOG.debug('Found {} active controller(s) {} for family {}'.format(len(l_ret), l_ret, p_family))
        return l_ret

# ## END DBK
