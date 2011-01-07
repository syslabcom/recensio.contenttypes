# -*- coding: utf-8 -*-
"""Definition of the Review Journal content type
"""

from cgi import escape
from zope.app.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implements
import Acquisition

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.Portal import PloneSite
from Products.PortalTransforms.transforms.safe_html import scrubHTML

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview, BaseReviewNoMagic
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IReviewJournal

ReviewJournalSchema = JournalReviewSchema.copy() + \
                      CoverPictureSchema.copy() + \
                      PageStartEndSchema.copy() + \
                      ReviewSchema.copy() + \
                      atapi.Schema((
    atapi.StringField(
        'editor',
        schemata="reviewed_text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Editor (name or institution)"),
            ),
        ),
))

ReviewJournalSchema['title'].storage = atapi.AnnotationStorage()

ReviewJournalSchema['title'].widget.label = _(u"Title (journal)")
ReviewJournalSchema['subtitle'].widget.label = _(u"Subtitle (journal)")
finalize_recensio_schema(ReviewJournalSchema)

class ReviewJournal(BaseReview):
    """Review Journal"""
    implements(IReviewJournal)

    meta_type = "ReviewJournal"
    schema = ReviewJournalSchema
    title = atapi.ATFieldProperty('title')
    # Journal = Printed 
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
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
    canonical_uri = atapi.ATFieldProperty('canonical_uri')

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

    # Journal
    issn = atapi.ATFieldProperty('issn')
    shortnameJournal = atapi.ATFieldProperty('shortnameJournal')
    volumeNumber = atapi.ATFieldProperty('volumeNumber')
    issueNumber = atapi.ATFieldProperty('issueNumber')
    officialYearOfPublication = \
                              atapi.ATFieldProperty('officialYearOfPublication')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # ReviewJournal
    editor = atapi.ATFieldProperty('editor')


    # Reorder the fields as required
    ordered_fields = [
        # Reviewed Text schemata
        "issn",
        "languageReviewedText",
        "editor",
        "title", # Title of the journal
        "subtitle", # Subtitle of the journal
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "placeOfPublication",
        "publisher",
        "coverPicture",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",

        # Review schemata
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "doc",
        "review",
        "customCitation",
        "uri",
        ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["metadata_review_type_code",
                       "metadata_review_author",
                       "languageReview", "languageReviewedText",
                       "editor", "title", "shortnameJournal",
                       "yearOfPublication",
                       "officialYearOfPublication", "volumeNumber",
                       "issueNumber", "placeOfPublication",
                       "publisher", "issn", "ddcSubject", "ddcTime",
                       "ddcPlace", "subject", "metadata_recensioID",
                       "idBvb", "canonical_uri"]

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

    def get_citation_string(self):
        """

        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        return ReviewJournalNoMagic(self).get_citation_string()

    def getDecoratedTitle(self):
        """
        """
        return ReviewJournalNoMagic(self).getDecoratedTitle()

    def getLicense(self):
        return ReviewJournalNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewJournalNoMagic(self).getFirstPublicationData()

class ReviewJournalNoMagic(BaseReviewNoMagic):

    def get_citation_string(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.customCitation = ''
        >>> at_mock.title = "Plone Mag"
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.officialYearOfPublication = '2010'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH'
        >>> at_mock.placeOfPublication = u'München'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.issueNumber = '3'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1'
        >>> at_mock.get_publication_title = lambda :'Open Source'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> review = ReviewJournalNoMagic(at_mock)
        >>> review.get_citation_string()
        u'de Roiste, Cillian: review of: Plone Mag, 1, 3 (2010/2009), in: Open Source, Open Source Mag Vol 1, Open Source Mag 1, http://www.syslab.com/@@redirect-to-uuid/12345'

        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode('utf8')
        rezensent_string = getFormatter(', ')(self.reviewAuthorLastname, \
                                      self.reviewAuthorFirstname)
        item = getFormatter(', ', ', ', ' ')
        mag_year = getFormatter('/')(self.officialYearOfPublication, \
                             self.yearOfPublication)
        mag_year = mag_year and '(' + mag_year + ')' or None
        item_string = item(self.title, self.volumeNumber, \
                           self.issueNumber, mag_year)
        reference_mag = getFormatter(', ',  ', ')
        reference_mag_string = reference_mag(self.get_publication_title(), \
            self.get_volume_title(), self.get_issue_title())
        full_citation  = getFormatter(': review of: ', ', in: ', ', ')
        return full_citation(rezensent_string, item_string, \
            reference_mag_string, real_self.getUUIDUrl())

    def getDecoratedTitle(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.title = "Plone Mag"
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.officialYearOfPublication = '2010'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.issueNumber = '3'
        >>> review = ReviewJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Plone Mag, 1, 3 (2010/2009) (reviewed by Cillian de Roiste)'
        """
        self = real_self.magic
        item = getFormatter(', ', ', ', ' ')
        mag_year = getFormatter('/')(self.officialYearOfPublication, \
                             self.yearOfPublication)
        mag_year = mag_year and '(' + mag_year + ')' or None
        item_string = item(self.title, self.volumeNumber, \
                           self.issueNumber, mag_year)
        reviewer_string = getFormatter(' ')(self.reviewAuthorFirstname, \
                                    self.reviewAuthorLastname)
        reviewer_string = reviewer_string and '(' + \
            real_self.directTranslate('reviewed by') + ' ' + \
            reviewer_string + ')' or None
        return ' '.join((item_string, reviewer_string))

atapi.registerType(ReviewJournal, PROJECTNAME)
