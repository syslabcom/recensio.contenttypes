"""
The auto-generated doctests here are disabled
"""

import doctest
import unittest

from plone.testing import layered
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from Testing import ZopeTestCase as ztc

# from zope.testing import doctestunit
# from zope.component import testing, eventtesting





def test_suite():
    return unittest.TestSuite(
        [
            # Demonstrate the main content types
            layered(
                doctest.DocFileSuite(
                    "fields.txt",
                    package="recensio.contenttypes",
                    optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
                    | doctest.NORMALIZE_WHITESPACE
                    | doctest.ELLIPSIS,
                ),
                layer=RECENSIO_INTEGRATION_TESTING,
            )
        ]
    )
