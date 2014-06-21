"""
@name: PyHouse/src/Modules/web/test/test_web_houseSelect.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jun 6, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.web import web_houseSelect
from Modules.utils.tools import PrettyPrintAny


class Test_10(unittest.TestCase):

    def setUp(self):
        self.m_api = web_houseSelect.HouseSelectElement(None)

    def tearDown(self):
        pass

    def test_1011_getHousesToSelect(self):
        l_json = self.m_api.getHousesToSelect(None)
        PrettyPrintAny(l_json, 'Houses to select')

    def test_1012_getSelectedHouseData(self):
        pass

# ## END DBK
