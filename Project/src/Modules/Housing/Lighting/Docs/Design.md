* Name:      PyHouse/Project/src/Modules/Housing/Lighting/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2018-10-16
* License:   MIT License
* Summary:   This is the design documentation for the Lighting Module of PyHouse.


# Lighting

Lighting was the first piece of PyHouse.

## Lighting

Since I started using Insteon, the lighting module became 3 sub modules:
* Controllers
* Switches
* Buttons

### Controllers

There are two different concepts called controllers.

The first is a device, connected to a computer, that sends commands from the computer to the devicer.
Insteon, UPB and X10 all have these controllers.  Other families may also have them also.
They connect to a serial port or a USB port on the computer side.

The second concept is a switch that 'controls' a responder.
A 'slave' switch, in a n-way group of switches, is the controller of the 'master' switch (which is wired to the fixture).
The 'master' switch responds to the 'controller' to send power to the fixture.

### Switch

### Buttons


### END DBK
