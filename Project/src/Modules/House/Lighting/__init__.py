"""
@name:      Modules/House/Lighting/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.
"""

__updated__ = '2020-01-20'
__version_info__ = (20, 1, 20)
__version__ = '.'.join(map(str, __version_info__))

VALID_LIGHTING_TYPE = ['Button', 'Controller', 'Light']

MODULES = [
    'Buttons',
    'Controllers',
    'Lights',
    'Outlets'
    ]

# ## END DBK
