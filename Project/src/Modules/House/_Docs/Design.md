* Name:      Modules/House/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2020 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2020-01-22
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.

# House

House is one of three manditory modules of PyHouse.
The others are Core and Computer.

Under the PyHouse banner, a user has one or more houses to automate/control.

Each house has one or more Mqtt brokers running.
They usually operate as a controlling broker with redundant brokers for backup.

Mqtt came into the picture after PyHouse was up and running, so not everything runs from a message.

## Mode
The house has 3 modes: Home, Away and Vacation.
* Home is the normal operation Where everything operates on a normal schedule.
* Away is the operation where the house is unoccupied but wishes not to appear that way.
* Vacation is for short term where the house is unoccupied but you still want services running.

## Design

Nodes are removed if last used > 2 months ago.

## Rooms


#

House is one of the major components of PyHouse and has aits own separate config file.
It has several parts (Location, Floors and Rooms) that have their own config files.

House also has a number of modules, most of which are optional.
These modules may have sub-modules and these sub-modules may have sub-modules to any depth.

Many modules are configed and are not loaded at run time unless the config file is present.
Some modules like Family are not directly configured but spring into being when a family is used in some of the config files.


### END DBK
