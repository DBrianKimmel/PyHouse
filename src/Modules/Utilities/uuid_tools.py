"""
-*- test-case-name: PyHouse.src.Modules.Utilities.test.test_uuid_tools -*-

@name:      PyHouse/src/Modules/Utilities/uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

"""

#  Import system type stuff
import uuid

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.UuidTools      ')


class Uuid(object):

    @staticmethod
    def make_valid(p_uuid):
        """
        Preserve the UUID if it is present.
        If UUID id not 36 bytes, return a correctly generated uuid.

        @param p_uuid: a string holding a UUID
        """
        try:
            if len(p_uuid) != 36:
                p_uuid = str(uuid.uuid1())
        except TypeError:
            p_uuid = str(uuid.uuid1())
        return p_uuid


class FileUuid(object):
    def __init__(self, p_path = '/etc/pyhouse'):
        self.m_path = p_path

    def read_file(self, p_filename):
        l_uuid = ""
        try:
            l_file = open(p_filename, 'r')
            l_uuid = l_file.read()
        except IOError as e_err:
            LOG.warn('UUID file {} error {}'.format(p_filename, e_err))
        return l_uuid

    def write_file(self, p_filename, p_uuid):
        l_ret = 0
        return l_ret

#  ## END DBK
