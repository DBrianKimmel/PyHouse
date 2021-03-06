"""
@name:      PyHouse/src/Modules.Core.Utilities.uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

"""

__updated__ = '2019-10-24'

#  Import system type stuff
import os
import uuid

#  Import PyMh files
# from Modules.Core.data_objects import UuidData
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.UuidTools      ')


def _file_name(p_pyhouse_obj, p_file_name):
    """ Find the name of the file we will be using.
    """
    l_file = 'xxx'  # os.path.join(p_pyhouse_obj._Config.ConfigDir, 'Uuid', p_file_name)
    return l_file


def get_uuid_file(p_pyhouse_obj, p_file_name):
    """ get the uuid for the file if it exists OR create the file with a persistent UUID if needed.
    """
    l_file_name = _file_name(p_pyhouse_obj, p_file_name + '.uuid')
    try:
        l_file = open(l_file_name, mode='r')
        l_uuid = l_file.read()
    except IOError:
        l_uuid = Uuid.create_uuid()
        l_file = open(l_file_name, mode='w')
        l_file.write (l_uuid)
    l_file.close()
    return l_uuid


class Uuid:

    @staticmethod
    def create_uuid():
        """ Create a new Type 1 UUID.
        """
        return str(uuid.uuid1())

    @staticmethod
    def make_valid(p_uuid):
        """
        Preserve the UUID if it is present.
        If UUID id not 36 bytes, return a correctly generated uuid.

        @param p_uuid: a string holding a UUID
        """
        try:
            if len(p_uuid) != 36:
                p_uuid = Uuid.create_uuid()
                LOG.error('Invalid UUID found (1) - Creating a new one.')
        except TypeError:
            p_uuid = Uuid.create_uuid()
            LOG.error('Invalid UUID found (2) - Creating a new one.')
        return p_uuid

    @staticmethod
    def add_uuid(p_pyhouse_obj, p_uuid_obj):
        """ Add the given UuidData() object to PyHouse.
        """
        l_uuid = p_uuid_obj.UUID
        if l_uuid in p_pyhouse_obj._Uuids.All:
            LOG.info('Duplicate UUIDs Detected.  Old:{}  New:{}'.format(
                        p_pyhouse_obj._Uuids.All[l_uuid].UuidType, p_uuid_obj.UuidType))
        p_pyhouse_obj._Uuids.All[l_uuid] = p_uuid_obj

#  ## END DBK
