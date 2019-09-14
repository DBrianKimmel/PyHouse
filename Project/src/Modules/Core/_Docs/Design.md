* Name:      PyHouse/Project/src/Modules/Core/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2018-10-01
* License:   MIT License
* Summary:   This is the design documentation for the Core Module of PyHouse.


# Design

## setup_pyhouse.py

The PyHouse.py singleton first calls setup_pyhouse.py to initialize everything.

## Utilities/config_file.py

This is used to read and write the config file.
The file can be located in several different directories.

If the file is missing, a properly formatted empty file is created in the default location.


# Logging


### END DBK
