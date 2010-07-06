from zope.interface import implements

from Products.ATContentTypes.content import base

from recensio.contenttypes.interfaces.review import IReview

class BaseReview(base.ATCTContent):
    implements(IReview)

    def listSupportedLanguages(self):
        return self.portal_languages.listSupportedLanguages()

    def setIsLicenceApproved(self, value):
        """
        The user needs to check the box every time they change the
        review to ensure they approve of the licence, so we don't want
        to save the value.
        """
        pass
