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

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME


AuthorsSchema = atapi.Schema((
    DataGridField(
        'authors',
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
        storage=atapi.AnnotationStorage(),
        widget=atapi.ImageWidget(
            label=_(u"Cover picture"),
            ),
        ),
    ))

InternetSchema = atapi.Schema((
    atapi.StringField(
        'url',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"URL"),
            ),
        ),
    ))

ReferenceAuthorsSchema = atapi.Schema((
    DataGridField(
        'referenceAuthors',
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
        return _(u"All submitted reviews must be published under the CC-BY licence.")

PresentationSchema = atapi.Schema((
    atapi.BooleanField(
        'isLicenceApproved',
        storage=atapi.AnnotationStorage(),
        value=False,
        validators=(isTrue(),),
        widget=atapi.BooleanWidget(
            label=_(
    u"Ich bin damit einverstanden, dass meine Präsentation von recensio.net"+\
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
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Page number (start)"),
            ),
        ),
    atapi.StringField(
        'pageEnd',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Page number (end)"),
            ),
        ),
    ))

PagecountSchema = atapi.Schema((
    atapi.StringField(
        'pages',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Pages"),
            ),
        ),
    ))

SerialSchema = atapi.Schema((
    atapi.StringField(
        'series',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Reihe"),
            ),
        ),
    atapi.StringField(
        'seriesVol',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Reihenvolume"),
            ),
        ),
    ))

BaseReviewSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        'reviewAuthorHonorific',
        storage=atapi.AnnotationStorage(),
        required=True,
        vocabulary=NamedVocabulary("honorifics"),
        widget=atapi.SelectionWidget(
            label=_(u"Honorific Title"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorLastname',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Lastname"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorFirstname',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Firstname"),
            ),
        ),
    atapi.StringField(
        'reviewAuthorEmail',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Email"),
            ),
        ),
    atapi.StringField(
        'languageReview',
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Textsprache der präsentierten Schrift"),
            size=3,
            ),
        ),
    atapi.StringField(
        'languagePresentation',
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Textsprache der Präsentation"),
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
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"PDF"),
            ),
        ),
    BlobField(
        'doc',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Word Document"),
            ),
        ),
    atapi.TextField(
        'review',
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"Review"),
            rows=20,
            ),
        ),
    atapi.TextField(
        'customCitation',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Citation"),
            description=_(
    u"A default citation is generated automatically. To use a custom "+\
    u"citation instead, add the required text here"),
            rows=3,
            ),
        ),
    atapi.StringField(
        'urn',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"URN"),
            ),
        ),
    ))

CommonReviewSchema = BaseReviewSchema.copy() + atapi.Schema((
    atapi.LinesField(
        'ddcPlace',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("region_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"ddc raum"),
            size=10,
            ),
        ),
    atapi.LinesField(
        'ddcSubject',
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
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary("epoch_values"),
        widget=atapi.MultiSelectionWidget(
            label=_(u"ddc zeit"),
            size=10,
            ),
        ),
    ))

PrintedReviewSchema = CommonReviewSchema.copy() + atapi.Schema((
    atapi.StringField(
        'subtitle',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Untertitel"),
            ),
        ),
    # Q: DateTimeField or perhaps IntegerField ?
    atapi.StringField(
        'yearOfPublication',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsjahr"),
            ),
        ),
    atapi.StringField(
        'placeOfPublication',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsort"),
            ),
        ),
    atapi.StringField(
        'publisher',
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
    atapi.StringField(
        'searchresults',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Zitation"),
            ),
        ),

    ))
# PrintedReviewSchema["title"].required = True

BookReviewSchema = PrintedReviewSchema.copy() + \
                   AuthorsSchema.copy() + \
                   atapi.Schema((
    atapi.StringField(
        'isbn',
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
    # Authors label is "Autor des Aufsatzes"
    atapi.StringField(
        'issn',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISSN"),
            ),
        ),
    atapi.StringField(
        'officialYearOfPublication',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Gezähltes Jahr"),
            ),
        ),
    ))
JournalReviewSchema["authors"].widget.label=_(u"Autor des Aufsatzes")

