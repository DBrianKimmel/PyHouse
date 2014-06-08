"""
@name: PyHouse/src/Modules/utils/test/test_pyh_log.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Apr 30, 2014
@license: MIT License
@summary: This module is for testing logging.\
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.utils import pyh_log as pyhLog
from src.test import xml_data
from Modules.Core.data_objects import PyHouseData

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_api = pyhLog.API()

    def test_0201_read_xml(self):
        self.m_api.read_xml(self.m_pyhouses_obj)
        self.assertEqual(self.m_pyhouses_obj.LogsData.Debug, '/var/log/pyhouse/debug')
        self.assertEqual(self.m_pyhouses_obj.LogsData.Error, '/var/log/pyhouse/error')


class Test_03_SetupLogging(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_api = pyhLog.API()
        self.m_api.read_xml(self.m_pyhouses_obj)
        self.LOG = pyhLog.getLogger('PyHouse.test_pyh_log ')

    def test_0301_openLogger(self):
        self.m_api.setup_debug_log(self.m_pyhouses_obj)
        self.LOG.debug('test-0301')
        print('self.LOG: {0:}'.format(self.LOG))

    def test_0302_openDebug(self):
        pass

'''
class Test_05_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        print('pyhLog_05  {0:}'.format(pyhLog))
        self.LOG = pyhLog.Manager().getLogger(__name__)

    def _test_level(self, level, messages_number):
        observer = pyhLog.CollectingObserver(level)
        pyhLog.addObserver(observer)

        self.LOG.debug('test debug')
        self.LOG.info('test info')
        self.LOG.warning('test warning')
        self.LOG.error('test error')
        self.LOG.critical('test critical')

        pyhLog.removeObserver(observer)
        self.assertEqual(len(observer.log), messages_number)

        for entry in observer.log:
            self.assertGreaterEqual(entry['level'], level)
            text = "test {0}".format(
                    logging.getLevelName(entry['level']).lower())
            self.assertEqual(entry['text'], text)
            self.assertEqual(entry['system'], __name__)

    def Xtest_0501_level_noset(self):
        self._test_level(logging.NOTSET, 5)

    def Xtest_0502_level_debug(self):
        self._test_level(logging.DEBUG, 5)

    def Xtest_0503_level_info(self):
        self._test_level(logging.INFO, 4)

    def Xtest_0504_level_warning(self):
        self._test_level(logging.WARNING, 3)

    def Xtest_0505_level_error(self):
        self._test_level(logging.ERROR, 2)

    def Xtest_0506_level_critical(self):
        self._test_level(logging.CRITICAL, 1)




class +
Test_06_LevelFileLogObserverTest(unittest.TestCase):

    rx = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})[+-]\d{2}\d{2}\s+([A-Z]+):\[([\w\.]+)\]:\s(.+)'

    def setUp(self):
        self.LOG = logging.getLogger(__name__)
        print('LOG {0:}'.format(self.LOG))
        self.log_path = tempfile.mktemp()
        self.log_file = open(self.log_path, 'w')

    def tearDown(self):
        self.log_file.close()
        os.remove(self.log_path)

    def _test_level(self, level, messages_number):
        observer = LevelFileLogObserver(self.log_file, level)
        pyhLog.addObserver(observer)

        self.LOG.debug('test debug')
        self.LOG.info('test info')
        self.LOG.warning('test warning')
        self.LOG.error('test error')
        self.LOG.critical('test critical')

        pyhLog.removeObserver(observer)

        with open(self.log_path) as f:
            lines = [line.strip() for line in f.readlines()]

        self.assertEqual(len(lines), messages_number)

        for line in lines:
            m = re.match(self.rx, line)
            self.assertIsNotNone(m)

            time, level_name, system, entry_text = m.groups()

            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            entry_level = logging.getLevelName(level_name)

            self.assertGreaterEqual(entry_level, level)
            self.assertEqual(system, __name__)

            text = "test {0}".format(level_name.lower())
            self.assertEqual(entry_text, text)

    def Xtest_0601_level_noset(self):
        print('Logging {0:}'.format(logging))
        self._test_level(logging.NOTSET, 5)

    def Xtest_0602_level_debug(self):
        self._test_level(logging.DEBUG, 5)

    def Xtest_0603_level_info(self):
        self._test_level(logging.INFO, 4)

    def Xtest_0604_level_warning(self):
        self._test_level(logging.WARNING, 3)

    def Xtest_0605_level_error(self):
        self._test_level(logging.ERROR, 2)

    def Xtest_0606_level_critical(self):
        self._test_level(logging.CRITICAL, 1)

'''

# ## END DBK
