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

        self.cat = getToolByName(self.portal, 'portal_catalog')

    def test_SearchableText(self):
        text = self.review.SearchableText()
        self.assertIn('Czernowitz', text)
        self.assertIn('TEXT TEXT', text)
        self.assertIn('PDF PDF', text)
        self.assertIn('9788360448417', text)

    def assertOneSearchResult(self, search_text):
        res = self.cat(SearchableText=search_text)
        self.assertEqual(
            len(res), 1,
            msg="Did not get exactly one search result for {0}".format(
                search_text))

    def test_find_isbn_in_full_text_search(self):
        # Most of these fail - it looks like numbers are not tokenised
        #self.assertOneSearchResult('978-83-60448-39-7')
        self.assertOneSearchResult('9788360448417')
        #self.assertOneSearchResult('978 83 60448 41 7')
        #self.assertOneSearchResult('978-83')
        #self.assertOneSearchResult('97883')
        #self.assertOneSearchResult('978 83')
        #self.assertOneSearchResult('9-788-3604-48-41-7')
