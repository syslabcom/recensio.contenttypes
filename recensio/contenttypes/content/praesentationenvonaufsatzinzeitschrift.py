"""Definition of the Praesentationen von Aufsatz in Zeitschrift content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IPraesentationenvonAufsatzinZeitschrift
from recensio.contenttypes.config import PROJECTNAME

PraesentationenvonAufsatzinZeitschriftSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((


))

PraesentationenvonAufsatzinZeitschriftSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationenvonAufsatzinZeitschriftSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonAufsatzinZeitschriftSchema,
                            moveDiscussion=False)


class PraesentationenvonAufsatzinZeitschrift(base.ATCTContent):
    """Praesentationen von Aufsatz in Zeitschrift"""
    implements(IPraesentationenvonAufsatzinZeitschrift)

    meta_type = "PraesentationenvonAufsatzinZeitschrift"
    schema = PraesentationenvonAufsatzinZeitschriftSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(PraesentationenvonAufsatzinZeitschrift, PROJECTNAME)
