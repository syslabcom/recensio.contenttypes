# -*- coding: utf-8 -*-
"""
Various functional tests
"""
import datetime
import os
import unittest2 as unittest

import zope.event
import transaction

from plone.testing.z2 import Browser
from Testing import makerequest
from plone.app.blob.utils import openBlob
from Products.Archetypes.event import ObjectEditedEvent

from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles

from recensio.contenttypes.tests.base import RECENSIO_FUNCTIONAL_TESTING

class TestCoverPicture(unittest.TestCase):
    """ Test adding, replacing and deleting a cover picture
    """
    layer = RECENSIO_FUNCTIONAL_TESTING

    def get_manager_browser(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(portal)
        portalURL = portal.absolute_url()
        self.browser.open(portalURL + '/login_form')
        self.browser.getControl(name='__ac_name').value = TEST_USER_NAME
        self.browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        self.browser.getControl(name='submit').click()

    def add_cover_picture(self):
        self.browser.open(self.presentation_url+"/edit")
        img = os.path.dirname(__file__)+"/test.jpg"
        img_data = open(img, "r").read()
        self.browser.getControl(
            name="coverPicture_file"
            ).add_file(img_data,
                       filename="cover",
                       content_type="image/jpeg")
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()

    def remove_cover_picture(self):
        self.browser.open(self.presentation_url+"/edit")
        self.browser.getControl(name="coverPicture_delete").value = ["delete"]
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()


    def setUp(self):
        self.portal = self.layer["portal"]
        self.get_manager_browser(self.portal)

        pm = self.portal.portal_membership
        self.home_folder = pm.getHomeFolder(TEST_USER_ID)

        self.browser.open(self.home_folder.absolute_url()+\
                     "/folder_factories?set_language=en")
        self.browser.getControl("Presentation Monograph").selected = True
        self.browser.getControl("Add").click()

        self.browser.getControl(name="title").value = "Test Cover Pic"
        self.browser.getControl(name="reviewAuthorLastname").value = "Last"
        self.browser.getControl(name="reviewAuthorFirstname").value = "First"
        self.browser.getControl(name="reviewAuthorEmail").value = "e@mail.com"
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()

        self.presentation_id = "test-cover-pic"
        self.presentation_url = self.browser.url
        self.presentation_obj = self.home_folder[self.presentation_id]
        self.presentation_path = "/".join(
            self.presentation_obj.getPhysicalPath()
            )
        self.view = self.portal.unrestrictedTraverse(
            self.presentation_path+"/@@review_view")

    def tearDown(self):
        # The workflow doesn't permit Presentations to be deleted so
        # we need to do it directly
        self.home_folder[self.presentation_id].wl_clearLocks()
        self.home_folder.manage_delObjects(self.presentation_id)
        transaction.commit()

    def test_has_no_cover_picture(self):
        self.assertFalse(self.view.has_coverpicture(),
                         msg=("The presentation has a cover picture, "
                              "although one has not been added")
                         )

    def test_add_cover_picture(self):
        self.add_cover_picture()
        self.assertTrue(self.view.has_coverpicture,
                        msg=("The presentation does not have a cover picture, "
                              "although one has been added")
                        )
        self.browser.open(self.presentation_url+"/edit")
        self.assertTrue("Current image" in self.browser.contents,
                        msg=("The presentation does not have a cover picture, "
                              "although one has been added")
                        )

    def test_remove_cover_picture(self):
        self.add_cover_picture()
        self.remove_cover_picture()
        self.assertFalse(self.view.has_coverpicture(),
                         msg=("The presentation cover picture has not been "
                              "deleted successfully")
                         )

    def test_cover_picture_validator(self):
        self.browser.open(self.presentation_url+"/edit")
        self.browser.getControl(
            name="coverPicture_file"
            ).add_file("a string where file data should be",
                       filename="cover",
                       content_type="image/jpeg")
        self.browser.getControl("Licence Agreement").selected = True
        self.browser.getControl("Save").click()
        self.assertTrue("cannot identify image file" in self.browser.contents,
                        msg=("A string was accepted instead of image data")
                        )
