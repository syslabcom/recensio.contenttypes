import unittest2 as unittest

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestSearch(unittest.TestCase):
    """ """
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

    def test_SearchableText(self):
        issue = self.portal["sample-reviews"].newspaperb.summer["issue-2"]
        review_id = issue.objectIds()[0]
        review = issue[review_id]
        text = review.SearchableText()
        self.assertIn('Czernowitz', text)
        self.assertIn('TEXT TEXT', text)
        self.assertIn('PDF PDF', text)
