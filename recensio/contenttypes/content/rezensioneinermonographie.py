"""Definition of the Rezension einer Monographie content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.interfaces import IRezensioneinerMonographie
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import BookRezensionSchema
from recensio.contenttypes.content.schemata import InternetSchema

RezensioneinerMonographieSchema = BookRezensionSchema.copy() + \
                                  BezugsautorenSchema.copy() + \
                                  InternetSchema.copy()

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

atapi.registerType(RezensioneinerMonographie, PROJECTNAME)
