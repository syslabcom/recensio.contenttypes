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

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        for field in context.ordered_fields:
            # skip fields which aren't considered metadata for Rezension types
            if field not in ["title", "description", "rezension"]:
                meta[field] = fields[field].widget.label
        return meta

    def has_pdf(self):
        """
        If a pdf is deleted a pdf object still exists with size 0
        """
        if hasattr(self.context, "pdf"):
            if self.context.pdf.size > 0:
                return True

    def get_rezension_title(self):
        """
        Review titles have a particular format consisting of a
        combination of particular metadata:

        Tadeusz Kotlowski: Niemcy. Dzieje panstwa i spoleczenstwa
        1890-1945 Krakow: Avalon 2008. 336 S. ISBN
        978-83-60448-39-7.
        """
        context = self.context

        def add_meta(method, separator):
            """
            Adds a section of metadata if it exists
            """
            meta = u''
            if hasattr(context, method):
                meta = context[method]()
                if meta:
                    meta = separator+" "+meta
            return meta

        rtitle = context.Title() + \
                 add_meta("getUntertitel", ":") + \
                 add_meta("getErscheinungsort", ".") + \
                 add_meta("getErscheinungsjahr", ":")
        return rtitle

    def __call__(self):
        return self.template()
