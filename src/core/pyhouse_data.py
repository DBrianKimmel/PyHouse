"""
Created on Mar 20, 2014

@author: briank
"""



class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        """PyHouse.
        """
        self.API = None
        self.CoreAPI = None
        self.HousesAPI = None
        self.LogsAPI = None
        self.WebAPI = None
        #
        self.WebData = None
        self.LogsData = None
        self.HousesData = None
        self.XmlRoot = None
        self.XmlFileName = ''
        self.Reactor = None
        self.Nodes = None

    def __str__(self):
        l_ret = "PyHouseData:: "
        l_ret += "\n\tHousesAPI:{0:}, ".format(self.HousesAPI)
        l_ret += "\n\tLogsAPI:{0:}, ".format(self.LogsAPI)
        l_ret += "\n\tWebAPI:{0:}, ".format(self.WebAPI)
        l_ret += "\n\tWebData:{0:}, ".format(self.WebData)
        l_ret += "\n\tLogsData:{0:}, ".format(self.LogsData)
        l_ret += "\n\tHousesData:{0:};".format(self.HousesData)
        l_ret += "\n\tXmlRoot:{0:}, ".format(self.XmlRoot)
        l_ret += "\n\tXmlFileName:{0:}, ".format(self.XmlFileName)
        return l_ret

    def reprJSON(self):
        """PyHouse.
        """
        l_ret = dict(
            XmlFileName = self.XmlFileName,
            HousesData = self.HousesData
            )
        return l_ret



# ## END DBK
