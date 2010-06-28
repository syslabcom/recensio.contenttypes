from zope.interface import implements

from Products.ATContentTypes.content import base

from recensio.contenttypes.interfaces.review import IReview

class BaseReview(base.ATCTContent):
    implements(IReview)

    def listSupportedLanguages(self):
        return self.portal_languages.listSupportedLanguages()
