#!/usr/bin/python
# -*- coding: utf-8 -*-

from collective.solr.interfaces import ISolrConnectionConfig
from DateTime import DateTime
from logging import getLogger
from OFS.Image import File
from plone import api
from plone.app.discussion.interfaces import IConversation
from plone.app.portlets.portlets import classic
from plone.app.portlets.utils import assignment_mapping_from_key
from plone.portlets.constants import CONTEXT_CATEGORY
from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName
from random import Random
from recensio.contenttypes.content.presentationarticlereview import PresentationArticleReview
from recensio.contenttypes.content.presentationcollection import PresentationCollection
from recensio.contenttypes.content.presentationmonograph import PresentationMonograph
from recensio.contenttypes.content.presentationonlineresource import PresentationOnlineResource
from recensio.contenttypes.content.reviewjournal import ReviewJournal
from recensio.contenttypes.content.reviewmonograph import ReviewMonograph
from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler
from recensio.contenttypes.interfaces import IReview
from recensio.policy.setuphandlers import hideAllFoldersUnguarded
from recensio.policy.setuphandlers import setViewsOnFoldersUnguarded
from Testing import makerequest
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.event import notify
from zope.globalrequest import setRequest
from zope.publisher.browser import TestRequest

import os


log = getLogger("recensio.contenttypes.setuphandlers")

mdfile = os.path.join(
    os.path.dirname(__file__), "profiles", "exampledata", "metadata.xml"
)

ALL_TYPES = [
    PresentationArticleReview,
    PresentationOnlineResource,
    ReviewMonograph,
    PresentationMonograph,
    PresentationCollection,
    ReviewJournal,
]


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


def add_number_of_each_review_type(portal, number_of_each, rez_classes=ALL_TYPES):
    """Add a particular number of each Review/Presentation type

    This is useful for testing
    """

    # Prepare values for the Review/Presentation fields

    setRequest(portal.REQUEST)
    gnd_view = api.content.get_view(
        context=portal,
        request=portal.REQUEST,
        name="gnd-view",
    )

    pdf_file = open(
        os.path.join(os.path.dirname(__file__), "tests", "test_content", "Review.pdf"),
        "r",
    )
    pdf_obj = File(
        id="test-pdf", title="Test Pdf", file=pdf_file, content_type="application/pdf"
    )
    word_doc_file = open(
        os.path.join(os.path.dirname(__file__), "tests", "test_content", "Review.doc"),
        "r",
    )
    word_doc_obj = File(
        id="test-word-doc",
        title="Test Word Doc",
        file=word_doc_file,
        content_type="application/msword",
    )
    gif_file = open(
        os.path.join(os.path.dirname(__file__), "tests", "test_content", "Review.gif"),
        "r",
    )
    gif_obj = File(
        id="test-gif", title="Test coverImage", file=gif_file, content_type="image/gif"
    )
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
    authors_list = [
        gnd_view.createPerson(**data) for data in [
            {"lastname": u"Kot\u0142owski", "firstname": "Tadeusz"},
            {"lastname": u"Huberm\xfcller", "firstname": u"F\xfcrchtegott"},
            {"lastname": u"Lam\xe8re", "firstname": u"Fran\xe7ois"},
            {"lastname": "Schmidt", "firstname": "Harald"},
            {
                "lastname": u"\u0421\u0442\u043e\u0438\u0447\u043a\u043e\u0432",
                "firstname": u"\u0425\u0440\u0438\u0441\u0442\u043e",
            },
            {"lastname": u"Anders", "firstname": u"Fredi"},
            {"lastname": u"Aumann", "firstname": u"Alexander"},
            {"lastname": u"Beckmann", "firstname": u"Muharrem"},
            {"lastname": u"Beer", "firstname": u"Hubert"},
            {"lastname": u"Benthin", "firstname": u"Patrick"},
            {"lastname": u"Biggen", "firstname": u"\xc4nne"},
            {"lastname": u"Birnbaum", "firstname": u"Marius"},
            {"lastname": u"Budig", "firstname": u"Janine"},
            {"lastname": u"B\xe4rer", "firstname": u"Helmar"},
            {"lastname": u"B\xe4rer", "firstname": u"Notburga"},
            {"lastname": u"Dippel", "firstname": u"Carl-Heinz"},
            {"lastname": u"Drewes", "firstname": u"Willi"},
            {"lastname": u"Ebert", "firstname": u"Traute"},
            {"lastname": u"Eberth", "firstname": u"Margarita"},
            {"lastname": u"Ehlert", "firstname": u"Erica"},
            {"lastname": u"Eimer", "firstname": u"Claudio"},
            {"lastname": u"Eimer", "firstname": u"Kathy"},
            {"lastname": u"Geisel", "firstname": u"Hans-Gerd"},
            {"lastname": u"Girschner", "firstname": u"Jeanette"},
            {"lastname": u"Graf", "firstname": u"Evangelia"},
            {"lastname": u"Gude", "firstname": u"Alma"},
            {"lastname": u"Hauffer", "firstname": u"Aysel"},
            {"lastname": u"Heinrich", "firstname": u"Grit"},
            {"lastname": u"Henschel", "firstname": u"Abram"},
            {"lastname": u"Heuser", "firstname": u"Adriane"},
            {"lastname": u"Huhn", "firstname": u"Willfried"},
            {"lastname": u"H\xe4nel", "firstname": u"Fanny"},
            {"lastname": u"H\xf6lzenbecher", "firstname": u"Wojciech"},
            {"lastname": u"H\xf6lzenbecher", "firstname": u"K\xe4thi"},
            {"lastname": u"H\xfcbel", "firstname": u"Philipp"},
            {"lastname": u"Jessel", "firstname": u"Liesa"},
            {"lastname": u"Junk", "firstname": u"Maria"},
            {"lastname": u"Junken", "firstname": u"Ivonne"},
            {"lastname": u"J\xe4ntsch", "firstname": u"Margita"},
            {"lastname": u"Kraushaar", "firstname": u"Karl-Friedrich"},
            {"lastname": u"Krebs", "firstname": u"J\xf6rg"},
            {"lastname": u"Kreusel", "firstname": u"Elsbeth"},
            {"lastname": u"Kroker", "firstname": u"Luitgard"},
            {"lastname": u"Lindner", "firstname": u"Heidelinde"},
            {"lastname": u"Lindner", "firstname": u"Ingelore"},
            {"lastname": u"Mosemann", "firstname": u"Gitte"},
            {"lastname": u"Mude", "firstname": u"Dragan"},
            {"lastname": u"Pechel", "firstname": u"Toni"},
            {"lastname": u"Pechel", "firstname": u"Marleen"},
            {"lastname": u"Pohl", "firstname": u"Ercan"},
            {"lastname": u"Reichmann", "firstname": u"Minna"},
            {"lastname": u"Rogner", "firstname": u"Lieselotte"},
            {"lastname": u"Rosenow", "firstname": u"Kristian"},
            {"lastname": u"Rosenow", "firstname": u"Siegrun"},
            {"lastname": u"Schaaf", "firstname": u"Annerose"},
            {"lastname": u"Schmidt", "firstname": u"Gusti"},
            {"lastname": u"Schuchhardt", "firstname": u"Hedda"},
            {"lastname": u"Segebahn", "firstname": u"Heinrich"},
            {"lastname": u"Seifert", "firstname": u"Marijan"},
            {"lastname": u"Stiebitz", "firstname": u"Krzysztof"},
            {"lastname": u"Vogt", "firstname": u"Kirsten"},
            {"lastname": u"Weitzel", "firstname": u"Eitel"},
            {"lastname": u"Weller", "firstname": u"Andree"},
            {"lastname": u"Wilmsen", "firstname": u"Ehrentraud"},
            {"lastname": u"Ziegert", "firstname": u"Ingelore"},
        ]
    ]
    review_author = gnd_view.createPerson(**{
        "lastname": u"Стоичков", "firstname": u"Христо"
    })
    review_authors_list = [
        gnd_view.createPerson(**data) for data in [
            {"lastname": u"Benthin", "firstname": u"Kristine"},
            {"lastname": u"Benthin", "firstname": u"Geert"},
            {"lastname": u"Benthin", "firstname": u"Heike"},
            {"lastname": u"Beyer", "firstname": u"Apostolos"},
            {"lastname": u"Birnbaum", "firstname": u"Leander"},
            {"lastname": u"Budig", "firstname": u"Angelina"},
            {"lastname": u"Christoph", "firstname": u"Bastian"},
            {"lastname": u"Drewes", "firstname": u"Sandra"},
            {"lastname": u"Dussen van", "firstname": u"Hanife"},
            {"lastname": u"Eckbauer", "firstname": u"Mirja"},
            {"lastname": u"Fiebig", "firstname": u"Helene"},
            {"lastname": u"Franke", "firstname": u"Simon"},
            {"lastname": u"Gorlitz", "firstname": u"Hans-Hermann"},
            {"lastname": u"Gotthard", "firstname": u"Vincenzo"},
            {"lastname": u"Gude", "firstname": u"Ortrun"},
            {"lastname": u"Gute", "firstname": u"Antonina"},
            {"lastname": u"Hellwig", "firstname": u"Eleni"},
            {"lastname": u"Hendriks", "firstname": u"Harri"},
            {"lastname": u"Hermann", "firstname": u"Ingbert"},
            {"lastname": u"Heser", "firstname": u"Bianca"},
            {"lastname": u"Hethur", "firstname": u"Karsten"},
            {"lastname": u"Hofmann", "firstname": u"Ralf-Peter"},
            {"lastname": u"Hofmann", "firstname": u"Traude"},
            {"lastname": u"Holt", "firstname": u"Falko"},
            {"lastname": u"Jessel", "firstname": u"Stephan"},
            {"lastname": u"Johann", "firstname": u"Burkhard"},
            {"lastname": u"Juncken", "firstname": u"Kordula"},
            {"lastname": u"Junitz", "firstname": u"Claudio"},
            {"lastname": u"J\xe4ntsch", "firstname": u"Zoran"},
            {"lastname": u"J\xfcttner", "firstname": u"Arne"},
            {"lastname": u"Kabus", "firstname": u"Ingetraud"},
            {"lastname": u"Karz", "firstname": u"Hildegund"},
            {"lastname": u"Kaul", "firstname": u"Annie"},
            {"lastname": u"Koch", "firstname": u"Gilbert"},
            {"lastname": u"Kusch", "firstname": u"Rena"},
            {"lastname": u"K\xf6hler", "firstname": u"Hanny"},
            {"lastname": u"K\xfchnert", "firstname": u"Anna-Maria"},
            {"lastname": u"L\xfcbs", "firstname": u"Dorina"},
            {"lastname": u"Martin", "firstname": u"Hilmar"},
            {"lastname": u"Meyer", "firstname": u"Ekkehard"},
            {"lastname": u"Misicher", "firstname": u"Orhan"},
            {"lastname": u"Mitschke", "firstname": u"Catherine"},
            {"lastname": u"Riehl", "firstname": u"Aneta"},
            {"lastname": u"Rosenow", "firstname": u"Friedhold"},
            {"lastname": u"Ruppersberger", "firstname": u"Carsten"},
            {"lastname": u"Rust", "firstname": u"Conrad"},
            {"lastname": u"R\xf6hricht", "firstname": u"Willibert"},
            {"lastname": u"Salz", "firstname": u"Dierk"},
            {"lastname": u"Sauer", "firstname": u"Monja"},
            {"lastname": u"Schacht", "firstname": u"Hannah"},
            {"lastname": u"Scheibe", "firstname": u"Niklas"},
            {"lastname": u"Schmiedt", "firstname": u"Josip"},
            {"lastname": u"Scholz", "firstname": u"Clemens"},
            {"lastname": u"Schuchhardt", "firstname": u"Hans-Adolf"},
            {"lastname": u"Seifert", "firstname": u"Micha"},
            {"lastname": u"Stey", "firstname": u"Agata"},
            {"lastname": u"Wagenknecht", "firstname": u"Petar"},
            {"lastname": u"Wieloch", "firstname": u"Elwira"},
            {"lastname": u"Wieloch", "firstname": u"Ottfried"},
            {"lastname": u"Winkler", "firstname": u"Gloria"},
        ]
    ]
    referenceAuthors_list = [
        dict(
            firstname="Tadeusz",
            lastname=u"Kot\u0142owski",
            email=u"dev0@syslab.com",
            address=u"",
            phone=u"",
        ),
        dict(
            firstname=u"F\xfcrchtegott",
            lastname=u"Huberm\xfcller",
            email=u"dev0@syslab.com",
            address=u"",
            phone=u"",
        ),
        dict(
            firstname=u"Fran\xe7ois",
            lastname=u"Lam\xe8re",
            email=u"dev0@syslab.com",
            address=u"",
            phone=u"",
        ),
        dict(
            firstname="Harald",
            lastname="Schmidt",
            email=u"dev0@syslab.com",
            address=u"",
            phone=u"",
        ),
    ]

    voc = getToolByName(portal, "portal_vocabularies")

    ddcPlace = voc.getVocabularyByName("region_values")
    ddcPlace_list = ddcPlace.getDisplayList(ddcPlace).keys()

    ddcSubject = voc.getVocabularyByName("topic_values")
    ddcSubject_list = ddcSubject.getDisplayList(ddcSubject).keys()

    ddcTime = voc.getVocabularyByName("epoch_values")
    ddcTime_list = ddcTime.getDisplayList(ddcTime).keys()
    random = Random()
    random.seed("recensio.syslab.com")

    def isbn():
        for idx in range(1000):
            yield (lambda s: "-".join([s[:3], s[3:5], s[5:10], s[10:12], s[12]]))(
                str(9788360448396 + idx)
            )

    isbn_generator = isbn()

    def test_data():
        """Randomise the values in certain fields"""

        return {
            "authors": [random.choice(authors_list)],
            "referenceAuthors": [
                random.choice(referenceAuthors_list),
                random.choice(referenceAuthors_list),
            ],
            "ddcPlace": random.choice(ddcPlace_list),
            "ddcSubject": random.choice(ddcSubject_list),
            "ddcTime": random.choice(ddcTime_list),
            "description": u"",
            "doc": word_doc_obj,
            "documenttypes_institution": u"",
            "documenttypes_cooperation": u"",
            "documenttypes_referenceworks": u"",
            "documenttypes_bibliographical": u"",
            "documenttypes_fulltexts": u"",
            "documenttypes_periodicals": u"",
            "yearOfPublication": u"2008",
            "placeOfPublication": u"Krakow",
            "officialYearOfPublication": "2008",
            "number": u"2",
            "editor": u"Avalon",
            "editorCollectedEdition": u"",
            "institution": [dict(institution=u"", lastname=u"", firstname=u"")],
            "isbn": isbn_generator.next(),
            "isLicenceApproved": True,
            "issn": u"1822-4016",
            "issue": u"5",
            "shortnameJournal": u"",
            "volume": "2",
            "pageStart": "2",
            "pageEnd": "3",
            "pageStartOfReviewInJournal": "2",
            "pageEndOfReviewInJournal": "3",
            "pdf": pdf_obj,
            "languageReviewedText": "en",
            "languageReview": "de",
            "recensioID": u"",
            "series": u"",
            "seriesVol": u"",
            "review": review_text,
            "reviewAuthor": u"",
            "subject": u"",
            "pages": u"",
            "title": u"Niemcy",
            "subtitle": u"Dzieje państwa i społeczeństwa 1890–1945",
            "uri": "http://www.syslab.com",
            "idBvb": u"",
            "publisher": u"",
            "customCitation": u"",
            "reviewAuthorHonorific": u"Dr. rer nat",
            "reviewAuthors": [random.choice(review_authors_list)],
            "reviewAuthorEmail": u"dev0@syslab.com",
            "titleJournal": u"",
            "documenttypes_institution": u"",
            "documenttypes_cooperation": u"",
            "documenttypes_bibliographical": u"",
            "documenttypes_individual": u"",
            "documenttypes_referenceworks": u"",
            "coverPicture": gif_obj,
            "existingOnlineReviews": [dict(name=u"Dzieje państwa", url="")],
            "publishedReviews": [dict(details=u"Journal A, 2008")],
            "titleCollectedEdition": u"",
            "editorsCollectedEdition": [random.choice(authors_list)],
            "urn": u"testing-data-urn",
            "doi": u"10.15463/rec.0123456",
        }

    # Add a folder to contain the sample-reviews

    portal_id = "recensio"
    if "sample-reviews" not in portal.objectIds():
        portal.invokeFactory("Folder", id="sample-reviews", title="Sample Reviews")
    sample_reviews = portal.get("sample-reviews")

    for rez_class in rez_classes:

        # Fill in all fields with dummy content data = test_data() for
        # field in rez_class.ordered_fields: try: data[field] =
        # test_data[field] except: print "MISSING", field

        if rez_class.__doc__.startswith("Review"):
            if "newspapera" not in sample_reviews.objectIds():
                sample_reviews.invokeFactory(
                    "Publication", id="newspapera", title="Zeitschrift 1"
                )
                sample_reviews["newspapera"].invokeFactory("Document", id="index_html")
            if "newspaperb" not in sample_reviews.objectIds():
                sample_reviews.invokeFactory(
                    "Publication", id="newspaperb", title="Zeitschrift 2"
                )
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
                data["title"] = "test title"
                data["languageReviewedText"] = "de"
                data["languageReview"] = "fr"
                data["shortnameJournal"] = "Zeitschrift 1"
                obj = addOneItem(containerb, rez_class, data)
                item = containerb.objectValues()[0]
                comment = createObject("plone.Comment")
                IConversation(item).addComment(comment)
            containerb = summerb["issue-2"]
            container = containera
        else:
            pm = portal.portal_membership
            pm.addMember(
                id="fake_member", password="fake_member_pw", roles=[], domains=[]
            )
            pm.createMemberArea("fake_member")
            container = pm.getMembersFolder().get("fake_member")

        for i in range(number_of_each):
            data = test_data()
            if i / 3 == 1:
                data["languageReviewedText"] = "fr"
                data["languageReview"] = "en"
            elif i / 3 == 2:
                data["languageReviewedText"] = "de"
                data["languageReview"] = "fr"
            data["shortnameJournal"] = "Zeitschrift 1"
            data["title"] = "Test %s No %d" % (rez_class.portal_type, i)
            obj = addOneItem(container, rez_class, data)

    # Create sample sehepunkte and francia reviews

    if "rezensionen" not in portal.objectIds():
        portal.invokeFactory("Folder", "rezensionen")
    rezensionen = portal.rezensionen
    if "zeitschriften" not in rezensionen.objectIds():
        rezensionen.invokeFactory("Folder", "zeitschriften")
    zeitschriften = rezensionen.zeitschriften
    if "sehepunkte" not in zeitschriften.objectIds():
        zeitschriften.invokeFactory("Publication", "sehepunkte")
    sehepunkte = zeitschriften.sehepunkte
    sehepunkte.invokeFactory("Volume", "vol1")
    sp_vol1 = sehepunkte.vol1
    sp_vol1.invokeFactory("Issue", "issue1")
    sp_issue1 = sp_vol1.issue1
    sp_issue1.invokeFactory("Review Monograph", "sp-rm", **test_data())
    sp_issue1.invokeFactory("Review Journal", "sp-rj", **test_data())

    if "francia-recensio" not in zeitschriften.objectIds():
        zeitschriften.invokeFactory("Publication", "francia-recensio")
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

    view = getMultiAdapter((portal, request), name="solr-maintenance")
    view.clear()
    view.reindex()


def guard(profiles):
    def inner_guard(func):
        def wrapper(self):
            for profile in profiles:
                if (
                    self.readDataFile("recensio.contenttypes_%s_marker.txt" % profile)
                    is not None
                ):
                    return func(self)
            return

        return wrapper

    return inner_guard


@guard(["exampledata"])
def recensio_example_content_all(context):
    """addOneItem calls:
    notify(ObjectAddedEvent(item, context, newid))
    notify(ObjectInitializedEvent(item, request))

    once either of these events get called the genericsetup registry
    of steps gets reset (no idea why or how). This causes all
    subsequent steps to be skipped in this profile. For this reason
    all the steps are called from recensio_example_content_all"""

    addExampleContent(context)
    setViewsOnFoldersUnguarded(context)
    hideAllFoldersUnguarded(context)


@guard(["exampledata"])
def addExampleContent(context):
    portal = context.getSite()
    add_number_of_each_review_type(portal, 10)


@guard(["exampledata"])
def addOneOfEachReviewType(context):
    """TODO: remove this? It isn\'t being used anywhere"""

    portal = context.getSite()
    add_number_of_each_review_type(portal, 1)


@guard(["default"])
def setTypesOnMemberFolder(self):
    """Only Presentations are allowed in user folders

    Setting the allowed types on the Member folder will achieve the
    appropriate result.
    """

    portal = getSite()

    portal.Members.setConstrainTypesMode(1)
    portal.Members.setLocallyAllowedTypes(
        [
            "Presentation Article Review",
            "Presentation Collection",
            "Presentation Online Resource",
            "Presentation Monograph",
        ]
    )
    portal.Members.setImmediatelyAddableTypes(
        [
            "Presentation Article Review",
            "Presentation Collection",
            "Presentation Online Resource",
            "Presentation Monograph",
        ]
    )


@guard(["initial_content"])
def addSecondaryNavPortlets(context):
    """Add and configure the Classic portlet for secondary navigation"""

    portal = getSite()
    objs = (
        portal.get("ueberuns"),
        portal.get("ueberuns-en"),
        portal.get("ueberuns-fr"),
    )
    for obj in objs:
        if obj:
            path = "/".join(obj.getPhysicalPath())
            left_portlet_assignment_mapping = assignment_mapping_from_key(
                obj, "plone.leftcolumn", CONTEXT_CATEGORY, path
            )
            if not left_portlet_assignment_mapping.has_key("secondarynavportlet"):
                left_portlet_assignment_mapping[
                    "secondarynavportlet"
                ] = classic.Assignment(template="secondarynavportlets", macro="ueberuns")

    objs = (portal.get("rezensionen"),)
    for obj in objs:
        if obj:
            path = "/".join(obj.getPhysicalPath())
            left_portlet_assignment_mapping = assignment_mapping_from_key(
                obj, "plone.leftcolumn", CONTEXT_CATEGORY, path
            )
            if not left_portlet_assignment_mapping.has_key("secondarynavportlet"):
                left_portlet_assignment_mapping[
                    "secondarynavportlet"
                ] = classic.Assignment(
                    template="secondarynavportlets", macro="rezensionen"
                )

    # TODO: set sec. nav for praesentationen


def initGndContainer(context=None):
    portal = api.portal.get()
    if "gnd" not in portal:
        gnd_folder = api.content.create(
            type="Folder",
            container=portal,
            id="gnd",
            title="GND",
        )
    else:
        gnd_folder = portal.get("gnd")
    try:
        api.content.transition(
            to_state="published",
            obj=gnd_folder,
        )
    except Exception as e:
        log.exception(e)
        pass
    api.group.grant_roles(
        obj=gnd_folder, groupname="AuthenticatedUsers", roles=["Contributor"]
    )


def v0to1(context):
    catalog = getToolByName(context, "portal_catalog")

    query_args = dict(
        modified=dict(query=DateTime("2012-06-18"), range="min"),
        object_provides=IReview.__identifier__,
    )

    for brain in catalog(query_args):
        review_pdf_updated_eventhandler(brain.getObject(), None)


def v1to2(context):
    catalog = getToolByName(context, "portal_catalog")

    pors = catalog(portal_type=["Presentation Online Resource"])
    migrated = 0
    for brain in pors:
        try:
            obj = brain.getObject()
        except:
            log.error("Could not get Object %s" % brain["getId"])
            continue
        institution = obj.getInstitution()
        if len(institution) > 0:
            unmigrated = [line for line in institution if "name" not in line]
            if not unmigrated:
                continue
            institution_new = []
            for line in unmigrated:
                if not line.get("lastname") and not line.get("firstname"):
                    continue
                if not line.get("firstname"):
                    institution_new.append({"name": line["lastname"]})
                elif not line.get("lastname"):
                    institution_new.append({"name": line["firstname"]})
                else:
                    institution_new.append(
                        {"name": "%s %s" % (line["firstname"], line["lastname"])}
                    )
            obj.setInstitution(tuple(institution_new))
            migrated += 1
    log.info("Migrated institution field of %d POR objects" % migrated)


def v2to3(context):
    catalog = getToolByName(context, "portal_catalog")
    for index in ["commentators", "authors"]:
        catalog.manage_reindexIndex(index)


def v3to4(context):
    # We temporarily set solr's max_results to the number of total objects
    # because plone.app.intid does an unbounded search with no b_size. This
    # works around this error:
    # AttributeError: 'NoneType' object has no attribute 'getPath'
    catalog = getToolByName(context, "portal_catalog")
    query = {
        "object_provides": IContentish.__identifier__,
        "Language": "all",
        "b_size": 0,
    }
    num_objects = len(catalog(query))
    solrconf = getUtility(ISolrConnectionConfig)
    max_results = solrconf.max_results
    solrconf.max_results = num_objects

    context.runAllImportStepsFromProfile("profile-plone.app.intid:default")

    solrconf.max_results = max_results


def v4to5(context):
    context.runImportStepFromProfile("profile-recensio.contenttypes:default", "skins")


def v5to6(context):
    catalog = getToolByName(context, "portal_catalog")
    portal = api.portal.get()
    authorsearch = api.content.get_view(
        name="authorsearch",
        context=portal,
        request=context.REQUEST,
    )
    query = {
        "portal_type": "Person",
        "b_start": 0,
        "b_size": 0,
        "sort_on": "sortable_title",
        "fl": "Title,UID,path_string",
        "path": "/".join(portal.getPhysicalPath()),
    }
    num_authors = len(catalog(query))
    query["b_size"] = num_authors
    authors = [author for author in catalog(query) if "/" in (author.Title or "")]

    log.info("Fixing {} authors".format(len(authors)))

    for author in authors:
        results = catalog(authorsFulltext=author["name"], use_solr=1)
        log.info(u"Reindexing {} item(s) for {}".format(len(results), author["name"]))
        for res in results:
            try:
                obj = res.getObject()
            except Exception as e:
                log.warn("Could not get object %s (%s)", res.getPath(), e)
            obj.reindexObject()
