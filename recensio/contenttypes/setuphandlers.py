# -*- coding: utf-8 -*-
import os

from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager

from zope.app.component.hooks import getSite

from recensio.contenttypes.content.rezensioneinermonographie import \
     RezensioneinerMonographie

from recensio.contenttypes.content.praesentationenvonaufsatzinzeitschrift \
     import PraesentationenvonAufsatzinZeitschrift
from recensio.contenttypes.content.rezensioneinerzeitschrift import \
     RezensioneinerZeitschrift
from recensio.contenttypes.content.praesentationenvoninternetressourcen import \
     PraesentationenvonInternetressourcen
from recensio.contenttypes.content.praesentationenvonmonographien import \
     PraesentationenvonMonographien
from recensio.contenttypes.content.praesentationvonaufsatzinsammelband import \
     PraesentationvonAufsatzinSammelband

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'exampledata',
    'metadata.xml')

def guard(func):
    def wrapper(self):
        if self.readDataFile('recensio.contenttypes_marker.txt') is None:
            return
        return func(self)
    return wrapper

@guard
def addExampleContent(context):
    portal = context.getSite()
    portal_id = "recensio"

    if "sample-reviews" not in portal.objectIds():
        portal.invokeFactory("Folder", id="sample-reviews", title="Sample Reviews")

    reviews = portal.get("sample-reviews")

    test_data={'authors': u'Tadeusz Kotłowski',
               'bezugsautoren': u'Tadeusz Kotłowski',
               'ddcRaum': u'Deutschland / Mitteleuropa allgemein, Polen',
               'ddcSach': u'Militär- und Kriegsgeschichte ',
               'ddcZeit': u'1939-1941 ',
               'description': u'',
               'doc': None,
               'documentarten_bibliographische': u'',
               'documentarten_individual':u'',
               'documentarten_institution':u'',
               'documentarten_kooperation':u'',
               'erscheinungsjahr':u'',
               'erscheinungsort':u'',
               'gezaehltesJahr':u'',
               'heftnummer':u'',
               'herausgeber':u'',
               'herausgeberSammelband':u'',
               'institution':u'',
               'isbn':u'',
               'issn':u'',
               'kuerzelZeitschrift':u'',
               'nummer':u'',
               'pdf': None,
               'praesentationTextsprache':u'',
               'praesentiertenSchriftTextsprache':u'',
               'recensioID':u'',
               'reihe':u'',
               'reihennummer':u'',
               'rezension':u'',
               'rezensionAutor':u'',
               'schlagwoerter':u'',
               'seitenzahl':u'',
               'title':u'',
               'trefferdaten':u'',
               'untertitel':u'',
               'url': 'http://www.syslab.com',
               'verbundID':u'',
               'verlag':u'',}

    for rez_class in [PraesentationenvonAufsatzinZeitschrift,
                      RezensioneinerZeitschrift,
                      PraesentationenvonInternetressourcen,
                      PraesentationenvonMonographien,
                      PraesentationvonAufsatzinSammelband]:
        # Fill in all fields with dummy content
        data = {}
        for field in rez_class.ordered_fields:
            data[field] = test_data[field]

        for i in range(10):
            data["id"] = reviews.generateId(rez_class.meta_type)
            data['title'] = 'Test %s No %d' %(rez_class.portal_type, i)
            review_id = reviews.invokeFactory(rez_class.__doc__, **data)
            print "Added %s" %reviews[review_id].absolute_url()
