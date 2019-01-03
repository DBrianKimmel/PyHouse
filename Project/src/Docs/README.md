* Name:      PyHouse/Project/src/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-01
* License:   MIT License
* Summary:   This is the design documentation for PyHouse.

# PyHouse

This is the top level documentation for PyHouse.

The initial execution is of PyHouse.py.
It is a singleton so we don't end up with multiple running instances.

Logging is setup and activated the very first thing so that the rest of the startup progress is logged.
The log file is /var/log/pyhouse/debug

The next thing activated is MQTT so we can begin with messaging.


## Running

Every called program has an API section.
There are several main parts in each part, Initialization, LoadXML, Start and SaveXML and Stop.
Stop is not used and may be removed in the near future.

### Initialization
Initialization is called first.
The reactor is not running during initialization.
Only major modules are initialized.
Logging is set up and started at the beginning of initialization.
Plugins are initialized later, during XML loading.

### Load XML

This happens next.
The reactor is started  first.


### Start

This happens next.


### Operational

This happens .

### END DBK
