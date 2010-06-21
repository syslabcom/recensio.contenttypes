"""Definition of the Praesentationen von Internetressourcen content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from recensio.contenttypes.interfaces import \
     IPraesentationenvonInternetressourcen
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import CommonRezensionSchema
from recensio.contenttypes.content.schemata import InternetSchema

PraesentationenvonInternetressourcenSchema = CommonRezensionSchema.copy() + \
                                             InternetSchema.copy() + \
                                             atapi.Schema((
    atapi.StringField(
        'institution',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Institution"),
        ),
    ),
    atapi.StringField(
        'dokumentartenzurMehrfachauswahl',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Dokumentarten zur Mehrfachauswahl"),
        ),
    ),
))

PraesentationenvonInternetressourcenSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationenvonInternetressourcenSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonInternetressourcenSchema,
                            moveDiscussion=False)


class PraesentationenvonInternetressourcen(base.ATCTContent):
    """Praesentationen von Internetressourcen"""
    implements(IPraesentationenvonInternetressourcen)

    meta_type = "PraesentationenvonInternetressourcen"
    schema = PraesentationenvonInternetressourcenSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Common = Base +

    # Base
    rezensionAutor = atapi.ATFieldProperty('rezensionAutor')
    praesentiertenSchriftTextsprache = atapi.ATFieldProperty(
        'praesentiertenSchriftTextsprache')
    praesentationTextsprache = atapi.ATFieldProperty('praesentationTextsprache')
    recensioID = atapi.ATFieldProperty('recensioID')
    schlagwoerter = atapi.ATFieldProperty('schlagwoerter')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    rezension = atapi.ATFieldProperty('rezension')

    # Common
    ddcRaum = atapi.ATFieldProperty('ddcRaum')
    ddcSach = atapi.ATFieldProperty('ddcSach')
    ddcZeit = atapi.ATFieldProperty('ddcZeit')
 
    # Internet
    url = atapi.ATFieldProperty('url')

atapi.registerType(PraesentationenvonInternetressourcen, PROJECTNAME)
