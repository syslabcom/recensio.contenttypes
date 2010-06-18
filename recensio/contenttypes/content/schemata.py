# -*- coding: utf-8 -*-
"""Definition of the base Rezension Schemata
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

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
        widget=atapi.TextWidget(
            label=_(u"URL"),
            ),
        ),
    ))

BezugsautorenSchema = atapi.Schema((
    atapi.StringField(
        'bezugsautoren',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextWidget(
            label=_(u"Bezugsautoren"),
            ),
        ),
    ))

ZeitenzahlSchema = atapi.Schema((
    atapi.StringField(
        'zeitenzahl',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextWidget(
            label=_(u"Zeitenzahl"),
            ),
        ),
    ))

SerialSchema = ZeitenzahlSchema.copy() + atapi.Schema((
    atapi.StringField(
        'reihe',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextWidget(
            label=_(u"Reihe"),
            ),
        ),
    atapi.StringField(
        'reihennummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextWidget(
            label=_(u"Reihennummer"),
            ),
        ),
    ))

BaseRezensionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.LinesField(
        'rezensionType',
        storage=atapi.AnnotationStorage(),
        required=True,
        vocabulary=("rm", "rz", "pm", "pasb", "paz", "kommentar"),
        widget=atapi.SelectionWidget(
            label=_(u"Typ der Rezension"),
            description=_(u"Rezension einer Monographie, Zeitschrift, usw."),
            format="select",
            ),
        ),
    atapi.StringField(
        'rezensionAutor',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Autor der Rezension"),
            ),
        ),
    atapi.StringField(
        'praesentiertenSchriftTextsprache',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Textsprache der präsentierten Schrift"),
            ),
        ),
    atapi.StringField(
        'praesentationTextsprache',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
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
        'schlagwoerter',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Schlagwörter"),
            ),
        ),
    ))

CommonRezensionSchema = BaseRezensionSchema.copy() + atapi.Schema((
    atapi.StringField(
        'ddcRaum',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc raum"),
            ),
        ),
    atapi.StringField(
        'ddcSach',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc sach"),
            ),
        ),
    # Q: DateTimeField ?
    atapi.StringField(
        'ddcZeit',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ddc zeit"),
        ),
        ),
    ))

PrintedRezensionSchema = CommonRezensionSchema.copy() + atapi.Schema((
    atapi.StringField(
        'untertitel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Untertitel"),
            ),
        ),
    # Q: DateTimeField or perhaps IntegerField ?
    atapi.StringField(
        'erscheinungsjahr',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsjahr"),
            ),
        ),
    atapi.StringField(
        'erscheinungsort',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Erscheinungsort"),
            ),
        ),
    atapi.StringField(
        'verlag',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Verlag"),
            ),
        ),
    atapi.StringField(
        'verbundID',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Verbund ID"),
            ),
        ),
    atapi.StringField(
        'trefferdaten',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Trefferdaten"),
            ),
        ),

    ))
PrintedRezensionSchema["title"].required = True

BookRezensionSchema = AuthorsSchema.copy() + \
                      PrintedRezensionSchema.copy() + \
                      atapi.Schema((
    atapi.StringField(
        'isbn',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISBN"),
            ),
        ),
    ))
# TODO check this works:
#BookRezensionSchema["authors"].widget.label=_(u"Autor des Buchs")

JournalRezensionSchema = AuthorsSchema.copy() + \
                         PrintedRezensionSchema.copy() + \
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
        'heftnummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Heftnummer"),
            ),
        ),
    atapi.StringField(
        'kuerzelZeitschrift',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Kürzel Zeitschrift"),
            ),
        ),
    atapi.StringField(
        'nummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Nummer"),
            ),
        ),
    atapi.StringField(
        'gazaehltesJahr',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Gezähltes Jahr"),
            ),
        ),
    ))
# TODO check this works:
# JournalSchema["authors"].widget.label=_(u"Autor des Aufsatzes")
