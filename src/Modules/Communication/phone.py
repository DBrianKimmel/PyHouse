"""
-*- test-case-name:  PyHouse/src/Modules/Communication/phone.py  -*-

@name:       PyHouse/src/Modules/Communication/phone.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on May 30, 2016
@licencse:   MIT License
@summary:

"""

#  Import system type stuff


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Communication = Utility().read_xml(p_pyhouse_obj)

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = ET.Element('CommunicationSection')
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        pass

# ## END DBK
