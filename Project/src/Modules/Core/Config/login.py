"""
@name:      Modules/House/Security/login.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2020 by D. Brian Kimmel
@note:      Created on Jul 23, 2019
@license:   MIT License
@summary:   Handle logging in.

"""

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')


class LoginInformation:
    """
    """

    def __init__(self):
        self.Name = None  # Username
        self.Password = None


class LocalConfig:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def load_name_password(self, p_config):
        """
        """
        l_required = ['Name', 'Password']
        l_obj = LoginInformation()
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Pandora Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

# ## END DBK
