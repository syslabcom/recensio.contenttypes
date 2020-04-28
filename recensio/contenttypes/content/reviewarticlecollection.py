# -*- coding: utf-8 -*-
"""Definition of the Review Article Collection content type
"""

from cgi import escape
from zope.i18nmessageid import Message
from zope.interface import implements

from Products.Archetypes import atapi
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from Products.validation.interfaces.IValidator import IValidator

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import (
    BaseReview,
    BaseReviewNoMagic,
    get_formatted_names,
)
from recensio.contenttypes.content.schemata import (
    ArticleSchema,
    BookReviewSchema,
    CoverPictureSchema,
    EditorialSchema,
    LicenceSchema,
    PageStartEndInPDFSchema,
    PageStartEndOfReviewInJournalSchema,
    PagecountSchema,
    ReviewSchema,
    SerialSchema,
    finalize_recensio_schema,
)
from recensio.contenttypes.interfaces import IReviewArticleCollection
from recensio.contenttypes.citation import getFormatter
from recensio.theme.browser.views import editorTypes


class YearOfPublicationValidator(object):
    implements(IValidator)
    name = ""

    def __call__(self, value, *args, **kwargs):
        request = kwargs["REQUEST"]
        if not (value or request.form.get("yearOfPublicationOnline")):
            return _(
                u"message_year_of_publication_validation_error",
                default=(
                    u"Please fill in at least one of the fields "
                    '"Year of publication" and "Year of publication '
                    '(online)".'
                ),
            )


ReviewArticleCollectionSchema = (
    BookReviewSchema.copy()
    + CoverPictureSchema.copy()
    + EditorialSchema.copy()
    + PageStartEndInPDFSchema.copy()
    + PageStartEndOfReviewInJournalSchema.copy()
    + PagecountSchema.copy()
    + ArticleSchema.copy()
    + ReviewSchema.copy()
    + SerialSchema.copy()
    + LicenceSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "titleEditedVolume",
                storage=atapi.AnnotationStorage(),
                required=True,
                widget=atapi.StringWidget(
                    label=_(u"title_edited_volume", default=u"Title (Edited Volume)"),
                ),
            ),
            atapi.StringField(
                "subtitleEditedVolume",
                storage=atapi.AnnotationStorage(),
                required=False,
                widget=atapi.StringWidget(
                    label=_(
                        u"subtitle_edited_volume", default=u"Subtitle (Edited Volume)"
                    ),
                ),
            ),
        )
    )
)

ReviewArticleCollectionSchema["title"].storage = atapi.AnnotationStorage()

ReviewArticleCollectionSchema["authors"].widget.label = _(
    u"Autor(en) des rezensierten Aufsatzes"
)
ReviewArticleCollectionSchema[
    "yearOfPublication"
].validators = YearOfPublicationValidator()
ReviewArticleCollectionSchema.changeSchemataForField(
    "heading__page_number_of_presented_review_in_journal", "review"
)
ReviewArticleCollectionSchema["doc"].widget.condition = "python:False"
ReviewArticleCollectionSchema[
    "help_authors_or_editors"
].widget.condition = "python:False"
ReviewArticleCollectionSchema["additionalTitles"].widget.condition = "python:False"
ReviewArticleCollectionSchema["editorial"].required = True
ReviewArticleCollectionSchema["editorial"].widget.label = _(u"Herausgeber")
ReviewArticleCollectionSchema[
    "heading_presented_work"
].widget.condition = "python:False"
ReviewArticleCollectionSchema["languageReviewedText"].label = _(u"Sprache (Aufsatz)")
finalize_recensio_schema(
    ReviewArticleCollectionSchema, review_type="review_article_collection"
)


class ReviewArticleCollection(BaseReview):
    """Review Article Collection"""

    implements(IReviewArticleCollection)

    meta_type = "ReviewArticleCollection"
    schema = ReviewArticleCollectionSchema

    title = atapi.ATFieldProperty("title")
    description = atapi.ATFieldProperty("description")
    # Book = Printed + Authors +
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
    canonical_uri = atapi.ATFieldProperty("canonical_uri")
    uri = atapi.ATFieldProperty("uri")
    urn = atapi.ATFieldProperty("urn")

    # Common
    ddcPlace = atapi.ATFieldProperty("ddcPlace")
    ddcSubject = atapi.ATFieldProperty("ddcSubject")
    ddcTime = atapi.ATFieldProperty("ddcTime")

    # Editorial
    editorial = atapi.ATFieldProperty("editorial")

    # Printed
    subtitle = atapi.ATFieldProperty("subtitle")
    additionalTitles = atapi.ATFieldProperty("additionalTitles")
    yearOfPublication = atapi.ATFieldProperty("yearOfPublication")
    placeOfPublication = atapi.ATFieldProperty("placeOfPublication")
    publisher = atapi.ATFieldProperty("publisher")
    yearOfPublicationOnline = atapi.ATFieldProperty("yearOfPublicationOnline")
    placeOfPublicationOnline = atapi.ATFieldProperty("placeOfPublicationOnline")
    publisherOnline = atapi.ATFieldProperty("publisherOnline")
    idBvb = atapi.ATFieldProperty("idBvb")

    # Authors
    authors = atapi.ATFieldProperty("authors")

    # Book
    isbn = atapi.ATFieldProperty("isbn")
    isbn_online = atapi.ATFieldProperty("isbn_online")
    url_monograph = atapi.ATFieldProperty("url_monograph")
    urn_monograph = atapi.ATFieldProperty("urn_monograph")
    doi_monograph = atapi.ATFieldProperty("doi_monograph")

    # Cover Picture
    coverPicture = atapi.ATFieldProperty("coverPicture")

    # PageStartEnd
    pageStart = atapi.ATFieldProperty("pageStart")
    pageEnd = atapi.ATFieldProperty("pageEnd")

    # PageStartEndOfReviewInJournal
    pageStartOfReviewInJournal = atapi.ATFieldProperty("pageStartOfReviewInJournal")
    pageEndOfReviewInJournal = atapi.ATFieldProperty("pageEndOfReviewInJournal")

    # Pagecount
    pages = atapi.ATFieldProperty("pages")

    # Serial
    series = atapi.ATFieldProperty("series")
    seriesVol = atapi.ATFieldProperty("seriesVol")

    # Article
    pageStartOfArticle = atapi.ATFieldProperty("pageStartOfArticle")
    pageEndOfArticle = atapi.ATFieldProperty("pageEndOfArticle")

    # Custom
    titleEditedVolume = atapi.ATFieldProperty("titleEditedVolume")
    subtitleEditedVolume = atapi.ATFieldProperty("subtitleEditedVolume")

    # Reorder the fields as required for the edit view
    collection_fields = [
        "isbn",
        "isbn_online",
        "url_monograph",
        "urn_monograph",
        "doi_monograph",
        "help_authors_or_editors",
        "editorial",
        "titleEditedVolume",
        "subtitleEditedVolume",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "yearOfPublicationOnline",
        "placeOfPublicationOnline",
        "publisherOnline",
        "series",
        "seriesVol",
        "pages",
        "coverPicture",
        "idBvb",
    ]
    article_fields = [
        "url_article",
        "urn_article",
        "doi_article",
        "languageReviewedText",
        "authors",
        "title",
        "subtitle",
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
    ordered_fields = collection_fields + article_fields + review_fields

    for field in collection_fields:
        schema.changeSchemataForField(field, "Sammelband")
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
        "metadata_start_end_pages_article",
        "editorial",
        "titleEditedVolume",
        "subtitleEditedVolume",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "yearOfPublicationOnline",
        "placeOfPublicationOnline",
        "publisherOnline",
        "series",
        "seriesVol",
        "pages",
        "isbn",
        "isbn_online",
        "url_monograph",
        "urn_monograph",
        "doi_monograph",
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

    def editorTypes(self):
        return editorTypes()

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

    def getDecoratedTitle(self, lastname_first=False):
        return ReviewArticleCollectionNoMagic(self).getDecoratedTitle(lastname_first)

    def get_citation_string(self):
        return ReviewArticleCollectionNoMagic(self).get_citation_string()

    def getLicense(self):
        return ReviewArticleCollectionNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewArticleCollectionNoMagic(self).getFirstPublicationData()


class ReviewArticleCollectionNoMagic(BaseReviewNoMagic):
    def getDecoratedTitle(real_self, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.formatted_authors_editorial = "Patrick Gerken / Alexander Pilz"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0. Das Benutzerhandbuch"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> review = ReviewArticleCollectionNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (reviewed_by)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        self = real_self.magic

        name_part_separator = " "
        if lastname_first:
            name_part_separator = ", "
        authors_string = self.formatted_authors

        rezensent_string = get_formatted_names(
            u" / ", " ", self.reviewAuthors, lastname_first=lastname_first
        )
        if rezensent_string:
            rezensent_string = "(%s)" % real_self.directTranslate(
                Message(
                    u"reviewed_by",
                    "recensio",
                    mapping={u"review_authors": rezensent_string},
                )
            )
        edited_volume = getFormatter(": ")
        edited_volume_string = edited_volume(
            get_formatted_names(
                u" / ", " ", self.getEditorial(), lastname_first=lastname_first
            ),
            self.titleEditedVolume,
        )

        full_citation = getFormatter(": ", ", in: ", " ")
        return full_citation(
            authors_string,
            self.punctuated_title_and_subtitle,
            edited_volume_string,
            rezensent_string,
        )

    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0♥? Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname' : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
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
        >>> review = ReviewArticleCollectionNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Spec:

        [Rezensent Nachname], [Rezensent Vorname]: review of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: gezähltes Jahr entfernt.
        Da es die Felder Zs-Titel, Nummer und Heftnummer werden die Titel der Objekte magazine, volume, issue genommen, in dem der Review liegt

        Müller, Klaus: review of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode("utf8")

        args = {
            "review_of": real_self.directTranslate(
                Message(u"text_review_of", "recensio", default="review of:")
            ),
            "review_in": real_self.directTranslate(
                Message(u"text_review_in", "recensio", default="review published in:")
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
        rev_details_formatter = getFormatter(
            u", ", u", %(in)s " % args, u"%(:)s " % args, ", %(page)s " % args
        )
        rezensent_string = get_formatted_names(
            u" / ", ", ", self.reviewAuthors, lastname_first=True
        )
        authors_string = self.formatted_authors
        editorial_string = get_formatted_names(
            u" / ", " ", self.getEditorial(), lastname_first=False
        )
        edited_volume_string = self.format(
            self.titleEditedVolume, self.subtitleEditedVolume,
        )
        title_subtitle_string = self.punctuated_title_and_subtitle
        item_string = rev_details_formatter(
            authors_string,
            title_subtitle_string,
            editorial_string,
            edited_volume_string,
            self.page_start_end_in_print_article,
        )
        mag_year_string = self.yearOfPublication.decode("utf-8")
        mag_year_string = mag_year_string and u"(" + mag_year_string + u")" or None

        mag_number_formatter = getFormatter(u", ", u", ")
        mag_number_string = mag_number_formatter(
            self.get_publication_title(),
            self.get_volume_title(),
            self.get_issue_title(),
        )

        location = real_self.get_citation_location()

        citation_formatter = getFormatter(
            u"%(:)s %(review_of)s " % args,
            ", %(review_in)s " % args,
            ", %(page)s " % args,
            u", ",
        )

        citation_string = citation_formatter(
            escape(rezensent_string),
            escape(item_string),
            escape(mag_number_string),
            self.page_start_end_in_print,
            location,
        )

        return citation_string


atapi.registerType(ReviewArticleCollection, PROJECTNAME)
