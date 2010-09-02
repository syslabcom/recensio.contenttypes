"""Definition of the Publication content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.GenericSetup.interfaces import IDAVAware
from recensio.contenttypes.content import container

# -*- Message Factory Imported Here -*-

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.interfaces import IPublication
from recensio.contenttypes.config import PROJECTNAME

PublicationSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.TextField(
        'long_description',
        storage=atapi.AnnotationStorage(),
        required=True,
        default_output_type="text/html",
        widget=atapi.RichWidget(
            label=_('Beschreibung'),
            rows=20,
        ),
    ),

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

PublicationSchema['title'].storage = atapi.AnnotationStorage()
PublicationSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    PublicationSchema,
    folderish=True,
    moveDiscussion=False
)


class Publication(container.Container):
    """A container for journals of a particular magazine"""
    implements(IPublication, IDAVAware)

    meta_type = "Publication"
    schema = PublicationSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Publication, PROJECTNAME)
