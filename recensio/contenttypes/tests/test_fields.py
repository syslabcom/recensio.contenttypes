"""
The auto-generated doctests here are disabled
"""

import unittest
import doctest

#from zope.testing import doctestunit
#from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from plone.testing import layered

from recensio.contenttypes.tests import base


def test_suite():
    return unittest.TestSuite([

        # Demonstrate the main content types
        layered(doctest.DocFileSuite(
            'fields.txt', package='recensio.contenttypes',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
               ),
               layer=base.RECENSIO_INTEGRATION_TESTING)])