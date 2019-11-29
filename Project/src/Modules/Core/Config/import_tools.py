"""
@name:      Modules/Core/Config/import_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 19, 2019
@Summary:   This handles

"""

__updated__ = '2019-11-28'
__version_info__ = (19, 11, 28)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import importlib

#  Import PyMh files
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.ImportTools    ')


class Tools:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _do_import(self, p_name, p_path):
        """ This will import a module.
        Used when we discover that the module is needed because:
            It is required
            Configuration calles for it.
        @param p_name: is the name of the module ('pandora')
        @param p_path: is the relative path to the module ('Modules.House.Entertainment')
        @return: a pointer to the module or None
        """
        l_path = p_path + '.' + p_name
        # l_package = p_path + '.'
        # LOG.debug('Importing\n\tModule:  {}\n\tPath:    {}'.format(p_name, l_path))
        try:
            l_ret = importlib.import_module(l_path)
        except ImportError as e_err:
            l_msg = 'PROG ERROR importing module: "{}"\n\tErr:{}.'.format(p_name, e_err)
            LOG.error(l_msg)
            l_ret = None
        # LOG.info('Imported "{}" ({})'.format(p_name, l_path))
        return l_ret

    def import_module_get_api(self, p_module, p_path):
        """ import a module with a path
        @param p_module: is a module name ("Cameras")
        @param p_path: is the starting point to look for the module to import.
        @return: an initialized Api
        """
        l_module_name = p_module.lower()
        l_ret = self._do_import(l_module_name, p_path)
        try:
            # LOG.debug(PrettyFormatAny.form(l_ret, 'Module'))
            l_api = l_ret.Api(self.m_pyhouse_obj)
        except Exception as e_err:
            LOG.error('ERROR - Initializing Module: "{}"\n\tError: {}'.format(p_module, e_err))
            # LOG.error('Ref: {}'.format(PrettyFormatAny.form(l_ret, 'ModuleRef')))
            l_api = None
        # LOG.debug('Imported: {}'.format(l_ret))
        return l_api

# ## END DBK
