"""Definition of the Praesentation von Aufsatz in Sammelband content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import \
     IPresentationCollection
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes import contenttypesMessageFactory as _

PraesentationvonAufsatzinSammelbandSchema = BookReviewSchema.copy() + \
                                            BezugsautorenSchema.copy() + \
                                            InternetSchema.copy() + \
                                            SerialSchema.copy() + \
                                            atapi.Schema((
    atapi.LinesField(
        'herausgeberSammelband',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.LinesWidget(
            label=_(u"Herausgeber Sammelband"),
            rows=3,
            ),
        ),
))

PraesentationvonAufsatzinSammelbandSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationvonAufsatzinSammelbandSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationvonAufsatzinSammelbandSchema,
                            moveDiscussion=False)


class PraesentationvonAufsatzinSammelband(BaseReview):
    """Praesentation von Aufsatz in Sammelband"""
    implements(IPresentationCollection)

    meta_type = "PraesentationvonAufsatzinSammelband"
    schema = PraesentationvonAufsatzinSammelbandSchema

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
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')

    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    # Printed
    subtitle = atapi.ATFieldProperty('subtitle')
    yearOfPublication = atapi.ATFieldProperty('yearOfPublication')
    yearOfPublication = atapi.ATFieldProperty('yearOfPublication')
    publisher = atapi.ATFieldProperty('publisher')
    idBvb = atapi.ATFieldProperty('idBvb')
    searchresults = atapi.ATFieldProperty('searchresults')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Bezugsautoren
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Serial = Seitenzahl +
    # Seitenzahl
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Praesentation von Aufsatz in Sammelband
    herausgeberSammelband = atapi.ATFieldProperty('herausgeberSammelband')

    # Reorder the fields as required

    ordered_fields = ["recensioID", "authors",
                      "herausgeberSammelband", "title", "subtitle",
                      "yearOfPublication", "yearOfPublication",
                      "pages", "description",
                      "languagePresentation",
                      "languageReview", "isbn",
                      "publisher", "idBvb", "searchresults",
                      "referenceAuthors", "series", "seriesVol",
                      "reviewAuthor", "url", "ddcPlace", "ddcSubject",
                      "ddcTime", "subject", "pdf", "doc",
                      "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(PraesentationvonAufsatzinSammelband, PROJECTNAME)
