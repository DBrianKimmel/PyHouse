"""
# lighting/__init__.py

When adding a family of lighting devices:
    * Create a new package named like 'Insteon'
    * Create a module in that package named like 'Insteon_device'
    * Create a module in that package named like 'Insteon_xml'
    * Create other modules as needed.
    * Add family name to VALID_FAMILIES in families.__init__.py

"""

import sys

__version_info__ = (1, 4, 0)
__version__ = '.'.join(map(str, __version_info__))

VALID_LIGHTS_TYPE = ['Button', 'Controller', 'Light']

# ## END DBK
