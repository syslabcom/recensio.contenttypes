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
        vocabulary=("Monographie", "Zeitscrift"),
        widget=atapi.SelectionWidget(
            label=_(u"Rezension Type"),
            description=_(u"Rezension einer Monographie, Zeitscrift, usw."),
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
        'praesentiertenScriftTextsprache',
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

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

RezensionSchema['title'].storage = atapi.AnnotationStorage()
RezensionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RezensionSchema, moveDiscussion=False)


class Rezension(base.ATCTContent):
    """Review Content Type"""
    implements(IRezension)

    meta_type = "Rezension"
    schema = RezensionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Rezension, PROJECTNAME)
