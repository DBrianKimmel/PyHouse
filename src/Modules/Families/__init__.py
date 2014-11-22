"""
families.__init__.py

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
    * Add the family name (Capitalized) to the list VALID_FAMILIES below.
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
add any family specific data for that device.  The data for the device MUST include a 'ControllerFamily'
attribute that is already initialized with the family name.

Each family consists of four or more major areas:
    Lights / Lighting Devices
    Controllers - connected to the computer
    Scenes - have one or more lights that are controlled together
    Buttons - extra buttons with no light directly attached (key-pad-link)

"""

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_FAMILIES = ['Insteon', 'UPB', 'X10', 'Null']

# ## END DBK
