import unittest2 as unittest
from Products.CMFPlone.utils import getToolByName

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestSearch(unittest.TestCase):
    """ """
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        issue = self.portal["sample-reviews"].newspapera.summer["issue-2"]
        review_id = issue.objectIds()[0]
        self.review = issue[review_id]

    def test_SearchableText(self):
        text = self.review.SearchableText()
        self.assertIn('Czernowitz', text)
        self.assertIn('TEXT TEXT', text)
        self.assertIn('PDF PDF', text)
        self.assertIn(
            self.review.getAuthors()[0]['lastname'].encode('utf-8'), text)
        self.assertIn(self.review.Creator(), text)

        self.assertIn(self.review.Title(), text)
        self.assertIn(self.review.getSubtitle(), text)
        self.assertIn(self.review.getYearOfPublication(), text)
        self.assertIn(self.review.getPlaceOfPublication(), text)
        self.assertIn(self.review.getPublisher(), text)
        self.assertIn(self.review.getSeries(), text)
        self.assertIn('9788360448417', text)
