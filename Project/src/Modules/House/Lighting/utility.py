"""
@name:      Modules/House/Lighting/utility.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jan 20, 2019
@license:   MIT License
@summary:
"""

__updated__ = '2019-12-11'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightUtility   ')


class lightingUtility:
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
        # LOG.debug(PrettyFormatAny.form(p_objs, 'Objs'))
        for l_obj in p_objs.values():
            # LOG.debug(PrettyFormatAny.form(l_obj, 'Obj'))
            l_ret = self._test_object_by_id(l_obj, name, key, UUID)
            if l_ret != None:
                return l_obj
        LOG.error('Light Lookup failed - arg error Name:{}, Key:{}, UUID:{}'.format(name, key, UUID))
        return None

    def get_object_type_by_id(self, p_objs, group=['Lights', 'Outlets'], name=None, key=None, UUID=None):
        """
        Return the device object from a dict of objects using the given value.
        one of several things may be used for the lookup, a name,a key, or a UUID may be used to identify the object.
        Only one object is returned.

        @param p_objs: is the tree of lighting objects such as lights, buttons or controllers
        @return: the object found or None.
        """
        # LOG.debug(PrettyFormatAny.form(p_objs, 'Objs'))
        for l_class in group:
            # LOG.debug('Class: "{}"'.format(l_class))
            l_objs = getattr(p_objs, l_class)
            # LOG.debug(PrettyFormatAny.form(l_objs, 'Objs'))
            self.get_object_by_id(p_objs, name, key, UUID)
        LOG.error('Light Lookup failed - arg error Name:{}, Key:{}, UUID:{}'.format(name, key, UUID))
        return None

    def get_controller_objs_by_family(self, p_objs, p_family):
        """ Gets all the controllers for a device.

        @param p_objs: a dict of objects to search - such as p_pyhouse_obj.House.Lighting.Controllers{}
        @param p_family: the family to search for - 'Insteon'
        @return: a list of controller objs that match the family
        """
        l_ret = []
        for l_obj in p_objs.values():
            l_family = l_obj.Family.Name.lower()
            if l_family == p_family.lower():
                LOG.info('Found Controller {}; Local:{}'.format(l_obj.Name, l_obj._isLocal))
                if l_obj._isLocal:
                    l_ret.append(l_obj)
                # LOG.debug(PrettyFormatAny.form(l_obj, 'Controller'))
        if l_ret == []:
            LOG.warning('Controller Lookup failed - arg error Family:{}'.format(p_family))
        else:
            # LOG.debug('Found {} active controller(s) for family {}'.format(len(l_ret), p_family))
            pass
        return l_ret

# ## END DBK
