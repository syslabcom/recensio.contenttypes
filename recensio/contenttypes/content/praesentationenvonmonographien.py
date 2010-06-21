"""Definition of the Praesentationen von Monographien content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import BookRezensionSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.interfaces import IPraesentationenvonMonographien

PraesentationenvonMonographienSchema = BookRezensionSchema.copy() + \
                                       BezugsautorenSchema.copy() + \
                                       InternetSchema.copy()


PraesentationenvonMonographienSchema['title'].storage = \
                                                      atapi.AnnotationStorage()
PraesentationenvonMonographienSchema['description'].storage = \
                                                      atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonMonographienSchema,
                            moveDiscussion=False)


class PraesentationenvonMonographien(base.ATCTContent):
    """Praesentationen von Monographien"""
    implements(IPraesentationenvonMonographien)

    meta_type = "PraesentationenvonMonographien"
    schema = PraesentationenvonMonographienSchema

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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Bezugsautoren
    bezugsautoren = atapi.ATFieldProperty('bezugsautoren')

    # Internet
    url = atapi.ATFieldProperty('url')

atapi.registerType(PraesentationenvonMonographien, PROJECTNAME)