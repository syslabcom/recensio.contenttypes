# -*- coding: utf-8 -*-
from random import Random
import os

from swiss.tabular import XlsReader

from Acquisition import aq_inner, aq_parent, aq_base, aq_chain, aq_get
from OFS.Image import File
from Testing import makerequest
from zope.app.component.hooks import getSite
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.container.contained import ObjectAddedEvent
from zope.container.contained import notifyContainerModified
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.publisher.browser import TestRequest

from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.interfaces import IConversation
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.portlets.constants import CONTEXT_CATEGORY

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

from recensio.policy.setuphandlers import (
    setViewsOnFoldersUnguarded, hideAllFoldersUnguarded)

mdfile = os.path.join(os.path.dirname(__file__), 'profiles', 'exampledata',
    'metadata.xml')


def addOneItem(context, type, data):
    """Add an item and fire the ObjectInitializedEvent

    This triggers file conversions for the Reviews/Presentations

    when invokeFactory is called it triggers the ObjectAddedEvent
    which somehow causes the GenericSetup steps registry to be
    reset. The end effect is that no further steps will be run in a
    profile which calls this function. All steps for example_content
    are now called from recensio_example_content_all.
    """
    data["id"] = context.generateId(type.meta_type)
    review_id = context.invokeFactory(type.__doc__, **data)
    obj = context[review_id]
    request = makerequest.makerequest(obj)
    event = ObjectInitializedEvent(obj, request)
    notify(event)
    return obj

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
    gif_file = open(os.path.join(
        os.path.dirname(__file__), "tests", "test_content","Review.gif"),
                    "r")
    gif_obj = File(id="test-gif", title="Test coverImage", file=gif_file,
        content_type='image/gif')
    gif_file.close()

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
        dict(firstname='Tadeusz', lastname='Kotłowski', email=u'dev0@syslab.com',
             address=u'', phone=u''),
        dict(firstname='Fürchtegott', lastname='Hubermüller',
             email=u'dev0@syslab.com', address=u'', phone=u''),
        dict(firstname='François', lastname='Lamère', email=u'dev0@syslab.com',
             address=u'', phone=u''),
        dict(firstname='Harald', lastname='Schmidt', email=u'dev0@syslab.com',
             address=u'', phone=u'')]

    voc = getToolByName(portal, 'portal_vocabularies')

    ddcPlace = voc.getVocabularyByName('region_values')
    ddcPlace_list = ddcPlace.getDisplayList(ddcPlace).keys()

    ddcSubject = voc.getVocabularyByName('topic_values')
    ddcSubject_list = ddcSubject.getDisplayList(ddcSubject).keys()

    ddcTime = voc.getVocabularyByName('epoch_values')
    ddcTime_list = ddcTime.getDisplayList(ddcTime).keys()
    random = Random()
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
               'subtitle':u'Dzieje państwa i społeczeństwa 1890–1945',
               'uri': 'http://www.syslab.com',
               'idBvb':u'',
               'publisher':u'',
               'customCitation':u'',
               'reviewAuthorHonorific':u'Dr. rer nat',
               'reviewAuthors':[{"lastname":u'Стоичков',
                                "firstname":u'Христо'}],
               'reviewAuthorEmail':u'dev0@syslab.com',
               'titleJournal':u'',
               'documenttypes_institution':u'',
               'documenttypes_cooperation':u'',
               'documenttypes_bibliographical':u'',
               'documenttypes_individual':u'',
               'documenttypes_referenceworks':u'',
               'coverPicture': gif_obj,
               'existingOnlineReviews':[dict(name=u'Dzieje państwa', url='')],
               'publishedReviews':[dict(details=u'Journal A, 2008',)],
               'titleCollectedEdition':u'',
               'editorsCollectedEdition':[random.choice(authors_list)],
               'urn': u'testing-data-urn'
                }

    # Add a folder to contain the sample-reviews
    portal_id = "recensio"
    if "sample-reviews" not in portal.objectIds():
        portal.invokeFactory("Folder", id="sample-reviews",
                             title="Sample Reviews")
    sample_reviews = portal.get("sample-reviews")

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
            if "newspapera" not in sample_reviews.objectIds():
                sample_reviews.invokeFactory("Publication", id="newspapera",
                                      title="Zeitschrift 1")
                sample_reviews["newspapera"].invokeFactory(
                    "Document", id="index_html")
            if "newspaperb" not in sample_reviews.objectIds():
                sample_reviews.invokeFactory("Publication", id="newspaperb",
                                      title="Zeitschrift 2")
            newspapera = sample_reviews["newspapera"]
            newspaperb = sample_reviews["newspaperb"]
            if "summer" not in newspapera.objectIds():
                newspapera.invokeFactory("Volume", id="summer", title="Summer")
            summera = newspapera["summer"]
            if "summer" not in newspaperb.objectIds():
                newspaperb.invokeFactory("Volume", id="summer", title="Summer")
            summerb = newspaperb["summer"]
            if "issue-2" not in summera.objectIds():
                summera.invokeFactory("Issue", id="issue-2", title="Issue 2")
            containera = summera["issue-2"]
            if "issue-2" not in summerb.objectIds():
                summerb.invokeFactory("Issue", id="issue-2", title="Issue 2")
                containerb = summerb["issue-2"]
                data = test_data()
                data['title'] = 'test title'
                data['languageReviewedText'] = 'de'
                data['languageReview'] = 'fr'
                data['shortnameJournal'] = 'Zeitschrift 1'
                obj = addOneItem(containerb, rez_class, data)
                item = containerb.objectValues()[0]
                comment = createObject('plone.Comment')
                IConversation(item).addComment(comment)
            containerb = summerb["issue-2"]
            container = containera
        else:
            pm = portal.portal_membership
            pm.addMember(id="fake_member", password="fake_member_pw",
                         roles=[], domains=[])
            pm.createMemberArea("fake_member")
            container = pm.getMembersFolder().get("fake_member")

        for i in range(number_of_each):
            data = test_data()
            if i / (number_of_each / 3) == 1:
                data['languageReviewedText'] = 'fr'
                data['languageReview'] = 'en'
            elif i / (number_of_each / 3) == 2:
                data['languageReviewedText'] = 'de'
                data['languageReview'] = 'fr'
            data['shortnameJournal'] = 'Zeitschrift 1'
            data['title'] = 'Test %s No %d' % (rez_class.portal_type, i)
            obj = addOneItem(container, rez_class, data)

    # Create sample sehepunkte and francia reviews
    if "rezensionen" not in portal.objectIds():
        portal.invokeFactory("Folder", "rezensionen")
    rezensionen = portal.rezensionen
    if "zeitschriften" not in rezensionen.objectIds():
        rezensionen.invokeFactory("Folder", "zeitschriften")
    zeitschriften = rezensionen.zeitschriften
    if "sehepunkte" not in zeitschriften.objectIds():
        zeitschriften.invokeFactory("Presentation", "sehepunkte")
    sehepunkte = zeitschriften.sehepunkte
    sehepunkte.invokeFactory("Volume", "vol1")
    sp_vol1 = sehepunkte.vol1
    sp_vol1.invokeFactory("Issue", "issue1")
    sp_issue1 = sp_vol1.issue1
    sp_issue1.invokeFactory("Review Monograph", "sp-rm", **test_data())
    sp_issue1.invokeFactory("Review Journal", "sp-rj", **test_data())

    if "francia-recensio" not in zeitschriften.objectIds():
        zeitschriften.invokeFactory("Presentation", "francia-recensio")
    francia_recensio = zeitschriften["francia-recensio"]
    francia_recensio.invokeFactory("Volume", "vol1")
    fr_vol1 = francia_recensio.vol1
    fr_vol1.invokeFactory("Issue", "issue1")
    fr_issue1 = fr_vol1.issue1
    fr_issue1.invokeFactory("Review Monograph", "fr-rm", **test_data())
    fr_issue1.invokeFactory("Review Journal", "fr-rj", **test_data())

    request = TestRequest()
    class FakeResponse(object):
        def write(a, b):
            pass
    request.RESPONSE = FakeResponse()

    view = getMultiAdapter((portal, request), name='solr-maintenance')
    view.clear()
    view.reindex()

def guard(profiles):
    def inner_guard(func):
        def wrapper(self):
            for profile in profiles:
                if self.readDataFile('recensio.contenttypes_%s_marker.txt' \
                   % profile) is not None:
                    return func(self)
            return
        return wrapper
    return inner_guard

@guard(['exampledata'])
def recensio_example_content_all(context):
    """  addOneItem calls:
    notify(ObjectAddedEvent(item, context, newid))
    notify(ObjectInitializedEvent(item, request))

    once either of these events get called the genericsetup registry
    of steps gets reset (no idea why or how). This causes all
    subsequent steps to be skipped in this profile. For this reason
    all the steps are called from recensio_example_content_all """
    addExampleContent(context)
    setViewsOnFoldersUnguarded(context)
    hideAllFoldersUnguarded(context)

@guard(['exampledata'])
def addExampleContent(context):
    add_number_of_each_review_type(context, 10)

@guard(['exampledata'])
def addOneOfEachReviewType(context):
    """TODO: remove this? It isn't being used anywhere"""
    add_number_of_each_review_type(context, 1)

@guard(['default'])
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

from plone.app.portlets.portlets import classic

@guard(['initial_content'])
def addSecondaryNavPortlets(context):
    """ Add and configure the Classic portlet for secondary navigation
    """
    portal = getSite()
    objs = (portal.get("ueberuns"),
            portal.get("ueberuns-en"),
            portal.get("ueberuns-fr")
            )
    for obj in objs:
        if obj:
            path = "/".join(obj.getPhysicalPath())
            left_portlet_assignment_mapping = assignment_mapping_from_key(
                obj, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
            if not left_portlet_assignment_mapping.has_key(
                "secondarynavportlet"):
                left_portlet_assignment_mapping["secondarynavportlet"] = \
                    classic.Assignment(template="secondarynavportlets",
                                       macro="ueberuns")

    objs = (portal.get("rezensionen"),
            )
    for obj in objs:
        if obj:
            path = "/".join(obj.getPhysicalPath())
            left_portlet_assignment_mapping = assignment_mapping_from_key(
                obj, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
            if not left_portlet_assignment_mapping.has_key(
                "secondarynavportlet"):
                left_portlet_assignment_mapping["secondarynavportlet"] = \
                    classic.Assignment(template="secondarynavportlets",
                                       macro="rezensionen")

    #TODO: set sec. nav for praesentationen
