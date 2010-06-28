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

RevieweinerZeitschriftSchema = JournalReviewSchema.copy() + atapi.Schema((
    atapi.StringField(
        'herausgeber',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Herausgeber"),
            ),
        ),
))

RevieweinerZeitschriftSchema['title'].storage = atapi.AnnotationStorage()
RevieweinerZeitschriftSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RevieweinerZeitschriftSchema,
                            moveDiscussion=False)


class RevieweinerZeitschrift(BaseReview):
    """Review einer Zeitschrift"""
    implements(IReviewJournal)

    meta_type = "RevieweinerZeitschrift"
    schema = RevieweinerZeitschriftSchema

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
    yearOfPublication = atapi.ATFieldProperty('yearOfPublication')
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

    # RevieweinerZeitschrift
    herausgeber = atapi.ATFieldProperty('herausgeber')

    # Reorder the fields as required

    ordered_fields = ["recensioID", "authors", "herausgeber", "title",
                      "subtitle", "yearOfPublication",
                      "yearOfPublication", "description",
                      "languagePresentation",
                      "languageReview", "issn",
                      "publisher", "idBvb", "searchresults",
                      "number", "shortnameJournal", "volume",
                      "reviewAuthor", "officialYearOfPublication", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(RevieweinerZeitschrift, PROJECTNAME)
