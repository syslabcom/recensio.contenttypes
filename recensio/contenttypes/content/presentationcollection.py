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
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes import contenttypesMessageFactory as _

PresentationCollectionSchema = BookReviewSchema.copy() + \
                               PresentationSchema.copy() + \
                               ReferenceAuthorsSchema.copy() + \
                               InternetSchema.copy() + \
                               PageStartEndSchema.copy() + \
                               SerialSchema.copy() + \
                               atapi.Schema((
    atapi.StringField(
        'titleCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title Collected Edition"),
            rows=3,
            ),
        ),

    DataGridField(
        'editorsCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        columns=("lastname", "firstname"),
        widget=DataGridWidget(
            label = _(u"Editor(s) Collected Edition"),
            columns = {"lastname" : Column(_(u"Lastname")),
                       "firstname" : Column(_(u"Firstname")),
                       }
            ),
        ),
))

PresentationCollectionSchema['title'].storage = atapi.AnnotationStorage()
PresentationCollectionSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationCollectionSchema,
                            moveDiscussion=False)

# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
PresentationCollectionSchema.changeSchemataForField('subject', 'default')


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
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languagePresentation = atapi.ATFieldProperty('languagePresentation')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    def getPdf(self, *args, **kwargs):
        return None
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    urn = atapi.ATFieldProperty('urn')


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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Serial = PageStartEnd +
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Collection
    titleCollectedEdition = atapi.ATFieldProperty('titleCollectedEdition')
    editorsCollectedEdition = atapi.ATFieldProperty('editorsCollectedEdition')

    # Reorder the fields as required
    ordered_fields = ["isbn", "url", "urn", "pdf", "doc", "review",
                      "reviewAuthorHonorific", "reviewAuthorLastname",
                      "reviewAuthorFirstname", "reviewAuthorEmail",
                      "authors", "languagePresentation",
                      "languageReview", "referenceAuthors", "title",
                      "subtitle", "pageStart", "pageEnd", "titleCollectedEdition",
                      "editorsCollectedEdition", "yearOfPublication",
                      "placeOfPublication", "publisher", "series",
                      "seriesVol", "ddcSubject", "ddcTime",
                      "ddcPlace", "subject", "searchresults",
                      "description", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Herausgeber, Titel. Untertitel, Erscheinungsort: Verlag Jahr,
    # URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of}: "+\
                        "{authors}, {title}, {subtitle}, {text_in}: "+\
                        "{editorsCollectedEdition}, "+\
                        "{title}, {subtitle}, {text_in}: "+\
                        "{placeOfPublication}: {publisher} "+\
                        "{yearOfPublication}"

atapi.registerType(PresentationCollection, PROJECTNAME)
