"""
hvac.__init__.py

This is the interface from HVAC to PyHouse.

The only valid function at this point is the thermostat.

"""

__version_info__ = (1, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_TEMP_SYSTEMS = ['C', 'F']
VALID_THERMOSTAT_MODES = ['Heat', 'Cool', 'Auto', 'EHeat']

# ## END
