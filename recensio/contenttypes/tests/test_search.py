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
        self.assertIn('9788360448417', text)
