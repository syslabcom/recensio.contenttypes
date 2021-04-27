"""
The auto-generated doctests here are disabled
"""

from recensio.contenttypes.tests import base
from Testing import ZopeTestCase as ztc

import doctest
import unittest


# from zope.testing import doctestunit
# from zope.component import testing, eventtesting


def test_suite():
    return unittest.TestSuite(
        [
            # Demonstrate the main content types
            ztc.ZopeDocFileSuite(
                "README.txt",
                package="recensio.contenttypes",
                test_class=base.RecensioContenttypes,
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                | doctest.NORMALIZE_WHITESPACE
                | doctest.ELLIPSIS,
            ),
        ]
    )
