* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/onkyo/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-03-23
* Updated:   2019-03-23
* License:   MIT License
* Summary:   This is the design documentation for the Onkyo Module of PyHouse.

# Onkyo


## Configuration

The onkyo section of master.xml looks like the following:

```xml
<OnkyoSection Active="True">
	<Type>Component</Type>
	<Device Active="True" Key="0" Name="Tx-555">
		<UUID>98765432-0001-0000-0000-0123456789ab</UUID>
		<Comment>Tx-555 Receiver</Comment>
		<Host>onkyo</Host>
		<IPv4>192.168.1.120</IPv4>
		<IPv6>2001:DB8::1</IPv6>
		<Model>Tx-555</Model>
		<Port>60128</Port>
		<RoomName>Living Room</RoomName>
		<RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
		<Type>Receiver</Type>
		<Volume>42</Volume>
	</Device>
</OnkyoSection>
```

The host name must be present in /etc/hosts and the IP address is obtained from there.
The IP addresses in the xml file are for documentation only.

## Design

## Packet Format

```
Bytes  1 -  4  'ISCP'
Bytes  5 -  8  4 byte bigendian header length (always 16 for version 1)
Bytes  9 - 12  4 byte bigendian data length which includes eol stuff
Byte  13       1 byte version number
Bytes 14 - 16  3 bytes reserves (should be all zeroes)
               command/response data
               \x1a\r\n for eol stuff
```


### Control Message

The pandora module will recieve a control message and perform the requested action:
The computer where 'PianoBar' is installed should be the one where the pandora service is configured.
These messages have topics:
        pyhouse/house name/entertainment/onkyo/control
The message payload will include "Control: xxx"
where xxx is one of:
* PowerOn
* PowerOff
* VolumeUp1
* VolumeUp5
* VolumeDown1
* VolumeDown5

.../control msg=on will have side effects of turning on and setting the "ConnectionName" device.

### Status Message

This module issues status messages,


## XML / Configuration

** The pandora device should only be configured on computers where PianoBar is installed. **

```xml
```

####

* AUDIO_INFO_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1IFAQSTN<cr>
* LISTEN_MODE_ALCHANSTEREO: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD0C<cr>
* LISTEN_MODE_AUDYSSEY_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD16<cr>
* LISTEN_MODE_NEO_CINEMA_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA3<cr>
* LISTEN_MODE_NEO_MUSIC_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA4<cr>
* LISTEN_MODE_NEURAL_DIGITAL_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA6<cr>
* LISTEN_MODE_NEURAL_SURROUND_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA5<cr>
* LISTEN_MODE_PLII_GAME_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA2<cr>
* LISTEN_MODE_PLII_MOVIE_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA0<cr>
* LISTEN_MODE_PLII_MUSIC_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA1<cr>
* LISTEN_MODE_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1LMDQSTN<cr>
* LISTEN_MODE_STEREO: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD00<cr>
* LISTEN_MODE_THEATER_DIMENSIONAL: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD0D<cr>
* MUTE: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1AMT01<cr>
* POWER_OFF: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1PWR00<cr>
* POWER_ON: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1PWR01<cr>
* POWER_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1PWRQSTN<cr>
* SOURCE_AM: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI25<cr>
* SOURCE_AUX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI03<cr>
* SOURCE_AUXILIARY: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI03<cr>
* SOURCE_BLURAY: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI10<cr>
* SOURCE_CD: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI23<cr>
* SOURCE_COMPUTER: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI05<cr>
* SOURCE_DOWN: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1SLIDOWN<cr>
* SOURCE_DVR: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI00<cr>
* SOURCE_FM: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI24<cr>

### END DBK
