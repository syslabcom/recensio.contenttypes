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
        browser = Browser(portal)
        portalURL = portal.absolute_url()
        browser.open(portalURL + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()
        return browser

    def test_add_cover_picture(self):
        portal = self.layer["portal"]
        browser = self.get_manager_browser(portal)

        pm = portal.portal_membership
        home_folder = pm.getHomeFolder(TEST_USER_ID)
        browser.open(home_folder.absolute_url()+\
                     "/folder_factories?set_language=en")
        browser.getControl("Presentation Monograph").selected = True
        browser.getControl("Add").click()

        browser.getControl(name="title").value = "Test Cover Pic"
        browser.getControl(name="reviewAuthorLastname").value = "Last"
        browser.getControl(name="reviewAuthorFirstname").value = "First"
        browser.getControl(name="reviewAuthorEmail").value = "e@mail.com"
        browser.getControl("Licence Agreement").selected = True
        browser.getControl("Save").click()

        presentation_url = browser.url
        edit_url = browser.url+"/edit"
        browser.open(edit_url)
        img = os.path.dirname(__file__)+"/test.jpg"
        img_data = open(img, "r").read()
        browser.getControl(
            name="coverPicture_file"
            ).add_file(img_data,
                       filename="cover",
                       content_type="image/jpeg")
        browser.getControl("Licence Agreement").selected = True
        browser.getControl("Save").click()
        browser.open(edit_url)
        self.assertTrue("Current image" in browser.contents)

        # Clean up:
        # The workflow doesn't permit Presentations to be deleted so
        # we need to do it directly
        parent_folder = portal.unrestrictedTraverse(
            "/plone/Members/test_user_1_")
        parent_folder["test-cover-pic"].wl_clearLocks()
        parent_folder.manage_delObjects("test-cover-pic")
        transaction.commit()
