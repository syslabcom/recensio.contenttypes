import Acquisition
from Products.CMFPlone.Portal import PloneSite
from recensio.contenttypes import interfaces
from zope import interface


class ParentGetter(object):
    """Get parent of a certain content type"""

    interface.implements(interfaces.IParentGetter)

    def __init__(self, context):
        self.context = context

    def get_title_from_parent_of_type(self, meta_type):
        """
        Return the title of the first object of a particular type
        which is a parent of the current object.
        """
        obj = self.get_parent_object_of_type(meta_type)
        if obj:
            return obj.Title()
        return ""

    def get_parent_object_of_type(self, meta_type):
        """ Return the object of a particular type which is
        the parent of the current object."""
        if hasattr(self.context, "meta_type") and self.context.meta_type == meta_type:
            return self.context
        obj = Acquisition.aq_inner(self.context)
        while not isinstance(obj, PloneSite):
            obj = Acquisition.aq_parent(obj)
            if hasattr(obj, "meta_type") and obj.meta_type == meta_type:
                return obj
        return None
