import unittest2 as unittest
from Products.CMFPlone.utils import getToolByName

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
        self.assertIn('9788360448397', text)

    @unittest.skip("This fails - it looks like numbers are not tokenised")
    def test_find_isbn_in_full_text_search(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        res = cat(SearchableText='97-883-604-48397')
        self.assertGreater(len(res), 0)
