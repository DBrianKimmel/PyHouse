"""
@name:      PyHouse/src/Modules/Housing/Entertainment/pandora/test/xml_pandora.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Aug 03, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-08-04'

TESTING_PANDORA_SECTION = 'PandoraSection'
TESTING_PANDORA_DEVICE = 'Device'

L_PANDORA_SECTION_START = '<' + TESTING_PANDORA_SECTION + '>'
L_PANDORA_SECTION_END = '</' + TESTING_PANDORA_SECTION + '>'
L_PANDORA_DEVICE_END = '</' + TESTING_PANDORA_DEVICE + '>'

TESTING_PANDORA_DEVICE_NAME_0 = 'On pi-06-ct '
TESTING_PANDORA_DEVICE_KEY_0 = '0'
TESTING_PANDORA_DEVICE_ACTIVE_0 = 'True'
TESTING_PANDORA_DEVICE_COMMENT_0 = 'Living Room'

L_PANDORA_DEVICE_START_0 = '    ' + \
    '<' + TESTING_PANDORA_DEVICE + \
    ' Name="' + TESTING_PANDORA_DEVICE_NAME_0 + \
    '" Key="' + TESTING_PANDORA_DEVICE_KEY_0 + \
    '" Active="' + TESTING_PANDORA_DEVICE_ACTIVE_0 + \
    '">'
L_PANDORA_COMMENT_0 = '<Comment>' + TESTING_PANDORA_DEVICE_COMMENT_0 + '</Comment>'

L_PANDORA_DEVICE_0 = '\n'.join([
    L_PANDORA_DEVICE_START_0,
    L_PANDORA_COMMENT_0,
    L_PANDORA_DEVICE_END
])

XML_PANDORA_SECTION = '\n'.join([
    L_PANDORA_SECTION_START,
    L_PANDORA_SECTION_END
])

# ## END DBK
