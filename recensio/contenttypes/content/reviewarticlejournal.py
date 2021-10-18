# -*- coding: utf-8 -*-
"""Definition of the Review Article Journal content type
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
from recensio.contenttypes.content.schemata import ArticleSchema
from recensio.contenttypes.content.schemata import AuthorsSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.content.schemata import isLazyURL
from recensio.contenttypes.content.schemata import JournalReviewSchema
from recensio.contenttypes.content.schemata import LicenceSchema
from recensio.contenttypes.content.schemata import PageStartEndInPDFSchema
from recensio.contenttypes.content.schemata import PageStartEndOfReviewInJournalSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import URLInCitationSchema
from recensio.contenttypes.interfaces import IReviewArticleJournal
from zope.i18nmessageid import Message
from zope.interface import implements


ReviewArticleJournalSchema = (
    JournalReviewSchema.copy()
    + CoverPictureSchema.copy()
    + PageStartEndInPDFSchema.copy()
    + PageStartEndOfReviewInJournalSchema.copy()
    + AuthorsSchema.copy()
    + ReviewSchema.copy()
    + URLInCitationSchema.copy()
    + LicenceSchema.copy()
    + ArticleSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "editor",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"Editor (name or institution)"),
                ),
            ),
            atapi.StringField(
                "titleJournal",
                storage=atapi.AnnotationStorage(),
                required=True,
                widget=atapi.StringWidget(
                    label=_(u"title_journal", default=u"Title (Journal)"),
                ),
            ),
            atapi.StringField(
                "translatedTitleJournal",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(
                        u"label_translated_title_journal",
                        default=u"Translated title (Journal)",
                    ),
                ),
            ),
        )
    )
)

ReviewArticleJournalSchema["title"].storage = atapi.AnnotationStorage()

ReviewArticleJournalSchema[
    "heading__page_number_of_presented_review_in_journal"
].widget.condition = "python:False"
ReviewArticleJournalSchema["doc"].widget.condition = "python:False"
ReviewArticleJournalSchema["heading_presented_work"].widget.condition = "python:False"
ReviewArticleJournalSchema["languageReviewedText"].label = _(u"Sprache (Aufsatz)")
finalize_recensio_schema(
    ReviewArticleJournalSchema, review_type="review_article_journal"
)


class ReviewArticleJournal(BaseReview):
    """Review Article Journal"""

    implements(IReviewArticleJournal)

    meta_type = "ReviewArticleJournal"
    schema = ReviewArticleJournalSchema
    title = atapi.ATFieldProperty("title")

    translatedTitle = atapi.ATFieldProperty("translatedTitle")
    translatedTitleJournal = atapi.ATFieldProperty("translatedTitleJournal")

    # Journal = Printed
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthors = atapi.ATReferenceFieldProperty("reviewAuthors")
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

    # Authors
    authors = atapi.ATReferenceFieldProperty("authors")

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
    url_journal = atapi.ATFieldProperty("url_journal")
    urn_journal = atapi.ATFieldProperty("urn_journal")
    doi_journal = atapi.ATFieldProperty("doi_journal")
    titleJournal = atapi.ATFieldProperty("titleJournal")
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

    # Article
    pageStartOfArticle = atapi.ATFieldProperty("pageStartOfArticle")
    pageEndOfArticle = atapi.ATFieldProperty("pageEndOfArticle")
    url_article = atapi.ATFieldProperty("url_article")
    urn_article = atapi.ATFieldProperty("urn_article")
    doi_article = atapi.ATFieldProperty("doi_article")

    # ReviewJournal
    editor = atapi.ATFieldProperty("editor")

    # Reorder the fields as required
    journal_fields = [
        "issn",
        "issn_online",
        "url_journal",
        "urn_journal",
        "doi_journal",
        "editor",
        "titleJournal",
        "translatedTitleJournal",
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
        "idBvb",
    ]
    article_fields = [
        "url_article",
        "urn_article",
        "doi_article",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "translatedTitle",
        "heading__page_number_of_article_in_journal_or_edited_volume",
        "pageStartOfArticle",
        "pageEndOfArticle",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
    ]
    review_fields = [
        "reviewAuthors",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "heading__page_number_of_presented_review_in_journal",
        "pageStartOfReviewInJournal",
        "pageEndOfReviewInJournal",
        "doc",
        "review",
        "customCitation",
        "canonical_uri",
        "urn",
        "bv",
        "ppn",
        "licence",
        "doi",
        "customCoverImage",
        "URLShownInCitationNote",
    ]
    ordered_fields = journal_fields + article_fields + review_fields

    for field in journal_fields:
        schema.changeSchemataForField(field, "Zeitschrift")
    for field in article_fields:
        schema.changeSchemataForField(field, "Aufsatz")
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
        "authors",
        "title",
        "subtitle",
        "translatedTitle",
        "metadata_start_end_pages_article",
        "editor",
        "titleJournal",
        "translatedTitleJournal",
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "placeOfPublication",
        "yearOfPublicationOnline",
        "placeOfPublicationOnline",
        "publisherOnline",
        "publisher",
        "issn",
        "issn_online",
        "url_journal",
        "urn_journal",
        "doi_journal",
        "url_article",
        "urn_article",
        "doi_article",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "canonical_uri",
        "urn",
        "effectiveDate",
        "metadata_recensioID",
        "idBvb",
        "doi",
    ]

    def get_publication_title(self):
        """Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    get_journal_title = get_publication_title  # 2542

    def get_publication_object(self):
        return self.get_parent_object_of_type("Publication")

    def get_volume_title(self):
        """Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

    def get_citation_string(self):
        """

        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        return ReviewArticleJournalNoMagic(self).get_citation_string()

    def getDecoratedTitle(self, lastname_first=False):
        """ """
        return ReviewArticleJournalNoMagic(self).getDecoratedTitle(lastname_first)

    def getLicense(self):
        return ReviewArticleJournalNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewArticleJournalNoMagic(self).getFirstPublicationData()


class ReviewArticleJournalNoMagic(BaseReviewNoMagic):
    def get_citation_string(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.customCitation = ''
        >>> at_mock.punctuated_title_and_subtitle = "The Plone Story. A CMS through the ages"
        >>> at_mock.formatted_authors = lambda: "Patrick Gerken / Alexander Pilz"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.officialYearOfPublication = '2010♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.page_start_end_in_print_article = '73-78'
        >>> at_mock.volumeNumber = '1♥'
        >>> at_mock.issueNumber = '3♥'
        >>> at_mock.titleJournal = "Plone Mag"
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
        >>> review = ReviewArticleJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Patrick Gerken / Alexander Pilz: The Plone Story. A CMS through the ages, in: Plone Mag, 1\u2665 (2010\u2665/2009\u2665), 3\u2665, p. 73-78, Review published in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Return the citation according to this schema:
        [Rezensent Nachname], [Rezensent Vorname]: review of: [Zs-Titel der rez. Zs.], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        The years of the magazine article reviewing the other magazine does
        not exist.
        """
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode("utf8")

        args = {
            "review_of": real_self.directTranslate(
                Message(u"text_review_of", "recensio", default="review of:")
            ),
            "review_in": real_self.directTranslate(
                Message(u"text_review_in", "recensio", default="Review published in:")
            ),
            "in:": real_self.directTranslate(
                Message(u"text_in", "recensio", default="in:")
            ),
            "page": real_self.directTranslate(
                Message(u"text_pages", "recensio", default="p.")
            ),
            ":": real_self.directTranslate(
                Message(u"text_colon", "recensio", default=":")
            ),
        }
        rev_details_formatter = getFormatter(
            u"%(:)s " % args,
            u", %(in:)s " % args,
            u", ",
            u" ",
            u", ",
            u", %(page)s " % args,
        )
        mag_year = getFormatter("/")(
            self.officialYearOfPublication, self.yearOfPublication
        )
        mag_year = mag_year and "(" + mag_year + ")" or None
        item_string = rev_details_formatter(
            self.formatted_authors(),
            self.punctuated_title_and_subtitle,
            self.titleJournal,
            self.volumeNumber,
            mag_year,
            self.issueNumber,
            self.page_start_end_in_print_article,
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
        citation_formatter = getFormatter(
            u"%(:)s %(review_of)s " % args,
            ", %(review_in)s " % args,
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
        >>> at_mock.title = "The Plone Story"
        >>> at_mock.punctuated_title_and_subtitle = "The Plone Story. A CMS through the ages"
        >>> at_mock.formatted_authors_editorial = lambda: "Patrick Gerken / Alexander Pilz"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> at_mock.titleJournal = "Plone Mag"
        >>> at_mock.translatedTitleJournal = "Plöne Mág"
        >>> at_mock.yearOfPublication = '2009'
        >>> at_mock.officialYearOfPublication = '2010'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.issueNumber = '3'
        >>> at_mock.page_start_end_in_print_article = '42-48'
        >>> review = ReviewArticleJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a.default
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: The Plone Story. A CMS through the ages, in: Plone Mag [Pl\\xf6ne M\\xe1g], 1 (2010/2009), 3, p. 42-48 (rezensiert von ${review_authors})'
        """
        self = real_self.magic

        args = {
            "in:": real_self.directTranslate(
                Message(u"text_in", "recensio", default="in:")
            ),
            "page": real_self.directTranslate(
                Message(u"text_pages", "recensio", default="p.")
            ),
            ":": real_self.directTranslate(
                Message(u"text_colon", "recensio", default=":")
            ),
        }

        item = getFormatter(" ", ", ", " ", ", ", ", %(page)s " % args)
        mag_year = getFormatter("/")(
            self.officialYearOfPublication, self.yearOfPublication
        )
        mag_year = mag_year and "(" + mag_year + ")" or None
        translated_title = self.translatedTitleJournal
        if translated_title:
            translated_title = "[{}]".format(translated_title)
        item_string = item(
            self.titleJournal,
            translated_title,
            self.volumeNumber,
            mag_year,
            self.issueNumber,
            self.page_start_end_in_print_article,
        )

        authors_string = self.formatted_authors_editorial()
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
                    default=u"rezensiert von ${review_authors}",
                    mapping={u"review_authors": reviewer_string},
                )
            )

        full_citation = getFormatter(": ", ", %(in:)s " % args, " ")
        return full_citation(
            authors_string,
            self.punctuated_title_and_subtitle,
            item_string,
            reviewer_string,
        )


atapi.registerType(ReviewArticleJournal, PROJECTNAME)
