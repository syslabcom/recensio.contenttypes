"""Definition of the Rezension einer Monographie content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.interfaces import IRezensioneinerMonographie
from recensio.contenttypes.content.schemata import BookRezensionSchema
from recensio.contenttypes.content.schemata import SerialSchema

RezensioneinerMonographieSchema = BookRezensionSchema.copy() + \
                                  SerialSchema.copy()

schemata.finalizeATCTSchema(RezensioneinerMonographieSchema,
                            moveDiscussion=False)

RezensioneinerMonographieSchema['title'].storage = atapi.AnnotationStorage()
RezensioneinerMonographieSchema['description'].storage = \
                                                       atapi.AnnotationStorage()


class RezensioneinerMonographie(base.ATCTContent):
    """Rezension einer Monographie"""
    implements(IRezensioneinerMonographie)

    meta_type = "RezensioneinerMonographie"
    schema = RezensioneinerMonographieSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
    # Printed = Common +
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

    # Printed
    untertitel = atapi.ATFieldProperty('untertitel')
    erscheinungsjahr = atapi.ATFieldProperty('erscheinungsjahr')
    erscheinungsort = atapi.ATFieldProperty('erscheinungsort')
    verlag = atapi.ATFieldProperty('verlag')
    verbundID = atapi.ATFieldProperty('verbundID')
    trefferdaten = atapi.ATFieldProperty('trefferdaten')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # isbn
    isbn = atapi.ATFieldProperty('isbn')

    # Serial
    reihe = atapi.ATFieldProperty('reihe')
    reihennummer = atapi.ATFieldProperty('reihennummer')

atapi.registerType(RezensioneinerMonographie, PROJECTNAME)
