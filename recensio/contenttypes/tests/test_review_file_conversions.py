# -*- coding: utf-8 -*-
"""
Various files (PDF, SWF) are associated with Reviews/Presentations
these tests cover the conversions on those files to other formats.
"""
import datetime
from os import fstat
import unittest2 as unittest

import zope.event

from Testing import makerequest
from plone.app.blob.utils import openBlob
from Products.Archetypes.event import ObjectEditedEvent

from wc.pageturner.settings import Settings

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING

class TestReviewFileConversions(unittest.TestCase):
    """Test file conversions.

    Test the file conversions (Word/HTML->PDF->SWF) that take place
    when a Review is added or edited.
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def test_review_with_custom_pdf_files(self):
        """Reviews / Presentations which have a custom pdf file will
        use that version for downloading and conversion to swf
        """
        portal = self.layer["portal"]
        sample_reviews = portal["sample-reviews"]
        review = sample_reviews[sample_reviews.objectIds()[0]]
        # The sample reviews have both a pdf and a word doc attached
        self.assertTrue(review.pdf.get_size() > 0,
                        msg=("Review: %s "
                             "doesn't have a pdf file attached."
                             %review.absolute_url()))
        self.assertTrue(review.doc.get_size() > 0,
                        msg=("Review: %s "
                             "doesn't have a doc file attached."
                             %review.absolute_url()))
        self.assertFalse(hasattr(review, "generatedPdf"),
                        msg=("Review: %s "
                             "A pdf has been generated, even though this "
                             "review has a custom pdf (this is wrong)."
                             %review.absolute_url()))
        # An swf file has been created
        settings = Settings(review)
        swf_blob = openBlob(settings.data)
        swf_size = fstat(swf_blob.fileno()).st_size
        swf_blob.close()
        self.assertTrue(swf_size > 0,
                        msg=("Review: %s "
                             "doesn't have an swf version."
                             %review.absolute_url()))
        self.assertTrue(review.pdf.blob == review.get_review_pdf()
                        msg=("Review: %s "
                             "get_review_pdf doesn't return the custom pdf."
                             %review.absolute_url()))
        # Remove the custom pdf and trigger the ObjectEditedEvent
        # This should cause the pdf to be generated from the Word doc
        # and the swf to be generated from that
        review.setPdf(None)
        self.assertTrue(review.getPdf().get_size() == 0,
                        msg=("Review: %s "
                             "still has an attached custom pdf file, "
                             "this should have been removed."
                             %review.absolute_url()))
        request = makerequest.makerequest(review)
        event = ObjectEditedEvent(review, request)
        zope.event.notify(event)
        self.assertTrue(hasattr(review, "generatedPdf")
                        msg=("Review: %s "
                             "A pdf has not successfully been generated."
                             %review.absolute_url()))
        self.assertTrue(review.generatedPdf == review.get_review_pdf(),
                        msg=("Review: %s "
                             "get_review_pdf is not returning the correct pdf."
                             %review.absolute_url()))
        settings = Settings(review)
        doc_swf_blob = openBlob(settings.data)
        doc_swf_size = fstat(doc_swf_blob.fileno()).st_size
        doc_swf_blob.close()
        self.assertTrue(doc_swf_size != swf_size,
                        msg=("Review: %s "
                             "The size of the swf generated from the doc "
                             "version is the same as the swf generated from "
                             "custom pdf. This should not be the case."
                             %review.absolute_url()))

        # Remove the Word doc and the review html content should be
        # used instead to create the pdf and swf versions
        review.setDoc(None)
        self.assertTrue(review.getDoc().get_size() == 0,
                        msg=("Review: %s "
                             "The attached doc file has not been "
                             "successfully removed."
                             %review.absolute_url()))
        request = makerequest.makerequest(review)
        event = ObjectEditedEvent(review, request)
        zope.event.notify(event)
        settings = Settings(review)
        html_swf_blob = openBlob(settings.data)
        html_swf_size = fstat(html_swf_blob.fileno()).st_size
        html_swf_blob.close()
        self.assertTrue(html_swf_size != swf_size,
                        msg=("Review: %s "
                             "The size of the swf generated from the review "
                             "html is the same as the swf generated from "
                             "custom pdf. This should not be the case."
                             %review.absolute_url()))
