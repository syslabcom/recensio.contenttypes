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
