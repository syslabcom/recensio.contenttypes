"""Definition of the Review einer Monographie content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.interfaces import IReviewMonograph
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import SerialSchema

RevieweinerMonographieSchema = BookReviewSchema.copy() + \
                                  SerialSchema.copy()

schemata.finalizeATCTSchema(RevieweinerMonographieSchema,
                            moveDiscussion=False)

RevieweinerMonographieSchema['title'].storage = atapi.AnnotationStorage()
RevieweinerMonographieSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

RevieweinerMonographieSchema['yearOfPublication'].required = True


class RevieweinerMonographie(BaseReview):
    """Review einer Monographie"""
    implements(IReviewMonograph)

    meta_type = "RevieweinerMonographie"
    schema = RevieweinerMonographieSchema

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
    placeOfPublication = atapi.ATFieldProperty('placeOfPublication')
    publisher = atapi.ATFieldProperty('publisher')
    idBvb = atapi.ATFieldProperty('idBvb')
    searchresults = atapi.ATFieldProperty('searchresults')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "authors", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "description",
                      "languageReview",
                      "languagePresentation", "isbn", "publisher",
                      "idBvb", "searchresults", "series",
                      "seriesVol", "reviewAuthor", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(RevieweinerMonographie, PROJECTNAME)
