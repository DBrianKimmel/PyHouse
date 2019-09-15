* Name:      PyHouse/Project/src/Modules/Core/Config/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-10-15
* Updated:   2019-10-15
* License:   MIT License
* Summary:   This is the design documentation for the Config Module of PyHouse.

# Config

This is responsible for loading all of the cunfiguration into the PyHouse structure.
It only loads what is configured in order to try to be as lean as possible running.

There may be several layers of config files to load a particular feature.

There is a house.yaml file that has entries for the house features that will be defined later.
For example, if there is no pool at a house, you would not place a "Pool" entry in the house.yaml configt file.
This way, if you wish to deactivate a system such as Irrigation, you do not have to delete the irrigation.yaml file
threby loosing all the config information.
You simply comment out the "Irrigation" entry in the house.yaml file and it will not be loaded.

All config files are locate under /etc/pyhouse and have a suffix of .yaml.
They can be located anywhere within that directory but are usually arranged in a heirarchy.

### END DBK
