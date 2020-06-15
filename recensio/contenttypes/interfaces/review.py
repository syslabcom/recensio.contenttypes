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


class IParentGetter(Interface):
    """Get parent of a certain content type"""

    def get_parent_object_of_type(meta_type):
        """
        Return the object of a particular type which is
        the parent of the current object.
        """

    def get_title_from_parent_of_type(meta_type):
        """
        Return the title of the first object of a particular type
        which is a parent of the current object.
        """

    def get_flag_with_override(field_name, override_value):
        """
        Retrieves a boolean field value, allowing for overrides from a parent.
        If any object in the acquisition chain has the override_value set for the
        field specified by field_name, then this value is used. Only if no object
        in the chain has it set is the inverse value used.
        """
