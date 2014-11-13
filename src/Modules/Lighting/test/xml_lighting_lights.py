"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Lighting/test/xml_lighting_lights.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 9, 2014
@Summary:

"""



LIGHTS_XML = """
        <LightSection>
            <Light Active="True" Key="0" Name="outside_front">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable>
                <RoomName>Foyer</RoomName>
                <LightingType>Light</LightingType>
                <ControllerFamily>Insteon</ControllerFamily>

                <Address>16.62.2D</Address>
                <IsController>True</IsController>
                <DevCat>02.0A</DevCat>
                <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>30.1A.35</ProductKey>
                <IsResponder>True</IsResponder>
                <CurLevel>73</CurLevel>
            </Light>
            <Light Active="True" Key="1" Name="outside_gar">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Garage</RoomName>
                <LightingType>Light</LightingType>
                <Address>17.47.A1</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|Outside|Garage(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="2" Name="dr_chand">
                <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable><ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName><LightingType>Light</LightingType><Address>16.C9.37</Address>
                <IsController>True</IsController><DevCat>0</DevCat><GroupList>All_Lights|DiningRoom(12;12)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>F4.20.20</ProductKey>
                <IsResponder>True</IsResponder></Light>
            <Light Active="True" Key="3" Name="dr_chand_slave">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName>
                <LightingType>Light</LightingType>
                <Address>16.C9.D0</Address>
                <IsController>True</IsController>
                <DevCat>8007</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>EB.2A.A8</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="4" Name="nook_chand">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Breakfast Nook</RoomName>
                <LightingType>Light</LightingType>
                <Address>17.C2.72</Address>
                <IsController>True</IsController>
                <DevCat>0xc44</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
        </LightSection>
"""

# ## END DBK
