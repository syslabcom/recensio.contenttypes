from Acquisition import aq_inner, aq_parent

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.CMFCore.utils import getToolByName

from recensio.contenttypes import contenttypesMessageFactory as _


class View(BrowserView):
    """Moderation View
    """
    template = ViewPageTemplateFile('rezension.pt')

    def metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        for field in context.ordered_fields:
            # skip fields which aren't considered metadata for Rezension types
            if field not in ["title", "description", "rezension"]:
                meta[field] = fields[field].widget.label
        return meta

    def __call__(self):
        return self.template()
