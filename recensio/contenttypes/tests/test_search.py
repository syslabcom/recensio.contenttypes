# -*- coding: utf-8 -*-
import unittest2 as unittest
from recensio.policy.indexer import authors
from recensio.policy.indexer import authorsFulltext
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestSearch(unittest.TestCase):
    """ """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        issue = self.portal["sample-reviews"].newspapera.summer["issue-2"]
        review_id = issue.objectIds()[0]
        self.review = issue[review_id]
        self.review.setAuthors(
            [
                {
                    "lastname": u"Kotłowski",
                    "firstname": u"Tadeusz",
                },
                {
                    "lastname": u"North",
                    "firstname": u"Pete",
                },
            ]
        )
        self.review.setReviewAuthors(
            [
                {
                    "lastname": u"Testchew",
                    "firstname": u"Vitali",
                },
                {
                    "lastname": u"Стоичков",
                    "firstname": u"Христо",
                },
            ]
        )

    def test_SearchableText(self):
        text = self.review.SearchableText()
        self.assertIn("Czernowitz", text)
        self.assertIn("TEXT TEXT", text)
        self.assertIn("PDF PDF", text)
        self.assertIn(u"Kotłowski".encode("utf-8"), text)
        self.assertIn(u"Testchew".encode("utf-8"), text)
        self.assertIn(self.review.Creator(), text)

        self.assertIn(self.review.Title(), text)
        self.assertIn(self.review.getSubtitle(), text)
        self.assertIn(self.review.getYearOfPublication(), text)
        self.assertIn(self.review.getPlaceOfPublication(), text)
        self.assertIn(self.review.getPublisher(), text)
        self.assertIn(self.review.getSeries(), text)
        self.assertIn("9788360448417", text)

    def test_authors_index(self):
        self.assertIn(u"Kotłowski, Tadeusz".encode("utf-8"), authors(self.review)())
        self.assertIn(u"North, Pete".encode("utf-8"), authors(self.review)())
        self.assertIn(u"Testchew, Vitali".encode("utf-8"), authors(self.review)())
        self.assertIn(u"Стоичков, Христо".encode("utf-8"), authors(self.review)())
        self.assertIn(
            u"Kotłowski, Tadeusz".encode("utf-8"), authorsFulltext(self.review)()
        )
        self.assertIn(u"North, Pete".encode("utf-8"), authorsFulltext(self.review)())
        self.assertIn(
            u"Testchew, Vitali".encode("utf-8"), authorsFulltext(self.review)()
        )
        self.assertIn(
            u"Стоичков, Христо".encode("utf-8"), authorsFulltext(self.review)()
        )
