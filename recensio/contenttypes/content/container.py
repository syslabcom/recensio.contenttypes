from plone.app.folder import folder
from Products.CMFCore.utils import getToolByName


class Container(folder.ATFolder):
    """A class that extends ATFolder but acts language-neutral.
    We make sure, by subclassing plone.app.folder's base class and
    not ATContentType's, that ITranslatable is not implemented"""

    def Language(self):
        """This content is neutral"""
        return ""

    def getTranslations(
        self, include_canonical=True, review_state=True, _is_canonical=None
    ):
        workflow_tool = getToolByName(self, "portal_workflow", None)
        if review_state:
            try:
                state = workflow_tool.getInfoFor(self, "review_state", None)
            except AttributeError:
                state = None
            return {"": [self, state]}
        else:
            return {"": self}
