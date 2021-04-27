# -*- coding: utf-8 -*-
"""
Tests for the Publication content type and items it can contain
"""
from contextlib import contextmanager
from plone import api
from plone.app.testing.helpers import login
from plone.app.testing.helpers import logout
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import TEST_USER_NAME
from recensio.contenttypes.interfaces.review import IParentGetter
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING

import unittest2 as unittest


@contextmanager
def change_language(request, language):
    language_tool = api.portal.get_tool("portal_languages")
    language_tool.use_request_negotiation = True
    language_tool.use_cookie_negotiation = True
    request.other["set_language"] = language
    language_tool.setLanguageBindings()
    yield request
    del request.other["set_language"]
    language_tool.setLanguageBindings()


class TestPublication(unittest.TestCase):
    """ """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review = self.portal.portal_catalog.search(
            {
                "portal_type": "Review Monograph",
                "path": {"query": "/".join(self.publication.getPhysicalPath())},
            }
        )[0].getObject()
        login(self.layer["app"], SITE_OWNER_NAME)
        self.custom_licence_doc_de = api.content.create(
            container=self.publication,
            id="fake_license_de",
            title="Fake Lizenz",
            type="Document",
        )
        self.custom_licence_doc_de.setLanguage("de")
        self.custom_licence_doc_de.setText(u"Dies ist eine übersetzte Lizenz")
        self.custom_licence_doc_en = api.content.create(
            container=self.publication,
            id="fake_license_en",
            title="Fake License",
            type="Document",
        )
        self.custom_licence_doc_en.setLanguage("en")
        self.custom_licence_doc_en.setText(u"This is a translated license")
        self.custom_licence_doc_de.addTranslationReference(self.custom_licence_doc_en)
        logout()

    def test_publication_schema_extension(self):
        """Ensure the Publication schema has been successfully
        extended"""
        self.assertEqual(True, hasattr(self.publication, "pdf_watermark"))
        self.assertEqual(True, hasattr(self.publication, "licence"))

    def test_review_licence(self):
        """Ensure that when a custom licence is set on the
        Publication this is visibile on its child review"""
        language_tool = api.portal.get_tool("portal_languages")
        language_tool.use_cookie_negotiation = True
        default_review_licence = u"license-note-review"
        with change_language(self.request, "de"):
            self.assertEqual(default_review_licence, self.review.getLicense())
        with change_language(self.request, "en"):
            self.assertEqual(default_review_licence, self.review.getLicense())

        custom_licence = u"Custom Licence"
        self.publication.licence = custom_licence
        with change_language(self.request, "de"):
            self.assertEqual(custom_licence, self.review.getLicense())
        with change_language(self.request, "en"):
            self.assertEqual(custom_licence, self.review.getLicense())

        self.publication.setLicence_ref(api.content.get_uuid(self.custom_licence_doc_de))
        with change_language(self.request, "de"):
            self.assertEqual(
                u"<p>Dies ist eine übersetzte Lizenz</p>".encode("utf-8"),
                self.review.getLicense(),
            )
        with change_language(self.request, "en"):
            self.assertEqual(
                u"<p>This is a translated license</p>".encode("utf-8"),
                self.review.getLicense(),
            )

        issue = self.review.aq_parent
        volume = issue.aq_parent

        volume_licence = u"Custom Volume Licence"
        volume.licence = volume_licence
        self.assertEqual(volume_licence, self.review.getLicense())

        volume.setLicence_ref(api.content.get_uuid(self.custom_licence_doc_de))
        with change_language(self.request, "de"):
            self.assertEqual(
                u"<p>Dies ist eine übersetzte Lizenz</p>".encode("utf-8"),
                self.review.getLicense(),
            )
        with change_language(self.request, "en"):
            self.assertEqual(
                u"<p>This is a translated license</p>".encode("utf-8"),
                self.review.getLicense(),
            )

        issue_licence = u"Custom Issue Licence"
        issue.licence = issue_licence
        self.assertEqual(issue_licence, self.review.getLicense())

        issue.setLicence_ref(api.content.get_uuid(self.custom_licence_doc_de))
        with change_language(self.request, "de"):
            self.assertEqual(
                u"<p>Dies ist eine übersetzte Lizenz</p>".encode("utf-8"),
                self.review.getLicense(),
            )
        with change_language(self.request, "en"):
            self.assertEqual(
                u"<p>This is a translated license</p>".encode("utf-8"),
                self.review.getLicense(),
            )

        review_licence = u"Custom Review Licence"
        self.review.licence = review_licence
        self.assertEqual(review_licence, self.review.getLicense())


class TestParentGetter(unittest.TestCase):
    """ """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        self.review = self.publication["summer"]["issue-2"].objectValues()[0]

    def test_get_parent_of_review_monograph(self):
        result = IParentGetter(self.review).get_parent_object_of_type("Publication")
        self.assertEqual(result, self.publication)

    def test_get_parent_of_publication(self):
        result = IParentGetter(self.publication).get_parent_object_of_type("Publication")
        self.assertEqual(result, self.publication)
