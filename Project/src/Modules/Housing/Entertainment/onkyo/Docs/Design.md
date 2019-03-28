* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/onkyo/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2019-03-23
* Updated:   2019-03-23
* License:   MIT License
* Summary:   This is the design documentation for the Onkyo Module of PyHouse.


# Onkyo


## Design


### Control Message

The pandora module will recieve a control message and perform the action:
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

I am trying to control an Integra 5.9 AV receiver via its TCP port. I have set it to the following settings, 1p 192.168.1.17 and port 60128.

I have these same settings in the commandfusion software, I can ping the receiver from my PC.
I think my problem is with the data I am sending it, I am not too sure whether it should be hex or not.
The message to send it for zone 1 off is "1PWR00" with a Carriage Return on the end.
I have tried converting it to hex and sending the following for the zone 1 off command I have tried
"\x31x50x57x52x30x30x0D" "\x31\x50\x57\x52\x30\x30\x0D" ""1PWR00"/x0D" without the quotes except for the ones inside the last example.
What am I doing wrong?

I can control the unit via my own pc software by sending "1PWR00" carriage return.
 - - -
The correct command should be: 1PWR00\x0D
Also try: 1PWR00\x0A\x0D
The last one is what telnet would be sending.
Also make sure you have "maintain constant connection" ticked in the system properties.
 - - -
You need to put a '!' before the command
  !1PWR00     - standby
  !1PWR01     - on
 - - -
According to a protocol document sent to me by CG, the correct format should be something like this:

ISCP\x00\x00\x00\x10\x00\x00\x00\x08\x01\x00\x00\x00!1PWR01\x0D
ISCP\x00\x00\x00\x10\x00\x00\x00\x08\x01\x00\x00\x00!1PWR00\x0D

The commands listed by other people are to be used by RS232. The command above is for Ethernet.
It seems their ethernet protocol requires various header bytes, which the RS232 protocol does not.
 - - -
I can confirm that the message format Jarrod sent through is correct and I have tried it with a test CF project I'm working with.
So the format of the message should be [eISCP Message][eISCP Data]
where [eISCP] is
Bytes 1 - 4      'ISCP'
Bytes 5 - 8      Message Header Size (probably always \x00\x00\x00\x10
(ie. x10 or 16 bytes for the eISCP message) for the moment)
Bytes 9 - 12    Data Size
Byte 13          Version (currently always \x01 )
Bytes 14 - 16  Reserved

and [eISCP Data] is the message as we were trying previously which is the RS-232 command.
So the header ( ISCP\x00\x00\x00\x10\x00\x00\x00\x08\x01\x00\x00\x00 ) will be the same for the bulk of the commands in the protocol, however
you will need to change Data Size from \x08 to whatever the size of other commands is.
Remember to drag the new commands back onto the buttons, and you might also need to switch the Receiver off and on as I seemed to get it into
a mode where it wouldn't accept any TCP/IP commands for some reason.
Hope that all makes sense.
Not too sure why the web server built into the receiver accepts and works with the eISCP Data only without the eISCP Message
 - - -
AUDIO_INFO_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1IFAQSTN<cr>

LISTEN_MODE_ALCHANSTEREO: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD0C<cr>

LISTEN_MODE_AUDYSSEY_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD16<cr>

LISTEN_MODE_NEO_CINEMA_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA3<cr>

LISTEN_MODE_NEO_MUSIC_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA4<cr>

LISTEN_MODE_NEURAL_DIGITAL_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA6<cr>

LISTEN_MODE_NEURAL_SURROUND_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA5<cr>

LISTEN_MODE_PLII_GAME_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA2<cr>

LISTEN_MODE_PLII_MOVIE_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA0<cr>

LISTEN_MODE_PLII_MUSIC_DSX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMDA1<cr>

LISTEN_MODE_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1LMDQSTN<cr>

LISTEN_MODE_STEREO: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD00<cr>

LISTEN_MODE_THEATER_DIMENSIONAL: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1LMD0D<cr>

MUTE: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1AMT01<cr>

POWER_OFF: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1PWR00<cr>

POWER_ON: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1PWR01<cr>

POWER_QUERY: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1PWRQSTN<cr>

SOURCE_AM: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI25<cr>

SOURCE_AUX: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI03<cr>

SOURCE_AUXILIARY: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI03<cr>

SOURCE_BLURAY: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI10<cr>

SOURCE_CD: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI23<cr>

SOURCE_COMPUTER: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI05<cr>

SOURCE_DOWN: ISCP0;0;0;16;0;0;0;26;1;0;0;0;!1SLIDOWN<cr>

SOURCE_DVR: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI00<cr>

SOURCE_FM: ISCP0;0;0;16;0;0;0;24;1;0;0;0;!1SLI24<cr>


### END DBK
