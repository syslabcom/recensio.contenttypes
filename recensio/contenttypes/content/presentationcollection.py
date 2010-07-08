"""Definition of the Presentation Collection content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import \
     IPresentationCollection
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes import contenttypesMessageFactory as _

PresentationCollectionSchema = BookReviewSchema.copy() + \
                               PresentationSchema.copy() + \
                               ReferenceAuthorsSchema.copy() + \
                               InternetSchema.copy() + \
                               SerialSchema.copy() + \
                               atapi.Schema((
    atapi.LinesField(
        'editorCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.LinesWidget(
            label=_(u"Editor Collected Edition"),
            rows=3,
            ),
        ),
))

PresentationCollectionSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationCollectionSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationCollectionSchema,
                            moveDiscussion=False)


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
    reviewAuthor = atapi.ATFieldProperty('reviewAuthor')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languagePresentation = atapi.ATFieldProperty('languagePresentation')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    def getPdf(self, *args, **kwargs):
        import pdb;pdb.set_trace()
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

    # Serial = Seitenzahl +
    # Seitenzahl
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Collection
    editorCollectedEdition = atapi.ATFieldProperty('editorCollectedEdition')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "authors",
                      "editorCollectedEdition", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "pages", "description", "languagePresentation",
                      "languageReview", "isbn", "publisher", "idBvb",
                      "searchresults", "referenceAuthors", "series",
                      "seriesVol", "reviewAuthor", "url", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "urn", "review", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(PresentationCollection, PROJECTNAME)
