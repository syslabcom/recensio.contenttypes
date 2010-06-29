# -*- coding: utf-8 -*-
import os

from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import getSecurityManager

from OFS.Image import File
from zope.app.component.hooks import getSite

from recensio.contenttypes.content.reviewmonograph import \
     ReviewMonograph

from recensio.contenttypes.content.presentationarticlereview \
     import PresentationArticleReview
from recensio.contenttypes.content.reviewjournal import \
     ReviewJournal
from recensio.contenttypes.content.presentationonlineresource import \
     PresentationOnlineResource
from recensio.contenttypes.content.presentationmonograph import \
     PresentationMonograph
from recensio.contenttypes.content.presentationcollection import \
     PresentationCollection

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

    pdf_file = open(os.path.join(
        os.path.dirname(__file__), "tests", "test_content","Testdatei.pdf"),
                    "r")

    pdf_obj = File(id="test-pdf", title="Test Pdf", file=pdf_file,
        content_type='application/pdf')

    test_data={'authors': u'Tadeusz Kotłowski',
               'referenceAuthors': u'Tadeusz Kotłowski',
               'ddcPlace': u'Deutschland / Mitteleuropa allgemein, Polen',
               'ddcSubject': u'Militär- und Kriegsgeschichte',
               'ddcTime': u'1939-1941',
               'description': u'',
               'doc': None,
               'documentarten_bibliographische': u'',
               'documentarten_individual':u'',
               'documentarten_institution':u'',
               'documentarten_kooperation':u'',
               'yearOfPublication':u'2008',
               'placeOfPublication':u'Krakow',
               'officialYearOfPublication':'2008',
               'number':u'2',
               'herausgeber':u'Avalon',
               'herausgeberSammelband':u'',
               'institution':u'',
               'isbn':u'978-83-60448-39-7',
               'issn':u'1822-4016',
               'shortnameJournal':u'',
               'volume':'2',
               'pdf': pdf_obj,
               'languagePresentation':'de',
               'languageReview':'pl',
               'recensioID':u'',
               'series':u'',
               'seriesVol':u'',
               'review':u'',
               'reviewAuthor':u'',
               'subject':u'',
               'pages':u'',
               'title':u'Niemcy',
               'searchresults':u'',
               'subtitle':u'Dzieje państwa i społeczeństwa 1890–1945',
               'url': 'http://www.syslab.com',
               'idBvb':u'',
               'publisher':u'',}

    for rez_class in [PresentationArticleReview,
                      ReviewJournal,
                      PresentationOnlineResource,
                      PresentationMonograph,
                      PresentationCollection]:
        # Fill in all fields with dummy content
        data = {}
        for field in rez_class.ordered_fields:
            data[field] = test_data[field]

        for i in range(10):
            data["id"] = reviews.generateId(rez_class.meta_type)
            data['title'] = 'Test %s No %d' %(rez_class.portal_type, i)
            review_id = reviews.invokeFactory(rez_class.__doc__, **data)
            print "Added %s" %reviews[review_id].absolute_url()
