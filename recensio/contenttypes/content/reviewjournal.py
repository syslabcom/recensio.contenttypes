# -*- coding: utf-8 -*-
"""Definition of the Review Journal content type
"""

from cgi import escape

from Products.Archetypes import atapi
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.review import BaseReviewNoMagic
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import LicenceSchema
from recensio.contenttypes.content.schemata import PageStartEndInPDFSchema
from recensio.contenttypes.content.schemata import PageStartEndOfReviewInJournalSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import URLInCitationSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IReviewJournal
from zope.i18nmessageid import Message
from zope.interface import implements

ReviewJournalSchema = (
    JournalReviewSchema.copy()
    + CoverPictureSchema.copy()
    + PageStartEndInPDFSchema.copy()
    + PageStartEndOfReviewInJournalSchema.copy()
    + ReviewSchema.copy()
    + URLInCitationSchema.copy()
    + LicenceSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "editor",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(label=_(u"Editor (name or institution)"),),
            ),
        )
    )
)

ReviewJournalSchema["title"].storage = atapi.AnnotationStorage()

ReviewJournalSchema["title"].widget.label = _(u"Title (journal)")
ReviewJournalSchema["subtitle"].widget.visible = {"view": "hidden", "edit": "hidden"}
finalize_recensio_schema(ReviewJournalSchema, review_type="review_journal")


class ReviewJournal(BaseReview):
    """Review Journal"""

    implements(IReviewJournal)

    meta_type = "ReviewJournal"
    schema = ReviewJournalSchema
    title = atapi.ATFieldProperty("title")
    # Journal = Printed
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthors = atapi.ATFieldProperty("reviewAuthors")
    languageReview = atapi.ATFieldProperty("languageReview")
    languageReviewedText = atapi.ATFieldProperty("languageReviewedText")
    recensioID = atapi.ATFieldProperty("recensioID")
    subject = atapi.ATFieldProperty("subject")
    pdf = atapi.ATFieldProperty("pdf")
    doc = atapi.ATFieldProperty("doc")
    doi = atapi.ATFieldProperty("doi")
    review = atapi.ATFieldProperty("review")
    customCitation = atapi.ATFieldProperty("customCitation")
    uri = atapi.ATFieldProperty("uri")
    urn = atapi.ATFieldProperty("urn")
    canonical_uri = atapi.ATFieldProperty("canonical_uri")

    # Common
    ddcPlace = atapi.ATFieldProperty("ddcPlace")
    ddcSubject = atapi.ATFieldProperty("ddcSubject")
    ddcTime = atapi.ATFieldProperty("ddcTime")

    # Printed
    subtitle = atapi.ATFieldProperty("subtitle")
    yearOfPublication = atapi.ATFieldProperty("yearOfPublication")
    placeOfPublication = atapi.ATFieldProperty("placeOfPublication")
    publisher = atapi.ATFieldProperty("publisher")
    yearOfPublicationOnline = atapi.ATFieldProperty("yearOfPublicationOnline")
    placeOfPublicationOnline = atapi.ATFieldProperty("placeOfPublicationOnline")
    publisherOnline = atapi.ATFieldProperty("publisherOnline")
    idBvb = atapi.ATFieldProperty("idBvb")

    # Journal
    issn = atapi.ATFieldProperty("issn")
    issn_online = atapi.ATFieldProperty("issn_online")
    issn = atapi.ATFieldProperty("url_journal")
    issn = atapi.ATFieldProperty("urn_journal")
    issn = atapi.ATFieldProperty("doi_journal")
    shortnameJournal = atapi.ATFieldProperty("shortnameJournal")
    volumeNumber = atapi.ATFieldProperty("volumeNumber")
    issueNumber = atapi.ATFieldProperty("issueNumber")
    officialYearOfPublication = atapi.ATFieldProperty("officialYearOfPublication")

    # PageStartEnd
    pageStart = atapi.ATFieldProperty("pageStart")
    pageEnd = atapi.ATFieldProperty("pageEnd")

    # PageStartEndOfReviewInJournal
    pageStartOfReviewInJournal = atapi.ATFieldProperty("pageStartOfReviewInJournal")
    pageEndOfReviewInJournal = atapi.ATFieldProperty("pageEndOfReviewInJournal")

    # ReviewJournal
    editor = atapi.ATFieldProperty("editor")

    # Reorder the fields as required
    ordered_fields = [
        # Reviewed Text schemata
        "issn",
        "issn_online",
        "url_journal",
        "urn_journal",
        "doi_journal",
        "languageReviewedText",
        "editor",
        "title",  # Title of the journal
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "placeOfPublication",
        "publisher",
        "yearOfPublicationOnline",
        "placeOfPublicationOnline",
        "publisherOnline",
        "coverPicture",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",
        # Review schemata
        "reviewAuthors",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "pageStartOfReviewInJournal",
        "pageEndOfReviewInJournal",
        "doc",
        "review",
        "customCitation",
        "canonical_uri",
        "urn",
        "bv",
        "ppn",
    ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = [
        "metadata_review_type_code",
        "get_journal_title",
        "metadata_start_end_pages",
        "metadata_review_author",
        "languageReview",
        "languageReviewedText",
        "editor",
        "title",
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "placeOfPublication",
        "publisher",
        "yearOfPublicationOnline",
        "placeOfPublicationOnline",
        "publisherOnline",
        "issn",
        "issn_online",
        "url_journal",
        "urn_journal",
        "doi_journal",
        "urn",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "canonical_uri",
        "metadata_recensioID",
        "idBvb",
        "doi",
    ]

    def get_publication_title(self):
        """ Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    get_journal_title = get_publication_title  # 2542

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

    def getDecoratedTitle(self, lastname_first=False):
        """
        """
        return ReviewJournalNoMagic(self).getDecoratedTitle(lastname_first)

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
        >>> at_mock.title = "Plone Mag♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.officialYearOfPublication = '2010♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.volumeNumber = '1♥'
        >>> at_mock.issueNumber = '3♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> at_mock.isDoiRegistrationActive = lambda: False
        >>> at_mock.getDoi = lambda: None
        >>> at_mock.generateDoi = lambda: None
        >>> review = ReviewJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Plone Mag\u2665, 1\u2665, 3\u2665 (2010\u2665/2009\u2665), in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode("utf8")

        rev_details_formatter = getFormatter(u", ", u", ", u" ")
        mag_year = getFormatter("/")(
            self.officialYearOfPublication, self.yearOfPublication
        )
        mag_year = mag_year and "(" + mag_year + ")" or None
        item_string = rev_details_formatter(
            self.title, self.volumeNumber, self.issueNumber, mag_year
        )

        reference_mag = getFormatter(", ", ", ")
        reference_mag_string = reference_mag(
            self.get_publication_title(),
            self.get_volume_title(),
            self.get_issue_title(),
        )

        location = real_self.get_citation_location()

        rezensent_string = get_formatted_names(
            u" / ", ", ", self.reviewAuthors, lastname_first=True
        )
        args = {
            "review_of": real_self.directTranslate(
                Message(u"text_review_of", "recensio", default="review of:")
            ),
            "in": real_self.directTranslate(
                Message(u"text_in", "recensio", default="in:")
            ),
            "page": real_self.directTranslate(
                Message(u"text_pages", "recensio", default="p.")
            ),
            ":": real_self.directTranslate(
                Message(u"text_colon", "recensio", default=":")
            ),
        }
        citation_formatter = getFormatter(
            u"%(:)s %(review_of)s " % args,
            ", %(in)s " % args,
            ", %(page)s " % args,
            u", ",
        )
        citation_string = citation_formatter(
            escape(rezensent_string),
            escape(item_string),
            escape(reference_mag_string),
            self.page_start_end_in_print,
            location,
        )
        return citation_string

    def getDecoratedTitle(real_self, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.title = "Plone Mag"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.officialYearOfPublication = '2010'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.issueNumber = '3'
        >>> review = ReviewJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Plone Mag, 1 (2010/2009), 3 (reviewed_by)'
        """
        self = real_self.magic

        item = getFormatter(", ", " ", ", ")
        mag_year = getFormatter("/")(
            self.officialYearOfPublication, self.yearOfPublication
        )
        mag_year = mag_year and "(" + mag_year + ")" or None
        item_string = item(self.title, self.volumeNumber, mag_year, self.issueNumber)

        if lastname_first:
            reviewer_string = get_formatted_names(
                u" / ", ", ", self.reviewAuthors, lastname_first=lastname_first
            )
        else:
            reviewer_string = get_formatted_names(
                u" / ", " ", self.reviewAuthors, lastname_first=lastname_first
            )

        if reviewer_string:
            reviewer_string = "(%s)" % real_self.directTranslate(
                Message(
                    u"reviewed_by",
                    "recensio",
                    mapping={u"review_authors": reviewer_string},
                )
            )

        return " ".join((item_string, reviewer_string))


atapi.registerType(ReviewJournal, PROJECTNAME)
