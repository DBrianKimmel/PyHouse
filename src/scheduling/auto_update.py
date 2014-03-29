"""
Created on Dec 31, 2013

@author: briank

This module checks with something central and updates the PyHouse software if an update is needed.
"""


# strategy:
#
# if there is a VERSION file, use its contents. otherwise, call git to
# get a version string. if that also fails, use 'latest'.
#

import os


class FindLocalVersion(object):

    def __init__(self):
        self.m_version = 'latest'
        self.m_source = 'latest'
        self.m_filename = None
        try:
            self.m_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION')
            with open(self.m_filename) as f:
                self.m_version = f.read().strip()
                self.m_source = 'Local file {0:}'.format(self.m_filename)

        except IOError:
            from subprocess import Popen, PIPE
            import re

            VERSION_MATCH = re.compile(r'\d+\.\d+\.\d+(\w|-)*')

            try:
                l_dir = os.path.dirname(os.path.abspath(__file__))
                l_pipe = Popen(['git', 'describe', '--tags', '--always'], cwd = l_dir, stdout = PIPE, stderr = PIPE)
                l_out = l_pipe.communicate()[0]

                if (not l_pipe.returncode) and l_out:
                    l_ver = VERSION_MATCH.search(l_out)
                    if l_ver:
                        self.m_version = l_ver.group()
                        self.m_source = 'Git repository {0:}, {1:}'.format(l_out, l_ver)
            except OSError:
                pass

    def get_version(self):
        return (self.m_version, self.m_source, self.m_filename)


class FindRepositoryVersion(object):

    def __init__(self):
        self.m_version = '0.0.0'

    def get_version(self):
        return self.m_version


class API(object):
    """
    """


# ## END DBK
