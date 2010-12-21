from plone.app.folder import folder


class Container(folder.ATFolder):
    """ A class that extends ATFolder but acts language-neutral.
    We make sure, by subclassing plone.app.folder's base class and
    not ATContentType's, that ITranslatable is not implemented"""

    def Language(self):
        """ This content is neutral """
        return ""
