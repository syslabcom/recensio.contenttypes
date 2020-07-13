"""Definition of the Volume content type
"""

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content import container
from recensio.contenttypes.content.schemata import LicenceSchema
from recensio.contenttypes.content.schemata import URLInCitationSchema
from recensio.contenttypes.interfaces import IVolume
from recensio.contenttypes.interfaces.review import IParentGetter
from zope.interface import implements

DoiSettingsSchema = atapi.Schema(
    (
        atapi.BooleanField(
            "doiRegistrationActive",
            accessor="isDoiRegistrationActive",
            storage=atapi.AnnotationStorage(),
            default=True,
            widget=atapi.BooleanWidget(
                label=_(u"Activate DOI registration"),
                description=_(
                    u"description_activate_doi_registration",
                    default=(u"Activates the registration of DOIs at da|ra"),
                ),
            ),
        ),
    )
)

FulltextSettingsSchema = atapi.Schema(
    (
        atapi.BooleanField(
            "useExternalFulltext",
            accessor="isUseExternalFulltext",
            storage=atapi.AnnotationStorage(),
            default=False,
            widget=atapi.BooleanWidget(
                label=_(u"Use external full text"),
                description=_(
                    u"description_use_external_full_text",
                    default=(
                        u"Don't show the full text of contained reviews "
                        "directly but link to the external source instead."
                    ),
                ),
            ),
        ),
    )
)

VolumeSchema = (
    folder.ATFolderSchema.copy()
    + DoiSettingsSchema.copy()
    + FulltextSettingsSchema.copy()
    + URLInCitationSchema.copy()
    + atapi.Schema(
        (
            atapi.StringField(
                "yearOfPublication",
                storage=atapi.AnnotationStorage(),
                widget=atapi.StringWidget(
                    label=_(
                        u"label_metadata_official_year_of_publication",
                        default=u"Official year of publication",
                    ),
                ),
            ),
        )
    )
    + LicenceSchema.copy()
)

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

VolumeSchema["title"].storage = atapi.AnnotationStorage()
VolumeSchema["description"].storage = atapi.AnnotationStorage()
VolumeSchema["URLShownInCitationNote"].schemata = "default"
VolumeSchema["labelURLShownInCitationNote"].schemata = "default"

schemata.finalizeATCTSchema(VolumeSchema, folderish=True, moveDiscussion=False)


class Volume(container.Container):
    """A container for volumes of a particular Publication / magazine"""

    implements(IVolume)

    meta_type = "Volume"
    schema = VolumeSchema

    title = atapi.ATFieldProperty("title")
    description = atapi.ATFieldProperty("description")

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    doiRegistrationActive = atapi.ATFieldProperty("doiRegistrationActive")
    useExternalFulltext = atapi.ATFieldProperty("useExternalFulltext")

    def isURLShownInCitationNote(self):
        """ If any parent has this deactivated then we also want it inactive here.
            SCR-341
        """
        return IParentGetter(self).get_flag_with_override(
            "URLShownInCitationNote", False
        )


atapi.registerType(Volume, PROJECTNAME)
