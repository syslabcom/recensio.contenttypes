"""Definition of the Rezension content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from recensio.contenttypes.interfaces import IRezension
from recensio.contenttypes.config import PROJECTNAME

RezensionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

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
