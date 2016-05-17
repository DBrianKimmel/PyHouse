"""
@name:      PyHouse/src/Modules/Lighting/test/xml_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

NO LONGER USED - REPLACED BY PyHouse/src/Modules/Core/test/xml_device.py

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

#  Import system type stuff

#  Import PyMh files

TXXESTING_LIGHTING_CORE_COMMENT = "SwitchLink On/Off"
TXXESTING_LIGHTING_CORE_COORDS = "['0', '0', '0']"
TXXESTING_LIGHTING_CORE_DIMMABLE = True
TXXESTING_LIGHTING_CORE_ROOM = "Master Bath"
TXXESTING_LIGHTING_CORE_INSTEON = "Insteon"
TXXESTING_LIGHTING_CORE_UPB = "UPB"

CORE_DEVICE = "<Comment>" + TXXESTING_LIGHTING_CORE_COMMENT + """</Comment>
    <Coords>""" + TXXESTING_LIGHTING_CORE_COORDS + """</Coords>
    <IsDimmable>""" + str(TXXESTING_LIGHTING_CORE_DIMMABLE) + """</IsDimmable>
    <RoomName>""" + TXXESTING_LIGHTING_CORE_ROOM + """</RoomName>
    <ControllerFamily>Insteon</ControllerFamily>"""

#  ## END DBK
