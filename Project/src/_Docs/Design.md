* Name:      PyHouse/Project/src/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2019-09-24
* License:   MIT License
* Summary:   This is the design documentation for the src of PyHouse.

# src

This is the design documentation of the source code for the PyHouse Project.

See PyHouse/Project/src/Modules/_Docs/Design.md 

# Design

At this level there is PyHouse.py and Modules/*

# Controllers.

Each house will have controllers that controll various devices througout the house.
Things like Insteon Switches, window controls, door locks, and many others have controllers to actuate the devices.
Controllers may be directly attached to the computer usually via a USB plug or stand-alone such as a hub or bridge.

Those directly attached must be operated by the computer to which they are attached.
Those that are in the home network may be operated by any computer.
Some care must be taken because some controllers gain increased reliability if a command is duplicated.
Other controllers will cause mis-operation if multiple commands are issued.
Things like setting a light level to 50% on will work if multiple commands are sent.
Others like roggle or brighten by 10% will be wrong if multiple commands are sent.

## PyHouse.py

It starts everything running.
It follows the singleton pattern so that it is not possible to have two running PyHouse programs competing for resources.
It is also a daemon.

It calls on Modules/Core to start everything running.

## Core

Here is where the nitty-gritty begins.
The logging process is started.
The logs are located at /var/log/pyhouse.
The core component loads some always required pieces into memory and then begins the Initalize phase.

The first thing that happens is called initializing.

### Initialize

This is the first phase of startup.
This checks the configuration set up on this computer.
It then loads the modules called for in that configuration.
Some modules require sub modules to be loaded.

### Loading

This is the second phase of startup.
During this phase, the config files are read and information is built up.
All the required helper needs are determined during this process.
The abstractions for Family and Drivers are determined.

### Start

This is the third phase of startup.
At the very beginning of this step, the twisted reactor is run.
This begins the event loop processing and PyHouse becomes an async, event driven, home control process.

### END DBK
