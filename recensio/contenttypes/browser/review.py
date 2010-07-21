from DateTime import DateTime
from os import fstat
from webdav.common import rfc1123_date
import recensio.theme
from ZODB.blob import Blob

from plone.app.blob.download import handleRequestRange
from plone.app.blob.iterators import BlobStreamIterator
from plone.app.blob.utils import openBlob
import plone.app.blob

from Products.Archetypes.utils import contentDispositionHeader
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from wc.pageturner.settings import Settings
from wc.pageturner.views import PageTurnerView
from wc.pageturner.views import pdf2swf_subprocess

from recensio.contenttypes import contenttypesMessageFactory as _


try:
    pdf2swf = pdf2swf_subprocess()
except IOError:
    pdf2swf = None


class View(BrowserView):
    """Moderation View
    """
    template = ViewPageTemplateFile('review.pt')
    review_journal_fields = {
        "get_publication_title": _("Publication Title"),
        "get_volume_title": _("Volume Title"),
        "get_issue_title": _("Issue Title")
        }

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}

        for field in context.metadata_fields:
            if field in self.review_journal_fields.keys():
                meta[field] = self.review_journal_fields[field]
            else:
                meta[field] = fields[field].widget.label
        return meta

    def has_pdf(self):
        """
        If a pdf is deleted a pdf object still exists with size 0
        """
        if hasattr(self.context, "pdf"):
            if self.context.pdf.get_size() > 0:
                return True

    def javascript(self):
        """
        Generates the block of javascript required to embed the flash
        based pdf viewer from wc.pageturner
        """
        if self.has_pdf():
            context = self.context
            ptv = PageTurnerView(context, self.request)
            ptv.settings = Settings(context)
            return ptv.javascript()

    def get_review_title(self):
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
        rtitle = context.Title().decode("utf-8") + \
                 add_meta("getUntertitel", ":") + \
                 add_meta("getErscheinungsort", ".") + \
                 add_meta("getErscheinungsjahr", ":")
        return rtitle

    def __call__(self):
        return self.template()

class DownloadSWFView(PageTurnerView):
    """
    Copied from wc.pageturner views.py since we need to display the
    pdf attached to this review. wc.pageturner expects the context to
    be a file
    """

    def render_blob_version(self):
        header_value = contentDispositionHeader(
            disposition='inline',
            filename=self.context.pdf.getFilename().replace('.pdf', '.swf'))

        blob = self.settings.data
        blobfi = openBlob(blob)
        length = fstat(blobfi.fileno()).st_size
        blobfi.close()

        self.request.response.setHeader('Last-Modified',
                                        rfc1123_date(self.context._p_mtime))
        self.request.response.setHeader('Accept-Ranges', 'bytes')
        self.request.response.setHeader('Content-Disposition', header_value)
        self.request.response.setHeader("Content-Length", length)
        self.request.response.setHeader('Content-Type',
                                        'application/x-shockwave-flash')
        range = handleRequestRange(self.context, length,
                                   self.request, self.request.response)
        return BlobStreamIterator(blob, **range)

    def __call__(self):
        self.settings = Settings(self.context)
        return self.render_blob_version()
