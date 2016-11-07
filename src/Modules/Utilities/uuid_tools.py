"""
-*- test-case-name: PyHouse.src.Modules.Utilities.test.test_uuid_tools -*-

@name:      PyHouse/src/Modules/Utilities/uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

"""

__updated__ = '2016-11-07'

#  Import system type stuff
import uuid

#  Import PyMh files
# from Modules.Core.data_objects import UuidData
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.UuidTools      ')


class Uuid(object):

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
        if l_uuid in p_pyhouse_obj.Uuids:
            LOG.info('Duplicate UUIDs Detected.  Old:{}  New:{}'.format(
                        p_pyhouse_obj.Uuids[l_uuid].UuidType, p_uuid_obj.UuidType))
        p_pyhouse_obj.Uuids[l_uuid] = p_uuid_obj


class FileUuid(object):

    def __init__(self, p_path='/etc/pyhouse'):
        self.m_path = p_path

    def XXXread_file(self, p_filename):
        l_uuid = ""
        try:
            l_file = open(p_filename, 'r')
            l_uuid = l_file.read()
        except IOError as e_err:
            LOG.warn('UUID file {} error {}'.format(p_filename, e_err))
        return l_uuid

    def XXXwrite_file(self, p_filename, p_uuid):
        l_ret = 0
        return l_ret

#  ## END DBK
