"""Definition of the Praesentationen von Aufsatz in Zeitschrift content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import \
     IPresentationArticleReview
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import SeitenzahlSchema



PresentationArticleReviewSchema = \
                                             JournalReviewSchema.copy() + \
                                             BezugsautorenSchema.copy() + \
                                             InternetSchema.copy() + \
                                             SeitenzahlSchema.copy()

PresentationArticleReviewSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationArticleReviewSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationArticleReviewSchema,
                            moveDiscussion=False)


class PresentationArticleReview(BaseReview):
    """Praesentationen von Aufsatz in Zeitschrift"""
    implements(IPresentationArticleReview)

    meta_type = "PresentationArticleReview"
    schema = PresentationArticleReviewSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Journal = Printed + Authors +
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

    # Journal
    issn = atapi.ATFieldProperty('issn')
    number = atapi.ATFieldProperty('number') 
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    volume = atapi.ATFieldProperty('volume')
    officialYearOfPublication = atapi.ATFieldProperty('officialYearOfPublication')

    # Bezugsautoren
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Seitenzahl
    pages = atapi.ATFieldProperty('pages')

    # Reorder the fields as required

    ordered_fields = ["recensioID", "authors", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "pages", "description",
                      "languagePresentation",
                      "languageReview", "issn",
                      "publisher", "idBvb", "searchresults",
                      "referenceAuthors", "reviewAuthor", "number",
                      "shortnameJournal", "volume",
                      "officialYearOfPublication", "url", "ddcPlace", "ddcSubject",
                      "ddcTime", "subject", "pdf", "doc",
                      "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(PresentationArticleReview, PROJECTNAME)
