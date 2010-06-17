# -*- coding: utf-8 -*-
"""Definition of the Rezension content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.interfaces import IRezension
from recensio.contenttypes.config import PROJECTNAME

RezensionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.LinesField(
        'rezensionType',
        storage=atapi.AnnotationStorage(),
        required=True,
        vocabulary=(u"Monographie", u"Zeitschrift",
                    u"Präsentationen von Monographien",
                    u"Präsentationen von Aufsatz in Sammelband",
                    u"Präsentationenvon Aufsatz in Zeitschrift",
                    u"Präsentationen von Internetressourcen",
                    u"Kommentar"),
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
    # May have multiple authors
    atapi.LinesField(
        'autorDesBuchs',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u"Author des Buchs"),
            rows=3,
        ),
    ),
    atapi.StringField(
        'titel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Titel"),
        ),
    ),
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
        'reihe',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Reihe"),
        ),
    ),
    atapi.StringField(
        'reihennummer',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Reihennummer"),
        ),
    ),
    atapi.StringField(
        'seitenzahl',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Seitenzahl"),
        ),
    ),
    atapi.StringField(
        'isbn',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"ISBN"),
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
    atapi.StringField(
        'schlagwoerter',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Schlagwörter"),
        ),
    ),
))

RezensionSchema['title'].storage = atapi.AnnotationStorage()
RezensionSchema['description'].storage = atapi.AnnotationStorage()

common_fields = ['rezensionType', 'rezensionAutor',
                 'praesentiertenSchriftTextsprache',
                 'praesentationTextsprache', 'recensioID', 'autorDesBuchs',
                 'titel', 'untertitel', 'erscheinungsjahr', 'erscheinungsort',
                 'verlag', 'reihe', 'reihennummer', 'seitenzahl', 'isbn',
                 'ddcSach', 'ddcZeit', 'schlagwoerter']


fields = {
    u"common" : ['rezensionType', 'rezensionAutor',
                'praesentiertenSchriftTextsprache',
                'praesentationTextsprache', 'recensioID',
                'autorDesBuchs', 'titel', 'untertitel',
                'erscheinungsjahr', 'erscheinungsort', 'verlag',
                'reihe', 'reihennummer', 'seitenzahl', 'isbn',
                'ddcSach', 'ddcZeit', 'schlagwoerter'],
    u"Monographie" : [],
    u"Zeitschrift" : [],
    u"Präsentationen von Monographien" : [],
    u"Präsentationen von Aufsatz in Sammelband" : [],
    u"Präsentationenvon Aufsatz in Zeitschrift" : [],
    u"Präsentationen von Internetressourcen" : [],
    u"Kommentar": []
    }

for field in sum(fields.values(), []):
    RezensionSchema[field].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RezensionSchema, moveDiscussion=False)


class Rezension(base.ATCTContent):
    """Review Content Type"""
    implements(IRezension)

    meta_type = "Rezension"
    schema = RezensionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    rezensionType = atapi.ATFieldProperty('rezensionType')
    rezensionAutor = atapi.ATFieldProperty('rezensionAutor')
    praesentiertenSchriftTextsprache = atapi.ATFieldProperty(
        'praesentiertenSchriftTextsprache')
    praesentationTextsprache = atapi.ATFieldProperty('praesentationTextsprache')
    recensioID = atapi.ATFieldProperty('recensioID')
    autorDesBuchs = atapi.ATFieldProperty('autorDesBuchs')
    titel = atapi.ATFieldProperty('titel')
    untertitel = atapi.ATFieldProperty('untertitel')
    erscheinungsjahr = atapi.ATFieldProperty('erscheinungsjahr')
    erscheinungsort = atapi.ATFieldProperty('erscheinungsort')
    verlag = atapi.ATFieldProperty('verlag')
    reihe = atapi.ATFieldProperty('reihe')
    reihennummer = atapi.ATFieldProperty('reihennummer')
    seitenzahl = atapi.ATFieldProperty('seitenzahl')
    isbn = atapi.ATFieldProperty('isbn')
    ddcSach = atapi.ATFieldProperty('ddcSach')
    ddcZeit = atapi.ATFieldProperty('ddcZeit')
    schlagwoerter = atapi.ATFieldProperty('schlagwoerter')

    def get_displayed_fields_by_rezension_type(self):
        return fields["common"] + fields[self.rezensionType]

atapi.registerType(Rezension, PROJECTNAME)
