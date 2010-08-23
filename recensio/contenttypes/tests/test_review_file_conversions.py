# -*- coding: utf-8 -*-
"""
Various files (PDF, SWF) are associated with Reviews/Presentations
these tests cover the conversions on those files to other formats.
"""
import datetime

import unittest2 as unittest
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestReviewFileConversions(unittest.TestCase):
    """Test file conversions.

    Test the file conversions (Word/HTML->PDF->SWF) that take place
    when a Review is added or edited.
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def test_conversions(self):
        pass

