import unittest2 as unittest
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import TEST_USER_NAME
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from recensio.contenttypes.setuphandlers import add_number_of_each_review_type
from recensio.contenttypes.content.reviewjournal import ReviewJournal
from recensio.contenttypes.content.reviewmonograph import ReviewMonograph
from recensio.policy.tests.layer import RECENSIO_BARE_INTEGRATION_TESTING


class TestDOI(unittest.TestCase):
    """Tests the handling of DOIs for the dara/LZA export."""
    layer = RECENSIO_BARE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        login(self.layer['app'], SITE_OWNER_NAME)
        add_number_of_each_review_type(
            self.portal, 1, rez_classes=[ReviewMonograph, ReviewJournal])

        self.newspapera = self.portal['sample-reviews']['newspapera']
        issue_2_a = self.newspapera['summer']['issue-2']
        self.review_a0 = issue_2_a.objectValues()[0]
        self.review_a1 = issue_2_a.objectValues()[1]

        login(self.portal, TEST_USER_NAME)

    def test_doi_export_active_by_default(self):
        self.assertTrue(self.newspapera.isDoiRegistrationActive())

    def test_set_doi_field(self):
        self.review_a0.setDoi('custom/doi.12345')
        self.assertEqual(self.review_a0.getDoi(), 'custom/doi.12345')

    def test_autogenerate_doi_field(self):
        intids = getUtility(IIntIds)
        self.assertEqual(
            self.review_a0.getDoi(),
            '10.15463/rec.{0}'.format(intids.getId(self.review_a0)))
