# -*- coding: utf-8 -*-
"""
Various files (PDF, Word docs) are associated with Reviews/Presentations
these tests cover the conversions on those files to other formats.
"""
import datetime
from os import fstat
import unittest2 as unittest

import zope.event

from Testing import makerequest
from plone.app.blob.utils import openBlob
from Products.Archetypes.event import ObjectEditedEvent

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING

class TestReviewFileConversions(unittest.TestCase):
    """Test file conversions.

    Test the file conversions (Word/HTML->PDF) that take place
    when a Review is added or edited.
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def test_review_with_custom_pdf_files(self):
        """Reviews / Presentations which have a custom pdf file will
        use that version for downloading
        """
        portal = self.layer["portal"]
        pm = portal.portal_membership
        fake_member_folder = pm.getMembersFolder().get("fake_member")
        online_resource = fake_member_folder.listFolderContents(
            contentFilter={"portal_type" : "Presentation Online Resource"}
            )[0]
        self.assertTrue(len(online_resource.pagePictures) > 0 and \
                        len(online_resource.pagePictures[0]) > 1000,
                        msg=("Presentation Online Resource: %s "
                             "The generated images for previewing the "
                             "online resource haven't been generated"
                             %(online_resource.absolute_url()
                               )
                             )
                        )

        # The sample reviews have both a pdf and a word doc attached

        # Get a ReviewMonograph
        issue = portal["sample-reviews"].newspaperb.summer["issue-2"]
        review_id = issue.objectIds()[0]
        review = issue[review_id]

        # The default sample content has a custom pdf to start with
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
        self.assertTrue(review.pdf.blob == review.get_review_pdf()["blob"],
                        msg=("Review: %s "
                             "get_review_pdf doesn't return the custom pdf."
                             %review.absolute_url()))
        self.assertTrue(len(review.pagePictures) > 0 and \
                        len(review.pagePictures[0]) > 1000,
                        msg=("Review: %s "
                             "The generated images for previewing the review "
                             "haven't been generated"
                             %(review.absolute_url()
                               )
                             )
                        )
        # Remove the custom pdf and trigger the ObjectEditedEvent
        # This should cause the pdf to be generated from the Word doc
        review.setPdf(None)
        self.assertTrue(review.getPdf().get_size() == 0,
                        msg=("Review: %s "
                             "still has an attached custom pdf file, "
                             "this should have been removed."
                             %review.absolute_url()))
        request = makerequest.makerequest(review)
        event = ObjectEditedEvent(review, request)
        zope.event.notify(event)
        self.assertTrue(hasattr(review, "generatedPdf"),
                        msg=("Review: %s "
                             "A pdf has not successfully been generated."
                             %review.absolute_url()))
        self.assertTrue(
            review.generatedPdf == review.get_review_pdf()["blob"],
            msg=("Review: %s get_review_pdf "
                 "is not returning the correct pdf."
                 %review.absolute_url()))

        # Remove the Word doc and the review html content should be
        # used instead to create the pdf version
        review.setDoc(None)
        self.assertTrue(review.getDoc().get_size() == 0,
                        msg=("Review: %s "
                             "The attached doc file has not been "
                             "successfully removed."
                             %review.absolute_url()))
        request = makerequest.makerequest(review)
        event = ObjectEditedEvent(review, request)
        zope.event.notify(event)
