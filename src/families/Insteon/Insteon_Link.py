#!/usr/bin/python

"""Insteon Link module.

Handle the all-link database(s) in insteon devices.
"""

# Import system type stuff
import logging

# Import PyMh files
# import configure_mh

g_debug = 9

Link_Data = {}

m_logger = None


class LinkData(object):
    """
    """

    def __init__(self):
        pass

    def dump_link_data(self):
        """
        """
        for k, v in self.Link_Data.iteritems():
            print k, v


class InsteonLinkAPI(LinkData):

    def store_link(self, p_dict):
        """Add the link to ???
        """
        pass

    def add_link_controller(self):
        pass

    def add_link_responder(self):
        pass

    def delete_link_controller(self, p_name):
        pass

    def delete_link_responder(self):
        pass

    def get_all_links_controller(self, p_lighting_obj):
        if g_debug > 1:
            print "Insteon_Link.get_all_links_controller()"

    def get_all_links_responder(self):
        pass


class API(InsteonLinkAPI):

    def __init__(self):
        self.m_logger = logging.getLogger('PyMh.Insteon_Link')
        self.m_logger.info('Initialized.')

    def Start(self, p_house_obj):
        self.m_house_obj = p_house_obj

# ## END
