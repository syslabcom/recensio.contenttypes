# -*- coding: utf-8 -*-
"""
Test the various methods we have for formatting particular
strings: authors, editors, with punctuation etc.
"""
import datetime
import os

import transaction
import unittest2 as unittest
import zope.event
from plone.app.blob.utils import openBlob
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from Products.Archetypes.event import ObjectEditedEvent
from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from Testing import makerequest


def raising(self, info):
    import traceback

    traceback.print_tb(info[2])
    print info[1]



SiteErrorLog.raising = raising


class TestStringFormatting(unittest.TestCase):
    """ Test various string formatting functions
    """

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.get_obj_of_type = lambda meta_type: self.portal.portal_catalog(
            {"meta_type": meta_type}
        )[0].getObject()

    def test_single_author_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([{"firstname": "Tadeusz", "lastname": "Kot\xc5\x82owski"}])
        self.assertEquals(pm.formatted_authors_editorial, u"Tadeusz Kot\u0142owski")

    def test_multiple_authors_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors(
            [
                {"firstname": "Tadeusz", "lastname": "Kot\xc5\x82owski"},
                {"firstname": "Aldous", "lastname": "Huxley"},
            ]
        )
        self.assertEquals(
            pm.formatted_authors_editorial, u"Tadeusz Kot\u0142owski / Aldous Huxley"
        )

    def test_single_author_single_editor_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([{"firstname": "Aldous", "lastname": "Huxley"}])
        pm.setEditorial([{"firstname": "Tadeusz", "lastname": "Kot\xc5\x82owski"}])
        authors_editorial = u"Tadeusz Kot\u0142owski (Hg.): Aldous Huxley"
        self.assertEquals(pm.formatted_authors_editorial, authors_editorial)

    def test_multiple_authors_multiple_editors_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors(
            [
                {"firstname": "Tadeusz", "lastname": "Kot\xc5\x82owski"},
                {"firstname": "Aldous", "lastname": "Huxley"},
            ]
        )
        pm.setEditorial(
            [
                {"firstname": "Ed1First", "lastname": "Ed1Last"},
                {"firstname": "Ed2First", "lastname": "Ed2Last"},
            ]
        )

        self.assertEquals(
            pm.formatted_authors_editorial,
            (
                u"Ed1First Ed1Last / Ed2First Ed2Last (Hg.): "
                u"Tadeusz Kot\u0142owski "
                u"/ Aldous Huxley"
            ),
        )
