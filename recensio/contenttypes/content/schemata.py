# -*- coding: utf-8 -*-
"""Definition of the base Review Schemata
"""
from AccessControl import ClassSecurityInfo
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from lxml.html import fromstring
from PIL import Image
from plone.app.blob.field import BlobField
from plone.app.blob.field import ImageField
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.CMFCore.utils import getToolByName
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.validators import DataGridValidator
from Products.validation import validation
from Products.validation.interfaces.IValidator import IValidator
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.browser.widgets import StringFallbackWidget
from recensio.contenttypes.browser.widgets import GNDReferenceBrowserWidget
from recensio.contenttypes.interfaces.publication import IPublication
from recensio.theme.interfaces import IRecensioLayer
from zope.component import adapts
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implements


def finalize_recensio_schema(schema, review_type="review"):
    """Custom replacement for schemata.finalizeATCTSchema

    Move fields to the correct schemata and hide fields we don't need

    """

    if review_type in [
        "presentation",
        "presentation_online",
        "presentation_article_review",
        "presentation_collection",
    ]:
        # Presentations only have one author
        schema["reviewAuthors"].allow_reorder = False
        schema["reviewAuthors"].allow_insert = False
        schema["reviewAuthors"].allow_delete = False
        schema["reviewAuthors"].widget.label = _(u"label_presentation_authors")
        # Rename the schemata for presentations
        presented = "presented_text"
        if review_type == "presentation_online":
            presented = "presented_resource"
        schema_field_names = [i.getName() for i in schema.fields()]
        for field_name in schema_field_names:
            if schema[field_name].schemata == "review":
                schema.changeSchemataForField(field_name, "presentation")
            elif schema[field_name].schemata == "presentation":
                pass
            else:
                schema.changeSchemataForField(field_name, presented)
            if field_name in ["pageStart", "pageEnd"]:
                # TODO: remove after running scripts/migrate_page_start_end.py
                schema[field_name].widget.visible = {"view": "hidden", "edit": "hidden"}
        # Third schemata for presentations with assocatied publications
        if review_type in ["presentation_article_review", "presentation_collection"]:
            if review_type == "presentation_article_review":
                associated_publication = "associated_journal"
            else:
                associated_publication = "associated_edited_volume"
            for field_name in schema_field_names:

                if field_name in [
                    "issn",
                    "isbn",
                    "titleCollectedEdition",
                    "heading_information_journal",
                    "titleJournal",
                    "shortnameJournal",
                    "editorsCollectedEdition",
                    "yearOfPublication",
                    "officialYearOfPublication",
                    "volumeNumber",
                    "issueNumber",
                    "series",
                    "seriesVol",
                    "pages",
                    "placeOfPublication",
                    "publisher",
                    "idBvb",
                ]:
                    schema.changeSchemataForField(field_name, associated_publication)

        schema["uri"].widget.visible["edit"] = "visible"
        schema.changeSchemataForField("uri", presented)
        multiselect_description = _(
            "description_ctrl_for_multiple",
            default=u"Mit gedrückter Strg-Taste können mehrere Zeilen gleichzeitig ausgewählt werden.",
        )
        schema["ddcSubject"].widget.label = _(u"Subject classification")
        schema["ddcSubject"].widget.description = multiselect_description
        schema["ddcTime"].widget.label = _(u"Time classification")
        schema["ddcTime"].widget.description = multiselect_description
        schema["ddcPlace"].widget.label = _(u"Regional classification")
        schema["ddcPlace"].widget.description = multiselect_description
        # fill in the review author first name and last name by default
        # schema['reviewAuthorLastname'].default_method = "get_user_lastname"
        # schema['reviewAuthorFirstname'].default_method = "get_user_firstname"
        schema["languageReview"].widget.label = _(u"Language(s) of presentation")
        if review_type == "presentation_online":
            schema["languageReviewedText"].widget.label = _(
                u"Language(s) of presented resource"
            )
        else:
            schema["languageReviewedText"].widget.label = _(
                u"Language(s) of presented work"
            )
        # Note: The characterLimit validator checks the portal_type to
        # see if it should be applied or not. Setting it here didn't
        # seem to work
    elif review_type in [
        "review_monograph",
        "review_journal",
        "review_article_journal",
        "review_article_collection",
        "review_exhibition",
    ]:
        schema.changeSchemataForField("licence", "review")
        schema.changeSchemataForField("licence_ref", "review")

    hidden_fields = [
        "allowDiscussion",
        "contributors",
        "creators",
        "description",
        "description",
        "effectiveDate",
        "excludeFromNav",
        "expirationDate",
        "generatedPdf",
        "id",
        "language",
        "location",
        "recensioID",
        "rights",
        "relatedItems",
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
    ]

    for field in hidden_fields:
        schema[field].widget.condition = "python:False"

    schemata.marshall_register(schema)


AuthorsSchema = atapi.Schema(
    (
        atapi.ReferenceField(
            "authors",
            schemata="reviewed_text",
            allowed_types=("Person",),
            vocabulary_factory="recensio.contenttypes.persons",
            multiValued=1,
            referencesSortable=True,
            relationship="author",
            widget=GNDReferenceBrowserWidget(
                label=_(u"Authors"),
            ),
        ),
    )
)


class isTrue:
    """
    Custom validator to ensure that the isLicenceApproved box is checked
    """

    implements(IValidator)
    name = "is_true_validator"

    def __call__(self, value, *args, **kwargs):
        if value == True:
            return 1
        site = getSite()
        language = getToolByName(site, "portal_languages").getPreferredLanguage()
        return translate(
            _(
                u"message_ccby_license",
                default=(
                    u"All submitted reviews must be published under "
                    "the CC-BY licence."
                ),
            ),
            target_language=language,
        )


class hasAtLeastOneAuthor(DataGridValidator):
    def __call__(self, value, *args, **kwargs):
        name = value[0]
        if name.get("firstname", "") == name.get("lastname", "") == "":
            return _("message_at_least_one_author_validation_error")
        return True


class isLazyURL:
    implements(IValidator)
    name = "is_lazy_url"

    def __call__(self, value, *args, **kwargs):
        isURL = validation.validatorFor("isURL")
        if isURL("http://%s" % value) == 1:
            return 1
        return isURL(value)


class ImageValidator:
    """
    Check that an image upload value is either an image or the command
    to delete the current image
    """

    implements(IValidator)
    name = ""

    def __call__(self, value, *args, **kwargs):
        if value != "DELETE_IMAGE":
            try:
                Image.open(value)
                value.seek(0)
                return True
            except IOError as e:
                return _(str(e))


class characterLimit:
    """
    Limit the number of characters of text, ignoring html markup

    NOTE: the TinyMCE character count may include html markup e.g. if
    pasted from a Word document. #2418
    """

    implements(IValidator)
    name = ""

    def __call__(self, value, *args, **kwargs):
        # "value" is a byte string. We need to decode it before we can
        # count the number of chars. We make the assumption that it is
        # utf-8 encoded
        html = fromstring(value.decode("utf-8"))
        # extract the text from the html
        textblocks = html.xpath("//text()")
        # join the textblocks except for line breaks (empty p tags)
        text = "".join([i for i in textblocks if i != "\r\n"])
        character_count = len(text)
        # TODO: setting the validator via the finalize_recensio_schema
        # method didn't work so I'm setting it here manually.
        is_review = kwargs["instance"]["portal_type"].startswith("Review")
        if is_review or character_count <= 6000:
            return 1
        else:
            return translate(
                _(
                    u"message_characters_exceeded",
                    default=(
                        u"You have exceeded the maximum number of characters you are "
                        "permitted to use."
                    ),
                )
            )


class ForceDefaulStringField(atapi.StringField):
    security = ClassSecurityInfo()

    security.declarePrivate("get")

    def get(self, instance, **kwargs):
        value = super(ForceDefaulStringField, self).get(instance, **kwargs)
        return value or self.getDefault(instance)


CoverPictureSchema = atapi.Schema(
    (
        ImageField(
            "coverPicture",
            schemata="reviewed_text",
            validators=(ImageValidator(),),
            storage=atapi.AnnotationStorage(),
            sizes={"cover": (200, 300)},
            widget=atapi.ImageWidget(
                label=_(u"Cover picture"),
            ),
        ),
    )
)

ReferenceAuthorsSchema = atapi.Schema(
    (
        DataGridField(
            "referenceAuthors",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            columns=(
                "lastname",
                "firstname",
                "email",
                "address",
                "phone",
                "preferred_language",
            ),
            default=[
                {
                    "lastname": "",
                    "firstname": "",
                    "email": "",
                    "address": "",
                    "phone": "",
                    "preferred_language": "",
                }
            ],
            widget=DataGridWidget(
                label=_(
                    u"label_reference_authors",
                    default=(
                        u"Reference Authors (email address, postal address and phone "
                        "number are not publicly visible)"
                    ),
                ),
                columns={
                    "lastname": Column(_(u"Lastname")),
                    "firstname": Column(_(u"Firstname")),
                    "email": Column(_(u"Email address")),
                    "address": Column(_(u"Institution")),
                    "phone": Column(""),
                    "preferred_language": SelectColumn(
                        _(u"label_preferred_language"),
                        vocabulary="listRecensioSupportedLanguages",
                    ),
                },
            ),
        ),
    )
)


ReviewSchema = atapi.Schema(
    (
        BlobField(
            "pdf",
            schemata=_(u"review"),
            storage=atapi.AnnotationStorage(),
            widget=atapi.FileWidget(
                label=_(u"PDF"),
                visible={"view": "hidden", "edit": "visible"},
            ),
            default_content_type="application/pdf",
        ),
        BlobField(
            "doc",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=atapi.FileWidget(
                label=_(u"Word Document"),
            ),
        ),
        atapi.TextField(
            "customCitation",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=atapi.TextAreaWidget(
                label=_(u"Optional citation format"),
                description=_(
                    u"description_custom_citation",
                    default=(
                        u"Please fill in only if you wish to use a citation format "
                        "different from the platform's"
                    ),
                ),
                rows=3,
            ),
        ),
        ForceDefaulStringField(
            "doi",
            default_method="generateDoi",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=StringFallbackWidget(
                label=_(u"label_doi", default=(u"DOI")),
                description=_(
                    u"description_doi",
                    default=(
                        u"Digital Object Identifier. Leave empty to use the "
                        "automatically generated value."
                    ),
                ),
                label_fallback_value=_(
                    u"label_doi_fallback",
                    default=(u"Automatically generated value"),
                ),
                label_fallback_unavailable=_(
                    u"label_doi_fallback_unavailable",
                    default=(u"not yet available"),
                ),
            ),
        ),
        ImageField(
            "customCoverImage",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            required=False,
            widget=atapi.FileWidget(
                label=_(u"Custom cover image"),
                description=_(
                    u"description_custom_cover_image",
                    default=u"Image that will be shown as a link to the external "
                    'full text. Only used if "Use external full text" is '
                    "activated on the volume or issue.",
                ),
            ),
        ),
    )
)

description_is_url_shown_in_citation_note = _(
    u"description_is_url_shown_in_citation_note",
    default=(
        u'Zeige die URL der Rezension in der "Zitierhinweis"-Box. '
        u"Diese Option kann hier nicht deaktiviert werden, wenn sie "
        u"bereits auf einer übergeordneten Ebene (Zeitschrift, Band, "
        u"Ausgabe) deaktiviert ist. Die Einstellung hat außerdem keine "
        u"Wirkung, falls ein externer Volltext für die Rezension "
        u"benutzt wird; in diesem Fall bleibt die URL immer versteckt. "
        u"Beachten Sie, dass diese Einstellung weder den eigentlichen "
        u"Zitierhinweis noch die Anzeige der Original-URL beeinflusst."
    ),
)

URLInCitationSchema = atapi.Schema(
    (
        atapi.BooleanField(
            "URLShownInCitationNote",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            accessor="isURLShownInCitationNote",
            default=True,
            widget=atapi.BooleanWidget(
                label=_(
                    u"label_is_url_shown_in_citation_note",
                    default=u"Show URL in citation rules box",
                ),
                description=description_is_url_shown_in_citation_note,
                condition="python:object.aq_parent.isURLShownInCitationNote() if object.aq_parent != object else True",
            ),
        ),
        atapi.StringField(
            "labelURLShownInCitationNote",
            schemata="review",
            widget=atapi.LabelWidget(
                label=_(
                    u"label_is_url_shown_in_citation_note",
                ),
                description=description_is_url_shown_in_citation_note,
                condition="python:not object.aq_parent.isURLShownInCitationNote() if object.aq_parent != object else False",
            ),
        ),
    )
)

PresentationSchema = atapi.Schema(
    (
        atapi.StringField(
            "labelPresentationAuthor",
            schemata="presentation",
            widget=atapi.LabelWidget(
                label=_(u"label_presentation_author", default=(u""))
            ),
            searchable=True,
        ),
        atapi.StringField(
            "reviewAuthorHonorific",
            schemata="presentation",
            storage=atapi.AnnotationStorage(),
            required=True,
            vocabulary=NamedVocabulary("honorifics"),
            widget=atapi.SelectionWidget(
                label=_(u"Honorific Title"),
            ),
        ),
        atapi.StringField(
            "reviewAuthorEmail",
            schemata="presentation",
            storage=atapi.AnnotationStorage(),
            required=True,
            default_method="get_user_email",
            widget=atapi.StringWidget(
                label=_(u"Email address (not publicly visible)"),
            ),
        ),
        atapi.StringField(
            "reviewAuthorPersonalUrl",
            schemata="presentation",
            storage=atapi.AnnotationStorage(),
            default_method="get_user_home_page",
            validators=(isLazyURL,),
            mutator="setReviewAuthorPersonalUrl",
            widget=atapi.StringWidget(
                label=_(u"Personal webpage URL/URN"),
                description=_(
                    u"description_personal_webpage",
                    default=(
                        u"Here you can link to your personal website (e.g. within a "
                        "network of historians, a university or research institution). "
                        "It should preferably be persistent or be corrected by you in "
                        "case of changes (e.g. change of university)."
                    ),
                ),
            ),
            #        accessor='getReviewAuthorPersonalUrl',
        ),
        atapi.BooleanField(
            "isLicenceApproved",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            value=False,
            required=True,
            validators=(isTrue(),),
            widget=atapi.BooleanWidget(
                label=_(u"Licence Agreement"),
                description=_(
                    u"description_ccby_licence_approval",
                    default=(
                        u"I agree that my presentation will be published by recensio.net "
                        "under the <a "
                        "href='http://creativecommons.org/licenses/by-nc-nd/2.0/deed.en' "
                        "target='_blank'>"
                        "creative-commons-licence Attribution-NonCommercial-"
                        "NoDerivs (CC-BY-NC-ND)</a>. Under these conditions, platform "
                        "users may use it electronically, distribute it, print it and "
                        "provide it for download. The editorial team reserves its right "
                        "to change incoming posts (see our user guidelines to this)."
                    ),
                ),
            ),
        ),
    )
)


PageStartEndInPDFSchema = atapi.Schema(
    (
        atapi.IntegerField(
            "pageStart",  # page number in pdf
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"Page number (start)"),
                description=_(
                    u"description_page_number",
                    default=u"Please fill in only if the review is part of a larger pdf-file",
                ),
            ),
        ),
        atapi.IntegerField(
            "pageEnd",  # page number in pdf
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"Page number (end)"),
                description="""<script type="text/javascript">
    jq(document).ready(function(){
        var my_elements = '#archetypes-fieldname-pageStart, #archetypes-fieldname-pageEnd';
        if(jq('#pdf_upload').length){
            jq(my_elements).hide();
            jq("#pdf_upload").click(function(){jq(my_elements).show();});
        }
    });
</script>""",
            ),
        ),
    )
)

# remove PageStartEndInPDFSchema after running
# scripts/migrate_page_start_end.py #2630
PageStartEndOfPresentedTextInPrintSchema = PageStartEndInPDFSchema.copy() + atapi.Schema(
    (
        atapi.StringField(
            "heading__page_number_of_presented_text_in_print",
            schemata="reviewed_text",
            widget=atapi.LabelWidget(
                label=_(
                    u"description_page_number_of_presented_text_in_print",
                    default=(u"Page numbers of the presented article"),
                )
            ),
        ),
        atapi.IntegerField(
            "pageStartOfPresentedTextInPrint",
            schemata="presented_text",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_start_of_presented_text_in_print"),
            ),
        ),
        atapi.IntegerField(
            "pageEndOfPresentedTextInPrint",
            schemata="presented_text",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_end_of_presented_text_in_print"),
            ),
        ),
    )
)


PageStartEndOfReviewInJournalSchema = atapi.Schema(
    (
        atapi.StringField(
            "heading__page_number_of_presented_review_in_journal",
            schemata="reviewed_text",
            widget=atapi.LabelWidget(
                label=_(
                    u"description_page_number_of_presented_review_in_journal",
                    default=(u"Page numbers of the presented article"),
                )
            ),
        ),
        atapi.IntegerField(
            "pageStartOfReviewInJournal",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_start_of_presented_review_in_journal"),
            ),
        ),
        atapi.IntegerField(
            "pageEndOfReviewInJournal",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_end_of_presented_review_in_journal"),
            ),
        ),
    )
)


PagecountSchema = atapi.Schema(
    (
        atapi.StringField(
            "pages",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Pages"),
            ),
        ),
    )
)

SerialSchema = atapi.Schema(
    (
        atapi.StringField(
            "series",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Series"),
            ),
            searchable=True,
        ),
        atapi.StringField(
            "seriesVol",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Series (vol.)"),
            ),
        ),
    )
)


BaseReviewSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema(
    (
        # TODO for presentations check that last name and first name are also
        # in the authors field
        atapi.StringField(
            "reviewAuthorLastname",  # for migration to reviewAuthors only
            schemata="review",
            storage=atapi.AnnotationStorage(),
            required=False,
            widget=atapi.StringWidget(
                label=_(u"Last name author"),
            ),
            searchable=True,
        ),
        atapi.StringField(
            "reviewAuthorFirstname",  # for migration to reviewAuthors only
            schemata="review",
            storage=atapi.AnnotationStorage(),
            required=False,
            widget=atapi.StringWidget(
                label=_(u"First name author"),
            ),
            searchable=True,
        ),
        atapi.ReferenceField(
            "reviewAuthors",
            schemata="review",
            #validators=(hasAtLeastOneAuthor(""),),
            required=True,
            allowed_types=("Person",),
            vocabulary_factory="recensio.contenttypes.persons",
            multiValued=1,
            referencesSortable=True,
            relationship="reviewAuthor",
            widget=GNDReferenceBrowserWidget(
                label=_(u"label_review_authors"),
            ),
        ),
        atapi.LinesField(
            "languageReview",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            vocabulary="listAvailableContentLanguages",
            widget=atapi.MultiSelectionWidget(
                label=_(u"Language(s) (review)"),
                size=3,
            ),
        ),
        atapi.LinesField(
            "languageReviewedText",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary="listAvailableContentLanguages",
            widget=atapi.MultiSelectionWidget(
                label=_(u"Language(s) (text)"),
                size=3,
            ),
        ),
        atapi.StringField(
            "recensioID",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                visible={"view": "hidden", "edit": "hidden"},
            ),
        ),
        BlobField(
            "generatedPdf",
            storage=atapi.AnnotationStorage(),
            widget=atapi.FileWidget(
                label=_(u"Generated Pdf"),
                visible={"view": "hidden", "edit": "visible"},
            ),
            default_content_type="application/pdf",
        ),
        atapi.TextField(
            "review",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            default_output_type="text/html",
            validators=(characterLimit(),),
            widget=atapi.RichWidget(
                label=_(u"Core Statements"),
                rows=20,
                maxlength=4000,
            ),
        ),
        atapi.StringField(
            # "Partner URL" is no longer used for reviews but is being
            # kept to avoid breakage, this is still used in presentations
            # #3103
            "uri",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators=(isLazyURL,),
            mutator="setUri",
            widget=atapi.StringWidget(
                label=_(u"URL"),
                description="",
                visible={"edit": "hidden"},
            ),
        ),
        atapi.StringField(
            "urn",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"URN"),
                description=_(
                    "description_urn", default="Filled in by the editorial staff"
                ),
            ),
        ),
        atapi.StringField(
            "bv",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"BV Number"),
                description=_(
                    "description_bv_number", default="Filled in by the editorial staff"
                ),
            ),
        ),
        atapi.StringField(
            "ppn",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"PPN"),
                description=_(
                    "description_bv_number", default="Filled in by the editorial staff"
                ),
            ),
        ),
        atapi.StringField(
            "canonical_uri",
            schemata="review",
            storage=atapi.AnnotationStorage(),
            validators=(isLazyURL,),
            mutator="setCanonical_uri",
            widget=atapi.StringWidget(
                label=_(u"Original Source URL"),
                description=_(
                    u"description_uri",
                    default=u"Please fill in only after consultation with the recensio.net team",
                ),
            ),
        ),
    )
)
BaseReviewSchema["title"].schemata = "reviewed_text"
BaseReviewSchema.changeSchemataForField("subject", "reviewed_text")
BaseReviewSchema["subject"].schemata = "reviewed_text"
BaseReviewSchema["subject"].widget = atapi.LinesWidget()
BaseReviewSchema["subject"].widget.label = _(u"Subject heading")
BaseReviewSchema["subject"].widget.description = _(
    "description_subject",
    default=u"Mehrere Schlagwörter bitte untereinander (per Return-Taste) auflisten, keine Kommas verwenden.",
)


CommonReviewSchema = BaseReviewSchema.copy() + atapi.Schema(
    (
        atapi.LinesField(
            "ddcSubject",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("topic_values"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"ddc subject"),
                size=10,
            ),
        ),
        # Q: DateTimeField ?
        atapi.LinesField(
            "ddcTime",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("epoch_values"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"ddc time"),
                size=10,
            ),
        ),
        atapi.LinesField(
            "ddcPlace",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("region_values"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"ddc place"),
                size=10,
            ),
        ),
    )
)

PrintedReviewSchema = CommonReviewSchema.copy() + atapi.Schema(
    (
        atapi.StringField(
            "heading_presented_work",
            schemata="reviewed_text",
            widget=atapi.LabelWidget(
                label=_(
                    u"heading_presented_work",
                    default=(u"Information on presented work"),
                )
            ),
        ),
        atapi.StringField(
            "subtitle",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Subtitle"),
            ),
        ),
        # Q: DateTimeField or perhaps IntegerField ?
        atapi.StringField(
            "yearOfPublication",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Year of publication"),
            ),
        ),
        atapi.StringField(
            "placeOfPublication",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Place of publication"),
            ),
        ),
        atapi.StringField(
            "publisher",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Publisher"),
            ),
            searchable=True,
        ),
        atapi.StringField(
            "yearOfPublicationOnline",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Year of publication (Online)"),
            ),
        ),
        atapi.StringField(
            "placeOfPublicationOnline",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Place of publication (Online)"),
            ),
        ),
        atapi.StringField(
            "publisherOnline",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Publisher (Online)"),
            ),
            searchable=True,
        ),
        atapi.StringField(
            "idBvb",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                visible={"view": "hidden", "edit": "hidden"},
            ),
        ),
    )
)
# PrintedReviewSchema["title"].required = True

BookReviewSchema = (
    PrintedReviewSchema.copy()
    + AuthorsSchema.copy()
    + atapi.Schema(
        (
            DataGridField(
                "additionalTitles",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                columns=("title", "subtitle"),
                default=[],
                widget=DataGridWidget(
                    label=_(u"Paralleltitel (andere Sprachen)"),
                    columns={
                        "title": Column(_(u"Title")),
                        "subtitle": Column(_(u"Subtitle")),
                    },
                ),
                searchable=True,
            ),
            atapi.StringField(
                "isbn",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"ISBN"),
                    description=_(
                        u"description_isbn",
                        default=(
                            u"With or without hyphens. In case of several numbers please "
                            "choose the hard cover edition."
                        ),
                    ),
                ),
            ),
            atapi.StringField(
                "isbn_online",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"ISBN (Online)"),
                    description=_(
                        u"description_isbn_online",
                        default=(
                            u"With or without hyphens. In case of several numbers please "
                            "choose the hard cover edition."
                        ),
                    ),
                ),
            ),
            atapi.StringField(
                "url_monograph",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                validators=(isLazyURL,),
                mutator="setUrl_monograph",
                widget=atapi.StringWidget(
                    label=_(u"URL (Monographie)"),
                ),
            ),
            atapi.StringField(
                "urn_monograph",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                validators=(isLazyURL,),
                mutator="setUrn_monograph",
                widget=atapi.StringWidget(
                    label=_(u"URN (Monographie)"),
                ),
            ),
            atapi.StringField(
                "doi_monograph",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"DOI (Monographie)"),
                ),
            ),
        )
    )
)
BookReviewSchema["authors"].widget.label = _(u"Author (monograph)")


EditorialSchema = atapi.Schema(
    (
        atapi.StringField(
            "help_authors_or_editors",
            schemata="reviewed_text",
            widget=atapi.LabelWidget(
                label=_(
                    u"help_authors_or_editors",
                    default=(
                        u"Please fill in either authors OR editors "
                        "(exception: Complete Works etc.)"
                    ),
                )
            ),
        ),
        atapi.ReferenceField(
            "editorial",
            schemata="reviewed_text",
            allowed_types=("Person",),
            vocabulary_factory="recensio.contenttypes.persons",
            multiValued=1,
            referencesSortable=True,
            relationship="editor",
            widget=GNDReferenceBrowserWidget(
                label=_(u"label_editorial"),
            ),
        ),
    )
)

JournalReviewSchema = (
    schemata.ATContentTypeSchema.copy()
    + PrintedReviewSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "issn",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"ISSN"),
                    description=_(
                        u"description_issn", default=(u"With or without hyphens.")
                    ),
                ),
            ),
            atapi.StringField(
                "issn_online",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"ISSN Online"),
                    description=_(
                        u"description_issn_online",
                        default=(u"With or without hyphens."),
                    ),
                ),
            ),
            atapi.StringField(
                "url_journal",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                validators=(isLazyURL,),
                mutator="setUrl_journal",
                widget=atapi.StringWidget(
                    label=_(u"URL (Zeitschrift)"),
                ),
            ),
            atapi.StringField(
                "urn_journal",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                validators=(isLazyURL,),
                mutator="setUrn_journal",
                widget=atapi.StringWidget(
                    label=_(u"URN (Zeitschrift)"),
                ),
            ),
            atapi.StringField(
                "doi_journal",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"DOI (Zeitschrift)"),
                ),
            ),
            atapi.StringField(
                "shortnameJournal",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"Shortname"),
                ),
            ),
            atapi.StringField(
                "volumeNumber",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"Vol."),
                ),
            ),
            atapi.StringField(
                "issueNumber",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"Number"),
                ),
            ),
            atapi.StringField(
                "officialYearOfPublication",
                schemata="reviewed_text",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(u"Official year of publication (if different)"),
                ),
            ),
        )
    )
)
# JournalReviewSchema["authors"].widget.label=_(u"Autor des Aufsatzes")
JournalReviewSchema["yearOfPublication"].widget.label = _(u"Actual year of publication")


LicenceSchema = atapi.Schema(
    (
        atapi.StringField(
            "licence",
            widget=atapi.TextAreaWidget(
                label=_(u"label_publication_licence", default=u"Publication Licence"),
                description=_(
                    u"description_publication_licence",
                    default=(
                        u"Please specify the licence terms under which reviews "
                        "may be used. This text will be displayed on the front "
                        "page of the PDF version and to the side of the web "
                        "version of each review for this publication."
                    ),
                ),
                rows=3,
            ),
        ),
        atapi.ReferenceField(
            "licence_ref",
            widget=ReferenceBrowserWidget(
                label=_(
                    u"label_publication_licence_ref",
                    default=u"Publication Licence (Translated)",
                ),
                description=_(
                    u"description_publication_licence_ref",
                    default=(
                        u"To specify a licence text that will be "
                        "displayed in the current UI language, select a "
                        "page that has been translated with the platform's "
                        "translation mechanism."
                    ),
                ),
            ),
            allowed_types=("Document",),
            multiValued=0,
            relationship="custom_licence",
        ),
    )
)


ArticleSchema = atapi.Schema(
    (
        atapi.StringField(
            "translatedTitle",
            schemata="Aufsatz",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Translated title"),
            ),
        ),
        atapi.StringField(
            "url_article",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            validators=(isLazyURL,),
            mutator="setUrl_article",
            widget=atapi.StringWidget(
                label=_(u"URL (Aufsatz)"),
            ),
        ),
        atapi.StringField(
            "urn_article",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            validators=(isLazyURL,),
            mutator="setUrn_article",
            widget=atapi.StringWidget(
                label=_(u"URN (Aufsatz)"),
            ),
        ),
        atapi.StringField(
            "doi_article",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"DOI (Aufsatz)"),
            ),
        ),
        atapi.StringField(
            "heading__page_number_of_article_in_journal_or_edited_volume",
            schemata="reviewed_text",
            widget=atapi.LabelWidget(
                label=_(
                    u"description_page_number_of_article_in_journal_or_edited_volume",
                    default=(u"Page numbers of the article"),
                )
            ),
        ),
        atapi.IntegerField(
            "pageStartOfArticle",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_start_of_article_in_journal_or_edited_volume"),
            ),
        ),
        atapi.IntegerField(
            "pageEndOfArticle",
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            validators="isInt",
            widget=atapi.IntegerWidget(
                label=_(u"label_page_end_of_article_in_journal_or_edited_volume"),
            ),
        ),
    )
)

ExhibitionSchema = CommonReviewSchema.copy() + atapi.Schema(
    (
        DataGridField(
            "exhibiting_institution",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            columns=("name", "gnd"),
            default=([{"name": "", "gnd": ""}]),
            widget=DataGridWidget(
                label=_(u"Ausstellende Institution"),
                columns={
                    "name": Column(_(u"Ausstellende Institution (z. B. Museum)")),
                    "gnd": Column(_(u"GND der Ausstellenden Institution")),
                },
            ),
            searchable=True,
        ),
        DataGridField(
            "dates",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            columns=("place", "runtime"),
            default=[{"place": "", "runtime": ""}],
            widget=DataGridWidget(
                label=_("Ort, Laufzeit"),
                columns={
                    "place": Column(_(u"Ort")),
                    "runtime": Column(_(u"Laufzeit")),
                },
            ),
            searchable=True,
        ),
        DataGridField(
            "years",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            columns=("year",),
            default=[{"year": ""}],
            widget=DataGridWidget(
                label=_(u"Ausstellungsjahr"),
                columns={"year": Column(_(u"Ausstellungsjahr"))},
            ),
        ),
        DataGridField(
            "exhibiting_organisation",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            columns=("name", "gnd"),
            default=(
                [
                    {
                        "name": "",
                        "gnd": "",
                    }
                ]
            ),
            widget=DataGridWidget(
                label=_(u"Ausstellende Organisation"),
                columns={
                    "name": Column(_(u"Ausstellende Organisation (z. B. Stiftung)")),
                    "gnd": Column(_(u"GND der Ausstellenden Organisation")),
                },
            ),
            searchable=True,
        ),
        atapi.ReferenceField(
            "curators",
            schemata="Ausstellung",
            allowed_types=("Person",),
            vocabulary_factory="recensio.contenttypes.persons",
            multiValued=1,
            referencesSortable=True,
            relationship="curator",
            widget=GNDReferenceBrowserWidget(
                label=_(u"Kurator / Mitwirkende"),
            ),
        ),
        atapi.BooleanField(
            "isPermanentExhibition",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            value=False,
            widget=atapi.BooleanWidget(
                label=_(u"Dauerausstellung"),
            ),
        ),
        atapi.StringField(
            "titleProxy",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Title"),
            ),
        ),
        atapi.StringField(
            "subtitle",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Subtitle"),
            ),
        ),
        atapi.StringField(
            "url_exhibition",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            validators=(isLazyURL,),
            mutator="setUrl_exhibition",
            widget=atapi.StringWidget(
                label=_(u"URL der Ausstellungswebsite"),
            ),
        ),
        atapi.StringField(
            "doi_exhibition",
            schemata="Ausstellung",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"DOI der Ausstellungswebsite"),
            ),
        ),
    )
)


class PublicationLogoWatermarkField(ExtensionField, ImageField):
    """Newspaper/Publication watermark logo #3104"""


class PublicationLicenceField(ExtensionField, atapi.StringField):
    """A licence can be specified for a particular Publication #3105"""


class PublicationExtender(object):
    adapts(IPublication)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = IRecensioLayer

    _fields = [
        PublicationLogoWatermarkField(
            "pdf_watermark",
            widget=atapi.ImageWidget(
                label=_(u"label_publication_pdf_watermark", default=u"PDF watermark"),
                description=_(
                    u"description_publication_pdf_watermark",
                    default=(
                        u"Upload a publication logo for the PDF "
                        "coversheet. Transparent PNG format images "
                        "are recommended."
                    ),
                ),
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields
