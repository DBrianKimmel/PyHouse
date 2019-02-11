* Name:      PyHouse/Project/src/Modules/Familiies/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-02-10
* Updated:   2010-02-10
* License:   MIT License
* Summary:   This is the design documentation for the Families Modules of PyHouse.

# Families

The putpose of the families is to allow us to have multiple families of devices.
Each family takes and provides the detailed control of the devices from the more abstract core of PyHouse.
For example, turning on an Insteon switch controlling a light is much different than controlling a UPB switch or a Lutron switch, etc.

families are defined in the XML by <DeviceFamily> tags.
A list of VALID_FAMILIES is 

There is a 'Null' family which does nothing.


## Adding a Family

To add a family named 'NewFamily', do the following:
    * Add a package named 'New_Family'.
    * Add the family name (Capitalized) to the list VALID_FAMILIES in __init__.
    * Add a module named <NewFamily>_device.py
    * Add any other modules needed by the Device module.
        <Newfamily>_xml
        <NewFamily>_data
        ...
    * A module to interface with the controller is recommended.
        <NewFamily>_pim

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional (2012).
The UPB family is work in progress (2012).
The X-10 family is mostly just a stub at present (2012)

When PyHouse is reading in the configuration for various devices, a call to family.ReadXml() is made to
add any family specific data for that device.  The data for the device MUST include a 'DeviceFamily'
attribute that is already initialized with the family name.

Each family consists of four or more major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)
    HVAC
    Security
    Entertainment
    Pools
    Irrigation

Since these controllers also control things other than lights, there is also a device type defined.
Devices to control include Lights, Thermostat, Irrigation valves Pool Equipment etc.


### END DBK
