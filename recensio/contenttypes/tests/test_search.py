# -*- coding: utf-8 -*-
from plone import api
from recensio.policy.indexer import authors
from recensio.policy.indexer import authorsFulltext
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING

import unittest2 as unittest


class TestSearch(unittest.TestCase):
    """ """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        issue = self.portal["sample-reviews"].newspapera.summer["issue-2"]
        review_id = issue.objectIds()[0]
        gnd_view = api.content.get_view(
            context=self.portal,
            request=self.layer["request"],
            name="gnd-view",
        )
        self.review = issue[review_id]
        self.authors = self.review.getAuthors()
        self.reviewAuthors = self.review.getReviewAuthors()

    def test_SearchableText(self):
        text = self.review.SearchableText()
        self.assertIn("Czernowitz", text)
        self.assertIn("TEXT TEXT", text)
        self.assertIn("PDF PDF", text)
        for author in self.authors:
            self.assertIn(author.lastname, text)
        for author in self.reviewAuthors:
            self.assertIn(author.lastname, text)
        self.assertIn(self.review.Creator(), text)

        self.assertIn(self.review.Title(), text)
        self.assertIn(self.review.getSubtitle(), text)
        self.assertIn(self.review.getYearOfPublication(), text)
        self.assertIn(self.review.getPlaceOfPublication(), text)
        self.assertIn(self.review.getPublisher(), text)
        self.assertIn(self.review.getSeries(), text)
        self.assertIn("9788360448417", text)

    def test_authors_index(self):
        for author in self.authors:
            self.assertIn(author.Title(), authors(self.review)())
            self.assertIn(author.Title(), authorsFulltext(self.review)())
        for author in self.reviewAuthors:
            self.assertIn(author.Title(), authors(self.review)())
            self.assertIn(author.Title(), authorsFulltext(self.review)())
