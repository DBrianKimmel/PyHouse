* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/onkyo/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-03-23
* Updated:   2019-04-13
* License:   MIT License
* Summary:   This is the design documentation for the Onkyo Module of PyHouse.

# Onkyo

A house may have one or more Onkyo devices in it's entertainment systems.

Many different nodes may, at various times, control the onkyo devices.
Different nodes may control different devices.
Any service thats wants to control onkyo devices must do so by sending Mqtt control messages.
The node currently connected to an Onkyo device will send the actual eISCP commands to the device.

As each Onkyo section of PyHouse establishes communication to an Onkyo device, it sends a Mqtt status message
claiming control of the device.
The controlling node has the _isControlling flag set, all other nodes have it reset.

It seems (unconfirmed) that the last PyHouse instance to start is the one controlling all the Onkyo devices.

## Connecting
It appears that at least some of the devices may not queue the commands we send them so we queue the commands
until the device responds and then we send the next command if we have one.

When PyHouse starts up we establish communication with the Onkyo device.
If we don't connect we assume some other node connected before and we just mark the device "dead".

We send out a status message when this happens - either connected or dead.


## Controlling

When we get a Mqtt control message to do something, we queue each of the commands called for in the message.
Then we start a loop performing each of the commands to the device.
When each command finishes we accumulate the response.
When the queue is empty, we send a Mqtt status message with the accumulated results.


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

There is also a seperate YAML document in /etc/pyhouse for each type of Onkyo device.
This file defines the specifics for each different Onkyo device.

The host name must be present in /etc/hosts and the IP address is obtained from there.
The IP addresses in the xml file are for documentation only.


```yaml
UnitType: 1

ControlCommands:
   Power:
      - PWR
      - PWZ
   Volume:
      - MVL
      - ZVL
   Mute:
      - AMT
      - ZMT
   InputSelect:
      - SLI
      - SLZ

Arguments:
   Power:
      'Off': '00'
      'On': '01'
      '?': 'QSTN'
   Volume:
      'Up': 'UP'
      'Down': 'DOWN'
      '?': 'QSTN'

InputSelect:
   'Video1': '00'        # 'VIDEO1', 'VCR/DVR', 'STB/DVR'
   'Cbl/Sat': '01'       # 'VIDEO2', 'CBL/SAT'
   'Game': '02'          # 'VIDEO3', 'GAME/TV', 'GAME', 'GAME1'
   'Aux': '03'           # 'VIDEO4', 'AUX1(AUX)'
   'Pc': '05'            # 'VIDEO6', 'PC'
   'Bd/Dvd': '10'        # 'DVD', 'BD/DVD'
   'Strmbox': '11'       # 'STRM BOX'
   'TV': '12'            # 'TV'
   'Phono': '22'         # 'PHONO'
   'Cd': '23'            # 'CD', 'TV/CD'

Zones:
   0: Inside
   1: Outside
```

## Design

### Packet Format

```
Bytes  1 -  4  'ISCP'
Bytes  5 -  8  4 byte bigendian header length (always 16 for version 1)
Bytes  9 - 12  4 byte bigendian data length which includes eol stuff
Byte  13       1 byte version number
Bytes 14 - 16  3 bytes reserves (should be all zeroes)
               command/response data
               \x1a\r\n for eol stuff
```
* Commands
'!' is the start character
'1' is the Unit Type - Unit Type is the model category ID. The Receiver is "1".
'XXX' is the 3 letter command
'ARGS' are the command arguments
'!1PWRQSTN'


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




{"id":"a3b10e27.39bb88","type":"inject","z":"fb28734e.0daa5",
	"name":"Play Pandora","topic":"Entertain","payload":"pandora","payloadType":"str",
	"repeat":"","crontab":"","once":false,"onceDelay":0.1,
	"x":130,"y":220,"wires":[["6aa0fe8a.6411f8"]]},

{"id":"6aa0fe8a.6411f8","type":"function","z":"fb28734e.0daa5","name":"Compose",
	"func":
		"//\n//\nmsg.topic = 'pyhouse/cannon trail/entertainment/pandora/play';\n
		msg.payload = {'Sender': 'Node-Red 04 CT'};\nreturn msg;","outputs":1,"noerr":0,
		"x":320,"y":220,"wires":[["7e47594a.cccde","bec0b9c0.4a53f"]]},

{"id":"7e47594a.cccde","type":"mqtt out","z":"fb28734e.0daa5",
	"name":"Send Msg","topic":"","qos":"","retain":"","broker":"737d2428.a53fa4","x":620,"y":220,"wires":[]},

{"id":"bec0b9c0.4a53f","type":"debug","z":"fb28734e.0daa5",
	"name":"PlayPandoraDebug","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"true","x":640,"y":300,"wires":[]},

{"id":"6a7ba440.b296c4","type":"function","z":"3f0540b.1917ec",
	"name":"Control Message",
	"func":"
		
		// Out 1 = To MQTT.
		// Out 2 = To Chart
		// Out 3 = To Debug.
		
		var mqtt_msg,
		    chart_msg,
		    debug_msg;
		var NAME   = \"Pandora Control\";
		var l_date = new Date();\n
		var l_house    = global.get('ms.house_name');
		var l_ip       = global.get('ms.public_ipv4');
		var l_node     = global.get('ms.node_name');
		var l_pandora  = global.get('ms.pandora');
		var PREFIX = 'pyhouse/' + l_house + '/entertainment/pandora/control';
		
		// .Sender
		// .System
		// .Zone
		// .Control p_msg
		//
		function build_mqtt_message(p_msg) {
		    var msg = {};
		    msg.topic = PREFIX;
		    msg.payload = {};
		    msg.payload.Sender  = l_node;
		    msg.payload.System  = 'Pandora';
		    msg.payload.Zone    = '1';
		    msg.payload.Control = p_msg;
		    return msg;
		}
		function build_chart_message(p_msg) {
		    var msg = {};\n
		    msg.topic = 'Pandora';\n
		    msg.payload = p_msg;\n
		    return msg;\n
		}
		function build_debug_message(p_msg) {\n
		    var msg = {};\n
		    msg.topic = 'Debug Message - Pandora Control';\n
		    msg.payload = p_msg;\n
		    msg.status = \"Pandora: \";\n
		    return msg;\n
		}\n
		// Turn Pandora on.\n
		function turnPandoraOn(pType) {\n
		    if (l_pandora !== 'On') {\n
		        l_msg = 'now';\n
		        debug_msg = build_debug_message('Turned ' + NAME + ' ON.');\n
		    } else {\n
		        l_msg = 'was';\n
		        debug_msg = build_debug_message('Kept ' + NAME +' ON.');\n
		    }\n
		    node.status({fill:\"green\", shape:\"dot\",text:\"Pandora \" + l_msg + \" On\"});\n
		    global.set('ms.pandora', 'On');\n
		    mqtt_msg  = build_mqtt_message('PowerOn');\n
		    chart_msg = null;\n
		    node.send([mqtt_msg, chart_msg, debug_msg]);\n
		}\n
		// Turn Pandora off.\n
		function turnPandoraOff(pType) {\n
		    if (l_pandora !== 'Off') {  // Turning drip system off.\n
		        l_msg = 'now';\n
		        debug_msg = build_debug_message('Turned ' + NAME + ' OFF');\n
		    } else {\n
		        l_msg = 'was';\n
		        debug_msg = build_debug_message('Kept ' + NAME +' OFF');\n
		    }\n
		    node.status({fill:\"yellow\", shape:\"dot\",text:\"Pandora \" + l_msg + \" Off\"});\n
		    global.set('ms.pandora', 'Off');\n
		    mqtt_msg  = build_mqtt_message('PowerOff');\n
		    node.send([mqtt_msg, chart_msg, debug_msg]);\n
		}\n
		\n
		// This node is triggered by any of several buttons:\n
		//      Power\n
		//      Volume\n
		//      Like\n
		//\n
		switch (msg.topic) {\n
		    case 'Power':\n
		        if (msg.payload === 'PowerOn') {\n
		            turnPandoraOn('PowerOn');\n
		        } else {  // Turn off\n
		            turnPandoraOff(\"PowerOff\");\n
		        }\n
		        break;\n
		        \n
		    case \"Volume\":\n
		    case \"Like\":\n
		    case \"Skip\":\n
		        mqtt_msg  = build_mqtt_message(msg.payload);\n
		        chart_msg = null;\n
		        node.send([mqtt_msg, chart_msg, debug_msg]);\n
		        break;  \n
		        \n
		    default:\n
		        debug_msg = build_debug_message('Unknown Input: topic= ' + msg.topic + ',  Payload=' + msg.payload);\n
		        node.warn(debug_msg);\n
		        break;\n
		    }\n
		return null;\n
		 \n
		 // ### END DBK\n",
	"outputs":3,"noerr":0,"x":590,"y":200,"wires":[["3325cd67.8db5e2","abfc7afd.4ac1b8"],[],["8ca77d9.839c68"]]},

{"id":"c23c9538.576538",
	"type":"ui_button","z":"3f0540b.1917ec",
	"name":"On","group":"f9596f90.235b38","order":,"width":"6","height":"1","passthru":false,
	"label":"On","color":"black","bgcolor":"lightgreen","icon":"fa-play",
	"payload":"PowerOn","payloadType":"str","topic":"Power",
	"x":130,"y":40,"wires":[["6a7ba440.b296c4"]]},


# References

https://

### END DBK
