"""
-*- test-case-name: PyHouse.Modules.Scheduling.test.test_auto_update -*-

@name:      PyHouse/src/Modules/Scheduling/auto_update.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@note:      Created on Dec 31, 2013
@license:   MIT License
@summary:   Handle the automatic updating of PyHouse

This module automatically updates PyHouse

"""

__updated__ = '2019-01-15'

# strategy:
#
# if there is a VERSION file, use its contents. otherwise, call git to
# get a version string. if that also fails, use 'latest'.
#

# Import system type stuff
import os.path
from twisted.web.client import getPage
from lxml import etree

# Import PyHouse files

VERSION_PATH = '../../../../VERSION'
REPOSITORY = b'https://github.com/DBrianKimmel/PyHouse/'
REPOSITORY_PATH = 'Project/VERSION'


def _find_pyhouse_version_file():
    """
    Find the normalized VERSION file name
    PyHouse/Project/src/VERSION
    """
    l_dir = os.path.abspath(__file__)
    l_filename = os.path.join(os.path.dirname(l_dir), VERSION_PATH)
    l_filename = os.path.normpath(l_filename)
    return l_filename


class FindLocalVersion(object):
    """ Find out what version that we are.
    """

    def __init__(self):
        self.m_version = 'latest'
        self.m_source = 'latest'
        self.m_filename = _find_pyhouse_version_file()
        try:
            with open(self.m_filename) as f:
                self.m_version = f.read().strip()
                self.m_source = 'Local file {}'.format(self.m_filename)

        except IOError:
            from subprocess import Popen, PIPE
            import re

            VERSION_MATCH = re.compile(r'\d+\.\d+\.\d+(\w|-)*')

            try:
                l_dir = os.path.dirname(os.path.abspath(__file__))
                l_pipe = Popen(['git', 'describe', '--tags', '--always'], cwd=l_dir, stdout=PIPE, stderr=PIPE)
                l_out = l_pipe.communicate()[0]

                if (not l_pipe.returncode) and l_out:
                    l_ver = VERSION_MATCH.search(l_out)
                    if l_ver:
                        self.m_version = l_ver.group()
                        self.m_source = 'Git repository {}, {}'.format(l_out, l_ver)
            except OSError:
                pass

    def get_version(self):
        return (self.m_version, self.m_source, self.m_filename)


class FindRepositoryVersion(object):
    """ Check the version in the repository
    """

    def __init__(self):
        self.m_version = '0.0.0'

    def print_page(self, p_html):
        """
        """
        print(p_html)
        pass

    def get_page(self):
        """
        """
        l_defer = getPage(REPOSITORY)
        l_defer.addCallback(self.print_page)

    def get_version(self):
        return self.m_version

    def parseHtml(self, p_html):
        l_parser = etree.HTMLParser(encoding='utf8')
        # tree = etree.parse(StringIO.StringIO(html), parser)
        # return tree

    def extractTitle(self, p_tree):
        # titleText = unicode(tree.xpath("//title/text()")[0])
        # return titleText
        pass

    # d = getPage('http://www.google.com')
    # d.addCallback(parseHtml)
    # d.addCallback(extraTitle)
    # d.addBoth(println)


class Utility(object):
    """
    """

    def compare_versions(self, p_local_ver, p_repos_ver):
        return True


class API(Utility):
    """
    """

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

# ## END DBK
