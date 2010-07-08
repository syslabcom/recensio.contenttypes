# -*- coding: utf-8 -*-
"""Definition of the Presentation Article Review content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.interfaces import IPresentationArticleReview


PresentationArticleReviewSchema = \
                                JournalReviewSchema.copy() + \
                                PresentationSchema.copy() + \
                                ReferenceAuthorsSchema.copy() + \
                                InternetSchema.copy() + \
                                PageStartEndSchema.copy() + \
                                atapi.Schema((
    atapi.StringField(
        'volume',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Volume"),
            ),
        ),
    atapi.StringField(
        'issue',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Issue"),
            ),
        ),
    atapi.StringField(
        'shortnameJournal',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Shortname (Journal)"),
            ),
        ),
))

PresentationArticleReviewSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationArticleReviewSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationArticleReviewSchema,
                            moveDiscussion=False)


class PresentationArticleReview(BaseReview):
    """Presentation Article Review"""
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
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    volume = atapi.ATFieldProperty('volume')
    officialYearOfPublication = atapi.ATFieldProperty('officialYearOfPublication')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Internet
    url = atapi.ATFieldProperty('url')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    volume = atapi.ATFieldProperty('volume')
    issue = atapi.ATFieldProperty('issue')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "authors", "title", "subtitle",
                      "yearOfPublication", "placeOfPublication",
                      "pageStart", "pageEnd", "description",
                      "languagePresentation", "languageReview",
                      "issn", "publisher", "idBvb", "searchresults",
                      "referenceAuthors", "reviewAuthor",
                      "shortnameJournal", "volume", "issue",
                      "officialYearOfPublication", "url", "ddcPlace",
                      "ddcSubject", "ddcTime", "subject", "pdf",
                      "doc", "urn", "review", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    def get_citation_string(self):
        """
        Präsentator, presentation of: Autor, Titel. Untertitel, in:
        Zs-Titel, Nummer, Heftnummer (gezähltes
        Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.
        """
        self.template =  u"%(reviewAuthor)s, presentation of: %(authors)s, "+\
                        "%(title)s, %(subtitle)s, in: "+\
                        "%(shortnameJournal)s, %(volume)s, %(issue)s, "+\
                        "(%(officialYearOfPublication)s/"+\
                        "%(yearOfPublication)s), "+\
                        "Page(s) %(pageStart)s/%(pageEnd)s, %(absolute_url)s."
        citation_dict = {}
        citation_dict["reviewAuthor"] = self.getReviewAuthor()
        citation_dict["authors"] = ", ".join(self.getAuthors())
        citation_dict["title"] = self.Title()
        citation_dict["subtitle"] = self.getSubtitle()
        citation_dict["shortnameJournal"] = self.getShortnameJournal()
        citation_dict["volume"] = self.getVolume()
        citation_dict["issue"] = self.getIssue()
        citation_dict["officialYearOfPublication"] = \
                                             self.getOfficialYearOfPublication()
        citation_dict["yearOfPublication"] = self.getYearOfPublication()
        citation_dict["pageStart"] = self.getPageStart()
        citation_dict["pageEnd"] = self.getPageEnd()
        citation_dict["absolute_url"] = self.absolute_url()
        return self.clean_citation(citation_dict)

atapi.registerType(PresentationArticleReview, PROJECTNAME)
