* Name:      PyHouse/Project/src/Modules/Core/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2018-10-01
* License:   MIT License
* Summary:   This is the design documentation for the Core Module of PyHouse.


# Core

This module contains "Core" components.
They are always resident, loaded at the initialization of the system.

## core.py

The PyHouse.py singleton first calls core.py to initialize everything.

## Config

The config package is responsible for configuring the entire system.

## Utilities/config_file.py

This is used to read and write the config file.
The file can be located in several different directories.

If the file is missing, a properly formatted empty file is created in the default location.


# Logging


### END DBK
