"""
XML to define the PyHouse.xml file

used for testing
"""




XML = """
<PyHouse>
    <Web WebPort="8580" />
    <Logs>
        <Debug>/var/log/pyhouse/debug</Debug>
        <Error>/var/log/pyhouse/error</Error>
    </Logs>
    <Nodes>
        <Node Name='PiNode-1' Key='0' Active='True'>
            <UUID>87654321-1001-11e3-b583-082e5f899999</UUID>
        </Node>
    </Nodes>
    <Houses>
        <House Active="True" Key="0" Name="Test House 1">
            <UUID>12345678-1002-11e3-b583-082e5f8cdfd2</UUID>
            <Location>
                <Street>Test Street 1</Street>
                <City>Test City 1</City>
                <State>Florida</State>
                <ZipCode>12345</ZipCode>
                <Phone>(800) 555-1212</Phone>
                <Latitude>28.938448</Latitude>
                <Longitude>-82.517208</Longitude>
                <TimeZone>-240.0</TimeZone>
                <SavingTime>60.0</SavingTime>
            </Location>
            <Rooms>
                <Room Active="True" Key="0" Name="Test Living Room">
                    <UUID>12341234-1003-11e3-82b3-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>0.50, 10.50</Corner>
                    <Size>14.00, 13.50</Size>
                </Room>
            </Rooms>
            <Hvac>
                <Thermostat>
                </Thermostat>
                <Thermostat>
                </Thermostat>
            </Hvac>
            <Pools>
                <Pool Name="Main Pool" Active="True" Key="0">
                </Pool>
                <Pool Name="Hot Tub" Active="True" Key="1">
                </Pool>
            </Pools>
        </House>
        <House Active="True" Key="0" Name="Test House 2">
            <UUID>ec955bcf-89c9-11e3-b583-082e5f8cdfd2</UUID>
            <Location>
                <Street>5191 N Pink Poppy Dr</Street>
                <City>Beverly Hills</City>
                <State>Florida</State>
                <ZipCode>34465</ZipCode>
                <Phone>(352) 270-8096</Phone>
                <Latitude>28.938448</Latitude>
                <Longitude>-82.517208</Longitude>
                <TimeZone>-240.0</TimeZone>
                <SavingTime>60.0</SavingTime>
            </Location>
            <Rooms>
                <Room Active="True" Key="0" Name="Master Bath">
                    <UUID>ec955bd0-89c9-11e3-82b3-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>0.83, 10.58</Corner>
                    <Size>14.00, 13.50</Size>
                </Room>
                <Room Active="False" Key="2" Name="Master Bedroom">
                    <UUID>ec955bd2-89c9-11e3-b50b-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>0.83, 25.08</Corner>
                    <Size>14.00, 18.00</Size>
                </Room>
                <Room Active="False" Key="6" Name="Living Room">
                    <UUID>ec9582e3-89c9-11e3-9595-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>21.00, 31.00</Corner>
                    <Size>10.00, 20.00</Size>
                </Room>
                <Room Active="False" Key="8" Name="Foyer">
                    <UUID>ec9582e5-89c9-11e3-ab35-082e5f8cdfd2</UUID>
                    <Comment>None</Comment><Corner>28.16, 20.25</Corner><Size>7.66, 11.41</Size>
                </Room>
                <Room Active="False" Key="9" Name="Game Room">
                    <UUID>ec9582e6-89c9-11e3-835a-082e5f8cdfd2</UUID>
                    <Comment>None</Comment><Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="10" Name="Laundry Room">
                    <UUID>ec9582e7-89c9-11e3-822f-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="11" Name="Back Bathroom">
                    <UUID>ec9582e8-89c9-11e3-baa4-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="12" Name="Office">
                    <UUID>ec9582e9-89c9-11e3-94d5-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="13" Name="Bedroom 2">
                    <UUID>ec9582ea-89c9-11e3-9089-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="14" Name="Guest Bathroom">
                    <UUID>ec9582eb-89c9-11e3-84d0-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="15" Name="Bedroom 3">
                    <UUID>ec95a9f0-89c9-11e3-8249-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="False" Key="17" Name="Garage">
                    <UUID>ec95a9f2-89c9-11e3-a84e-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>2.00, 2.00</Corner><Size>1.00, 1.00</Size>
                </Room>
                <Room Active="True" Key="18" Name="Dining Room">
                    <UUID>ec95a9f3-89c9-11e3-a1d0-082e5f8cdfd2</UUID><Comment>None</Comment>
                    <Corner>0,0</Corner><Size>12, 12</Size>
                </Room>
                <Room Active="False" Key="19" Name="Breakfast Nook">
                    <UUID>ec95a9f4-89c9-11e3-baf2-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>0, 0</Corner>
                    <Size>10, 10</Size>
                </Room>
                <Room Active="False" Key="20" Name="Kitchen">
                    <UUID>ec95a9f5-89c9-11e3-b210-082e5f8cdfd2</UUID>
                    <Comment>None</Comment>
                    <Corner>1,1</Corner>
                    <Size>10, 10</Size>
                </Room>
            </Rooms>
            <Schedules>
                <Schedule Active="True" Key="0" Name="Evening">
                    <Level>100</Level>
                    <LightName>lr_cans</LightName>
                    <LightNumber>10</LightNumber>
                    <Rate>0</Rate>
                    <RoomName>Living Room</RoomName>
                    <Time>sunset - 00:06</Time>
                    <Type>Device</Type>
                    <UUID>ec95d100-89c9-11e3-90cb-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="1" Name="Evening">
                    <Level>100</Level>
                    <LightName>lr_rope</LightName>
                    <LightNumber>7</LightNumber>
                    <Rate>0</Rate>
                    <RoomName>Living Room</RoomName>
                    <Time>sunset - 00:08</Time>
                    <Type>Device</Type>
                    <UUID>ec95d101-89c9-11e3-bb08-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="2" Name="Evening">
                    <Level>100</Level><LightName>outside_gar</LightName><LightNumber>1</LightNumber>
                    <Rate>0</Rate><RoomName>Garage</RoomName><Time>sunset - 00:02</Time>
                    <Type>Device</Type><UUID>ec95d102-89c9-11e3-abe6-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="3" Name="Evening">
                    <Level>100</Level><LightName>outside_front</LightName>
                    <LightNumber>0</LightNumber><Rate>0</Rate><RoomName>Foyer</RoomName>
                    <Time>sunset</Time><Type>Device</Type>
                    <UUID>ec95d103-89c9-11e3-8567-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="4" Name="Evening">
                <Level>100</Level><LightName>wet_bar</LightName><LightNumber>8</LightNumber>
                    <Rate>0</Rate><RoomName>Living Room</RoomName>
                    <Time>sunset - 00:04</Time><Type>Device</Type>
                    <UUID>ec95d104-89c9-11e3-b921-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="False" Key="5" Name="Night xxx">
                    <Level>60</Level>
                    <LightName>mbr_rope</LightName><LightNumber>6</LightNumber>
                    <Rate>0</Rate><RoomName>Master Bedroom</RoomName>
                    <Time>22:00</Time><Type>Device</Type>
                    <UUID>ec95d105-89c9-11e3-8b11-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="6" Name="Night">
                    <Level>0</Level><LightName>outside_gar</LightName>
                    <LightNumber>1</LightNumber>
                    <Rate>0</Rate><RoomName>Garage</RoomName><Time>23:00</Time>
                    <Type>Device</Type><UUID>ec95f811-89c9-11e3-a802-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="7" Name="Night">
                    <Level>0</Level><LightName>outside_front</LightName><LightNumber>0</LightNumber>
                    <Rate>0</Rate><RoomName>Foyer</RoomName><Time>23:00</Time>
                    <Type>Device</Type><UUID>ec95f812-89c9-11e3-931a-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="8" Name="Evening">
                    <Level>60</Level><LightName>mbr_rope</LightName>
                    <LightNumber>6</LightNumber><Rate>0</Rate><RoomName>Master Bedroom</RoomName>
                    <Time>22:10</Time><Type>Device</Type><UUID>ec95f813-89c9-11e3-a132-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="9" Name="Night">
                    <Level>0</Level><LightName>lr_rope</LightName><LightNumber>7</LightNumber>
                    <Rate>0</Rate><RoomName>Living Room</RoomName>
                    <Time>23:30</Time>
                    <Type>Device</Type><UUID>ec95f814-89c9-11e3-91e0-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="10" Name="Night">
                    <Level>0</Level><LightName>lr_cans</LightName>
                    <LightNumber>10</LightNumber><Rate>0</Rate><RoomName>Living Room</RoomName>
                    <Time>23:31</Time><Type>Device</Type><UUID>ec95f815-89c9-11e3-b6de-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="11" Name="Night">
                    <Level>0</Level><LightName>wet_bar</LightName><LightNumber>8</LightNumber>
                    <Rate>0</Rate><RoomName>Living Room</RoomName><Time>00:15</Time>
                    <Type>Device</Type><UUID>ec95f816-89c9-11e3-b338-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="True" Key="12" Name="Morning">
                    <Level>0</Level><LightName>mbr_rope</LightName>
                    <LightNumber>6</LightNumber><Rate>0</Rate>
                    <RoomName>Master Bedroom</RoomName>
                    <Time>sunrise + 00:30</Time><Type>Device</Type>
                    <UUID>ec95f817-89c9-11e3-9bc6-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="False" Key="13" Name="Testing">
                    <Level>100</Level><LightName>lr_rope</LightName><LightNumber>7</LightNumber>
                    <Rate>0</Rate><RoomName>Office</RoomName><Time>10:06</Time>
                    <Type>Device</Type><UUID>ec961f21-89c9-11e3-a428-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="False" Key="14" Name="Testing">
                    <Level>0</Level>
                    <LightName>lr_rope</LightName><LightNumber>7</LightNumber><Rate>0</Rate><RoomName>Office</RoomName>
                    <Time>10:31</Time><Type>Device</Type><UUID>ec961f22-89c9-11e3-a510-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="False" Key="15" Name="Testing">
                    <Level>0</Level><LightName>test_lamp1</LightName><LightNumber>9</LightNumber><Rate>0</Rate>
                    <RoomName>Breakfast Nook</RoomName><Time>10:24</Time>
                    <Type>Device</Type><UUID>ec961f23-89c9-11e3-af9e-082e5f8cdfd2</UUID>
                </Schedule>
                <Schedule Active="False" Key="16" Name="Testing">
                    <Level>0</Level><LightName>kitchen_counter</LightName>
                    <LightNumber>11</LightNumber><Rate>0</Rate>
                    <RoomName>Kitchen</RoomName>
                    <Time>21:56</Time><Type>Device</Type><UUID>ec961f24-89c9-11e3-ae3a-082e5f8cdfd2</UUID>
                </Schedule>
            </Schedules>
            <Lights>
                <Light Active="True" Key="0" Name="outside_front">
                    <Comment>SwitchLink On/Off</Comment>
                    <Coords>['0', '0']</Coords>
                    <Dimmable>False</Dimmable>
                    <Family>Insteon</Family>
                    <Room>Foyer</Room>
                    <Type>Light</Type>
                    <UUID>ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2</UUID>
                    <Address>16.62.2D</Address>
                    <Controller>True</Controller>
                    <DevCat>3140</DevCat>
                    <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
                    <GroupNumber>0</GroupNumber>
                    <Master>0</Master>
                    <ProductKey>30.1A.35</ProductKey>
                    <Responder>True</Responder>
                </Light>
                <Light Active="True" Key="1" Name="outside_gar">
                    <Comment>SwitchLink On/Off</Comment><Coords>['0', '0']</Coords><Dimmable>False</Dimmable>
                    <Family>Insteon</Family><Room>Garage</Room><Type>Light</Type>
                    <UUID>ec9d9931-89c9-11e3-8fd7-082e5f8cdfd2</UUID><Address>17.47.A1</Address>
                    <Controller>True</Controller><DevCat>0x0</DevCat><GroupList>All_Lights|Outside|Garage(0;0)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master>
                    <ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Light>
                <Light Active="True" Key="2" Name="dr_chand">
                    <Comment>SwitchLink dimmer</Comment>
                    <Coords>['0', '0']</Coords><Dimmable>True</Dimmable><Family>Insteon</Family>
                    <Room>Dining Room</Room><Type>Light</Type>
                    <UUID>ec9d9932-89c9-11e3-a921-082e5f8cdfd2</UUID>
                    <Address>16.C9.37</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList>All_Lights|DiningRoom(12;12)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master>
                    <ProductKey>F4.20.20</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="3" Name="dr_chand_slave">
                    <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>True</Dimmable><Family>Insteon</Family><Room>Dining Room</Room>
                    <Type>Light</Type><UUID>ec9dc040-89c9-11e3-b4ce-082e5f8cdfd2</UUID><Address>16.C9.D0</Address>
                    <Controller>True</Controller><DevCat>8007</DevCat>
                    <GroupList>All_Lights|Pantry(0;0)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>EB.2A.A8</ProductKey>
                    <Responder>True</Responder>
                </Light>
                <Light Active="True" Key="4" Name="nook_chand">
                    <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>True</Dimmable>
                    <Family>Insteon</Family><Room>Breakfast Nook</Room><Type>Light</Type>
                    <UUID>ec9dc041-89c9-11e3-b15f-082e5f8cdfd2</UUID>
                    <Address>17.C2.72</Address><Controller>True</Controller>
                    <DevCat>0xc44</DevCat><GroupList>All_Lights|Pantry(0;0)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="5" Name="nook_chand_slave">
                    <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>True</Dimmable><Family>Insteon</Family>
                    <Room>Breakfast Nook</Room><Type>Light</Type>
                    <UUID>ec9dc042-89c9-11e3-a4b0-082e5f8cdfd2</UUID>
                    <Address>17.C3.30</Address><Controller>True</Controller><DevCat>0x0</DevCat>
                    <GroupList>All_Lights|Nook(12;12)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Light>
                <Light Active="True" Key="6" Name="mbr_rope">
                    <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>True</Dimmable><Family>Insteon</Family>
                    <Room>Master Bedroom</Room><Type>Light</Type><UUID>ec9de74f-89c9-11e3-9706-082e5f8cdfd2</UUID>
                    <Address>16.C0.C4</Address><Controller>True</Controller><DevCat>61324</DevCat>
                    <GroupList>All_Lights|MasterBedroom(7;9)</GroupList><GroupNumber>0</GroupNumber>
                    <Master>0</Master><ProductKey>D0.30.D9</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="7" Name="lr_rope">
                    <Comment>SwitchLink dimmer Dual Band (*A*)</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>True</Dimmable><Family>Insteon</Family><Room>Living Room</Room>
                    <Type>Light</Type><UUID>ec9de750-89c9-11e3-9709-082e5f8cdfd2</UUID>
                    <Address>18.C9.4A</Address><Controller>True</Controller><DevCat>0x20a</DevCat>
                    <GroupList>All_Lights|LR|LivingRoom(21;0)</GroupList><GroupNumber>0</GroupNumber>
                    <Master>0</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="8" Name="wet_bar">
                    <Comment>SwitchLink dimmer Dual Band (*A*)</Comment><Coords>['0', '0']</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room>Living Room</Room>
                    <Type>Light</Type><UUID>ec9de751-89c9-11e3-a0d4-082e5f8cdfd2</UUID>
                    <Address>18.C5.8F</Address><Controller>True</Controller><DevCat>36787</DevCat>
                    <GroupList>All_Lights|LR|LivingRoom(11;10)</GroupList><GroupNumber>0</GroupNumber>
                    <Master>0</Master><ProductKey>9451516</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="9" Name="test_lamp1">
                    <Comment>v4.3 LampLink</Comment><Coords>['0', '0']</Coords><Dimmable>False</Dimmable>
                    <Family>Insteon</Family><Room>Office</Room><Type>Light</Type>
                    <UUID>ec9de752-89c9-11e3-b1b8-082e5f8cdfd2</UUID><Address>11.11.11</Address>
                    <Controller>True</Controller><DevCat>0x0</DevCat><GroupList>All_Lights|Office(8;8)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>1</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="10" Name="lr_cans">
                    <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords><Dimmable>True</Dimmable>
                    <Family>Insteon</Family><Room>Living Room</Room><Type>Light</Type>
                    <UUID>ec9e0e61-89c9-11e3-a9d4-082e5f8cdfd2</UUID><Address>16.C2.9A</Address>
                    <Controller>True</Controller><DevCat>0x0</DevCat><GroupList>All_Lights|LR|LivingRoom(20;0)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="True" Key="11" Name="kitchen_counter">
                    <Comment>None</Comment><Coords>None</Coords><Dimmable>False</Dimmable>
                    <Family>UPB</Family><Room>Kitchen</Room><Type>Light</Type>
                    <UUID>ec9e0e62-89c9-11e3-9e00-082e5f8cdfd2</UUID><NetworkID>6</NetworkID>
                    <Password>1293</Password><UnitID>20</UnitID>
                </Light>
                <Light Active="False" Key="12" Name="test_light_u1">
                    <Comment>None</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>UPB</Family><Room>Music Room</Room>
                    <Type>Light</Type><UUID>ec9e0e63-89c9-11e3-a2ce-082e5f8cdfd2</UUID>
                    <NetworkID>6</NetworkID><Password>1293</Password><UnitID>21</UnitID>
                </Light>
                <Light Active="False" Key="13" Name="Christmas_01 a">
                    <Comment>None</Comment><Coords>None</Coords><Dimmable>False</Dimmable>
                    <Family>Insteon</Family>
                    <Room>Living Room</Room><Type>Light</Type>
                    <UUID>ec9e0e64-89c9-11e3-b116-082e5f8cdfd2</UUID><Address>1A.E7.12</Address>
                    <Controller>True</Controller><DevCat>0x0</DevCat><GroupList />
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>00.00.00</ProductKey>
                    <Responder>True</Responder>
                </Light>
                <Light Active="False" Key="14" Name="Christmas_02">
                    <Comment>None</Comment><Coords>None</Coords><Dimmable>False</Dimmable>
                    <Family>Insteon</Family><Room>Living Room</Room><Type>Light</Type>
                    <UUID>ec9e3570-89c9-11e3-b762-082e5f8cdfd2</UUID>
                    <Address>1A.EB.84</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList /><GroupNumber>0</GroupNumber><Master>0</Master>
                    <ProductKey>00.00.00</ProductKey><Responder>True</Responder>
                </Light>
                <Light Active="False" Key="15" Name="Christmas_03">
                    <Comment>None</Comment><Coords>None</Coords><Dimmable>False</Dimmable>
                    <Family>Insteon</Family><Room>Living Room</Room><Type>Light</Type>
                    <UUID>ec9e3571-89c9-11e3-9165-082e5f8cdfd2</UUID><Address>1A.EB.29</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList />
                    <GroupNumber>0</GroupNumber><Master>0</Master><ProductKey>00.00.00</ProductKey>
                    <Responder>True</Responder>
                </Light>
            </Lights>
            <Buttons>
                <Button Active="False" Key="0" Name="kpl_1_A">
                    <Comment>KeypadLink Button A</Comment>
                    <Coords>None</Coords>
                    <Dimmable>False</Dimmable>
                    <Family>Insteon</Family>
                    <Room>Master Bath</Room>
                    <Type>Button</Type>
                    <UUID>ec97308f-89c9-11e3-a78b-082e5f8cdfd2</UUID>
                    <Address>16.E5.B6</Address>
                    <Controller>True</Controller>
                    <DevCat>0x0</DevCat>
                    <GroupList>All_Lights|MasterBedroom(0;0)</GroupList>
                    <GroupNumber>1</GroupNumber>
                    <Master>0</Master>
                    <ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Button>
                <Button Active="False" Key="1" Name="kpl_1_B">
                    <Comment>KeypadLink Button B</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family>
                    <Room /><Type>Button</Type><UUID>ec97579e-89c9-11e3-832c-082e5f8cdfd2</UUID>
                    <Address>16.E5.B6</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList>All_Buttons</GroupList><GroupNumber>2</GroupNumber>
                    <Master>False</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Button>
                <Button Active="False" Key="2" Name="kpl_1_C">
                    <Comment>KeypadLink Button C</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room /><Type>Button</Type>
                    <UUID>ec97579f-89c9-11e3-b0d7-082e5f8cdfd2</UUID><Address>16.E5.B6</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList>All_Buttons</GroupList>
                    <GroupNumber>3</GroupNumber><Master>False</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Button>
                <Button Active="False" Key="3" Name="kpl_1_D">
                    <Comment>KeypadLink Button D</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room /><Type>Button</Type>
                    <UUID>ec9757a0-89c9-11e3-a0c5-082e5f8cdfd2</UUID><Address>16.E5.B6</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList>All_Buttons</GroupList>
                    <GroupNumber>4</GroupNumber><Master>False</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Button>
                <Button Active="False" Key="4" Name="kpl_1_E">
                    <Comment>KeypadLink Button E</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room /><Type>Button</Type>
                    <UUID>ec9757a1-89c9-11e3-a7c3-082e5f8cdfd2</UUID><Address>16.E5.B6</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList>All_Buttons</GroupList>
                    <GroupNumber>5</GroupNumber><Master>False</Master>
                    <ProductKey>0</ProductKey><Responder>True</Responder>
                </Button>
                <Button Active="False" Key="5" Name="kpl_1_F">
                    <Comment>KeypadLink Button F</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room />
                    <Type>Button</Type><UUID>ec977eb0-89c9-11e3-bf6d-082e5f8cdfd2</UUID>
                    <Address>16.E5.B6</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList>All_Buttons</GroupList><GroupNumber>6</GroupNumber>
                    <Master>False</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Button>
                <Button Active="False" Key="6" Name="kpl_1_G">
                    <Comment>KeypadLink Button G</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family>
                    <Room /><Type>Button</Type><UUID>ec977eb1-89c9-11e3-82d4-082e5f8cdfd2</UUID>
                    <Address>16.E5.B6</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList>All_Buttons</GroupList><GroupNumber>7</GroupNumber>
                    <Master>False</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Button><Button Active="False" Key="7" Name="kpl_1_H">
                    <Comment>KeypadLink Button H</Comment><Coords>None</Coords>
                    <Dimmable>False</Dimmable><Family>Insteon</Family><Room />
                    <Type>Button</Type><UUID>ec977eb2-89c9-11e3-a4ef-082e5f8cdfd2</UUID>
                    <Address>16.E5.B6</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList>All_Buttons</GroupList>
                    <GroupNumber>8</GroupNumber><Master>False</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Button>
                <Button Active="False" Key="8" Name="nook_chand_slave">
                    <Comment>SwitchLink dimmer</Comment><Coords>None</Coords><Dimmable>True</Dimmable>
                    <Family>Insteon</Family><Room /><Type>Light</Type>
                    <UUID>ec97a5c0-89c9-11e3-bbea-082e5f8cdfd2</UUID><Address>17.C3.30</Address>
                    <Controller>True</Controller><DevCat>0</DevCat><GroupList>All_Lights|Nook(12;12)</GroupList>
                    <GroupNumber>0</GroupNumber><Master>False</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                </Button>
                <Button Active="False" Key="9" Name="dr_chand2">
                    <Comment>SwitchLink dimmer</Comment><Coords>None</Coords><Dimmable>True</Dimmable>
                    <Family>Insteon</Family><Room /><Type>Light</Type>
                    <UUID>ec97a5c1-89c9-11e3-ac93-082e5f8cdfd2</UUID>
                    <Address>16.C9.D0</Address><Controller>True</Controller><DevCat>0</DevCat>
                    <GroupList>All_Lights|Pantry(0;0)</GroupList><GroupNumber>0</GroupNumber>
                    <Master>False</Master><ProductKey>0</ProductKey><Responder>True</Responder>
                </Button>
                <Button Active="False" Key="10" Name="TestButton">
                    <Comment>None</Comment>
                    <Coords>None</Coords><Dimmable>False</Dimmable><Family>UPB</Family><Room />
                    <Type /><UUID>ec97a5c2-89c9-11e3-bb03-082e5f8cdfd2</UUID><NetworkID>6</NetworkID>
                    <Password>1293</Password><UnitID>85</UnitID>
                </Button>
            </Buttons>
            <Controllers>
                <Controller Active="False" Key="0" Name="PLM_1">
                    <Comment>Dongle using serial converter 067B:2303</Comment>
                    <Coords>None</Coords>
                    <Dimmable>True</Dimmable>
                    <Family>Insteon</Family>
                    <Room>Office</Room>
                    <Type>Controller</Type>
                    <UUID>ec97a5c3-89c9-11e3-ab54-082e5f8cdfd2</UUID>
                    <Address>AA.AA.AA</Address>
                    <Controller>True</Controller>
                    <DevCat>0x0</DevCat>
                    <GroupList />
                    <GroupNumber>0</GroupNumber>
                    <Master>False</Master>
                    <ProductKey>0</ProductKey>
                    <Responder>True</Responder>
                    <Interface>Serial</Interface>
                    <Port>/dev/ttyUSB0</Port>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize>
                    <Parity>N</Parity>
                    <StopBits>1.0</StopBits>
                    <Timeout>1.0</Timeout>
                    <DsrDtr>False</DsrDtr>
                    <RtsCts>False</RtsCts>
                    <XonXoff>False</XonXoff>
                </Controller>
                <Controller Active="False" Key="1" Name="PowerLink">
                    <Comment>2413UH Powerlink Controller</Comment><Coords>None</Coords><Dimmable>True</Dimmable>
                    <Family>Insteon</Family><Room>Office</Room><Type>Controller</Type>
                    <UUID>ec99a18f-89c9-11e3-b271-082e5f8cdfd2</UUID><Address>17.03.B2</Address>
                    <Controller>True</Controller><DevCat>0x0</DevCat><GroupList />
                    <GroupNumber>0</GroupNumber><Master>False</Master><ProductKey>0</ProductKey>
                    <Responder>True</Responder><Interface>Serial</Interface><Port>/dev/ttyUSB0</Port>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize><Parity>N</Parity><StopBits>1.0</StopBits>
                    <Timeout>1.0</Timeout><DsrDtr>False</DsrDtr><RtsCts>False</RtsCts><XonXoff>False</XonXoff>
                </Controller>
                <Controller Active="False" Key="2" Name="UPB_PIM">
                    <Comment>UPB PIM  using USB connection</Comment><Coords>None</Coords>
                    <Dimmable>True</Dimmable>
                    <Family>UPB</Family><Room>Master Bath</Room><Type>Controller</Type>
                    <UUID>ec9bc470-89c9-11e3-8f15-082e5f8cdfd2</UUID>
                    <NetworkID>0</NetworkID><Password>0</Password><UnitID>255</UnitID>
                    <Interface>USB</Interface><Port>None</Port><Vendor>6109</Vendor><Product>21760</Product>
                </Controller>
            </Controllers>
            <Internet ExternalDelay="28800" ExternalIP="None" ExternalUrl="http://snar.co/ip">
                <DynamicDNS Active="True" Key="0" Name="Afraid">
                    <Interval>21600</Interval>
                    <Url>http://freedns.afraid.org/dynamic/update.php?VDZtSkE2MzFVMVVBQVd5QXg2MDo5MjU1MzYw</Url>
                </DynamicDNS>
            </Internet>
        </House>
    </Houses>
</PyHouse>
"""



XML1 = """
<PyHouse>
    <Web>
    </Web>
    <Nodes>
        <Node Name='PiNode-1' Key='0' Active='True'>
            <UUID>ec955bcf-89c9-11e3-b583-082e5f8cdfd2</UUID>
        </Node>
    </Nodes>
    <Houses>
        <House Name='House_1' Key='0' Active='True'>
            <Controllers>
                <Controller Name='Serial_1' Key='0' Active='True'>
                    <Interface>Serial</Interface>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize>
                    <DsrDtr>False</DsrDtr>
                    <Parity>N</Parity>
                    <RtsCts>False</RtsCts>
                    <StopBits>1.0</StopBits>
                    <Timeout>0</Timeout>
                    <XonXoff>False</XonXoff>
                </Controller>
                <Controller Name='USB_1' Key='1' Active='True'>
                    <Interface>USB</Interface>
                    <Vendor>12345</Vendor>
                    <Product>9876</Product>
                </Controller>
            </Controllers>
        </House>
    </Houses>
</PyHouse>
"""

# ## END DBK
