"""Definition of the Praesentationen von Monographien content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IPresentationMonograph
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema

PraesentationenvonMonographienSchema = BookReviewSchema.copy() + \
                                       BezugsautorenSchema.copy() + \
                                       InternetSchema.copy()


PraesentationenvonMonographienSchema['title'].storage = \
                                                      atapi.AnnotationStorage()
PraesentationenvonMonographienSchema['description'].storage = \
                                                      atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonMonographienSchema,
                            moveDiscussion=False)


class PraesentationenvonMonographien(BaseReview):
    """Praesentationen von Monographien"""
    implements(IPresentationMonograph)

    meta_type = "PraesentationenvonMonographien"
    schema = PraesentationenvonMonographienSchema

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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Bezugsautoren
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "title", "subtitle",
                      "reviewAuthor", "yearOfPublication",
                      "yearOfPublication", "description",
                      "languagePresentation",
                      "languageReview", "isbn",
                      "publisher", "idBvb", "searchresults",
                      "referenceAuthors", "url", "ddcPlace", "ddcSubject",
                      "ddcTime", "subject", "pdf", "doc",
                      "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(PraesentationenvonMonographien, PROJECTNAME)