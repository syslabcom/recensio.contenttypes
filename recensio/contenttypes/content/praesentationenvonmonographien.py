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
    untertitel = atapi.ATFieldProperty('untertitel')
    erscheinungsjahr = atapi.ATFieldProperty('erscheinungsjahr')
    erscheinungsort = atapi.ATFieldProperty('erscheinungsort')
    verlag = atapi.ATFieldProperty('verlag')
    verbundID = atapi.ATFieldProperty('verbundID')
    trefferdaten = atapi.ATFieldProperty('trefferdaten')
    authors = atapi.ATFieldProperty('authors')
    isbn = atapi.ATFieldProperty('isbn')
    bezugsautoren = atapi.ATFieldProperty('bezugsautoren')
    url = atapi.ATFieldProperty('url')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    rezension = atapi.ATFieldProperty('rezension')

atapi.registerType(PraesentationenvonMonographien, PROJECTNAME)
