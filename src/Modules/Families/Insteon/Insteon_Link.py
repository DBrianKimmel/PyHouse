"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_Link -*-

@name: PyHouse/src/Modules/Families/Insteon/Insteon_Link.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Feb 18, 2010  Split into separate file Jul 9, 2014
@license: MIT License
@summary: Handle the all-link database(s) in Insteon devices.
"""

class LinkData(object):
    """
    """

    def __init__(self):
        self.InsteonAddess = 12345
        self.Data = '00.00.00'
        self.Flag = 0xC2
        self.Group = 0


class API(LinkData):
    """
    """


# ## END DBK
