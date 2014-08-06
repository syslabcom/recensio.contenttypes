#-*- coding: utf-8 -*-
"""Definition of the Review Monograph content type
"""

from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Archetypes import atapi

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import (
    BaseReview, BaseReviewNoMagic)
from recensio.contenttypes.content.schemata import (
    BookReviewSchema, CoverPictureSchema, EditorialSchema,
    PageStartEndInPDFSchema, PageStartEndOfReviewInJournalSchema,
    PagecountSchema, ReviewSchema, SerialSchema,
    finalize_recensio_schema)
from recensio.contenttypes.interfaces import IReviewMonograph
from recensio.contenttypes.interfaces import IMetadataFormat
from recensio.theme.browser.views import editorTypes


ReviewMonographSchema = BookReviewSchema.copy() + \
                        CoverPictureSchema.copy() + \
                        EditorialSchema.copy() + \
                        PageStartEndInPDFSchema.copy() + \
                        PageStartEndOfReviewInJournalSchema.copy() + \
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
    reviewAuthors = atapi.ATFieldProperty('reviewAuthors')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    customCitation = atapi.ATFieldProperty('customCitation')
    canonical_uri = atapi.ATFieldProperty('canonical_uri')
    uri = atapi.ATFieldProperty('uri')
    urn = atapi.ATFieldProperty('urn')

    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    #Editorial
    editorial = atapi.ATFieldProperty('editorial')

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

    #PageStartEndOfReviewInJournal
    pageStartOfReviewInJournal = atapi.ATFieldProperty(
        'pageStartOfReviewInJournal')
    pageEndOfReviewInJournal = atapi.ATFieldProperty(
        'pageEndOfReviewInJournal')

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
        'help_authors_or_editors',
        "authors",
        "editorial",
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
        "reviewAuthors",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "pageStartOfReviewInJournal",
        "pageEndOfReviewInJournal",
        "doc",
        "review",
        "customCitation",
        "canonical_uri",
        "urn",
        "bv",
    ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = [
        "metadata_review_type_code", "get_journal_title",
        "metadata_start_end_pages", "metadata_review_author",
        "languageReview", "languageReviewedText", "authors",
        "editorial", "title", "subtitle", "yearOfPublication",
        "placeOfPublication", "publisher", "series", "seriesVol",
        "pages", "isbn", "urn", "ddcSubject", "ddcTime", "ddcPlace",
        "subject", "canonical_uri", "metadata_recensioID", "idBvb"]

    def editorTypes(self):
        return editorTypes()

    def get_publication_title(self):
        """ Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    get_journal_title = get_publication_title #2542

    def get_publication_object(self):
        return self.get_parent_object_of_type("Publication")

    def get_volume_title(self):
        """ Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """ Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

    def getDecoratedTitle(self, lastname_first=False):
        metadata_format = getMultiAdapter((self, self.REQUEST), IMetadataFormat)
        return metadata_format.getDecoratedTitle(self, lastname_first)

    def get_citation_string(self):
        metadata_format = getMultiAdapter((self, self.REQUEST), IMetadataFormat)
        return metadata_format.get_citation_string(self)

    def getLicense(self):
        return ReviewMonographNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewMonographNoMagic(self).getFirstPublicationData()


class ReviewMonographNoMagic(BaseReviewNoMagic):
    pass


atapi.registerType(ReviewMonograph, PROJECTNAME)
