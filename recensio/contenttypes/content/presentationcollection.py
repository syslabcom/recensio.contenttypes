# -*- coding: utf-8 -*-
"""Definition of the Presentation Collection content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import \
     IPresentationCollection
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes import contenttypesMessageFactory as _

PresentationCollectionSchema = BookReviewSchema.copy() + \
                               PresentationSchema.copy() + \
                               ReferenceAuthorsSchema.copy() + \
                               InternetSchema.copy() + \
                               PageStartEndSchema.copy() + \
                               SerialSchema.copy() + \
                               atapi.Schema((
    atapi.LinesField(
        'editorCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.LinesWidget(
            label=_(u"Editor Collected Edition"),
            rows=3,
            ),
        ),
))

PresentationCollectionSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationCollectionSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationCollectionSchema,
                            moveDiscussion=False)


class PresentationCollection(BaseReview):
    """Presentation Collection"""
    implements(IPresentationCollection)

    meta_type = "PresentationCollection"
    schema = PresentationCollectionSchema

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
    def getPdf(self, *args, **kwargs):
        return None
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Serial = PageStartEnd +
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Collection
    editorCollectedEdition = atapi.ATFieldProperty('editorCollectedEdition')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "authors",
                      "editorCollectedEdition", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "pageStart", "pageEnd", "description",
                      "languagePresentation", "languageReview",
                      "isbn", "publisher", "idBvb", "searchresults",
                      "referenceAuthors", "series", "seriesVol",
                      "reviewAuthor", "url", "ddcPlace", "ddcSubject",
                      "ddcTime", "subject", "pdf", "doc", "urn",
                      "review", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    def get_citation_string(self):
        """
        Präsentator, presentation of: Autor, Titel. Untertitel, in:
        Zs-Titel, Nummer, Heftnummer (gezähltes
        Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.
        """
        template = u"%(reviewAuthor)s, review of: %(shortnameJournal)s,"+\
                   u"%(volume)s, %(number)s, "+\
                   u"(%(yearOfPublication)s/%(officialYearOfPublication)s,"+\
                   u"%(absolute_url)s"
        citation_dict = {}
        citation_dict["reviewAuthor"] = self.getReviewAuthor()
        citation_dict["shortnameJournal"] = self.getShortnameJournal()
        citation_dict["volume"] = self.getVolume()
        citation_dict["number"] = self.getNumber()
        citation_dict["yearOfPublication"] = self.getYearOfPublication()
        citation_dict["officialYearOfPublication"] = \
                                             self.getOfficialYearOfPublication()
        citation_dict["absolute_url"] = self.absolute_url()
        return template % citation_dict


atapi.registerType(PresentationCollection, PROJECTNAME)
