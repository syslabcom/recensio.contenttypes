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


def hide_unused_fields(schema):
    """Move the default fields which we don't use to the"default"
    schemata and hide them.
    """
    for field in ["allowDiscussion", "contributors", "creators",
                  "description", "description", "effectiveDate",
                  "excludeFromNav", "expirationDate", "generatedPdf",
                  "id", "idBvb", "language", "location", "recensioID",
                  "relatedItems", "rights", "subject"]:
        schema.changeSchemataForField(field, "review")
        schema[field].widget.visible={"view":"hidden",
                               "edit":"hidden"}

AuthorsSchema = atapi.Schema((
    DataGridField(
        'authors',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        columns=("lastname", "firstname"),
        widget=DataGridWidget(
            label = _(u"Authors"),
            columns = {"lastname" : Column(_(u"Lastname")),
                       "firstname" : Column(_(u"Firstname")),
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
            label=_(u"Reference Authors"),
            columns = {"lastname" : Column(_(u"Lastname")),
                       "firstname" : Column(_(u"Firstname")),
                       "email" : Column(_(u"Email")),
                       "address" : Column(_(u"Address")),
                       "phone" : Column(_(u"Phone")),
                       }
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
            label=_(u"Email"),
            ),
        ),
    atapi.BooleanField(
        'isLicenceApproved',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        value=False,
        validators=(isTrue(),),
        widget=atapi.BooleanWidget(
            label=_(u'text_ccby_license_approval',
    default=u"Ich bin damit einverstanden, dass meine Präsentation von recensio.net"+\
    u"unter der Creative-Commons-Lizenz "+\
    u"Namensnennung-Keine kommerzielle Nutzung-Keine Bearbeitung "+\
    u"(CC-BY-NC-ND) publiziert wird. Sie darf"+\
    u"unter diesen Bedingungen von Plattformnutzern elektronisch"+\
    u"benutzt, übermittelt, ausgedruckt und zum Download bereitgestellt"+\
    u"werden."),
            ),
        ),
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
            label=_(u"Reihe"),
            ),
        ),
    atapi.StringField(
        'seriesVol',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Reihenvolume"),
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
            label=_(u"Lastname"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorFirstname',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Firstname"),
            ),
        ),
    atapi.LinesField(
        'languageReview',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Textsprache der Präsentation"),
            size=3,
            ),
        ),
    atapi.LinesField(
        'languageReviewedText',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Textsprache der präsentierten Schrift"),
            size=3,
            ),
        ),
    atapi.StringField(
        'recensioID',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Recensio ID"),
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
        'review',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        default_output_type="text/html",
        widget=atapi.RichWidget(
            label=_(u"Text"),
            rows=20,
            ),
        ),
    atapi.TextField(
        'customCitation',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Citation"),
            description=_(u'description_custom_citation',
    default=u"A default citation is generated automatically. To use a custom "+\
    u"citation instead, add the required text here"),
            rows=3,
            ),
        ),
    atapi.StringField(
        'uri',
        schemata="review", 
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"URI"),
            ),
        ),
    ))
BaseReviewSchema["title"].schemata = _(u"reviewed text")

CommonReviewSchema = BaseReviewSchema.copy() + atapi.Schema((
    atapi.LinesField(
        'ddcPlace',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("region_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"ddc raum"),
            size=10,
            ),
        ),
    atapi.LinesField(
        'ddcSubject',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("topic_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"ddc sach"),
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
            label=_(u"ddc zeit"),
            size=10,
            ),
        ),
    ))

PrintedReviewSchema = CommonReviewSchema.copy() + \
                      CoverPictureSchema.copy() + atapi.Schema((
    atapi.StringField(
        'subtitle',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Untertitel"),
            ),
        ),
    # Q: DateTimeField or perhaps IntegerField ?
    atapi.StringField(
        'yearOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsjahr"),
            ),
        ),
    atapi.StringField(
        'placeOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsort"),
            ),
        ),
    atapi.StringField(
        'publisher',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Verlag"),
            ),
        ),
    atapi.StringField(
        'idBvb',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Verbund ID"),
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
            ),
        ),
    ))
BookReviewSchema["authors"].widget.label=_(u"Autor des Buchs")

JournalReviewSchema = schemata.ATContentTypeSchema.copy() + \
                         AuthorsSchema.copy() + \
                         PrintedReviewSchema.copy() + \
                         atapi.Schema((
    atapi.StringField(
        'shortnameJournal',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Shortname (Journal)"),
            ),
        ),
    atapi.StringField(
        'issn',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISSN"),
            ),
        ),
    atapi.StringField(
        'officialYearOfPublication',
        schemata="reviewed text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Gezähltes Jahr"),
            ),
        ),
    ))
JournalReviewSchema["authors"].widget.label=_(u"Autor des Aufsatzes")
