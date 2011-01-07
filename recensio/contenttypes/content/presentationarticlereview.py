# -*- coding: utf-8 -*-
"""Definition of the Presentation Article Review content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview, \
    BasePresentationNoMagic

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
            label=_(
    u"title_journal",
    default=u"Title (Journal)"
    ),
            description=_(
    u'description_title_journal',
    default=u"Information on the journal"
    ),
            ),
        ),
))

PresentationArticleReviewSchema['title'].storage = atapi.AnnotationStorage()
PresentationArticleReviewSchema["authors"].widget.label=_(
    "label_presentation_article_authors",
    default=u"Author(s) of presented article")
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
                         review_type="presentation_article_review")


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
        'labelPresentationAuthor',
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

    metadata_fields = ["metadata_review_type_code",
                       "metadata_presentation_author",
                       "languageReview", "languageReviewedText",
                       "authors", "title", "subtitle", "pageStart",
                       "pageEnd", "titleJournal", "shortnameJournal",
                       "yearOfPublication",
                       "officialYearOfPublication", "volumeNumber",
                       "issueNumber", "placeOfPublication",
                       "publisher", "issn", "ddcSubject", "ddcTime",
                       "ddcPlace", "subject", "referenceAuthors",
                       "uri", "metadata_recensioID", "idBvb"]

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

    def getLicense(self):
        return PresentationArticleReviewNoMagic(self).getLicense()

    def getLicenseURL(self):
        return PresentationArticleReviewNoMagic(self).getLicenseURL()

class PresentationArticleReviewNoMagic(BasePresentationNoMagic):

    def getDecoratedTitle(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0"
        >>> at_mock.subtitle = "Alles neu in 2010"
        >>> review = PresentationArticleReviewNoMagic(at_mock)
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Das neue Plone 4.0. Alles neu in 2010'

        Original Specification

        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel]

        Hans Meier: Geschichte des Abendlandes. Ein Abriss

        """
        self = real_self.magic
        authors_string = u' / '.join([getFormatter(' ')(x['firstname'], x['lastname'])
             for x in self.authors])
        titles_string = getFormatter(u'. ')(self.title, self.subtitle)
        return u": ".join((authors_string, titles_string))

    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.customCitation = ''
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0"
        >>> at_mock.subtitle = "Alles neu in 2010"
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH'
        >>> at_mock.placeOfPublication = u'München'
        >>> at_mock.issueNumber = '3'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.titleJournal = 'Open Source Mag'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> presentation = PresentationArticleReviewNoMagic(at_mock)
        >>> presentation.get_citation_string()
        u'de Roiste, Cillian: presentation of: Gerken, Patrick / Pilz, Alexander, Das neue Plone 4.0. Alles neu in 2010, in: Open Source Mag, 1, 3 (2009), http://www.syslab.com/@@redirect-to-uuid/12345'

        Original Specification

        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
Note: gezähltes Jahr entfernt.

        Meier, Hans: presentation of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        self = real_self.magic
        rezensent = getFormatter(u', ')
        item = getFormatter(u', ', u'. ')
        mag_number_and_year = getFormatter(u', ', u', ', u' ')
        full_citation_inner = getFormatter(u': presentation of: ', u', in: ', u', ')
        rezensent_string = rezensent(self.reviewAuthorLastname, \
                                     self.reviewAuthorFirstname)
        authors_string = u' / '.join([getFormatter(', ')(x['lastname'], x['firstname'])
                                    for x in self.authors])
        item_string = item(authors_string,
                           self.title,
                           self.subtitle)
        mag_year_string = self.yearOfPublication
        mag_year_string = mag_year_string and u'(' + mag_year_string + u')' \
            or None
        mag_number_and_year_string = mag_number_and_year(\
            self.titleJournal, \
            self.volumeNumber, self.issueNumber, mag_year_string)
        return full_citation_inner(rezensent_string, item_string, \
            mag_number_and_year_string, real_self.getUUIDUrl())

atapi.registerType(PresentationArticleReview, PROJECTNAME)

