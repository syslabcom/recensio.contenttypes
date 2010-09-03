from zope.interface import Interface
# -*- Additional Imports Here -*-


class IReview(Interface):
    """Review Content Type"""

    def getAllAuthorData(self):
        """
        Return a string with all possible authors,
        inclusive the document owner
        """

    # -*- schema definition goes here -*-

class IReviewPDF(Interface):
    """Review with PDF data"""

    def generateImage(self):
        """
        generate a cover image from pdf data
        """

    def generatePageImages(self):
        """
        generate an image for each page of the pdf
        """
