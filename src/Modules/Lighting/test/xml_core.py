"""
@name: PyHouse/src/Modules/Lighting/test/xml_core.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 22, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files

TESTING_LIGHTING_CORE_COMMENT = "SwitchLink On/Off"
TESTING_LIGHTING_CORE_COORDS = "['0', '0']"
TESTING_LIGHTING_CORE_DIMMABLE = True
TESTING_LIGHTING_CORE_ROOM = "Master Bath"

CORE_DEVICE = "<Comment>" + TESTING_LIGHTING_CORE_COMMENT + """</Comment>
    <Coords>""" + TESTING_LIGHTING_CORE_COORDS + """</Coords>
    <IsDimmable>""" + str(TESTING_LIGHTING_CORE_DIMMABLE) + """</IsDimmable>
    <RoomName>""" + TESTING_LIGHTING_CORE_ROOM + """</RoomName>"""
#    <CurLevel>""" + TESTING_LIGHTING_CORE_CUR_LEVEL + """</CurLevel>"""

# ## END DBK
