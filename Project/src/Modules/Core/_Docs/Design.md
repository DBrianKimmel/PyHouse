* Name:      Modules/Core/Xonfig/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2020 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2020-01-22
* License:   MIT License
* Summary:   This is the design documentation for the Config Module of PyHouse.


# Config

The config package is responsible for configuring the entire system.

Having all the configuration in one config file would be far to complex to maintain so the config
is broken down into smaller files which are much easier to manage.

The file suffix is always .yaml for the current implementation.

The top level file is pyhouse.yaml.

The config system is case sensitive.



### END DBK
