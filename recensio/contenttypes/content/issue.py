"""Definition of the Issue content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from recensio.contenttypes.interfaces import IIssue
from recensio.contenttypes.config import PROJECTNAME

IssueSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

IssueSchema['title'].storage = atapi.AnnotationStorage()
IssueSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    IssueSchema,
    folderish=True,
    moveDiscussion=False
)


class Issue(folder.ATFolder):
    """A container for Publication issues"""
    implements(IIssue)

    meta_type = "Issue"
    schema = IssueSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Issue, PROJECTNAME)
