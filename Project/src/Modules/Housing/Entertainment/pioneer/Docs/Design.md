* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/pioneer/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-04
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.


# Pioneer


## Design

The pioneer module (so far) is kinda a passive module.
It gets set up when the XML defines one or more Pioneer devices.
Then it sends out a Mqtt status message declaring the status when first connected to.]
It then waits for a control message.
Control messages can come from services sch as Pandora, or from a Node-Red dashboard triggering something.

The pioneer device I have does not wake up from a TCP connection.

There is the possibility of having more than one pioneer devices in a house.
The name of the devide is used for the key.
Be sure to configure the name to be unique and reference the name in the services.


## XML / Config

<PioneerSection Active="True">
    <Device Active="True" Key="0" Name="L/R Receiver VSX-822-K">
        <UUID>Pioneer.-0000-0000-0000-0123456789ab</UUID>
        <Comment>VSX-822-K Receiver</Comment>
        <CommandSet>2015</CommandSet>
        <IPv4>192.168.9.121</IPv4>
        <Port>8102</Port>
        <RoomName>Living Room</RoomName>
        <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
        <Status>On</Status>
        <Type>Receiver</Type>
        <Volume>75</Volume>
    </Device>
    <Device Active="True" Key="0" Name="Missing Device">
        <UUID>Pioneer.-0001-0000-0000-0123456789ab</UUID>
        <CommandSet>2015</CommandSet>
        <Comment>VSX-822-K Bogus</Comment>
        <IPv4>192.168.1.122</IPv4>
        <Port>8102</Port>
        <RoomName>Master Bedroom</RoomName>
        <RoomUUID>Room....-0001-0000-0000-0123456789ab</RoomUUID>
        <Type>Fake Receiver</Type>
    </Device>
</PioneerSection>

### END DBK
