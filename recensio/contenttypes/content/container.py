from Products.ATContentTypes.content import folder

class Container(folder.ATFolder):
    """ A class that extends ATFolder but acts language-neutral """

    def Language(self):
        """ This content is neutral """
        return ""