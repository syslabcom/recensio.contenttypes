# -*- coding: utf-8 -*-
"""
Tests for the Publication content type and items it can contain
"""
import unittest2 as unittest

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING

class TestCitationString(unittest.TestCase):
    """
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal      = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review_mono = self.portal.portal_catalog.search(
            {"portal_type" :"Review Monograph",
             "path"        :{
                    "query": "/".join(self.publication.getPhysicalPath())
                    }
             }
            )[0].getObject()
        self.review_jour = self.portal.portal_catalog.search(
            {"portal_type" :"Review Journal",
             "path"        :{
                    "query": "/".join(self.publication.getPhysicalPath())
                    }
             }
            )[0].getObject()

    def test_review_citation_wrt_canonical_uri(self):
        """ Reviews which have a canonical_uri should not link to the
        recensio url in the citation #3102 """

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
