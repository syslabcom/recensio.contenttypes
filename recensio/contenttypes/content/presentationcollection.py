# -*- coding: utf-8 -*-
"""Definition of the Presentation Collection content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from recensio.contenttypes.interfaces import \
     IPresentationCollection
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema

PresentationCollectionSchema = BookReviewSchema.copy() + \
                               PagecountSchema.copy() + \
                               PresentationSchema.copy() + \
                               ReferenceAuthorsSchema.copy() + \
                               PageStartEndSchema.copy() + \
                               SerialSchema.copy() + \
                               atapi.Schema((
    atapi.StringField(
        'titleCollectedEdition',
        schemata=_(u"presented text"),
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title / Subtitle"),
            description=_(
    u'description_title_collected_edition',
    default=u"Information on the associated edited volume"
    ),
            ),
        ),

    DataGridField(
        'editorsCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        columns=("lastname", "firstname"),
        widget=DataGridWidget(
            label = _(u"Editor(s)"),
            columns = {"lastname" : Column(_(u"Last name")),
                       "firstname" : Column(_(u"First name")),
                       }
            ),
        ),
))

PresentationCollectionSchema['title'].storage = atapi.AnnotationStorage()
PresentationCollectionSchema["authors"].widget.label=_(
    "label_presentation_collection_authors",
    default=u"Author(s) of presented article")
PresentationCollectionSchema["referenceAuthors"].widget.description = _(
    u'description_reference_authors',
    default=(u"Which scholarly author's work have you mainly engaged with in "
             "your article? Please give us the most detailed information "
             "possible on the &raquo;contemporary&laquo; names amongst them as "
             "the recensio.net editorial team will usually try to inform these "
             "authors of the existence of your article, your presentation, "
             "and the chance to comment on it. Only the reference author's "
             "name will be visible to the public. Please name historical "
             "reference authors (e.g. Aristotle, Charles de Gaulle) further "
             "below as subject heading.")
    )

finalize_recensio_schema(PresentationCollectionSchema,
                         review_type="presentation")

class PresentationCollection(BaseReview):
    """Presentation Collection"""
    implements(IPresentationCollection)

    meta_type = "PresentationCollection"
    schema = PresentationCollectionSchema

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
    reviewAuthorPersonalUrl = atapi.ATFieldProperty('reviewAuthorPersonalUrl')
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Serial = PageStartEnd +
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Collection
    titleCollectedEdition = atapi.ATFieldProperty('titleCollectedEdition')
    editorsCollectedEdition = atapi.ATFieldProperty('editorsCollectedEdition')

    # Reorder the fields as required
    ordered_fields = [
        # Presented Text
        "isbn",
        "uri",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "pageStart",
        "pageEnd",
        "titleCollectedEdition",
        "editorsCollectedEdition",
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
        "idBvb",

        # Presentation
        "review",
        'reviewAuthorPersonalUrl',
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
                       "recensioID", "uri", "idBvb", "authors",
                       "title", "subtitle", "pageStart", "pageEnd",
                       "editorsCollectedEdition",
                       "titleCollectedEdition", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "isbn", "ddcSubject", "ddcTime",
                       "ddcPlace", "subject"]

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Herausgeber, Titel. Untertitel, Erscheinungsort: Verlag Jahr,
    # URL recensio.
    citation_template =  (u"{reviewAuthorLastname}, {text_presentation_of} "
                          "{authors}, {title}, {subtitle}, {text_in} "
                          "{editorsCollectedEdition}, "
                          "{title}, {subtitle}, "
                          "{placeOfPublication}: {publisher} "
                          "{yearOfPublication}")

atapi.registerType(PresentationCollection, PROJECTNAME)
