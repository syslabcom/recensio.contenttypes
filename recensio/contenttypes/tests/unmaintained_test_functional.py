# -*- coding: utf-8 -*-
"""
Various functional tests
"""
from plone.app.blob.utils import openBlob
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.Archetypes.event import ObjectEditedEvent
from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
from recensio.policy.tests.layer import RECENSIO_FUNCTIONAL_TESTING
from Testing import makerequest

import datetime
import os
import transaction
import unittest2 as unittest
import zope.event


def raising(self, info):
    import traceback

    traceback.print_tb(info[2])
    print info[1]


SiteErrorLog.raising = raising


class TestCoverPicture(unittest.TestCase):
    """Test adding, replacing and deleting a cover picture"""

    layer = RECENSIO_FUNCTIONAL_TESTING

    def get_manager_browser(self, portal):
        setRoles(portal, TEST_USER_ID, ["Manager"])
        self.browser = Browser(portal)
        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()
        self.portal_url = portal.absolute_url()
        self.browser.open(self.portal_url + "/login_form")
        self.browser.getControl(name="__ac_name").value = TEST_USER_NAME
        self.browser.getControl(name="__ac_password").value = TEST_USER_PASSWORD
        self.browser.getControl(name="submit").click()

    def add_cover_picture(self):
        self.browser.open(self.presentation_url + "/edit")
        img = os.path.dirname(__file__) + "/test.jpg"
        img_data = open(img, "r").read()
        self.browser.getControl(name="coverPicture_file").add_file(
            img_data, filename="cover", content_type="image/jpeg"
        )
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()

    def remove_cover_picture(self):
        self.browser.open(self.presentation_url + "/edit")
        self.browser.getControl(name="coverPicture_delete").value = ["delete"]
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()

    def setUp(self):
        self.portal = self.layer["portal"]
        self.get_manager_browser(self.portal)

        pm = self.portal.portal_membership
        self.home_folder = pm.getHomeFolder(TEST_USER_ID)

        self.browser.open(
            self.home_folder.absolute_url() + "/folder_factories?set_language=en"
        )
        self.browser.getControl("Presentation (monograph)").selected = True
        self.browser.getControl("Add").click()

        self.browser.getControl(name="title").value = "Test Cover Pic"
        self.browser.getControl(
            name="reviewAuthors.firstname:records", index=0
        ).value = "First"
        self.browser.getControl(
            name="reviewAuthors.lastname:records", index=0
        ).value = "Last"
        self.browser.getControl(name="reviewAuthorEmail").value = "e@mail.com"
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()

        self.presentation_id = "test-cover-pic"
        self.presentation_url = self.browser.url
        self.presentation_obj = self.home_folder[self.presentation_id]
        self.presentation_path = "/".join(self.presentation_obj.getPhysicalPath())
        self.view = self.portal.unrestrictedTraverse(
            self.presentation_path + "/@@review_view"
        )

    def tearDown(self):
        # The workflow doesn't permit Presentations to be deleted so
        # we need to do it directly
        self.home_folder[self.presentation_id].wl_clearLocks()
        self.home_folder.manage_delObjects(self.presentation_id)
        transaction.commit()

    def unmaintained_test_has_no_cover_picture(self):
        self.assertFalse(
            self.view.has_coverpicture(),
            msg=(
                "The presentation has a cover picture, "
                "although one has not been added"
            ),
        )

    def unmaintained_test_add_cover_picture(self):
        self.add_cover_picture()
        self.assertTrue(
            self.view.has_coverpicture,
            msg=(
                "The presentation does not have a cover picture, "
                "although one has been added"
            ),
        )
        self.browser.open(self.presentation_url + "/edit")
        self.assertTrue(
            "Current image" in self.browser.contents,
            msg=(
                "The presentation does not have a cover picture, "
                "although one has been added"
            ),
        )

    def unmaintained_test_remove_cover_picture(self):
        self.add_cover_picture()
        self.remove_cover_picture()
        self.assertFalse(
            self.view.has_coverpicture(),
            msg=("The presentation cover picture has not been " "deleted successfully"),
        )

    def unmaintained_test_cover_picture_validator(self):
        self.browser.open(self.presentation_url + "/edit")
        self.browser.getControl(name="coverPicture_file").add_file(
            "a string where file data should be",
            filename="cover",
            content_type="image/jpeg",
        )
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()
        self.assertTrue(
            "cannot identify image file" in self.browser.contents,
            msg=("A string was accepted instead of image data"),
        )


class TestBrowserViews(unittest.TestCase):
    """Test various browser views"""

    layer = RECENSIO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.portal)

        self.get_url_of_type = (
            lambda meta_type: "http://nohost"
            + self.portal.portal_catalog({"meta_type": meta_type})[0]["path_string"]
        )

    def unmaintained_test_presentationarticlereview_view(self):
        self.browser.open(self.get_url_of_type("PresentationArticleReview"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_presentationcollection_view(self):
        self.browser.open(self.get_url_of_type("PresentationCollection"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_presentationmonograph_view(self):
        self.browser.open(self.get_url_of_type("PresentationMonograph"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_presentationonlineresource_view(self):
        self.browser.open(self.get_url_of_type("PresentationOnlineResource"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_reviewjournal_view(self):
        self.browser.open(self.get_url_of_type("ReviewJournal"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_reviewmonograph_view(self):
        self.browser.open(self.get_url_of_type("ReviewMonograph"))
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_decorated_folder_listing(self):
        issue_url = self.portal_url + (
            "/rezensionen/zeitschriften/sehepunkte/vol1/issue1/"
            "decorated_folder_listing"
        )
        self.browser.open(issue_url)
        self.assertEquals("200 Ok", self.browser.headers["status"])

    def unmaintained_test_browse_topics(self):
        self.browser.open(self.portal_url + "/browse-topics")
        self.assertTrue("Rezension" in self.browser.contents)
