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
        self.maxDiff = None

    def test_review_monograph_decorated_title(self):
        item_id = "rm1"
        self.issue.invokeFactory(
            'Review Monograph',
            id=item_id,
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        generated_title = self.issue[item_id].getDecoratedTitle()
        correct_title = (
            u"Gioia Paradisi (Hg.): Béroul: Tristano e Isotta (rezensiert von Margherita Lecco)")
        self.assertEqual(correct_title, generated_title)

    def test_reviewjournal_decorated_title(self):
        item_id = "rj1"
        self.issue.invokeFactory(
            'Review Journal',
            id=item_id,
            title='Plone Mag',
            reviewAuthors=({'firstname': 'Cillian', 'lastname': 'de Róiste'},),
            yearOfPublication="2009",
            officialYearOfPublication="2010",
            volumeNumber="1",
            issueNumber="3",
        )
        generated_title = self.issue[item_id].getDecoratedTitle()
        correct_title = u'Plone Mag, 1 (2010/2009), 3 (rezensiert von Cillian de Róiste)'
        self.assertEqual(correct_title, generated_title)

    def test_presentationarticlereview_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "par1"
        member_folder.invokeFactory(
            'Presentation Article Review',
            id=item_id,
            title=u'À la recherche d’une paix de compromis',
            subtitle=u'Kessler, Haguenin et la diplomatie secrète de l’hiver 1916-1917',
            authors=({'firstname': 'Landry', 'lastname': 'Charrier'},),
            reviewAuthors=({'firstname': 'Landry', 'lastname': 'Charrier'},),
            yearOfPublication="2010",
            volumeNumber="11",
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u'Landry Charrier: À la recherche d’une paix de '
            u'compromis. Kessler, Haguenin et la diplomatie secrète de '
            u'l’hiver 1916-1917 (präsentiert von Landry Charrier)'
        )
        self.assertEqual(correct_title, generated_title)

    def test_presentationcollection_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pc1"
        member_folder.invokeFactory(
            'Presentation Collection',
            id=item_id,
            title=u'Christmas Truce',
            subtitle=u'Die Amateurfotos vom Weihnachtsfrieden 1914 und ihre Karriere',
            authors=({'firstname': 'Christian', 'lastname': ' Bunnenberg'},),
            reviewAuthors=({'firstname': 'Christian', 'lastname': 'Bunnenberg'},),
            yearOfPublication="2009",
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u'Christian Bunnenberg: Christmas Truce. Die Amateurfotos vom '
            u'Weihnachtsfrieden 1914 und ihre Karriere (präsentiert von '
            u'Christian Bunnenberg)'
        )
        self.assertEqual(correct_title, generated_title)

    def test_presentationmonograph_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pm1"
        member_folder.invokeFactory(
            'Presentation Monograph',
            id=item_id,
            title=u'Gelebter Internationalismus',
            subtitle=u'Österreichs Linke und der algerische Widerstand (1958-1963)',
            authors=({'firstname': 'Fritz', 'lastname': ' Keller'},),
            reviewAuthors=({'firstname': 'Fritz', 'lastname': 'Keller'},),
            yearOfPublication="2009",
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u'Fritz Keller: Gelebter Internationalismus. Österreichs '
            u'Linke und der algerische Widerstand (1958-1963) (präsentiert von '
            u'Fritz Keller)'
        )
        self.assertEqual(correct_title, generated_title)

    def test_presentationonlineresource_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "por1"
        member_folder.invokeFactory(
            'Presentation Online Resource',
            id=item_id,
            title=(
                u'Revues.org, plateforme de revues et de collections de livres en sciences '
                u'humaines et sociales'
            ),
            reviewAuthors=({'firstname': 'Delphine', 'lastname': 'Cavallo'},),
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u'Revues.org, plateforme de revues et de collections de livres en sciences humaines '
            u'et sociales (präsentiert von Delphine Cavallo)'
        )
        self.assertEqual(correct_title, generated_title)

    def test_review_monograph_citation_string_title(self):
        item_id = "rm1"
        self.issue.invokeFactory(
            'Review Monograph',
            id=item_id,
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        item = self.issue[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Lecco, Margherita: Rezension über: Gioia Paradisi (Hg.): Béroul, Tristano e Isotta, '
            u'2013, in: Zeitschrift 1, Summer, Issue 2, <a href="http://nohost/plone/r/%s">'
            u'http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_reviewjournal_citation_string(self):
        item_id = "rj1"
        self.issue.invokeFactory(
            'Review Journal',
            id=item_id,
            title='Plone Mag',
            reviewAuthors=({'firstname': 'Cillian', 'lastname': 'de Róiste'},),
            yearOfPublication="2009",
            officialYearOfPublication="2010",
            volumeNumber="1",
            issueNumber="3",
        )
        item = self.issue[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'de Róiste, Cillian: Rezension über: Plone Mag, 1, 3 (2010/2009), in: Zeitschrift 1, '
            u'Summer, Issue 2, <a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' %
            (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationarticlereview_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "par1"
        member_folder.invokeFactory(
            'Presentation Article Review',
            id=item_id,
            title=u'À la recherche d’une paix de compromis',
            subtitle=u'Kessler, Haguenin et la diplomatie secrète de l’hiver 1916-1917',
            authors=({'firstname': 'Landry', 'lastname': 'Charrier'},),
            reviewAuthors=({'firstname': 'Landry', 'lastname': 'Charrier'},),
            yearOfPublication="2010",
            volumeNumber="11",
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Charrier, Landry: Präsentation von: Charrier, Landry, À la recherche d’une paix de '
            u'compromis. Kessler, Haguenin et la diplomatie secrète de l’hiver 1916-1917, in: 11 '
            u'<a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationcollection_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pc1"
        member_folder.invokeFactory(
            'Presentation Collection',
            id=item_id,
            title=u'Christmas Truce',
            subtitle=u'Die Amateurfotos vom Weihnachtsfrieden 1914 und ihre Karriere',
            authors=({'firstname': 'Christian', 'lastname': ' Bunnenberg'},),
            reviewAuthors=({'firstname': 'Christian', 'lastname': 'Bunnenberg'},),
            yearOfPublication="2009",
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Bunnenberg, Christian: Präsentation von: Bunnenberg, Christian, Christmas Truce. Die '
            u'Amateurfotos vom Weihnachtsfrieden 1914 und ihre Karriere, in: 2009 '
            u'<a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationmonograph_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pm1"
        member_folder.invokeFactory(
            'Presentation Monograph',
            id=item_id,
            title=u'Gelebter Internationalismus',
            subtitle=u'Österreichs Linke und der algerische Widerstand (1958-1963)',
            authors=({'firstname': 'Fritz', 'lastname': ' Keller'},),
            reviewAuthors=({'firstname': 'Fritz', 'lastname': 'Keller'},),
            yearOfPublication="2009",
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Keller, Fritz: Präsentation von: Fritz Keller, Gelebter Internationalismus. '
            u'Österreichs Linke und der algerische Widerstand (1958-1963), 2009, '
            u'<a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationonlineresource_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "por1"
        member_folder.invokeFactory(
            'Presentation Online Resource',
            id=item_id,
            title=(
                u'Revues.org, plateforme de revues et de collections de livres en sciences '
                u'humaines et sociales'
            ),
            reviewAuthors=({'firstname': 'Delphine', 'lastname': 'Cavallo'},),
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Cavallo, Delphine: Präsentation von: Revues.org, plateforme de revues et de '
            u'collections de livres en sciences humaines et sociales, '
            '<a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)
