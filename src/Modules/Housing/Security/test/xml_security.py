"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Housing/Security/test/xml_security.py -*-

@name:      /home/briank/PyHouse/src/Modules/Housing/Security/test/xml_security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Nov 1, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-11-01'

# Import system type stuff

# Import PyMh files
from Modules.Housing.Security.test.xml_garage_door import XML_GARAGE_DOOR_SECTION
from Modules.Housing.Security.test.xml_motion_sensors import XML_MOTION_SENSOR_SECTION


L_SECURITY_SECTION_START = '<SecuritySection>'
L_SECURITY_SECTION_END = '</SecuritySection>'

XML_SECURITY = '\n'.join([
    L_SECURITY_SECTION_START,
    XML_GARAGE_DOOR_SECTION,
    XML_MOTION_SENSOR_SECTION,
    L_SECURITY_SECTION_END
    ])

# ## END DBK
