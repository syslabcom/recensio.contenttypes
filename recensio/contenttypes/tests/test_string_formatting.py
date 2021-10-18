# -*- coding: utf-8 -*-
"""
Test the various methods we have for formatting particular
strings: authors, editors, with punctuation etc.
"""
from plone import api
from plone.app.blob.utils import openBlob
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.Archetypes.event import ObjectEditedEvent
from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from Testing import makerequest

import datetime
import os
import transaction
import unittest2 as unittest
import zope.event


def raising(self, info):
    import traceback

    traceback.print_tb(info[2])
    print(info[1])


SiteErrorLog.raising = raising


class TestStringFormatting(unittest.TestCase):
    """Test various string formatting functions"""

    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.get_obj_of_type = lambda meta_type: self.portal.portal_catalog(
            {"meta_type": meta_type}
        )[0].getObject()
        self.kotlowski = self.gnd_view.createPerson(**{
            "firstname": "Tadeusz", "lastname": "Kot\xc5\x82owski"
        })
        self.huxley = self.gnd_view.createPerson(**{
            "firstname": "Aldous", "lastname": "Huxley"
        })
        self.editor1 = self.gnd_view.createPerson(**{
            "firstname": "Ed1First", "lastname": "Ed1Last"
        })
        self.editor2 = self.gnd_view.createPerson(**{
            "firstname": "Ed2First", "lastname": "Ed2Last"
        })

    @property
    def gnd_view(self):
        gnd_view = api.content.get_view(
            context=self.portal,
            request=self.layer["request"],
            name="gnd-view",
        )
        return gnd_view

    def test_single_author_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([self.kotlowski])
        self.assertEquals(pm.formatted_authors_editorial(), u"Tadeusz Kot\u0142owski")

    def test_multiple_authors_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([self.kotlowski, self.huxley])
        self.assertEquals(
            pm.formatted_authors_editorial(), u"Aldous Huxley / Tadeusz Kot\u0142owski"
        )

    def test_single_author_single_editor_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([self.huxley])
        pm.setEditorial([self.kotlowski])
        authors_editorial = u"Tadeusz Kot\u0142owski (Hg.): Aldous Huxley"
        self.assertEquals(pm.formatted_authors_editorial(), authors_editorial)

    def test_multiple_authors_multiple_editors_formatting(self):
        pm = self.get_obj_of_type("PresentationMonograph")
        pm.setAuthors([self.kotlowski, self.huxley])
        pm.setEditorial([self.editor1, self.editor2])

        self.assertEquals(
            pm.formatted_authors_editorial(),
            (
                u"Ed1First Ed1Last / Ed2First Ed2Last (Hg.): "
                u"Aldous Huxley "
                u"/ Tadeusz Kot\u0142owski"
            ),
        )
