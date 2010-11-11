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

from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.schemata import AuthorsSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IPresentationArticleReview


PresentationArticleReviewSchema = \
                                AuthorsSchema.copy() + \
                                JournalReviewSchema.copy() + \
                                PresentationSchema.copy() + \
                                ReferenceAuthorsSchema.copy() + \
                                PageStartEndSchema.copy() + \
                                atapi.Schema((
    atapi.StringField(
        'titleJournal',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title"),
            description=_(
    u'description_title_journal',
    default=u"Information on the journal"
    ),
            ),
        ),
))

PresentationArticleReviewSchema['title'].storage = atapi.AnnotationStorage()
PresentationArticleReviewSchema["volumeNumber"].widget.label = _(u"Volume")
PresentationArticleReviewSchema["issueNumber"].widget.label = _(u"Number")
PresentationArticleReviewSchema["referenceAuthors"].widget.description = _(
    u'description_reference_authors',
    default=(u"Which scholarly author's work have you mainly engaged with in "
             "your article? Please give us the most detailed information "
             "possible on the &raquo;contemporary&laquo; names amongst them as "
             "the recensio.net editorial team will usually try to inform these "
             "authors of the existence of your article, your presentation, "
             "and the chance to comment on it. Only the reference author's "
             "name will be visible to the public. Please name historical "
             "reference authors (e.g. Aristotle, Charles de Gaulle) further "
             "below as subject heading.")
    )

finalize_recensio_schema(PresentationArticleReviewSchema,
                         review_type="presentation")


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
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    reviewAuthorPersonalUrl = atapi.ATFieldProperty('reviewAuthorPersonalUrl')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    review = atapi.ATFieldProperty('review')
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

    # Journal
    issn = atapi.ATFieldProperty('issn')
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    officialYearOfPublication = \
                              atapi.ATFieldProperty('officialYearOfPublication')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    titleJournal = atapi.ATFieldProperty('titleJournal')
    volumeNumber = atapi.ATFieldProperty('volumeNumber')
    issueNumber = atapi.ATFieldProperty('issueNumber')

    # Reorder the fields as required
    ordered_fields = [
        # Presented Text
        "issn",
        "uri",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "pageStart",
        "pageEnd",
        "titleJournal",
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "placeOfPublication",
        "publisher",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",

        # Presentation
        "review",
        'reviewAuthorPersonalUrl',
        "reviewAuthorHonorific",
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "reviewAuthorEmail",
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "referenceAuthors",
                       "recensioID", "uri", "authors", "title",
                       "subtitle", "pageStart", "pageEnd",
                       "titleJournal", "shortnameJournal",
                       "yearOfPublication",
                       "officialYearOfPublication", "volumeNumber",
                       "issueNumber", "placeOfPublication",
                       "publisher", "issn", "ddcSubject", "ddcTime",
                       "ddcPlace", "subject"]

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Zs-Titel, Nummer, Heftnummer (gezähltes Jahr/Erscheinungsjahr),
    # Seite von/bis, URL recensio.

    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of} "+\
                        "{authors}, {title}, {subtitle}, {text_in} "+\
                        "{shortnameJournal}, {volumeNumber}, {issueNumber}, "+\
                        "({officialYearOfPublication}/"+\
                        "{yearOfPublication}), "+\
                        "Page(s) {pageStart}/{pageEnd}"

    def getDecoratedTitle(self):
        return PresentationArticleReviewNoMagic(self).getDecoratedTitle()

    def get_citation_string(self):
        return PresentationArticleReviewNoMagic(self).get_citation_string()

class PresentationArticleReviewNoMagic(object):
    def __init__(self, at_object):
        self.magic = at_object

    def getDecoratedTitle(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0"
        >>> at_mock.subtitle = "Alles neu in 2010"
        >>> review = PresentationArticleReviewNoMagic(at_mock)
        >>> review.getDecoratedTitle()
        'Patrick Gerken / Alexander Pilz: Das neue Plone 4.0. Alles neu in 2010'
        """
        self = real_self.magic
        authors_string = ' / '.join([' '.join((x['firstname'], x['lastname']))
             for x in self.authors])
        titles_string = '. '.join((self.title, self.subtitle))
        return ": ".join((authors_string, titles_string))

    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0"
        >>> at_mock.subtitle = "Alles neu in 2010"
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH'
        >>> at_mock.placeOfPublication = u'München'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1'
        >>> at_mock.get_publication_title = lambda :'Open Source'
        >>> at_mock.absolute_url = lambda :'http://www.syslab.com'
        >>> presentation = PresentationArticleReviewNoMagic(at_mock)
        >>> presentation.get_citation_string()
        u'de Roiste, Cillian: presentation of: Gerken, Patrick / Pilz, Alexander, Das neue Plone 4.0. Alles neu in 2010, in: Open Source, Open Source Mag Vol 1, Open Source Mag 1 (2009), http://www.syslab.com'
        """
        self = real_self.magic
        if self.get('customCitation'):
            return scrubHTML(self.customCitation)
        rezensent = getFormatter(u', ')
        item = getFormatter(u', ', u'. ')
        mag_number_and_year = getFormatter(u', ', u', ', u' ')
        full_citation_inner = getFormatter(u': presentation of: ', u', in: ', u', ')
        rezensent_string = rezensent(self.reviewAuthorLastname, \
                                     self.reviewAuthorFirstname)
        authors_string = u' / '.join([u', '.join((x['lastname'], x['firstname']))
                                    for x in self.authors])
        item_string = item(authors_string,
                           self.title,
                           self.subtitle)
        mag_year_string = self.yearOfPublication
        mag_year_string = mag_year_string and u'(' + mag_year_string + u')' \
            or None
        mag_number_and_year_string = mag_number_and_year(\
            self.get_publication_title(), \
            self.get_volume_title(), self.get_issue_title(), mag_year_string)
        return full_citation_inner(rezensent_string, item_string, \
            mag_number_and_year_string, self.absolute_url())
atapi.registerType(PresentationArticleReview, PROJECTNAME)

