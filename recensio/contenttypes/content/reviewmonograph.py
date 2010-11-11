#-*- coding: utf-8 -*-
"""Definition of the Review Monograph content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IReviewMonograph
from recensio.contenttypes.citation import getFormatter


ReviewMonographSchema = BookReviewSchema.copy() + \
                        CoverPictureSchema.copy() + \
                        PageStartEndSchema.copy() + \
                        PagecountSchema.copy() + \
                        ReviewSchema.copy() + \
                        SerialSchema.copy()

ReviewMonographSchema['title'].storage = atapi.AnnotationStorage()
ReviewMonographSchema['yearOfPublication'].required = True
finalize_recensio_schema(ReviewMonographSchema)


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
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
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

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Cover Picture
    coverPicture = atapi.ATFieldProperty('coverPicture')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Reorder the fields as required for the edit view
    ordered_fields = [
        # Reviewed Text schemata
        "isbn",
        "languageReviewedText",
        "authors",
        "title",
        "subtitle",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "series",
        "seriesVol",
        "pages",
        "coverPicture",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",

        # Review schemata
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "doc",
        "review",
        "customCitation",
        "uri",
        ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "recensioID", "idBvb",
                       "authors", "title", "subtitle",
                       "yearOfPublication", "placeOfPublication",
                       "publisher", "series", "seriesVol", "pages",
                       "isbn", "ddcSubject", "ddcTime", "ddcPlace",
                       "subject"]

    #  Rezensent, review of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: ReviewMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  (u"{reviewAuthorLastname}, {text_review_of} "
                          "{authors}, {title}, {subtitle}, "
                          "{placeOfPublication}: {yearOfPublication}, "
                          "{text_in} {publisher}, {series}, {seriesVol}"
                          "({yearOfPublication}), Pages {pages}")

    def get_publication_title(self):
        """ Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    def get_publication_object(self):
        return self.get_parent_object_of_type("Publication")

    def get_volume_title(self):
        """ Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """ Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

    def get_citation_string(self):
        """
        Either return the custom citation or the generated one
        """
        if self.get('customCitation'):
            return scrubHTML(self.customCitation)
        rezensent = getFormatter(', ')
        item = getFormatter(', ', '. ', ', ', ': ', ', ')
        mag_number_and_year = getFormatter(', ', ', ', ' ')
        full_citation_inner = getFormatter(': review of: ', ', in: ', ', ')
        rezensent_string = rezensent(self.reviewAuthorLastname, \
                                     self.reviewAuthorFirstname)
        authors_string = ', '.join([' / '.join((x['lastname'], x['firstname']))
                                    for x in self.authors])
        item_string = item(authors_string,
                           self.title,
                           self.subtitle,
                           self.placeOfPublication,
                           self.publisher,
                           self.yearOfPublication)
        mag_year_string = self.yearOfPublication
        mag_year_string = mag_year_string and '(' + mag_year_string + ')' \
            or None
        mag_number_and_year_string = mag_number_and_year(\
            self.get_publication_title(), \
            self.get_volume_title(), self.get_issue_title(), mag_year_string)
        return full_citation_inner(rezensent_string, item_string, \
            mag_number_and_year_string, self.absolute_url())

    def getDecoratedTitle(self):
        authors_string = ' / '.join([' '.join((x['firstname'], x['lastname']))
             for x in self.authors])
        titles_string = '. '.join((self.title, self.subtitle))
        rezensent_string = ' '.join((self.reviewAuthorFirstname, \
                                     self.reviewAuthorLastname))
        rezensent_string = rezensent_string and "(reviewed by " + rezensent_string + ")" or ""
        full_citation = getFormatter(': ', ' ')
        return full_citation(authors_string, titles_string, rezensent_string)
atapi.registerType(ReviewMonograph, PROJECTNAME)
