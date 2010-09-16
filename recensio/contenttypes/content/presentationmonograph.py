#-*- coding: utf-8 -*-
"""Definition of the Presentation Monograph content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IPresentationMonograph

PresentationMonographSchema = BookReviewSchema.copy() + \
                              CoverPictureSchema.copy() + \
                              PagecountSchema.copy() + \
                              PresentationSchema.copy() + \
                              ReferenceAuthorsSchema.copy() + \
                              SerialSchema.copy() + \
                              atapi.Schema((
    atapi.TextField(
        'tableOfContents',
        schemata="presentation text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Table of contents of monograph you are presenting"),
            rows=9,
            ),
        ),

    DataGridField(
        'existingOnlineReviews',
        schemata=u"presentation",
        storage=atapi.AnnotationStorage(),
        required=True,
        columns=("name", "url"),
        widget=DataGridWidget(
            label = _(u"Existing online reviews"),
            description=_(
    u'description_existing_online_reviews',
    default=(u"Are there reviews on your text which are already available "
             "online?")
    ),
            columns = {"name" : Column(_(
    u"Name of journal/newspaper/yearbook")),
                       "url" : Column(_(u"URL")),
                       }
            ),
        ),
        atapi.StringField(
        'publishedReviews',
        schemata="presentation",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Published Reviews"),
            description=_(
    u'description_pubished_reviews',
    default=(u"Insert here the place of publication of reviews on your text "
             "that have already been published in print.")
    ),
            rows=3,
            ),
        ),
))

PresentationMonographSchema['title'].storage = atapi.AnnotationStorage()
PresentationMonographSchema['authors'].widget.label = _(
    u"Author(s) of presented monograph")
PresentationMonographSchema['authors'].widget.description = _(
    u'description_presentation_monograph_authors',
    default=u"Author(s) of presented monograph"
    )
PresentationMonographSchema["uri"].widget.description = _(
    u'description_presentation_uri',
    default=(u"Is the monograph you are presenting available free of "
             "charge online?")
    )
PresentationMonographSchema["coverPicture"].widget.label = _(
    u"Upload of cover picture")

finalize_recensio_schema(PresentationMonographSchema,
                         review_type="presentation")


class PresentationMonograph(BaseReview):
    """Presentation Monograph"""
    implements(IPresentationMonograph)

    meta_type = "PresentationMonograph"
    schema = PresentationMonographSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    languageReview = atapi.ATFieldProperty('languageReview')
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    tableOfContents = atapi.ATFieldProperty('tableOfContents')

    # Cover Picture
    coverPicture = atapi.ATFieldProperty('coverPicture')

    # Presentation
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Monograph
    existingOnlineReviews = atapi.ATFieldProperty('existingOnlineReviews')
    publishedReviews = atapi.ATFieldProperty('publishedReviews')

    # Reorder the fields as required
    ordered_fields = [
        # Presented text
        "isbn",
        "uri",
        "tableOfContents",
        "coverPicture",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "series",
        "seriesVol",
        "pages",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",

        # Presentation
        "review",
        "existingOnlineReviews",
        "publishedReviews", # Name, url 
        
        "reviewAuthorHonorific",
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "reviewAuthorEmail",
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved",
        ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "referenceAuthors",
                       "recensioID", "uri", "idBvb", "authors",
                       "title", "subtitle", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "pages", "isbn", "ddcSubject",
                       "ddcTime", "ddcPlace", "subject"]

    # Citation:
    # Präsentator, presentation of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: PresentationMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  (u"{reviewAuthorLastname}, {text_presentation_of} "
                          "{authors}, {title}, {subtitle}, "
                          "{placeOfPublication}: {yearOfPublication}, "
                          "{text_in} {publisher}, {series}, {seriesVol}"
                          "({yearOfPublication}), {text_pages} {pages}")

atapi.registerType(PresentationMonograph, PROJECTNAME)
