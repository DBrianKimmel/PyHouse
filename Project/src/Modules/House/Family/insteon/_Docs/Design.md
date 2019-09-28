* Name:      PyHouse/Project/src/Modules/Families/Insteon/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-01-20
* Updated:   2019-01-20
* License:   MIT License
* Summary:   This is the design for Insteon..

#Insteon

Insteon is / was the 3rd family of lighting control devices I used.
It is beginning to show its age in 2018.

When switching to Raspberry Pis as control nodes, it became possible to have several Insteon PLMs in a house.
Then came the HTTP device, the Insteon Link???
Then came the Insteon Hub which is/was a cloud type device with perhaps some local control.

# Design

There will only be one active PLM per node.


## Device Types

Insteon devices are of many different types

- Controllers
- Lights
- Buttons
- Switches
- Thermostats
- Garage Door Sensor/controller
- motion detector
- camera
- door sensor
- waterleak detectors

## Controller Types

### PLM

This was the first device to be coded in PyHouse.

It is connected as a serial device which nowdays is a USB connection emulating a serial port.


### Link

This has not yet (and may never be) been coded in PyHouse.


### Hub

This is just beginning to be coded (2019) in PyHouse.


### END DBK
