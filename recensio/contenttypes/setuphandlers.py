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
    referenceAuthors_list = [dict(firstname='Tadeusz', lastname='Kotłowski', email=u'', address=u'', phone=u''),
                    dict(firstname='Fürchtegott', lastname='Hubermüller', email=u'', address=u'', phone=u''),
                    dict(firstname='François', lastname='Lamère', email=u'', address=u'', phone=u''),
                    dict(firstname='Harald', lastname='Schmidt', email=u'', address=u'', phone=u'')]

    voc = getToolByName(portal, 'portal_vocabularies')

    ddcPlace = voc.getVocabularyByName('region_values')
    ddcPlace_list = ddcPlace.getDisplayList(ddcPlace).keys()

    ddcSubject = voc.getVocabularyByName('topic_values')
    ddcSubject_list = ddcSubject.getDisplayList(ddcSubject).keys()

    ddcTime = voc.getVocabularyByName('epoch_values')
    ddcTime_list = ddcTime.getDisplayList(ddcTime).keys()

    random.seed('recensio.syslab.com')

    def test_data():
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

        if rez_class.__doc__ == "Review Journal":
            reviews.invokeFactory("Publication", id="newspapera", title="NewspaperA")
            newspapera = reviews["newspapera"]
            newspapera.invokeFactory("Volume", id="summer", title="Summer")
            summer = newspapera["summer"]
            summer.invokeFactory("Issue", id="issue-2", title="Issue 2")
            container = summer["issue-2"]
        else:
            container = reviews

        for i in range(10):
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

def addOneItem(context, type, data):
    data["id"] = context.generateId(type.meta_type)
    review_id = context.invokeFactory(type.__doc__, **data)
    obj = context[review_id]
    request = makerequest.makerequest(obj)
    event=ObjectInitializedEvent(obj, request)
    zope.event.notify(event)
    return context[review_id]


class StructureFolderWalkingAdapter(object):
    """ Tree-walking exporter for "folderish" types.

    Folderish instances are mapped to directories within the 'structure'
    portion of the profile, where the folder's relative path within the site
    corresponds to the path of its directory under 'structure'.

    The subobjects of a folderish instance are enumerated in the '.objects'
    file in the corresponding directory.  This file is a CSV file, with one
    row per subobject, with the following wtructure::

     "<subobject id>","<subobject portal_type>"

    Subobjects themselves are represented as individual files or
    subdirectories within the parent's directory.
    If the import step finds that any objects specified to be created by the
    'structure' directory setup already exist, these objects will be deleted
    and then recreated by the profile.  The existence of a '.preserve' file
    within the 'structure' hierarchy allows specification of objects that
    should not be deleted.  '.preserve' files should contain one preserve
    rule per line, with shell-style globbing supported (i.e. 'b*' will match
    all objects w/ id starting w/ 'b'.

    Similarly, a '.delete' file can be used to specify the deletion of any
    objects that exist in the site but are NOT in the 'structure' hierarchy,
    and thus will not be recreated during the import process.
    """

    implements(IFilesystemExporter, IFilesystemImporter)

    def __init__(self, context):
        self.context = context

    def export(self, export_context, subdir, root=False):
        """ See IFilesystemExporter.
        """
        # Enumerate exportable children
        exportable = self.context.contentItems()
        exportable = [x + (IFilesystemExporter(x, None),) for x in exportable]
        exportable = [x for x in exportable if x[1] is not None]

        stream = StringIO()
        csv_writer = writer(stream)

        for object_id, object, ignored in exportable:
            csv_writer.writerow((object_id, object.getPortalTypeName()))

        if not root:
            subdir = '%s/%s' % (subdir, self.context.getId())

        export_context.writeDataFile('.objects',
                                     text=stream.getvalue(),
                                     content_type='text/comma-separated-values',
                                     subdir=subdir,
                                    )

        stream = self.parseProperties()

        export_context.writeDataFile('.properties',
                                    text=stream.getvalue(),
                                    content_type='text/plain',
                                    subdir=subdir,
                                    )

        for id, object in self.context.objectItems():

            adapter = IFilesystemExporter(object, None)

            if adapter is not None:
                adapter.export(export_context, subdir)

    def import_(self, import_context, subdir, root=False):
        """ See IFilesystemImporter.
        """
        context = self.context
        if not root:
            subdir = '%s/%s' % (subdir, context.getId())

        objects = import_context.readDataFile('.objects', subdir)
        if objects is None:
            return

        dialect = 'excel'
        stream = StringIO(objects)

        rowiter = reader(stream, dialect)
        ours = filter(None, tuple(rowiter))
        our_ids = set([item[0] for item in ours])

        prior = set(context.contentIds())

        preserve = import_context.readDataFile('.preserve', subdir)
        if not preserve:
            preserve = set()
        else:
            preservable = prior.intersection(our_ids)
            preserve = set(_globtest(preserve, preservable))

        delete = import_context.readDataFile('.delete', subdir)
        if not delete:
            delete= set()
        else:
            deletable = prior.difference(our_ids)
            delete = set(_globtest(delete, deletable))

        # if it's in our_ids and NOT in preserve, or if it's not in
        # our_ids but IS in delete, we're gonna delete it
        delete = our_ids.difference(preserve).union(delete)

        for id in prior.intersection(delete):
            context._delObject(id)

        existing = context.objectIds()

        for object_id, portal_type in ours:

            if object_id not in existing:
                object = self._makeInstance(object_id, portal_type,
                                            subdir, import_context)
                if object is None:
                    logger = import_context.getLogger('SFWA')
                    logger.warning("Couldn't make instance: %s/%s" %
                                   (subdir, object_id))
                    continue

            wrapped = context._getOb(object_id)

            IFilesystemImporter(wrapped).import_(import_context, subdir)

    def parseProperties(self):
        parser = ConfigParser()

        parser.set('DEFAULT', 'Title', self.context.Title())
        parser.set('DEFAULT', 'Description', self.context.Description())
        stream = StringIO()
        parser.write(stream)

        return stream

    def _makeInstance(self, id, portal_type, subdir, import_context):

        context = self.context
        properties = import_context.readDataFile('.properties',
                                                 '%s/%s' % (subdir, id))
        tool = getToolByName(context, 'portal_types')

        try:
            tool.constructContent(portal_type, context, id)
        except ValueError: # invalid type
            return None

        content = context._getOb(id)

        if properties is not None:
            lines = properties.splitlines()

            stream = StringIO('\n'.join(lines))
            parser = ConfigParser(defaults={'title': '', 'description': 'NONE'})
            parser.readfp(stream)

            title = parser.get('DEFAULT', 'title')
            description = parser.get('DEFAULT', 'description')

            content.setTitle(title)
            content.setDescription(description)

        return content

class MagazineFolderWalkingAdapter(StructureFolderWalkingAdapter):
    adapts(IPublication)
    def parseProperties(self):
        parser = ConfigParser()

        parser.set('DEFAULT', 'Title', self.context.Title())
        parser.set('DEFAULT', 'Description', self.context.Description())
        parser.set('DEFAULT', 'long_description', self.context.getLong_description())
        stream = StringIO()
        parser.write(stream)

        return stream

    def _makeInstance(self, id, portal_type, subdir, import_context):

        context = self.context
        properties = import_context.readDataFile('.properties',
                                                 '%s/%s' % (subdir, id))
        tool = getToolByName(context, 'portal_types')

        try:
            tool.constructContent(portal_type, context, id)
        except ValueError: # invalid type
            return None

        content = context._getOb(id)

        if properties is not None:
            lines = properties.splitlines()

            stream = StringIO('\n'.join(lines))
            parser = ConfigParser(defaults={'title': '', 'description': 'NONE'})
            parser.readfp(stream)

            title = parser.get('DEFAULT', 'title')
            description = parser.get('DEFAULT', 'description')
            long_description = parser.get('DEFAULT', 'long_description')

            content.setTitle(title)
            content.setDescription(description)
            content.setLong_description(long_description)

        return content
