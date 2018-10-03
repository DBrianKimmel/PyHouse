* Name:      PyHouse/Project/src/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-01
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.

MAIN
====

This is the top level documentation for PyHouse.

The initial portion is PyHouse.py.
It is a singleton so we don't end up with multiple running instances.

Logging is setup and activated the very first thing so that the rest of the startup progress is logged.
The log file is /var/log/pyhouse/debug

Every called program has an API section.
There are several main parts in each part, Initialization, LoadXML, Start and SaveXML and Stop.
Stop is not used and may be removed in the near future.

### END DBK
