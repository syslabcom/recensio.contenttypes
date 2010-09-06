# -*- coding: utf-8 -*-
"""Definition of the Review Journal content type
"""

from zope.interface import implements
import Acquisition

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFPlone.Portal import PloneSite

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.interfaces import IReviewJournal

ReviewJournalSchema = JournalReviewSchema.copy() + \
                      PageStartEndSchema.copy() + \
                      atapi.Schema((
    atapi.StringField(
        'editor',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Editor"),
            ),
        ),
))

ReviewJournalSchema['title'].storage = atapi.AnnotationStorage()
ReviewJournalSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ReviewJournalSchema,
                            moveDiscussion=False)
# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
ReviewJournalSchema.changeSchemataForField('subject', 'default')

class ReviewJournal(BaseReview):
    """Review Journal"""
    implements(IReviewJournal)

    meta_type = "ReviewJournal"
    schema = ReviewJournalSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Journal = Printed + Authors +
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

    # Journal
    issn = atapi.ATFieldProperty('issn')
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    officialYearOfPublication = \
                              atapi.ATFieldProperty('officialYearOfPublication')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # ReviewJournal
    editor = atapi.ATFieldProperty('editor')


    # Reorder the fields as required
    ordered_fields = ["coverPicture", "issn", "uri", "pdf", "doc", "review",
                      "customCitation", "reviewAuthorHonorific",
                      "reviewAuthorLastname", "reviewAuthorFirstname",
                      "reviewAuthorEmail", "authors",
                      "languageReviewedText", "languageReview",
                      "editor", "title", "subtitle", "pageStart",
                      "pageEnd", "yearOfPublication",
                      "officialYearOfPublication",
                      "placeOfPublication", "publisher",
                      "description", "searchresults", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "recensioID",
                       "searchresults", "idBvb", "editor",
                       "get_publication_title", "shortnameJournal",
                       "yearOfPublication",
                       "officialYearOfPublication",
                       "get_volume_title", "get_issue_title",
                       "placeOfPublication", "publisher", "issn",
                       "ddcSubject", "ddcTime", "ddcPlace", "subject"]

    # Rezensent, review of: Zs-Titel, Nummer, Heftnummer (gezähltes
    # Jahr/Erscheinungsjahr), in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio
    citation_template =  (u"{reviewAuthorLastname}, {text_review_of} "
                          "{get_publication_title}, {get_volume_title},"
                          "{get_issue_title}, "
                          "({officialYearOfPublication}/{yearOfPublication}), "
                          "{text_in} "
                          "{get_publication_title}, {get_volume_title}, "
                          "{get_issue_title}, ({officialYearOfPublication}/"
                          "{yearOfPublication}) {text_pages} "
                          "{pageStart}/{pageEnd}")

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

atapi.registerType(ReviewJournal, PROJECTNAME)
