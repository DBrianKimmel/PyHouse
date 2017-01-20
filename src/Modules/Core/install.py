"""
@name:      PyHouse/src/Modules/Core/install.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 7, 2015
@Summary:

"""

__updated__ = '2017-01-20'


# Import system type stuff
import pip

def install_astral():
    pip.main(['install', 'astral'])

class API(object):

    def __init__(self):
        pass

# ## END DBK
