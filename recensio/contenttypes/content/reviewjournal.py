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
ReviewJournalSchema['shortnameJournal'].widget.label = _(u"Short name (journal)")

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

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Journal
    issn = atapi.ATFieldProperty('issn')
    number = atapi.ATFieldProperty('number') 
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    officialYearOfPublication = atapi.ATFieldProperty('officialYearOfPublication')

    # ReviewJournal
    editor = atapi.ATFieldProperty('editor')

    # Reorder the fields as required

    ordered_fields = ["recensioID", "authors", "editor", "title",
                      "subtitle", "yearOfPublication",
                      "placeOfPublication", "description",
                      "languagePresentation",
                      "languageReview", "issn",
                      "publisher", "idBvb", "searchresults",
                      "number", "shortnameJournal",
                      "reviewAuthor", "officialYearOfPublication", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "urn", "review"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    def get_publication_title(self):
        """
        Get the "Title (Journal)" from containing Publication Title
        """
        publication_title = ""
        parents = self.REQUEST.PARENTS
        for parent in parents:
            if parent.meta_type == "Publication":
                publication_title = parent.Title()
                break
        return publication_title

    def get_volume_title(self):
        """
        Get the "Volume Title" from containing Volume Title
        """
        volume_title = ""
        parents = self.REQUEST.PARENTS
        for parent in parents:
            if parent.meta_type == "Volume":
                volume_title = parent.Title()
                break
        return volume_title

atapi.registerType(ReviewJournal, PROJECTNAME)
