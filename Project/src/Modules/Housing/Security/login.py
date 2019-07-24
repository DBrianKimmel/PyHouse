"""
@name:      Modules/Housing/Security/login.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul 23, 2019
@license:   MIT License
@summary:   Handle logging in.

"""


class LoginInformation:
    """
    """

    def __init__(self):
        self.Name = None  # Username
        self.Password = None


class Config:
    """
    """

    def load_name_password(self, p_config):
        """
        """
        l_obj = LoginInformation()
        return l_obj

# ## END DBK
