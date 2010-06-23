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
        for field in fields.keys():
            meta[field] = fields[field].getAccessor()
        import pdb; pdb.set_trace()

    def __call__(self):
        return self.template()
