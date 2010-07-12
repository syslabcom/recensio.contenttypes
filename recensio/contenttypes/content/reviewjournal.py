# -*- coding: utf-8 -*-
"""Definition of the Review Journal content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.interfaces import IReviewJournal

ReviewJournalSchema = JournalReviewSchema.copy() + atapi.Schema((
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

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Journal
    issn = atapi.ATFieldProperty('issn')
    officialYearOfPublication = atapi.ATFieldProperty('officialYearOfPublication')

    # ReviewJournal
    editor = atapi.ATFieldProperty('editor')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "authors", "editor", "title",
                      "subtitle", "yearOfPublication",
                      "placeOfPublication", "description",
                      "languagePresentation", "languageReview",
                      "issn", "publisher", "idBvb", "searchresults",
                      "reviewAuthorHonorific", "reviewAuthorLastname",
                      "reviewAuthorFirstname", "reviewAuthorEmail",
                      "officialYearOfPublication", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "urn", "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Rezensent, review of: Zs-Titel, Nummer, Heftnummer (gezähltes
    # Jahr/Erscheinungsjahr), in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio

    # NOTE: No pages
    citation_template =  u"{reviewAuthorLastname}, {text_review_of}: "+\
                        "{get_volume_title}, {get_issue_title}, "+\
                        "({officialYearOfPublication}/"+\
                        "{yearOfPublication}), {text_in}: "+\
                        "{reviewAuthorLastname}, {text_review_of}: "+\
                        "{get_volume_title}, {get_issue_title}, "+\
                        "({officialYearOfPublication}/"+\
                        "{yearOfPublication})"


    def get_title_from_parent_of_type(self, meta_type):
        """
        Return the title of the first object of a particular type
        which is a parent of the current object.
        """
        title = ""
        parents = self.REQUEST.PARENTS
        for parent in parents:
            if parent.meta_type == meta_type:
                title = parent.Title()
                break
        return title

    def get_publication_title(self):
        """ Equivalent of 'shortnameJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    def get_volume_title(self):
        """ Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """ Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

atapi.registerType(ReviewJournal, PROJECTNAME)
