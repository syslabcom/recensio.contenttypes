#-*- coding: utf-8 -*-
"""Definition of the base Review Schemata
"""
from zope.interface import implements

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.validation.interfaces.IValidator import IValidator
from plone.app.blob.field import BlobField
from plone.app.blob.field import ImageField
from zope.i18n import translate
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME

def finalize_recensio_schema(schema, review_type="review"):
    """Custom replacement for schemata.finalizeATCTSchema

    Move fields to the correct schemata and hide fields we don't need

    """

    hidden_fields = ["allowDiscussion", "contributors", "creators",
                     "description", "description", "effectiveDate",
                     "excludeFromNav", "expirationDate",
                     "generatedPdf", "id", "language", "location",
                     "recensioID", "rights"]
    for field in hidden_fields:
        schema.changeSchemataForField(field, "review")
        schema[field].widget.visible={"view":"hidden",
                                      "edit":"hidden"}

    # We can't just hide "relatedItems" as it leads to an error on save:
    #   *  Module Products.Archetypes.ReferenceEngine, line 319, in addReference
    #   ReferenceException: Invalid target UID
    # However, we can delete it.
    schema.delField("relatedItems")

    # Rename the schemata for presentations
    if review_type in ["presentation", "presentation_online"]:
        presented = _(u"presented text")
        if review_type == "presentation_online":
            presented = _(u"presented resource")
        schema_field_names  = [i.getName() for i in schema.fields()]
        for field_name in schema_field_names:
            if schema[field_name].schemata == "review":
                schema.changeSchemataForField(field_name, "presentation")
            else:
                schema.changeSchemataForField(field_name, presented)
            if field_name in ["pageStart", "pageEnd"]:
                schema.changeSchemataForField(field_name, presented)
        # Presentations have some addtional text for labels and descriptions
        if review_type == "presentation":
            schema["title"].widget.description = _(
                u'description_presentation_title',
                default=u"Information on presented work"
                )
        else:
            schema["title"].widget.description = _(
                u'description_presentation_title',
                default=u""
                )
        schema["review"].widget.description = _(
            u'description_presentation_html',
            default=(u"Please give a brief and clear outline of your thesis "
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
                     )
            )
        schema.changeSchemataForField("uri", presented)
        schema["uri"].widget.label = _(u"URL/URN")

    schemata.marshall_register(schema)

AuthorsSchema = atapi.Schema((
    DataGridField(
        'authors',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        columns=("lastname", "firstname"),
        widget=DataGridWidget(
            label = _(u"Authors"),
            columns = {"lastname" : Column(_(u"Last name")),
                       "firstname" : Column(_(u"First name")),
                       }
            ),
        ),
    ))

CoverPictureSchema = atapi.Schema((
    ImageField(
        'coverPicture',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Cover picture"),
            ),
        ),
    ))

ReferenceAuthorsSchema = atapi.Schema((
    DataGridField(
        'referenceAuthors',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        columns=("lastname", "firstname", "email", "address", "phone"),
        widget=DataGridWidget(
            label=_(
    u"label_reference_authors",
    default=(u"Reference Authors (email address, postal address and phone "
             "number are not publicly visible)"
             )
    ),
            columns = {"lastname" : Column(_(u"Lastname")),
                       "firstname" : Column(_(u"Firstname")),
                       "email" : Column(_(u"Email address")),
                       "address" : Column(_(u"Address")),
                       "phone" : Column(_(u"Phone")),
                       },
            description=_(
    u'description_reference_authors',
    default=(u"Which scholarly author's work have you mainly engaged with in "
             "your monograph? Please give us the most detailed information "
             "possible on the &raquo;contemporary&laquo; names amongst them as "
             "the recensio.net editorial team will usually try to inform these "
             "authors of the existence of your monograph, your presentation, "
             "and the chance to comment on it. Only the reference author's "
             "name will be visible to the public. Please name historical "
             "reference authors (e.g. Aristotle, Charles de Gaulle) further "
             "below as subject heading.")
    ),
            ),
        ),
    ))


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
        language = getToolByName(site, 'portal_languages').getPreferredLanguage()
        return translate(_(u'message_ccby_license', 
            default=u"All submitted reviews must be published under the CC-BY licence."),
            target_language=language)

ReviewSchema = atapi.Schema((
    BlobField(
        'pdf',
        schemata=_(u"review"),
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"PDF"),
            visible={"view":"hidden",
                     "edit":"visible"},
            ),
        ),
    BlobField(
        'doc',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Word Document"),
            ),
        ),
        atapi.TextField(
        'customCitation',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Optional citation format"),
            description=_(
    u'description_custom_citation',
    default=(u"Please fill in only if you wish to use a citation format "
             "different from the platform's")
    ),
            rows=3,
            ),
        ),
    ))

PresentationSchema = atapi.Schema((
    atapi.StringField(
        'reviewAuthorHonorific',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        required=True,
        vocabulary=NamedVocabulary("honorifics"),
        widget=atapi.SelectionWidget(
            label=_(u"Honorific Title"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorEmail',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Email address (not publicly visible)"),
            ),
        ),
    atapi.BooleanField(
        'isLicenceApproved',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        value=False,
        required=True,
        validators=(isTrue(),),
        widget=atapi.BooleanWidget(
            label=_(u"Licence Agreement"),
            description=_(
    u'description_ccby_licence_approval',
    default=(u"I agree that my presentation will be published by recensio.net "
             "under the <a "
             "href='http://creativecommons.org/licenses/by-nc-nd/2.0/deed.en' "
             "target='_blank'>"
             "creative-commons-licence Attribution-NonCommercial-"
             "NoDerivs (CC-BY-NC-ND)</a>. Under these conditions, platform "
             "users may use it electronically, distribute it, print it and "
             "provide it for download. The editorial team reserves its right "
             "to change incoming posts (see our user guidelines to this)."
             )
    ),
            )
        )
    ))

# TODO find out how to have a link in the label:
# u"<a href='http://creativecommons.org/licenses/by-nc-nd/3.0/de'>"+\
# u"Namensnennung-Keine kommerzielle Nutzung-Keine Bearbeitung</a> "+\


PageStartEndSchema = atapi.Schema((
    atapi.StringField(
        'pageStart',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Page number (start)"),
            description=_(
    u'description_page_number',
    default=u"Please fill in only if the review is part of a larger pdf-file"
    ),
            ),
        ),
    atapi.StringField(
        'pageEnd',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Page number (end)"),
            ),
        ),
    ))

PagecountSchema = atapi.Schema((
    atapi.StringField(
        'pages',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Pages"),
            ),
        ),
    ))

SerialSchema = atapi.Schema((
    atapi.StringField(
        'series',
        schemata=_(u"reviewed text"),
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Series"),
            ),
        ),
    atapi.StringField(
        'seriesVol',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Series (vol.)"),
            ),
        ),
    ))

BaseReviewSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
# TODO Add LabelWidget to show "Author (review)"
    atapi.StringField(
        'reviewAuthorLastname',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Last name author"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorFirstname',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"First name author"),
            ),
        ),
    atapi.LinesField(
        'languageReview',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Language(s)"),
            size=3,
            ),
        ),
    atapi.LinesField(
        'languageReviewedText',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Language(s)"),
            size=3,
            ),
        ),
    atapi.StringField(
        'recensioID',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            visible={"view":"hidden",
                     "edit":"hidden"},
            ),
        ),
    BlobField(
        'generatedPdf',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Generated Pdf"),
            visible={"view":"hidden",
                     "edit":"hidden"},
            ),
        ),
    atapi.TextField(
        'review',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        default_output_type="text/html",
        widget=atapi.RichWidget(
            label=_(u"HTML"),
            rows=20,
            ),
        ),
    atapi.StringField(
        'uri',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Partner URL"),
            description=_(
    u'description_uri',
    default=u"Please fill in only after consultation with the recensio.net team"
    ),

            ),
        ),
    ))
BaseReviewSchema["title"].schemata = _(u"reviewed text")
BaseReviewSchema.changeSchemataForField('subject', 'reviewed text')
BaseReviewSchema["subject"].schemata = _(u"reviewed text")
BaseReviewSchema["subject"].widget.label = _(u"Subject heading")
BaseReviewSchema["subject"].widget.description = ""


CommonReviewSchema = BaseReviewSchema.copy() + atapi.Schema((
    atapi.LinesField(
        'ddcSubject',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("topic_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Subject classification"),
            size=10,
            ),
        ),
    # Q: DateTimeField ?
    atapi.LinesField(
        'ddcTime',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("epoch_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Time classification"),
            size=10,
            ),
        ),
    atapi.LinesField(
        'ddcPlace',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("region_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Regional classification"),
            size=10,
            ),
        ),
    ))

PrintedReviewSchema = CommonReviewSchema.copy() + \
                      atapi.Schema((
    atapi.StringField(
        'subtitle',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Subtitle"),
            ),
        ),
    # Q: DateTimeField or perhaps IntegerField ?
    atapi.StringField(
        'yearOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Year of publication"),
            ),
        ),
    atapi.StringField(
        'placeOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Place of publication"),
            ),
        ),
    atapi.StringField(
        'publisher',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Publisher"),
            ),
        ),
    atapi.StringField(
        'idBvb',
        schemata=_(u"review"),
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            visible={"view":"hidden",
                     "edit":"hidden"},
            ),
        ),
    ))
# PrintedReviewSchema["title"].required = True

BookReviewSchema = PrintedReviewSchema.copy() + \
                   AuthorsSchema.copy() + \
                   atapi.Schema((
    atapi.StringField(
        'isbn',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISBN"),
            description=_(
    u'description_isbn',
    default=(u"With or without hyphens. In case of several numbers "
             "please choose the hard cover edition.")
    ),
            ),
        ),
    ))
BookReviewSchema["authors"].widget.label=_(u"Author (monograph)")

JournalReviewSchema = schemata.ATContentTypeSchema.copy() + \
                      PrintedReviewSchema.copy() + \
                      atapi.Schema((
    atapi.StringField(
        'issn',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISSN"),
            description=_(
    u'description_issn',
    default=(u"With or without hyphens. In case of several numbers please "
             "choose the hard cover edition.")
    ),

            ),
        ),
    atapi.StringField(
        'shortnameJournal',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Shortname"),
            ),
        ),
    atapi.StringField(
        'volumeNumber',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Vol."),
            ),
        ),
    atapi.StringField(
        'issueNumber',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Number"),
            ),
        ),
    atapi.StringField(
        'officialYearOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Official year of publication (if different)"),
            ),
        ),
    ))
#JournalReviewSchema["authors"].widget.label=_(u"Autor des Aufsatzes")
JournalReviewSchema['yearOfPublication'].widget.label = _(
    u"Actual year of publication")
