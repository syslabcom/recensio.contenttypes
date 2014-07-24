# -*- coding: utf-8 -*-
"""
Tests for the Publication content type and items it can contain
"""
import unittest2 as unittest
from recensio.contenttypes.interfaces.review import IParentGetter
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestPublication(unittest.TestCase):
    """
    """
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal      = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review      = self.portal.portal_catalog.search(
            {"portal_type" :"Review Monograph",
             "path"        :{
                    "query": "/".join(self.publication.getPhysicalPath())
                    }
             }
            )[0].getObject()

    def test_publication_schema_extension(self):
        """ Ensure the Publication schema has been successfully
        extended """
        self.assertEqual(True,
                         hasattr(self.publication, "pdf_watermark"))
        self.assertEqual(True,
                         hasattr(self.publication, "licence"))

    def test_review_licence(self):
        """ Ensure that when a custom licence is set on the
        Publication this is visibile on it's child review"""
        default_review_licence = u'license-note-review'
        self.assertEqual(default_review_licence,
                         self.review.getLicense())
        custom_licence = u"Custom Licence"
        self.publication.licence = custom_licence
        self.assertEqual(custom_licence,
                         self.review.getLicense())


class TestParentGetter(unittest.TestCase):
    """ """
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review = self.publication['summer']['issue-2'].objectValues()[0]

    def test_get_parent_of_review_monograph(self):
        result = IParentGetter(self.review).get_parent_object_of_type(
            'Publication')
        self.assertEqual(result, self.publication)

    def test_get_parent_of_publication(self):
        result = IParentGetter(self.publication).get_parent_object_of_type(
            'Publication')
        self.assertEqual(result, self.publication)
