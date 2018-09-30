@name:      PyHouse/Project/src/Modules/Housing/Entertainment/Docs/Design
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Sep 30, 2018
@license:   MIT License
@summary:   This is the design documentation for the Entertainment Module of PyHouse.

Design
======

The entertainment is a load on demand module.
In a running instance of PyHouse only the sub-modules that are defined in the config file are loaded.
This makes it sort of a plugin system.
This lowers the memory footprint of the system.  Since there are a lot of different entertainment device modules,
this will be a big savings of memory.

This module is message driven.  A Mqtt message is sent to entertainment.py and it dispatches it to the appropriate module.
These messages have topics that begin with:
		pyhouse/house name/entertainment/...

The modules may return a status message, control other submodules or ...


### END DBK
