"""Definition of the Volume content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from recensio.contenttypes.content import container

from recensio.contenttypes import contenttypesMessageFactory as _

from recensio.contenttypes.interfaces import IVolume
from recensio.contenttypes.config import PROJECTNAME

VolumeSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    atapi.StringField(
        'yearOfPublication',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Year of publication"),
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

VolumeSchema['title'].storage = atapi.AnnotationStorage()
VolumeSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    VolumeSchema,
    folderish=True,
    moveDiscussion=False
)


class Volume(container.Container):
    """A container for volumes of a particular Publication / magazine"""
    implements(IVolume)

    meta_type = "Volume"
    schema = VolumeSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Volume, PROJECTNAME)
