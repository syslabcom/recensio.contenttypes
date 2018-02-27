# -*- coding: utf-8 -*-
"""Definition of the Publication content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from recensio.contenttypes.content import container
from recensio.contenttypes.content.schemata import LicenceSchema

# -*- Message Factory Imported Here -*-

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.interfaces import IPublication
from recensio.contenttypes.config import PROJECTNAME

PublicationSchema = folder.ATFolderSchema.copy() + \
    atapi.Schema((

    atapi.BooleanField(
        'useCanonicalUriForBVID',
        accessor='isUseCanonicalUriForBVID',
        storage=atapi.AnnotationStorage(),
        default=False,
        widget=atapi.BooleanWidget(
            label=_(u"Original-URL für BVID-Export"),
            description=_(
                u'description_use_canonical_for_bvid',
                default=(u"Benutze die Original-URL von Rezensionen dieser "
                         "Zeitschrift im BVID-Export. Ist diese Option "
                         "deaktiviert wird die recensio.net-URL verwendet."),
            ),
        ),
    ),

)) + LicenceSchema.copy()

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
    implements(IPublication)

    meta_type = "Publication"
    schema = PublicationSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    useCanonicalUriForBVID = atapi.ATFieldProperty('useCanonicalUriForBVID')

atapi.registerType(Publication, PROJECTNAME)
