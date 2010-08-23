# -*- coding: utf-8 -*-
"""
Various files (PDF, SWF) are associated with Reviews/Presentations
these tests cover the conversions on those files to other formats.
"""
import datetime
from os import fstat

import unittest2 as unittest
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from plone.app.blob.utils import openBlob

from wc.pageturner.settings import Settings


class TestReviewFileConversions(unittest.TestCase):
    """Test file conversions.

    Test the file conversions (Word/HTML->PDF->SWF) that take place
    when a Review is added or edited.
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def test_conversions(self):
        portal = self.layer["portal"]
        sample_reviews = portal["sample-reviews"]
        review = sample_reviews[sample_reviews.objectIds()[0]]
        # The sample reviews have pdf and word doc
        self.assertTrue(review.doc.get_size() > 0)
        self.assertTrue(review.pdf.get_size() > 0)
        # Since there is a custom pdf, a pdf has not been generated
        self.assertFalse(hasattr(review, "generatedPdf"))
        settings = Settings(review)
        swf_blob = openBlob(settings.data)
        swf_size = fstat(swf_blob.fileno()).st_size
        swf_blob.close()
        self.assertTrue(swf_size > 0)
        pass

