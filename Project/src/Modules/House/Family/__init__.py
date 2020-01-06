"""
@name:      PyHouse/src/Modules/Family/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:


Various families of lighting systems.

insteon
upb
x-10
zigbee
z-wave
lutron
and others

To add a family named 'NewFamily', do the following:
    * Add a package named 'New_Family'.
    * Add the family name (Capitalized) to the list MODULES below.
    * Add a module named <NewFamily>_device.py
    * Add any other modules needed by the Device module.
        <Newfamily>_xml
        <NewFamily>_data
        ...
    * A module to interface with the controller is recommended.
        <NewFamily>_pim

There are a number of lighting 'Family' types handled here.
The Insteon family is now functional (2012).
The UPB family is work in progress
The X-10 family is mostly just a stub at present (2012)

When PyHouse is reading in the configuration for various devices, a call to family.ReadXml() is made to
add any family specific data for that device.  The data for the device MUST include a 'DeviceFamily'
attribute that is already initialized with the family name.

Each family consists of four or more major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

Since these controllers also control things other than lights, there is also a device type defined.
Devices to control include Lights, Thermostat, Irrigation valves Pool Equipment etc.

"""

__updated__ = '2020-01-05'
__version_info__ = (19, 11, 28)
__version__ = '.'.join(map(str, __version_info__))

VALID_DEVICE_TYPES = ['Light', 'Thermostat', 'Irrigation', 'Pool']

CONFIG_NAME = 'families'

MODULES = [
    'Acurite',
    'Hue',
    'Insteon',
    'Lutron',
    'Sonoff',
    'Upb',
    'X10',
    'Zwave',
    'Null'
    ]

# ## END DBK
