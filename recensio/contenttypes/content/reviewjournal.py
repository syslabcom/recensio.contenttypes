"""Definition of the Review einer Zeitschrift content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IReviewJournal
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import JournalReviewSchema

ReviewJournalSchema = JournalReviewSchema.copy() + atapi.Schema((
    atapi.StringField(
        'herausgeber',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Herausgeber"),
            ),
        ),
))

ReviewJournalSchema['title'].storage = atapi.AnnotationStorage()
ReviewJournalSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ReviewJournalSchema,
                            moveDiscussion=False)


class ReviewJournal(BaseReview):
    """Review einer Zeitschrift"""
    implements(IReviewJournal)

    meta_type = "ReviewJournal"
    schema = ReviewJournalSchema

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

    # ReviewJournal
    herausgeber = atapi.ATFieldProperty('herausgeber')

    # Reorder the fields as required

    ordered_fields = ["recensioID", "authors", "herausgeber", "title",
                      "subtitle", "yearOfPublication",
                      "placeOfPublication", "description",
                      "languagePresentation",
                      "languageReview", "issn",
                      "publisher", "idBvb", "searchresults",
                      "number", "shortnameJournal", "volume",
                      "reviewAuthor", "officialYearOfPublication", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(ReviewJournal, PROJECTNAME)
