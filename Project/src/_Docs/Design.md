* Name:      PyHouse/Project/src/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2019-09-15
* License:   MIT License
* Summary:   This is the design documentation for the src of PyHouse.

# src

This is the design documentation of the source code for the PyHouse Project.

See PyHouse/Project/src/Modules/_Docs/Design.md 

# Design

At this level there is PyHouse.py and Modules/*

## PyHouse.py

It starts everything running.
It follows the singleton pattern so that it is not possible to have two running PyHouse programs competing for resources.
It is also a daemon.

It calls on Modules/Core to set up everything.



### END DBK
