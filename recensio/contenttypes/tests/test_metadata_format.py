#-*- coding: utf-8 -*-
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING
from recensio.theme.interfaces import IRecensioLayer
from zope.interface import directlyProvides

import unittest2 as unittest


class TestMetadataFormat(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        # register the browser layer
        self.request = self.layer["request"]
        directlyProvides(self.request, IRecensioLayer)

        self.issue = self.portal["sample-reviews"]["newspapera"]["summer"]["issue-2"]
        login(self.layer['app'], SITE_OWNER_NAME)

    def test_review_monograph_decorated_title(self):
        rm_id = self.issue.invokeFactory(
            'Review Monograph',
            id='rm1',
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        reviewmonograph = self.issue[rm_id]
        generated_title = reviewmonograph.getDecoratedTitle()
        correct_title = (
            u"Gioia Paradisi (Hg.): Béroul: Tristano e Isotta (rezensiert von Margherita Lecco)")
        self.assertEqual(correct_title, generated_title)

    def test_review_journal_decorated_title(self):
        rj_id = self.issue.invokeFactory(
            'Review Journal',
            id='rj1',
            title='Plone Mag',
            reviewAuthors=({'firstname': 'Cillian', 'lastname': 'de Róiste'},),
            yearOfPublication="2009",
            officialYearOfPublication="2010",
            volumeNumber="1",
            issueNumber="3",
        )
        reviewjournal = self.issue[rj_id]
        generated_title = reviewjournal.getDecoratedTitle()
        correct_title = u'Plone Mag, 1 (2010/2009), 3 (rezensiert von Cillian de Róiste)'
        self.assertEqual(correct_title, generated_title)
