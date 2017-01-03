# -*- coding: utf-8 -*-
"""
Tests for the Publication content type and items it can contain
"""
import unittest2 as unittest

from plone.app.testing.helpers import login
from plone.app.testing.interfaces import SITE_OWNER_NAME
from recensio.contenttypes.setuphandlers import add_number_of_each_review_type
from recensio.contenttypes.content.reviewjournal import ReviewJournal
from recensio.contenttypes.content.reviewmonograph import ReviewMonograph
from recensio.contenttypes.interfaces import IParentGetter
from recensio.policy.tests.layer import RECENSIO_BARE_INTEGRATION_TESTING

class TestCitationString(unittest.TestCase):
    """
    """
    layer = RECENSIO_BARE_INTEGRATION_TESTING

    def setUp(self):
        self.portal      = self.layer["portal"]
        login(self.layer['app'], SITE_OWNER_NAME)
        add_number_of_each_review_type(
            self.portal, 1, rez_classes=[ReviewMonograph, ReviewJournal])

        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review_mono = self.portal.portal_catalog.search(
            {"portal_type" :"Review Monograph",
             "path"        :{
                    "query": "/".join(self.publication.getPhysicalPath())
                    }
             }
            )[0].getObject()
        pg = IParentGetter(self.review_mono)
        self.issue_mono = pg.get_parent_object_of_type('Issue')
        self.review_jour = self.portal.portal_catalog.search(
            {"portal_type" :"Review Journal",
             "path"        :{
                    "query": "/".join(self.publication.getPhysicalPath())
                    }
             }
            )[0].getObject()
        pg = IParentGetter(self.review_jour)
        self.issue_jour = pg.get_parent_object_of_type('Issue')

    def test_review_citation_wrt_canonical_uri(self):
        """ Reviews which have a canonical_uri should not link to the
        recensio url in the citation #3102 """

        self.review_mono.doi = None
        self.issue_mono.setDoiRegistrationActive(False)
        self.review_jour.doi = None
        self.issue_jour.setDoiRegistrationActive(False)

        monograph_citation = self.review_mono.get_citation_string()
        self.assertEquals('<a href="http://nohost/plone' in monograph_citation,
                          True)

        journal_citation = self.review_jour.get_citation_string()
        self.assertEquals('<a href="http://nohost/plone' in journal_citation,
                          True)

        self.review_mono.canonical_uri = "http://example.com"
        monograph_citation = self.review_mono.get_citation_string()
        self.assertEquals('<a href="http://nohost/plone' in monograph_citation,
                          False)

        self.review_jour.canonical_uri = "http://example.com"
        journal_citation = self.review_jour.get_citation_string()
        self.assertEquals('<a href="http://nohost/plone' in journal_citation,
                          False)

    def unmaintained_test_first_publication_data(self):
        self.assertEquals(
            self.review_jour.getFirstPublicationData(),
            [u'Zeitschrift 1, Summer, Issue 2'])

        self.review_jour.canonical_uri = "W"*30
        self.assertEquals(
            self.review_jour.getFirstPublicationData(),
            [('<a href="WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW">'
              'WWWWWWWWWWWWWWWWWWWWWWWWWWW...</a>')],
             msg = u"Long canonical_uri has not been shortened")

    def test_page_start_end_in_print(self):
        self.review_mono.pageStartOfReviewInJournal = "10"
        self.review_mono.pageEndOfReviewInJournal = "20"
        self.assertEquals(
            self.review_mono.page_start_end_in_print, "10-20")
        self.review_mono.pageStartOfReviewInJournal = ""
        self.review_mono.pageEndOfReviewInJournal = "20"
        self.assertEquals(
            self.review_mono.page_start_end_in_print, "20")
        self.review_mono.pageStartOfReviewInJournal = ""
        self.review_mono.pageEndOfReviewInJournal = ""
        self.assertEquals(
            self.review_mono.page_start_end_in_print, "")

    def test_doi_link(self):
        # No custom DOI and no canonical_uri: Show UUID URL
        self.review_mono.doi = None
        self.issue_mono.setDoiRegistrationActive(False)
        self.assertNotIn('<a rel="doi"',
                         self.review_mono.get_citation_string())
        self.assertIn('<a href="http://nohost/plone/r/',
                      self.review_mono.get_citation_string())
        # Custom DOI and no canonical_uri: Show doi.org URL
        self.review_mono.doi = '10.15463/rec.724704480'
        self.assertIn('<a rel="doi" '
                      'href="http://dx.doi.org/10.15463/rec.724704480">'
                      '10.15463/rec.724704480</a>',
                      self.review_mono.get_citation_string())
        self.assertNotIn('<a href="http://nohost/plone/r/',
                         self.review_mono.get_citation_string())

        # No custom DOI and no canonical_uri: Show UUID URL
        self.review_jour.doi = None
        self.issue_jour.setDoiRegistrationActive(False)
        self.assertNotIn('<a rel="doi"',
                         self.review_jour.get_citation_string())
        self.assertIn('<a href="http://nohost/plone',
                      self.review_jour.get_citation_string())
        # Custom DOI and no canonical_uri: Show doi.org URL
        self.review_jour.doi = '10.15463/rec.724704481'
        self.assertIn('<a rel="doi" '
                      'href="http://dx.doi.org/10.15463/rec.724704481">'
                      '10.15463/rec.724704481</a>',
                      self.review_jour.get_citation_string())
        self.assertNotIn('<a href="http://nohost/plone',
                         self.review_jour.get_citation_string())

    def test_doi_link_with_canonical_uri(self):
        # Custom DOI and canonical_uri: Show doi.org URL. canonical_uri is also
        # shown in the default view, but not as part of the citation string.
        self.review_mono.doi = '10.15463/rec.724704480'
        self.review_mono.canonical_uri = "http://example.com"
        self.assertIn('<a rel="doi" '
                      'href="http://dx.doi.org/10.15463/rec.724704480">'
                      '10.15463/rec.724704480</a>',
                      self.review_mono.get_citation_string())

        self.review_jour.doi = '10.15463/rec.724704481'
        self.review_jour.canonical_uri = "http://example.com"
        self.assertIn('<a rel="doi" '
                      'href="http://dx.doi.org/10.15463/rec.724704481">'
                      '10.15463/rec.724704481</a>',
                      self.review_jour.get_citation_string())
