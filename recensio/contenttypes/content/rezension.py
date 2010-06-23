from zope.interface import implements

from Products.ATContentTypes.content import base

from recensio.contenttypes.interfaces.rezension import IRezension

class BaseRezension(base.ATCTContent):
    implements(IRezension)

    def listSupportedLanguages(self):
        return self.portal_languages.listSupportedLanguages()
