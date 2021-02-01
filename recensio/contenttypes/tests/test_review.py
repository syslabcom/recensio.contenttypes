# -*- coding: utf-8 -*-
import unittest

from recensio.contenttypes.content.review import BaseReview
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestReviewTitle(unittest.TestCase):
    def test_one_title_and_one_subtitle(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        schema = obj.schema.copy()
        schema._fields["additionalTitles"] = "dummy"
        obj.schema = schema
        obj.getAdditionalTitles = lambda: []
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus",
        )

    def test_two_titles_and_two_subtitles(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        schema = obj.schema.copy()
        schema._fields["additionalTitles"] = "dummy"
        obj.schema = schema
        obj.getAdditionalTitles = lambda: [
            {
                "title": u"La Constitución española de 1812",
                "subtitle": u"El comienzo del constitucionalismo europeo",
            },
        ]
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus / La Constitución española de 1812. El "
            u"comienzo del constitucionalismo europeo",
        )

    def test_one_title_and_one_subtitle_and_translated_title(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        schema = obj.schema.copy()
        schema._fields["translatedTitle"] = "dummy"
        obj.translatedTitle = (
            u"The Spanish constitution of 1812. The beginning of European "
            "constitutionalism"
        )
        schema._fields["additionalTitles"] = "dummy"
        obj.schema = schema
        obj.getAdditionalTitles = lambda: []
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus [The Spanish constitution of 1812. The beginning of "
            "European constitutionalism]",
        )

    def test_two_titles_and_two_subtitles_and_translated_title(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        schema = obj.schema.copy()
        schema._fields["translatedTitle"] = "dummy"
        obj.translatedTitle = (
            u"The Spanish constitution of 1812. The beginning of European "
            "constitutionalism"
        )
        schema._fields["additionalTitles"] = "dummy"
        obj.schema = schema
        obj.getAdditionalTitles = lambda: [
            {
                "title": u"La Constitución española de 1812",
                "subtitle": u"El comienzo del constitucionalismo europeo",
            },
        ]
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus / La Constitución española de 1812. El "
            u"comienzo del constitucionalismo europeo [The Spanish constitution of "
            "1812. The beginning of European constitutionalism]",
        )


class TestReviewIntegration(unittest.TestCase):
    """
    """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review = self.portal.portal_catalog.search(
            {
                "portal_type": "Review Monograph",
                "path": {"query": "/".join(self.publication.getPhysicalPath())},
            }
        )[0].getObject()
        self.issue = self.review.aq_parent
        self.volume = self.issue.aq_parent

    def test_external_fulltext(self):
        self.assertFalse(self.review.isUseExternalFulltext())

        self.issue.setUseExternalFulltext(True)
        self.assertTrue(
            self.review.isUseExternalFulltext(), msg="Setting on Issue not used!"
        )

        self.volume.setUseExternalFulltext(True)
        self.assertTrue(
            self.review.isUseExternalFulltext(), msg="Setting on Issue not used!"
        )

        self.issue.setUseExternalFulltext(False)
        self.volume.setUseExternalFulltext(True)
        self.assertTrue(
            self.review.isUseExternalFulltext(), msg="Setting on Volume not used!"
        )

    def test_url_in_citation_review(self):
        self.assertTrue(self.review.isURLShownInCitationNote())
        self.review.setURLShownInCitationNote(False)
        self.assertFalse(self.review.isURLShownInCitationNote())

    def test_url_in_citation_issue(self):
        self.issue.setURLShownInCitationNote(False)
        self.volume.setURLShownInCitationNote(True)
        self.publication.setURLShownInCitationNote(True)
        self.assertFalse(
            self.review.isURLShownInCitationNote(), msg="Setting on Issue not used!"
        )

    def test_url_in_citation_issue_and_volume(self):
        self.issue.setURLShownInCitationNote(False)
        self.volume.setURLShownInCitationNote(False)
        self.publication.setURLShownInCitationNote(True)
        self.assertFalse(
            self.review.isURLShownInCitationNote(), msg="Setting on Issue not used!"
        )

    def test_url_in_citation_volume(self):
        self.issue.setURLShownInCitationNote(True)
        self.volume.setURLShownInCitationNote(False)
        self.publication.setURLShownInCitationNote(True)
        self.assertFalse(
            self.review.isURLShownInCitationNote(),
            msg="Setting on Volume not used by Review!",
        )
        self.assertFalse(
            self.issue.isURLShownInCitationNote(),
            msg="Setting on Volume not used by Issue!",
        )

    def test_url_in_citation_volume_and_publication(self):
        self.issue.setURLShownInCitationNote(True)
        self.volume.setURLShownInCitationNote(False)
        self.publication.setURLShownInCitationNote(False)
        self.assertFalse(
            self.review.isURLShownInCitationNote(),
            msg="Setting on Volume not used by Review!",
        )
        self.assertFalse(
            self.issue.isURLShownInCitationNote(),
            msg="Setting on Volume not used by Issue!",
        )

    def test_url_in_citation_publication(self):
        self.issue.setURLShownInCitationNote(True)
        self.volume.setURLShownInCitationNote(True)
        self.publication.setURLShownInCitationNote(False)
        self.assertFalse(
            self.review.isURLShownInCitationNote(),
            msg="Setting on Publication not used by Review!",
        )
        self.assertFalse(
            self.issue.isURLShownInCitationNote(),
            msg="Setting on Publication not used by Issue!",
        )
        self.assertFalse(
            self.volume.isURLShownInCitationNote(),
            msg="Setting on Publication not used by Volume!",
        )
