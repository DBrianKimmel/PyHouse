"""
@name:      Modules/House/Security/_test/xml_security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@note:      Created on Nov 1, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2019-07-31'

# Import system type stuff

# Import PyMh files
from Modules.House.Security.test.xml_garage_door import XML_GARAGE_DOOR_SECTION
from Modules.House.Security.test.xml_motion_sensors import XML_MOTION_SENSOR_SECTION

L_SECURITY_SECTION_START = '<SecuritySection>'
L_SECURITY_SECTION_END = '</SecuritySection>'

XML_SECURITY = '\n'.join([
    L_SECURITY_SECTION_START,
    XML_GARAGE_DOOR_SECTION,
    XML_MOTION_SENSOR_SECTION,
    L_SECURITY_SECTION_END
    ])

# ## END DBK
