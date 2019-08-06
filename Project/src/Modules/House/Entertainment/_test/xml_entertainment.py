"""
@name:      PyHouse/src/Modules/Entertainment/_test/xml_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""

__updated__ = '2018-08-21'

# Import system type stuff

# Import PyMh files
from Modules.Housing.Entertainment.onkyo.test.xml_onkyo import XML_ONKYO_SECTION
from Modules.Housing.Entertainment.panasonic.test.xml_panasonic import XML_PANASONIC_SECTION
from Modules.Housing.Entertainment.pandora.test.xml_pandora import XML_PANDORA_SECTION
from Modules.Housing.Entertainment.pioneer.test.xml_pioneer import XML_PIONEER_SECTION
from Modules.Housing.Entertainment.samsung.test.xml_samsung import XML_SAMSUNG_SECTION

TESTING_ENTERTAINMENT_SECTION = 'EntertainmentSection'
TESTING_DEVICE = 'Device'

L_ENTERTAINMENT_SECTION_START = '<' + TESTING_ENTERTAINMENT_SECTION + '>'
L_ENTERTAINMENT_SECTION_END = '</' + TESTING_ENTERTAINMENT_SECTION + '>'

L_DEVICE_END = '</' + TESTING_DEVICE + '>'

XML_ENTERTAINMENT = '\n'.join([
    L_ENTERTAINMENT_SECTION_START,
    XML_ONKYO_SECTION,
    XML_PANASONIC_SECTION,
    XML_PANDORA_SECTION,
    XML_PIONEER_SECTION,
    XML_SAMSUNG_SECTION,
    L_ENTERTAINMENT_SECTION_END
])

# ## END DBK
