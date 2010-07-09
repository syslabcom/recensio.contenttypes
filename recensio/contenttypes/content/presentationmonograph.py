#-*- coding: utf-8 -*-
"""Definition of the Presentation Monograph content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IPresentationMonograph
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema

PresentationMonographSchema = BookReviewSchema.copy() + \
                              InternetSchema.copy() + \
                              PagecountSchema.copy() + \
                              PresentationSchema.copy() + \
                              ReferenceAuthorsSchema.copy() + \
                              SerialSchema.copy()

PresentationMonographSchema['title'].storage = atapi.AnnotationStorage()
PresentationMonographSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationMonographSchema,
                            moveDiscussion=False)


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
    reviewAuthor = atapi.ATFieldProperty('reviewAuthor')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languagePresentation = atapi.ATFieldProperty('languagePresentation')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "title", "subtitle",
                      "reviewAuthor", "yearOfPublication",
                      "placeOfPublication", "description",
                      "languagePresentation", "languageReview",
                      "isbn", "publisher", "pages", "idBvb",
                      "searchresults", "referenceAuthors", "series",
                      "seriesVol", "url", "ddcPlace", "ddcSubject",
                      "ddcTime", "subject", "pdf", "doc", "urn",
                      "review", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Präsentator, presentation of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: PresentationMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  u"{reviewAuthor}, {text_presentation_of}: "+\
                        "{authors}, {title}, {subtitle}, {text_in}: "+\
                        "{placeOfPublication}: {yearOfPublication}, "+\
                        "{text_in}: {publisher}, {series}, {seriesVol}"+\
                        "({yearOfPublication}), Pages {pages}"

atapi.registerType(PresentationMonograph, PROJECTNAME)
