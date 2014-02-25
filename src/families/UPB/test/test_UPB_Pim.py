"""
Created on Apr 8, 2013

@author: briank
"""

from twisted.trial import unittest
import xml.etree.ElementTree as ET

from src.families.UPB import UPB_Pim
from src.lights import lighting_core


"""
<House Name='House_1' Key='0' Active='True'>
    <Controllers>
        <Controller Name='Serial_1' Key='0' Active='True'>
            <Interface>Serial</Interface>
            <BaudRate>19200</BaudRate>
            <ByteSize>8</ByteSize>
            <DsrDtr>False</DsrDtr>
            <Parity>N</Parity>
            <RtsCts>False</RtsCts>
            <StopBits>1.0</StopBits>
            <Timeout>0</Timeout>
            <XonXoff>False</XonXoff>
        </Controller>
        <Controller Name='USB_1' Key='1' Active='True'>
            <Interface>USB</Interface>
            <Vendor>12345</Vendor>
            <Product>9876</Product>
        </Controller>
    </Controllers>
</House>
"""
XML = """
<Test>
</Test>
"""

class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        """PyHouse.
        """
        self.API = None
        self.HousesAPI = None
        self.LogsAPI = None
        self.WebAPI = None
        self.WebData = None
        self.LogsData = None
        self.HousesData = None
        self.XmlRoot = None
        self.XmlFileName = ''

class HouseData(object):

    def __init__(self):
        """House.
        """
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.UUID = None
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        # self.Location = location.LocationData()  # one location per house.
        # a dict of zero or more of the following.
        self.Buttons = {}
        self.Controllers = {}
        self.FamilyData = {}
        self.Internet = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedules = {}

class ControllerData(lighting_core.CoreData):
    """This data is common to all controllers.

    There is also interface information that controllers need.
    """

    def __init__(self):
        super(ControllerData, self).__init__()  # The core data
        self.Type = 'Controller'  # Override the core definition
        self.Interface = ''
        self.Port = ''
        #
        self._DriverAPI = None  # Interface API() - Serial, USB etc.
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        #
        self._Data = None  # Interface specific data
        self._Message = ''
        self._Queue = None

class Test(unittest.TestCase):


    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_house_obj = HouseData()
        self.m_controller = ControllerData()
        self.m_api = UPB_Pim.API()

    def tearDown(self):
        pass


    def test_001_load_xml(self):
        print "Root Element", self.m_root_element
        self.m_api.Start(self.m_house_obj, self.m_controller)

# ## END DBK
