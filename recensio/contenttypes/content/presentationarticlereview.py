# -*- coding: utf-8 -*-
"""Definition of the Presentation Article Review content type
This is now:
Presentation Article in Journal
"""
from zope.interface import implements
from cgi import escape
from zope.i18nmessageid import Message

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BasePresentationNoMagic, BaseReview
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.schemata import (
    AuthorsSchema,
    JournalReviewSchema,
    PageStartEndOfPresentedTextInPrintSchema,
    PresentationSchema,
    ReferenceAuthorsSchema,
    finalize_recensio_schema,
)
from recensio.contenttypes.interfaces import IPresentationArticleReview


PresentationArticleReviewSchema = (
    AuthorsSchema.copy()
    + JournalReviewSchema.copy()
    + PresentationSchema.copy()
    + ReferenceAuthorsSchema.copy()
    + PageStartEndOfPresentedTextInPrintSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "heading_information_journal",
                schemata="reviewed_text",
                widget=atapi.LabelWidget(
                    label=_(
                        u"heading_information_journal",
                        default=(u"Information on the journal"),
                    )
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
        )
    )
)

PresentationArticleReviewSchema["title"].storage = atapi.AnnotationStorage()
PresentationArticleReviewSchema["authors"].widget.label = _(
    "label_presentation_article_authors", default=u"Author(s) of presented article"
)
PresentationArticleReviewSchema["review"].widget.description = _(
    u"description_presentation_article_review",
    default=(
        u"Please give a brief and clear outline of your thesis "
        "statements, your methodology and/or your discussion of "
        "existing research approaches. We would kindly ask you "
        "to avoid a mere summary of your text. Don't be shy, "
        "however, of wording your statements in a provocative "
        "way. By separating out paragraphs you will make your "
        "statement more readable. You can increase the number of "
        "characters available for your own presentation from 4000 "
        "to 6000 by commenting on an already existing "
        "review/presentation on recensio.net. Please note that "
        "both comments and presentations will be checked by the "
        "editorial team before being published in order to "
        "prevent misuse. Because of this texts will be available "
        "online at the earliest after three working days."
    ),
)
PresentationArticleReviewSchema["volumeNumber"].widget.label = _(u"Volume")
PresentationArticleReviewSchema["issueNumber"].widget.label = _(u"Number")
PresentationArticleReviewSchema["referenceAuthors"].widget.description = _(
    u"description_reference_authors",
    default=(
        u"Which scholarly author's work have you mainly engaged with in "
        "your article? Please give us the most detailed information "
        "possible on the &raquo;contemporary&laquo; names amongst them as "
        "the recensio.net editorial team will usually try to inform these "
        "authors of the existence of your article, your presentation, "
        "and the chance to comment on it. Only the reference author's "
        "name will be visible to the public. Please name historical "
        "reference authors (e.g. Aristotle, Charles de Gaulle) further "
        "below as subject heading."
    ),
)

PresentationArticleReviewSchema["canonical_uri"].widget.visible = {
    "edit": "invisible",
    "view": "invisible",
}

finalize_recensio_schema(
    PresentationArticleReviewSchema, review_type="presentation_article_review"
)


class PresentationArticleReview(BaseReview):
    """Presentation Article Review"""

    implements(IPresentationArticleReview)

    meta_type = "PresentationArticleReview"
    schema = PresentationArticleReviewSchema

    title = atapi.ATFieldProperty("title")
    description = atapi.ATFieldProperty("description")
    # Journal = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty("reviewAuthorHonorific")
    reviewAuthors = atapi.ATFieldProperty("reviewAuthors")
    reviewAuthorPersonalUrl = atapi.ATFieldProperty("reviewAuthorPersonalUrl")
    languageReview = atapi.ATFieldProperty("languageReview")
    languageReviewedText = atapi.ATFieldProperty("languageReviewedText")
    recensioID = atapi.ATFieldProperty("recensioID")
    subject = atapi.ATFieldProperty("subject")
    review = atapi.ATFieldProperty("review")
    uri = atapi.ATFieldProperty("uri")
    urn = atapi.ATFieldProperty("urn")

    # Common
    ddcPlace = atapi.ATFieldProperty("ddcPlace")
    ddcSubject = atapi.ATFieldProperty("ddcSubject")
    ddcTime = atapi.ATFieldProperty("ddcTime")

    # Printed
    subtitle = atapi.ATFieldProperty("subtitle")
    yearOfPublication = atapi.ATFieldProperty("yearOfPublication")
    placeOfPublication = atapi.ATFieldProperty("placeOfPublication")
    publisher = atapi.ATFieldProperty("publisher")
    idBvb = atapi.ATFieldProperty("idBvb")

    # Authors
    authors = atapi.ATFieldProperty("authors")

    # Journal
    issn = atapi.ATFieldProperty("issn")
    shortnameJournal = atapi.ATFieldProperty("shortnameJournal")
    officialYearOfPublication = atapi.ATFieldProperty("officialYearOfPublication")

    # Presentation
    isLicenceApproved = atapi.ATFieldProperty("isLicenceApproved")

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty("referenceAuthors")

    # PageStartEnd
    pageStart = atapi.ATFieldProperty("pageStart")
    pageEnd = atapi.ATFieldProperty("pageEnd")

    # PageStartEndOfPresentedTextInPrint
    pageStartOfPresentedTextInPrint = atapi.ATFieldProperty(
        "pageStartOfPresentedTextInPrint"
    )
    pageEndOfPresentedTextInPrint = atapi.ATFieldProperty(
        "pageEndOfPresentedTextInPrint"
    )

    titleJournal = atapi.ATFieldProperty("titleJournal")
    volumeNumber = atapi.ATFieldProperty("volumeNumber")
    issueNumber = atapi.ATFieldProperty("issueNumber")

    # Reorder the fields as required
    ordered_fields = [
        # Presented Text
        "issn",
        "heading_presented_work",
        "uri",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "pageStart",
        "pageEnd",
        "heading__page_number_of_presented_text_in_print",
        "pageStartOfPresentedTextInPrint",
        "pageEndOfPresentedTextInPrint",
        "heading_information_journal",
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
        "labelPresentationAuthor",
        "reviewAuthorHonorific",
        "reviewAuthors",
        "reviewAuthorEmail",
        "reviewAuthorPersonalUrl",
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved",
        "canonical_uri",
        "urn",
        "bv",
    ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = [
        "metadata_review_type_code",
        "metadata_presentation_author",
        "languageReview",
        "languageReviewedText",
        "authors",
        "title",
        "subtitle",
        "titleJournal",
        "shortnameJournal",
        "yearOfPublication",
        "officialYearOfPublication",
        "volumeNumber",
        "issueNumber",
        "metadata_start_end_pages",
        "placeOfPublication",
        "publisher",
        "issn",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "uri",
        "urn",
        "metadata_recensioID",
        "idBvb",
    ]

    def getDecoratedTitle(self):
        return PresentationArticleReviewNoMagic(self).getDecoratedTitle()
        return u": ".join(
            (self.formatted_authors_editorial, self.punctuated_title_and_subtitle)
        )

    def get_citation_string(self):
        return PresentationArticleReviewNoMagic(self).get_citation_string()

    def getLicense(self):
        return PresentationArticleReviewNoMagic(self).getLicense()

    def getLicenseURL(self):
        return PresentationArticleReviewNoMagic(self).getLicenseURL()


class PresentationArticleReviewNoMagic(BasePresentationNoMagic):
    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.customCitation = ''
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick♥', 'Gerken♥'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0♥?"
        >>> at_mock.subtitle = "Alles neu in 2010♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = u'München'
        >>> at_mock.issueNumber = '3♥'
        >>> at_mock.volumeNumber = '1♥'
        >>> at_mock.titleJournal = 'Open Source Mag♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> presentation = PresentationArticleReviewNoMagic(at_mock)
        >>> presentation.directTranslate = lambda m: m.default
        >>> presentation.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: presentation of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Das neue Plone 4.0\u2665? Alles neu in 2010\u2665, in: Open Source Mag\u2665, 1\u2665, 3\u2665, p. 11-21 <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'

        Original Specification

        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
Note: gezähltes Jahr entfernt.

        Meier, Hans: presentation of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        self = real_self.magic
        rezensent = getFormatter(u", ")
        if self.title[-1] in "!?:;.,":
            title_subtitle = getFormatter(u" ")
        else:
            title_subtitle = getFormatter(u". ")
        item = getFormatter(u", ")
        mag_number = getFormatter(u", ", u", ")
        rezensent_string = rezensent(
            self.reviewAuthors[0]["lastname"], self.reviewAuthors[0]["firstname"]
        )
        authors_string = u" / ".join(
            [getFormatter(", ")(x["lastname"], x["firstname"]) for x in self.authors]
        )
        title_subtitle_string = title_subtitle(self.title, self.subtitle)
        item_string = item(authors_string, title_subtitle_string)
        mag_year_string = self.yearOfPublication.decode("utf-8")
        mag_year_string = mag_year_string and u"(" + mag_year_string + u")" or None
        mag_number = mag_number(self.titleJournal, self.volumeNumber, self.issueNumber)

        args = {
            "presentation_of": real_self.directTranslate(
                Message(u"text_presentation_of", "recensio", default="presentation of:")
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
        full_citation_inner = getFormatter(
            u"%(:)s %(presentation_of)s " % args,
            u", %(in)s " % args,
            ", %(page)s " % args,
            u" ",
        )
        return full_citation_inner(
            escape(rezensent_string),
            escape(item_string),
            escape(mag_number),
            self.page_start_end_in_print,
            real_self.getUUIDUrl(),
        )

    def getDecoratedTitle(real_self):
        """
        Dude, where is my doctest?
        """
        self = real_self.magic
        rezensent_string = getFormatter(" ")(
            self.reviewAuthors[0]["firstname"], self.reviewAuthors[0]["lastname"]
        )
        if rezensent_string:
            rezensent_string = "(%s)" % real_self.directTranslate(
                Message(
                    u"presented_by",
                    "recensio",
                    mapping={u"review_authors": rezensent_string},
                )
            )
        full_citation = getFormatter(": ", " ")
        return full_citation(
            self.formatted_authors_editorial,
            self.punctuated_title_and_subtitle,
            rezensent_string,
        )


atapi.registerType(PresentationArticleReview, PROJECTNAME)
