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

__updated__ = '2019-01-30'

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
        return None

    def _get_object_by_id(self, p_objs, name=None, key=None, UUID=None):
        """
        Return the device object from a dict of objects using the given value.
        Either a name or a key may be used to identify the light.

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

        Check for this Node
        """
        for l_obj in p_objs.values():
            l_family = l_obj.DeviceFamily
            if l_family == p_family:
                return l_obj
        LOG.error('Controller Lookup failed - arg error Family:{}'.format(p_family))
        return None

# ## END DBK
