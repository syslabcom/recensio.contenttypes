# -*- coding: utf-8 -*-
"""Definition of the Presentation Article Review content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.interfaces import IPresentationArticleReview


PresentationArticleReviewSchema = \
                                JournalReviewSchema.copy() + \
                                PresentationSchema.copy() + \
                                ReferenceAuthorsSchema.copy() + \
                                PageStartEndSchema.copy() + \
                                atapi.Schema((
    atapi.StringField(
        'titleJournal',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title Journal"),
            rows=3,
            ),
        ),
    atapi.StringField(
        'shortnameJournal',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Shortname (Journal)"),
            ),
        ),
    atapi.StringField(
        'volume',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Volume"),
            ),
        ),
    atapi.StringField(
        'issue',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Issue"),
            ),
        ),
))

PresentationArticleReviewSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationArticleReviewSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationArticleReviewSchema,
                            moveDiscussion=False)

# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
PresentationArticleReviewSchema.changeSchemataForField('subject', 'default')


class PresentationArticleReview(BaseReview):
    """Presentation Article Review"""
    implements(IPresentationArticleReview)

    meta_type = "PresentationArticleReview"
    schema = PresentationArticleReviewSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Journal = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languagePresentation = atapi.ATFieldProperty('languagePresentation')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    customCitation = atapi.ATFieldProperty('customCitation')
    uri = atapi.ATFieldProperty('uri')

    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    # Printed
    subtitle = atapi.ATFieldProperty('subtitle')
    yearOfPublication = atapi.ATFieldProperty('yearOfPublication')
    placeOfPublication = atapi.ATFieldProperty('placeOfPublication')
    publisher = atapi.ATFieldProperty('publisher')
    idBvb = atapi.ATFieldProperty('idBvb')
    searchresults = atapi.ATFieldProperty('searchresults')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Journal
    issn = atapi.ATFieldProperty('issn')
    titleJournal = atapi.ATFieldProperty('titleJournal')
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    volume = atapi.ATFieldProperty('volume')
    officialYearOfPublication = atapi.ATFieldProperty('officialYearOfPublication')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    volume = atapi.ATFieldProperty('volume')
    issue = atapi.ATFieldProperty('issue')

    # Reorder the fields as required
    ordered_fields = ["issn", "uri", "pdf", "doc", "review",
                      "customCitation", "reviewAuthorHonorific",
                      "reviewAuthorLastname", "reviewAuthorFirstname",
                      "reviewAuthorEmail", "authors",
                      "languagePresentation", "languageReview",
                      "referenceAuthors", "title", "subtitle",
                      "pageStart", "pageEnd", "titleJournal",
                      "shortnameJournal", "yearOfPublication",
                      "officialYearOfPublication", "volume", "issue",
                      "placeOfPublication", "publisher",
                      "description", "searchresults", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject",
                      "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Zs-Titel, Nummer, Heftnummer (gezähltes Jahr/Erscheinungsjahr),
    # Seite von/bis, URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of}: "+\
                        "{authors}, {title}, {subtitle}, {text_in}: "+\
                        "{shortnameJournal}, {volume}, {issue}, "+\
                        "({officialYearOfPublication}/"+\
                        "{yearOfPublication}), "+\
                        "Page(s) {pageStart}/{pageEnd}"

atapi.registerType(PresentationArticleReview, PROJECTNAME)
