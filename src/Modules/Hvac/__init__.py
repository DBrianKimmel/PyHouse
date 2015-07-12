"""

@name:      PyHouse/src/Modules/Hvac/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 27, 2013
@Summary:

This is the interface from HVAC to PyHouse.

The only valid function at this point is the thermostat.

"""

__version_info__ = (1, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_TEMP_SYSTEMS = ['C', 'F']
VALID_THERMOSTAT_MODES = ['Heat', 'Cool', 'Auto', 'EHeat']

# ## END
