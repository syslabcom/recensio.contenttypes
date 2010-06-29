# -*- coding: utf-8 -*-
"""Definition of the base Review Schemata
"""
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from plone.app.blob.field import BlobField

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME


AuthorsSchema = atapi.Schema((
    atapi.LinesField(
        'authors',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.LinesWidget(
            label=_(u"Authors"),
            rows=3,
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

BezugsautorenSchema = atapi.Schema((
    atapi.StringField(
        'referenceAuthors',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Bezugsautoren"),
            ),
        ),
    ))

SeitenzahlSchema = atapi.Schema((
    atapi.StringField(
        'pages',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Seitenzahl"),
            ),
        ),
    ))

SerialSchema = SeitenzahlSchema.copy() + atapi.Schema((
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
        'reviewAuthor',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Autor der Review"),
            ),
        ),
    atapi.StringField(
        'languageReview',
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.SelectionWidget(
            label=_(u"Textsprache der präsentierten Schrift"),
            ),
        ),
    atapi.StringField(
        'languagePresentation',
        storage=atapi.AnnotationStorage(),
        vocabulary="listSupportedLanguages",
        widget=atapi.SelectionWidget(
            label=_(u"Textsprache der Präsentation"),
            ),
        ),
    atapi.StringField(
        'recensioID',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Recensio ID"),
            ),
        ),
    atapi.StringField(
        'subject',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Schlagwörter"),
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
            ),
        )
    ))

CommonReviewSchema = BaseReviewSchema.copy() + atapi.Schema((
    atapi.StringField(
        'ddcPlace',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc raum"),
            ),
        ),
    atapi.StringField(
        'ddcSubject',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc sach"),
            ),
        ),
    # Q: DateTimeField ?
    atapi.StringField(
        'ddcTime',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc zeit"),
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
            ),
        ),
    atapi.StringField(
        'searchresults',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Trefferdaten"),
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
        'number',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Heftvolume"),
            ),
        ),
    atapi.StringField(
        'shortnameJournal',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Kürzel Zeitschrift"),
            ),
        ),
    atapi.StringField(
        'volume',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Nummer"),
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
