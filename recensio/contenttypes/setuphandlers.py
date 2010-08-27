# -*- coding: utf-8 -*-
from cStringIO import StringIO
from csv import writer, reader
from ConfigParser import ConfigParser
from zope.component import adapts
from zope.interface import implements
import os

from OFS.Image import File
from zope.app.component.hooks import getSite
import zope.event
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest
from Testing import makerequest

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IFilesystemExporter, \
    IFilesystemImporter

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
from recensio.contenttypes.interfaces.publication import IPublication
from swiss.tabular import XlsReader
import random

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'exampledata',
    'metadata.xml')

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

def addOneItem(context, type, data):
    """Add an item and fire the ObjectInitializedEvent

    This triggers file conversions for the Reviews/Presentations
    """
    data["id"] = context.generateId(type.meta_type)
    review_id = context.invokeFactory(type.__doc__, **data)
    obj = context[review_id]
    request = makerequest.makerequest(obj)
    event=ObjectInitializedEvent(obj, request)
    zope.event.notify(event)
    return context[review_id]

def add_number_of_each_review_type(context, number_of_each):
    """Add a particular number of each Review/Presentation type

    This is useful for testing
    """
    portal = context.getSite()

    # Prepare values for the Review/Presentation fields
    pdf_file = open(os.path.join(
        os.path.dirname(__file__), "tests", "test_content","Review.pdf"),
                    "r")
    pdf_obj = File(id="test-pdf", title="Test Pdf", file=pdf_file,
        content_type='application/pdf')
    word_doc_file = open(os.path.join(
        os.path.dirname(__file__), "tests", "test_content","Review.doc"),
                    "r")
    word_doc_obj = File(id="test-word-doc", title="Test Word Doc",
                   file=word_doc_file,
                   content_type='application/msword')
    review_text = u"""
TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT TEXT 

Deutschland, Österreich, der Schweiz, Tschechien, Ungarn, Kroatien,
Slowenien, der Republik Moldau, der Ukraine, Großbritannien und
Frankreich. Das Themenspektrum reicht von den frühesten
deutschsprachigen Zeitungen und Zeitschriften in Osteuropa aus der
Zeit vor 1848 bis hin zu dem nach dem Zweiten Weltkrieg für die
deutsche Minderheit in Rumänien gegründeten Blatt Neuer Weg. Der
dritte Teil des Bandes beleuchtet die Zeitungslandschaft der Bukowina
und ihrer Hauptstadt Czernowitz/Černivci/Cernăuţi. Einige Aufsätze,
die die thematische Spannweite des Bandes zeigen, seien im Folgenden
exemplarisch genannt: Walter Schmitz: Medien und
Milieu. Deutschsprachige Zeitschriften in Prag um 1900; Hans-Jürgen
Schrader: „Gottes starres Lid“ – Reflexionen geographischer und
metaphysischer Grenzen in der Lyrik Manfred Winklers; Peter Vodopivec:
Die Presse der Deutschen in der Untersteiermark und in Krain
1861–1941; András F. Balogh: Deutsche Presse in den Revolutionsjahren
1848/49 in Ungarn; Marijan Bobinac: Niedergang des deutschen und das
Aufkommen des kroatischen Theaters in Zagreb nach 1848 im Spiegelbild
der zeitgenössischen Publizistik; Bianca Bican: Die Zeitschrift
„Frühling“ (Hermannstadt, 1920) und ihre Herausgeber; Mihai-Ştefan
Ceauşu: Die Presse und das politische Leben in der Bukowina am Anfang
des 20. Jahrhunderts. Der Fall der Zeitschrift „Die Wahrheit“; Mariana
Hausleitner: Öffentlichkeit und Pressezensur in der Bukowina und in
Bessarabien zwischen 1918 und 1938.  Ana-Maria Pălimariu
"""
    authors_list = [dict(firstname='Tadeusz', lastname='Kotłowski'),
                    dict(firstname='Fürchtegott', lastname='Hubermüller'),
                    dict(firstname='François', lastname='Lamère'),
                    dict(firstname='Harald', lastname='Schmidt'),
                    dict(lastname='Стоичков', fistname='Христо')]
    referenceAuthors_list = [
        dict(firstname='Tadeusz', lastname='Kotłowski', email=u'',
             address=u'', phone=u''),
        dict(firstname='Fürchtegott', lastname='Hubermüller',
             email=u'', address=u'', phone=u''),
        dict(firstname='François', lastname='Lamère', email=u'',
             address=u'', phone=u''),
        dict(firstname='Harald', lastname='Schmidt', email=u'',
             address=u'', phone=u'')]

    voc = getToolByName(portal, 'portal_vocabularies')

    ddcPlace = voc.getVocabularyByName('region_values')
    ddcPlace_list = ddcPlace.getDisplayList(ddcPlace).keys()

    ddcSubject = voc.getVocabularyByName('topic_values')
    ddcSubject_list = ddcSubject.getDisplayList(ddcSubject).keys()

    ddcTime = voc.getVocabularyByName('epoch_values')
    ddcTime_list = ddcTime.getDisplayList(ddcTime).keys()

    random.seed('recensio.syslab.com')
    def test_data():
        """Randomise the values in certain fields
        """
        return {'authors': [random.choice(authors_list)],
               'referenceAuthors': [random.choice(referenceAuthors_list),
                                    random.choice(referenceAuthors_list)],
               'ddcPlace': random.choice(ddcPlace_list),
               'ddcSubject': random.choice(ddcSubject_list),
               'ddcTime': random.choice(ddcTime_list),
               'description': u'',
               'doc': word_doc_obj,
               'documenttypes_institution': u'',
               'documenttypes_cooperation': u'',
               'documenttypes_referenceworks': u'',
               'documenttypes_bibliographical': u'',
               'documenttypes_fulltexts': u'',
               'documenttypes_periodicals': u'',
               'yearOfPublication':u'2008',
               'placeOfPublication':u'Krakow',
               'officialYearOfPublication':'2008',
               'number':u'2',
               'editor':u'Avalon',
               'editorCollectedEdition':u'',
               'institution':[dict(institution=u'', lastname=u'', 
                   firstname=u'')],
               'isbn':u'978-83-60448-39-7',
               'isLicenceApproved':True,
               'issn':u'1822-4016',
               'issue':u'5',
               'shortnameJournal':u'',
               'volume':'2',
               'pageStart':'2',
               'pageEnd':'3',
               'pdf': pdf_obj,
               'languageReviewedText':'en',
               'languageReview':'de',
               'recensioID':u'',
               'series':u'',
               'seriesVol':u'',
               'review': review_text,
               'reviewAuthor':u'',
               'subject':u'',
               'pages':u'',
               'title':u'Niemcy',
               'searchresults':u'',
               'subtitle':u'Dzieje państwa i społeczeństwa 1890–1945',
               'uri': 'http://www.syslab.com',
               'idBvb':u'',
               'publisher':u'',
               'customCitation':u'',
               'reviewAuthorHonorific':u'Dr. rer nat',
               'reviewAuthorLastname':u'Стоичков',
               'reviewAuthorFirstname':u'Христо',
               'reviewAuthorEmail':u'',
               'titleJournal':u'',
               'documenttypes_institution':u'',
               'documenttypes_cooperation':u'',
               'documenttypes_bibliographical':u'',
               'documenttypes_individual':u'',
               'documenttypes_referenceworks':u'',
               'coverPicture':None,
               'existingOnlineReviews':[dict(name=u'Dzieje państwa', url='')],
               'publishedReviews':u'',
               'titleCollectedEdition':u'',
               'editorsCollectedEdition':[random.choice(authors_list)],
               'urn': u'testing-data-urn'}

    # Add a folder to contain the sample-reviews
    portal_id = "recensio"
    if "sample-reviews" not in portal.objectIds():
        portal.invokeFactory("Folder", id="sample-reviews",
                             title="Sample Reviews")

    for rez_class in [PresentationArticleReview,
                      PresentationOnlineResource,
                      ReviewMonograph,
                      PresentationMonograph,
                      PresentationCollection,
                      ReviewJournal,]:

        # Fill in all fields with dummy content
        #data = test_data()
        #for field in rez_class.ordered_fields:
          # try:
        #    data[field] = test_data[field]
          # except: print "MISSING", field

        if rez_class.__doc__.startswith("Review"):
            if "newspapera" not in reviews.objectIds():
                reviews.invokeFactory("Publication", id="newspapera",
                                      title="NewspaperA")
            newspapera = reviews["newspapera"]
            if "summer" not in newspapera.objectIds():
                newspapera.invokeFactory("Volume", id="summer", title="Summer")
            summer = newspapera["summer"]
            if "issue-2" not in summer.objectIds():
                summer.invokeFactory("Issue", id="issue-2", title="Issue 2")
            container = summer["issue-2"]
        else:
            container = portal.Members.admin

        for i in range(number_of_each):
            data = test_data()
            data['title'] = 'Test %s No %d' % (rez_class.portal_type, i)
            addOneItem(container, rez_class, data)

    request = TestRequest()
    class FakeResponse(object):
        def write(a, b):
            pass
    request.RESPONSE = FakeResponse()

    view = getMultiAdapter((portal, request), name='solr-maintenance')
    view.clear()
    view.reindex()

def guard(func):
    def wrapper(self):
        if self.readDataFile('recensio.contenttypes_marker.txt') is None:
            return
        return func(self)
    return wrapper

@guard
def addExampleContent(context):
    add_number_of_each_review_type(context, 10)

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
def addOneOfEachReviewType(context):
    add_number_of_each_review_type(context, 1)

@guard
def setTypesOnMemberFolder(self):
    """Only Presentations are allowed in user folders

    Setting the allowed types on the Member folder will achieve the
    appropriate result.
    """
    portal = getSite()

    portal.Members.setConstrainTypesMode(1)
    portal.Members.setLocallyAllowedTypes(["Presentation Article Review",
                                           "Presentation Collection",
                                           "Presentation Online Resource",
                                           "Presentation Monograph",])
    portal.Members.setImmediatelyAddableTypes(["Presentation Article Review",
                                               "Presentation Collection",
                                               "Presentation Online Resource",
                                               "Presentation Monograph",])
