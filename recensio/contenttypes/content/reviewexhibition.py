# -*- coding: utf-8 -*-
"""Definition of the Review Exhibition content type
"""

from cgi import escape

from Products.Archetypes import atapi
from Products.CMFPlone.utils import safe_unicode
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from Products.validation.interfaces.IValidator import IValidator
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.review import BaseReviewNoMagic
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.content.schemata import ExhibitionSchema
from recensio.contenttypes.content.schemata import LicenceSchema
from recensio.contenttypes.content.schemata import PageStartEndInPDFSchema
from recensio.contenttypes.content.schemata import PageStartEndOfReviewInJournalSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import URLInCitationSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IReviewExhibition
from recensio.theme.browser.views import editorTypes
from zope.i18nmessageid import Message
from zope.interface import implements

ReviewExhibitionSchema = (
    ExhibitionSchema.copy()
    + PageStartEndInPDFSchema.copy()
    + PageStartEndOfReviewInJournalSchema.copy()
    + ReviewSchema.copy()
    + URLInCitationSchema.copy()
    + LicenceSchema.copy()
)

ReviewExhibitionSchema["title"].required = False
ReviewExhibitionSchema["title"].widget.modes = ("view",)
ReviewExhibitionSchema["doc"].widget.condition = "python:False"
ReviewExhibitionSchema["languageReviewedText"].widget.condition = "python:False"
ReviewExhibitionSchema.changeSchemataForField(
    "heading__page_number_of_presented_review_in_journal", "review"
)
for field in ["title", "subtitle", "ddcSubject", "ddcPlace", "ddcTime", "subject"]:
    ReviewExhibitionSchema.changeSchemataForField(field, "Ausstellung")
finalize_recensio_schema(ReviewExhibitionSchema, review_type="review_exhibition")


class ReviewExhibition(BaseReview):
    """Review Exhibition"""

    implements(IReviewExhibition)

    meta_type = "ReviewExhibition"
    schema = ReviewExhibitionSchema

    description = atapi.ATFieldProperty("description")

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

    # Exhibition
    exhibiting_institution = atapi.ATFieldProperty("exhibiting_institution")
    dates = atapi.ATFieldProperty("dates")
    years = atapi.ATFieldProperty("years")
    exhibiting_organisation = atapi.ATFieldProperty("exhibiting_organisation")
    curators = atapi.ATFieldProperty("curators")
    isPermanentExhibition = atapi.ATFieldProperty("isPermanentExhibition")
    titleProxy = atapi.ATFieldProperty("titleProxy")
    subtitle = atapi.ATFieldProperty("subtitle")
    url_exhibition = atapi.ATFieldProperty("url_exhibition")
    doi_exhibition = atapi.ATFieldProperty("doi_exhibition")

    # PageStartEnd
    pageStart = atapi.ATFieldProperty("pageStart")
    pageEnd = atapi.ATFieldProperty("pageEnd")

    # PageStartEndOfReviewInJournal
    pageStartOfReviewInJournal = atapi.ATFieldProperty("pageStartOfReviewInJournal")
    pageEndOfReviewInJournal = atapi.ATFieldProperty("pageEndOfReviewInJournal")

    # Reorder the fields as required for the edit view
    ordered_fields = [
        # Exhibition schemata
        "exhibiting_institution",
        "dates",
        "years",
        "exhibiting_organisation",
        "curators",
        "isPermanentExhibition",
        "titleProxy",
        "subtitle",
        "url_exhibition",
        "doi_exhibition",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        # Review schemata
        "reviewAuthors",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "heading__page_number_of_presented_review_in_journal",
        "pageStartOfReviewInJournal",
        "pageEndOfReviewInJournal",
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

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    @property
    def title(self):
        return self.titleProxy or u"Ausstellung"

    @title.setter
    def title(self, value):
        self.titleProxy = value

    @property
    def exhibitor(self):
        return (
            u" / ".join(
                [
                    safe_unicode(institution["name"]).strip()
                    for institution in self.exhibiting_institution
                    if institution["name"]
                ]
            )
            or u" / ".join(
                [
                    safe_unicode(organisation["name"].decode("utf-8")).strip()
                    for organisation in self.exhibiting_organisation
                    if organisation["name"]
                ]
            )
            or get_formatted_names(
                u" / ",
                u" ",
                [
                    person
                    for person in self.curators
                    if person["firstname"] or person["lastname"]
                ],
            )
        )

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = [
        "metadata_review_type_code",
        "get_journal_title",
        "metadata_start_end_pages",
        "metadata_review_author",
        "languageReview",
        "languageReviewedText",
        "exhibiting_institution",
        "exhibiting_organisation",
        "curators",
        "titleProxy",
        "subtitle",
        "dates",
        "url_exhibition",
        "doi_exhibition",
        "urn",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "canonical_uri",
        "effectiveDate",
        "metadata_recensioID",
        "doi",
    ]

    def listDates(self):
        if not getattr(self, "dates", None):
            return u""
        dates_list = []
        for date in self.dates:
            if date["place"]:
                if self.isPermanentExhibition or not date["runtime"]:
                    dates_list.append(safe_unicode(date["place"]).strip())
                else:
                    dates_list.append(
                        ", ".join(
                            [
                                safe_unicode(date["place"]).strip(),
                                safe_unicode(date["runtime"]).strip(),
                            ]
                        )
                    )
        return u" / ".join(dates_list) if dates_list else u""

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

    @property
    def exhibitor(self):
        return ReviewExhibitionNoMagic(self).exhibitor

    def getDecoratedTitle(self, lastname_first=False):
        return ReviewExhibitionNoMagic(self).getDecoratedTitle(lastname_first)

    def get_citation_string(self):
        return ReviewExhibitionNoMagic(self).get_citation_string()

    def getLicense(self):
        return ReviewExhibitionNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewExhibitionNoMagic(self).getFirstPublicationData()


class ReviewExhibitionNoMagic(BaseReviewNoMagic):
    @property
    def exhibitor(real_self):
        self = real_self.magic
        return (
            u" / ".join(
                [
                    safe_unicode(institution["name"]).strip()
                    for institution in self.exhibiting_institution
                    if institution["name"]
                ]
            )
            or u" / ".join(
                [
                    safe_unicode(organisation["name"].decode("utf-8")).strip()
                    for organisation in self.exhibiting_organisation
                    if organisation["name"]
                ]
            )
            or get_formatted_names(
                u" / ",
                u" ",
                [
                    person
                    for person in self.curators
                    if person["firstname"] or person["lastname"]
                ],
            )
        )

    def getDecoratedTitle(real_self, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.punctuated_title_and_subtitle = u"Algol. Eine Retrospektive"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> at_mock.dates = [{"place": "M\xc3\xbcnchen", "runtime": ""}]
        >>> at_mock.exhibiting_institution = [{"name": "Museum f\xc3\xbcr Software", "gnd": ""}]
        >>> at_mock.exhibiting_organisation = [{"name": "Verein f\xc3\xbcr Softwareerhaltung", "gnd": ""}]
        >>> at_mock.curators = [{'firstname': 'Alexander', 'lastname': 'Pilz'}]
        >>> at_mock.isPermanentExhibition = False
        >>> review = ReviewExhibitionNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Museum f\\xfcr Software: Algol. Eine Retrospektive, M\\xfcnchen (exhibition_reviewed_by)'
        >>> at_mock.punctuated_title_and_subtitle = u""
        >>> at_mock.isPermanentExhibition = True
        >>> review.getDecoratedTitle()
        u'Museum f\\xfcr Software: Dauerausstellung, M\\xfcnchen (exhibition_reviewed_by)'
        >>> at_mock.exhibiting_institution = [{"name": "", "gnd": ""}]
        >>> review.getDecoratedTitle()
        u'Verein f\\xfcr Softwareerhaltung: Dauerausstellung, M\\xfcnchen (exhibition_reviewed_by)'
        >>> at_mock.exhibiting_organisation = [{"name": "", "gnd": ""}]
        >>> review.getDecoratedTitle()
        u'Alexander Pilz: Dauerausstellung, M\\xfcnchen (exhibition_reviewed_by)'
        >>> at_mock.curators = [{'firstname': '', 'lastname': ''}]
        >>> review.getDecoratedTitle()
        u'Dauerausstellung, M\\xfcnchen (exhibition_reviewed_by)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        self = real_self.magic

        rezensent_string = get_formatted_names(
            u" / ", " ", self.reviewAuthors, lastname_first=lastname_first
        )
        if rezensent_string:
            rezensent_string = u"(%s)" % real_self.directTranslate(
                Message(
                    u"exhibition_reviewed_by",
                    "recensio",
                    mapping={u"review_authors": rezensent_string},
                )
            )
        dates_formatter = getFormatter(u", ")
        dates_string = u" / ".join(
            [
                dates_formatter(
                    date["place"].decode("utf-8"), date["runtime"].decode("utf-8"),
                )
                for date in self.dates
            ]
        )

        permanent_exhib_string = real_self.directTranslate(
            Message(u"Dauerausstellung", "recensio")
        )
        title_string = getFormatter(u". ")(
            self.punctuated_title_and_subtitle,
            permanent_exhib_string if self.isPermanentExhibition else u"",
        )

        full_title = getFormatter(u": ", u", ", u" ")
        return full_title(
            real_self.exhibitor, title_string, dates_string, rezensent_string,
        )

        full_title = getFormatter(u": ", u", ", u" ")
        return full_title(self.exhibitor, title_string, dates_string, rezensent_string,)

    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0♥? Eine Retrospektive♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname' : 'de Roiste♥'}]
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> at_mock.isDoiRegistrationActive = lambda: False
        >>> at_mock.getDoi = lambda: None
        >>> at_mock.generateDoi = lambda: None
        >>> at_mock.dates = [{"place": "M\xc3\xbcnchen", "runtime": ""}]
        >>> at_mock.exhibiting_institution = [{"name": "Museum f\xc3\xbcr Software", "gnd": ""}]
        >>> at_mock.exhibiting_organisation = [{"name": "Verein f\xc3\xbcr Softwareerhaltung", "gnd": ""}]
        >>> at_mock.curators = [{'firstname': 'Alexander', 'lastname': 'Pilz'}]
        >>> at_mock.isPermanentExhibition = False
        >>> review = ReviewExhibitionNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Museum f\\xfcr Software: Plone 4.0\u2665? Eine Retrospektive\u2665, M\\xfcnchen, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'
        >>> at_mock.punctuated_title_and_subtitle = u""
        >>> at_mock.isPermanentExhibition = True
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Museum f\\xfcr Software: Dauerausstellung, M\\xfcnchen, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'
        >>> at_mock.exhibiting_institution = [{"name": "", "gnd": ""}]
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Verein f\\xfcr Softwareerhaltung: Dauerausstellung, M\\xfcnchen, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'
        >>> at_mock.exhibiting_organisation = [{"name": "", "gnd": ""}]
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Alexander Pilz: Dauerausstellung, M\\xfcnchen, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'
        >>> at_mock.curators = [{'firstname': '', 'lastname': ''}]
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Dauerausstellung, M\\xfcnchen, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'

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
        rev_details_formatter = getFormatter(u"%(:)s " % args, u", ", u" " % args)
        rezensent_string = get_formatted_names(
            u" / ", ", ", self.reviewAuthors, lastname_first=True
        )

        dates_formatter = getFormatter(", ")
        dates_string = " / ".join(
            [dates_formatter(date["place"], date["runtime"],) for date in self.dates]
        )
        permanent_exhib_string = real_self.directTranslate(
            Message(u"Dauerausstellung", "recensio", default="Dauerausstellung")
        )
        title_string = getFormatter(u". ")(
            self.punctuated_title_and_subtitle,
            permanent_exhib_string if self.isPermanentExhibition else u"",
        )
        item_string = rev_details_formatter(
            real_self.exhibitor, title_string, dates_string,
        )
        item_string = rev_details_formatter(self.exhibitor, title_string, dates_string,)

        mag_number_formatter = getFormatter(u", ", u", ")
        mag_number_string = mag_number_formatter(
            self.get_publication_title(),
            self.get_volume_title(),
            self.get_issue_title(),
        )

        location = real_self.get_citation_location()

        citation_formatter = getFormatter(
            u"%(:)s %(review_of)s " % args,
            ", %(in)s " % args,
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


atapi.registerType(ReviewExhibition, PROJECTNAME)
