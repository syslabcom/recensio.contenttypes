"""Definition of the Issue content type
"""

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content import container
from recensio.contenttypes.content.schemata import LicenceSchema
from recensio.contenttypes.content.schemata import URLInCitationSchema
from recensio.contenttypes.content.volume import DoiSettingsSchema
from recensio.contenttypes.content.volume import FulltextSettingsSchema
from recensio.contenttypes.interfaces import IIssue
from recensio.contenttypes.interfaces.review import IParentGetter
from zope.interface import implements

# -*- Message Factory Imported Here -*-


IssueSchema = (
    folder.ATFolderSchema.copy()
    + DoiSettingsSchema.copy()
    + FulltextSettingsSchema.copy()
    + URLInCitationSchema.copy()
    + LicenceSchema.copy()
    + atapi.Schema(
        (
            # -*- Your Archetypes field definitions here ... -*-
        )
    )
)

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

IssueSchema["title"].storage = atapi.AnnotationStorage()
IssueSchema["description"].storage = atapi.AnnotationStorage()
IssueSchema["URLShownInCitationNote"].schemata = "default"
IssueSchema["labelURLShownInCitationNote"].schemata = "default"

schemata.finalizeATCTSchema(IssueSchema, folderish=True, moveDiscussion=False)


class Issue(container.Container):
    """A container for Publication issues"""

    implements(IIssue)

    meta_type = "Issue"
    schema = IssueSchema

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


atapi.registerType(Issue, PROJECTNAME)
