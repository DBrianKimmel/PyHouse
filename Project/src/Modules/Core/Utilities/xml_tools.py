"""
@name:      Modules/Core/Utilities/xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2020 by D. Brian Kimmel
@note:      Created on Jun 2, 2012
@license:   MIT License
@summary:   Various XML functions and utility methods.

"""

__updated__ = '2020-02-14'

#  Import system type stuff

#  Import PyMh files

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.XmlTools       ')


def stuff_new_attrs(p_target_obj, p_data_obj):
    """
    Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes

    @param p_target_obj: is the object that eill receive the attrs
    @param p_data_obj: is the obj whose public attrs will be pushed into the target obj
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))  # Get all non private attrs in p_obj
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

#  ## END
