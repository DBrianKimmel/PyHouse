"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON
from Modules.Families.UPB.test.xml_upb import XML_UPB


L_LIGHT_SECTION_START = '<LightSection>'
L_LIGHT_SECTION_END = '</LightSection>'
L_LIGHT_END = '</Light>'


TESTING_LIGHT_NAME_0 = "Insteon Light"
TESTING_LIGHT_KEY_0 = '0'
TESTING_LIGHT_ACTIVE_0 = 'True'
TESTING_LIGHT_DIMMABLE_0 = 'True'
TESTING_LIGHT_CUR_LEVEL_0 = "12"
TESTING_LIGHT_FAMILY_0 = 'Insteon'
TESTING_LIGHT_TYPE_0 = 'Light'

L_LIGHT_START_0 = '<Light Name="' + TESTING_LIGHT_NAME_0 + '" Key="' + TESTING_LIGHT_KEY_0 + '" Active="' + TESTING_LIGHT_ACTIVE_0 + '">'
L_LIGHT_DIMMABLE_0 = '    <IsDimmable>' + TESTING_LIGHT_DIMMABLE_0 + '</IsDimmable>'
L_LIGHT_TYPE_0 = '    <LightingType>' + TESTING_LIGHT_TYPE_0 + '</LightingType>'
L_LIGHT_LEVEL_0 = "    <CurLevel>" + TESTING_LIGHT_CUR_LEVEL_0 + "</CurLevel>"
L_LIGHT_FAMILY_0 = "    <DeviceFamily>" + TESTING_LIGHT_FAMILY_0 + "</DeviceFamily>"

L_LIGHT_0 = '\n'.join([
    L_LIGHT_START_0,
    L_LIGHT_DIMMABLE_0,
    L_LIGHT_FAMILY_0,
    L_LIGHT_TYPE_0,
    L_LIGHT_LEVEL_0,
    XML_INSTEON,
    L_LIGHT_END
    ])


TESTING_LIGHT_NAME_1 = "UPB Light"
TESTING_LIGHT_KEY_1 = '1'
TESTING_LIGHT_ACTIVE_1 = 'True'
TESTING_LIGHT_DIMMABLE_1 = 'True'
TESTING_LIGHT_CUR_LEVEL_1 = "12"
TESTING_LIGHT_FAMILY_1 = 'UPB'
TESTING_LIGHT_TYPE_1 = 'Light'

L_LIGHT_START_1 = '<Light Name="' + TESTING_LIGHT_NAME_1 + '" Key="' + TESTING_LIGHT_KEY_1 + '" Active="' + TESTING_LIGHT_ACTIVE_1 + '">'
L_LIGHT_TYPE_1 = '    <LightingType>' + TESTING_LIGHT_TYPE_1 + '</LightingType>'
L_LIGHT_DIMMABLE_1 = '    <IsDimmable>' + TESTING_LIGHT_DIMMABLE_1 + '</IsDimmable>'
L_LIGHT_CUR_LEVEL_1 = "    <CurLevel>" + TESTING_LIGHT_CUR_LEVEL_1 + "</CurLevel>"
L_LIGHT_FAMILY_1 = "    <DeviceFamily>" + TESTING_LIGHT_FAMILY_1 + "</DeviceFamily>"

L_LIGHT_1 = '\n'.join([
    L_LIGHT_START_1,
    L_LIGHT_DIMMABLE_1,
    L_LIGHT_FAMILY_1,
    L_LIGHT_TYPE_1,
    L_LIGHT_CUR_LEVEL_1,
    XML_UPB,
    L_LIGHT_END
    ])


XML_LIGHT_SECTION = '\n'.join([
    L_LIGHT_SECTION_START,
    L_LIGHT_0,
    L_LIGHT_1,
    L_LIGHT_SECTION_END
    ])

# ## END DBK
