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

from recensio.contenttypes.content.schemata import AuthorsSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.interfaces import IPresentationArticleReview


PresentationArticleReviewSchema = \
                                AuthorsSchema.copy() + \
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

PresentationArticleReviewSchema['title'].storage = atapi.AnnotationStorage()

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
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    review = atapi.ATFieldProperty('review')
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

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Journal
    issn = atapi.ATFieldProperty('issn')
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    officialYearOfPublication = \
                              atapi.ATFieldProperty('officialYearOfPublication')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    titleJournal = atapi.ATFieldProperty('titleJournal')
    volume = atapi.ATFieldProperty('volume')
    issue = atapi.ATFieldProperty('issue')

    # Reorder the fields as required
    ordered_fields = [
        # Presented Text
        "issn",
        "uri",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "pageStart",
        "pageEnd",
        "titleJournal",
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volume",
        "issue",
        "placeOfPublication",
        "publisher",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        
        # Presentation
        "review",
        "reviewAuthorHonorific",
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "reviewAuthorEmail",
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "referenceAuthors",
                       "recensioID", "uri", "authors", "title",
                       "subtitle", "pageStart", "pageEnd",
                       "titleJournal", "shortnameJournal",
                       "yearOfPublication",
                       "officialYearOfPublication", "volume", "issue",
                       "placeOfPublication", "publisher", "issn",
                       "ddcSubject", "ddcTime", "ddcPlace", "subject"]

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Zs-Titel, Nummer, Heftnummer (gezähltes Jahr/Erscheinungsjahr),
    # Seite von/bis, URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of} "+\
                        "{authors}, {title}, {subtitle}, {text_in} "+\
                        "{shortnameJournal}, {volume}, {issue}, "+\
                        "({officialYearOfPublication}/"+\
                        "{yearOfPublication}), "+\
                        "Page(s) {pageStart}/{pageEnd}"


atapi.registerType(PresentationArticleReview, PROJECTNAME)

