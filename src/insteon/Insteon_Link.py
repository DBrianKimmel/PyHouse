#!/usr/bin/python

"""Insteon Link module.

Handle the all-link database(s) in insteon devices.
"""

# Import system type stuff
import logging

# Import PyMh files
#import configure_mh

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

    def get_all_links_controller(self):
        pass

    def get_all_links_responder(self):
        pass


class InsteonLinkMain(InsteonLinkAPI):

    def __init__(self):
        self.m_logger = logging.getLogger('PyMh.Insteon_Link')
        self.m_logger.info('Initialized.')

### END
