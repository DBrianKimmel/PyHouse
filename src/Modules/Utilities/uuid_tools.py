"""

@name:      PyHouse/src/Modules/Utilities/uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

"""

# Import system type stuff
import uuid

# Import PyMh files


def get_uuid(p_uuid):
    """
    Preserve the UUID if it is present.
    If UUID id not 36 bytes, return a correctly generated uuis.

    @param p_uuid: a string holding a UUID
    """
    try:
        if len(p_uuid) != 36:
            p_uuid = str(uuid.uuid1())
    except TypeError:
        p_uuid = str(uuid.uuid1())
    return p_uuid

# ## END DBK
