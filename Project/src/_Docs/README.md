* Name:      PyHouse/Project/src/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2019-06-19
* License:   MIT License
* Summary:   This is the design documentation for PyHouse.

# PyHouse

This is the top level documentation for PyHouse.

The initial execution is of PyHouse.py.
It is a singleton so we don't end up with multiple running instances.

Logging is setup and activated the very first thing so that the rest of the startup progress is logged.
The log file is /var/log/pyhouse/XXX where XXX is error, warn, debug, and info

Now the configuration is read in.
Initially is was XML.
Due, in part, to the difficulty of correctly hand editing the XML file to add services, we are switching to Yaml.
The yaml file is a bit more forgiving of structual flaws.
yamllint is a good way of checking the yaml fragments.

The next thing activated is MQTT so we can begin with messaging.


## Running

Every called program has an API section.
There are several main parts in each part, Initialization, LoadXML, Start and SaveXML and Stop.
Stop is not used and may be removed in the near future.

### Initialization
Initialization is called first.
The reactor is not running during initialization.
Only major modules are initialized, plugins are initialized during the load config phase if they are defined.
Logging is set up and started at the beginning of initialization.

### Load Config

This happens next.
The reactor is started  first.


### Start

This happens next.


### Operational

This happens .

# Data Structure

There is an internal data structure that is built mostly from the config files.
It gets added to during the operation of PyHouse.
The pyhouse_obj construct has 2 major sections.
Data read in from and saved to the configuration file has the form of DataName.
Privte information that will not be saved to config files has the form of _DataName.
Entries with a leading underscore are never saved to a file.

## pyhouse_obj

pyhouse.{}
	Yaml.{}
		YamlConfigDir
        YamlFileName
        YamlTree.{}
        	Root.{}
        		Computer.{}
        		Core.{}
        		Driver.{}
        		Family.{}
        		House.{}
Root.{}
	Path
	
  

# Scheme
## Entity
This is the top level.
The self signing certificate for the entire organazation is at this level.
For all purposes this is the family.
Contains all lower levels down to houses

## Levels

## House


# Structure

```
Application
	Service
		Sub-Service
---	---	---
PyHouse
	Lighting
	HVAC
	Outside
		Pool
		Irrigation
```
### END DBK
