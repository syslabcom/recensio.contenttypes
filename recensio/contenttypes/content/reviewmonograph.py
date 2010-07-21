#-*- coding: utf-8 -*-
"""Definition of the Review Monograph content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.interfaces import IReviewMonograph
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import SerialSchema

ReviewMonographSchema = BookReviewSchema.copy() + \
                        CoverPictureSchema.copy() + \
                        PagecountSchema.copy() + \
                        SerialSchema.copy()

ReviewMonographSchema['title'].storage = atapi.AnnotationStorage()
ReviewMonographSchema['description'].storage = \
                                                       atapi.AnnotationStorage()
ReviewMonographSchema['yearOfPublication'].required = True

schemata.finalizeATCTSchema(ReviewMonographSchema,
                            moveDiscussion=False)

# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
ReviewMonographSchema.changeSchemataForField('subject', 'default')


class ReviewMonograph(BaseReview):
    """Review Monograph"""
    implements(IReviewMonograph)

    meta_type = "ReviewMonograph"
    schema = ReviewMonographSchema

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
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Cover Picture
    coverPicture = atapi.ATFieldProperty('coverPicture')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Reorder the fields as required for the edit view
    ordered_fields = ["isbn", "uri", "pdf", "doc", "review",
                      "customCitation", "coverPicture",
                      "reviewAuthorHonorific", "reviewAuthorLastname",
                      "reviewAuthorFirstname", "reviewAuthorEmail",
                      "authors", "languageReviewedText",
                      "languageReview", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "publisher", "series", "seriesVol", "pages",
                      "ddcTime", "ddcPlace", "ddcSubject", "subject",
                      "searchresults", "description"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "recensioID",
                       "searchresults", "idBvb", "authors", "title",
                       "subtitle", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "pages", "isbn", "ddcSubject",
                       "ddcTime", "ddcPlace", "subject"]

    #  Rezensent, review of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: ReviewMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  u"{reviewAuthorLastname}, {text_review_of}: "+\
                        "{authors}, {title}, {subtitle}, {text_in}: "+\
                        "{placeOfPublication}: {yearOfPublication}, "+\
                        "{text_in}: {publisher}, {series}, {seriesVol}"+\
                        "({yearOfPublication}), Pages {pages}"

atapi.registerType(ReviewMonograph, PROJECTNAME)
