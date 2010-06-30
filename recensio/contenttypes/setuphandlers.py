# -*- coding: utf-8 -*-
import os

from OFS.Image import File
from zope.app.component.hooks import getSite
import zope.event
from Testing import makerequest

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName

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
from swiss.tabular import XlsReader

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'exampledata',
    'metadata.xml')

def guard(func):
    def wrapper(self):
        if self.readDataFile('recensio.contenttypes_marker.txt') is None:
            return
        return func(self)
    return wrapper

portal_type_mappings =  {
    'rm' : {
        'portal_type' : ReviewMonograph
       ,'ISBN/ISSN' : 'isbn'
       ,'Jahr' : 'yearOfPublication'
       ,'Rez.-Name' : 'reviewAuthor'
       ,'Autor-Name Werk' : 'Authors'
       ,'Titel Werk' : 'title'
       ,'PDF-Seitenzahl Beginn' : 'pages'
       ,'PDF-Seitenzahl Ende' : 'pages'
       ,'Type (rm, rz, pm, pasb, paz)' : 'ignore'
       ,'freies Feld für Zitierschema' : 'unknown'}
    ,'rz' : {
        'portal_type' : ReviewJournal
       ,'ISBN/ISSN' : 'isbn'
       ,'Jahr' : 'yearOfPublication'
       ,'Rez.-Name' : 'reviewAuthor'
       ,'Autor-Name Werk' : 'Authors'
       ,'Titel Werk' : 'title'
       ,'PDF-Seitenzahl Beginn' : 'pages'
       ,'PDF-Seitenzahl Ende' : 'pages'
       ,'Type (rm, rz, pm, pasb, paz)' : 'ignore'
       ,'freies Feld für Zitierschema' : 'unknown'}
    ,'pm' : {
        'portal_type' : PresentationMonograph
       ,'ISBN/ISSN' : 'isbn'
       ,'Jahr' : 'yearOfPublication'
       ,'Rez.-Name' : 'reviewAuthor'
       ,'Autor-Name Werk' : 'Authors'
       ,'Titel Werk' : 'title'
       ,'PDF-Seitenzahl Beginn' : 'pages'
       ,'PDF-Seitenzahl Ende' : 'pages'
       ,'Type (rm, rz, pm, pasb, paz)' : 'ignore'
       ,'freies Feld für Zitierschema' : 'unknown'}
    ,'pasb' : {
        'portal_type' : PresentationCollection
       ,'ISBN/ISSN' : 'isbn'
       ,'Jahr' : 'yearOfPublication'
       ,'Rez.-Name' : 'reviewAuthor'
       ,'Autor-Name Werk' : 'Authors'
       ,'Titel Werk' : 'title'
       ,'PDF-Seitenzahl Beginn' : 'pages'
       ,'PDF-Seitenzahl Ende' : 'pages'
       ,'Type (rm, rz, pm, pasb, paz)' : 'ignore'
       ,'freies Feld für Zitierschema' : 'unknown'}
    ,'paz' : {
        'portal_type' : PresentationArticleReview
       ,'ISBN/ISSN' : 'isbn'
       ,'Jahr' : 'yearOfPublication'
       ,'Rez.-Name' : 'reviewAuthor'
       ,'Autor-Name Werk' : 'Authors'
       ,'Titel Werk' : 'title'
       ,'PDF-Seitenzahl Beginn' : 'pages'
       ,'PDF-Seitenzahl Ende' : 'pages'
       ,'Type (rm, rz, pm, pasb, paz)' : 'ignore'
       ,'freies Feld für Zitierschema' : 'unknown'}
    }
ignored_fields = [u'freies Feld für Zitierschema', 'Type (rm, rz, pm, pasb, paz)']

@guard
def addExampleContent2(context):
    portal = context.getSite()
    portal_id = 'recensio'

    if 'reviews' not in portal.objectIds():
        portal.invokeFactory('Folder', id='reviews', title='Reviews')
    reviews = portal.get('reviews')

    xls_data = XlsReader(context.openDataFile('initial.xls')).read().data
    keys = xls_data[0]
    for row in xls_data[1:]:
        mapping = portal_type_mappings[row[keys.index('Type (rm, rz, pm, pasb, paz)')]]
        data = {'portal_type' : mapping['portal_type']}
        for index, key in enumerate(keys):
            if key not in ignored_fields:
                data[mapping[key]] = row[index]
        portal_type = data.pop('portal_type')
        addOneItem(reviews, portal_type, data)

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
               'editor':u'Avalon',
               'editorCollectedEdition':u'',
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
               'publisher':u'',
               'urn': u'testing-data-urn'}

    for rez_class in [PresentationArticleReview,
                      PresentationOnlineResource,
                      ReviewJournal,
                      ReviewMonograph,
                      PresentationMonograph,
                      PresentationCollection]:
        # Fill in all fields with dummy content
        data = {}
        for field in rez_class.ordered_fields:
            data[field] = test_data[field]

        for i in range(10):
            data['title'] = 'Test %s No %d' % (rez_class.portal_type, i)
            addOneItem(reviews, rez_class, data)
 
def addOneItem(context, type, data):
    data["id"] = context.generateId(type.meta_type)
    review_id = context.invokeFactory(type.__doc__, **data)
    obj = context[review_id]
    request = makerequest.makerequest(obj)
    event=ObjectInitializedEvent(obj, request)
    zope.event.notify(event)
    print "Added %s" %context[review_id].absolute_url()
