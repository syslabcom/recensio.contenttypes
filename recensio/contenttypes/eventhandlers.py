import logging
from DateTime import DateTime
import cStringIO as StringIO
import ho.pisa

from zope.annotation.interfaces import IAnnotations
from ZODB.blob import Blob

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import PageTemplateFile

from plone.app.blob.utils import openBlob

from wc.pageturner.views import pdf2swf_subprocess
from wc.pageturner.settings import Settings
from wc.pageturner.interfaces import IPageTurnerSettings

from recensio.contenttypes import contenttypesMessageFactory as _

from helperutilities import wvPDF

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')
pdf2swf = pdf2swf_subprocess()

# http://tools.cherrypy.org/wiki/ZPT
class SimpleZpt(PageTemplateFile):
    """ Customise ViewPageTemplateFile so that we can pass in a dict
    to be used as the context """
    def pt_getContext(self, args=(), options={}, **kw):
        rval = PageTemplateFile.pt_getContext(self, args=args)
        options.update(rval)
        return options


def review_pdf_updated_eventhandler(obj, evt):
    """
    Update the swf version of a review pdf when the review has been
    edited

    If there isn't a custom pdf version of the review, generate the
    pdf from an MS Word .doc file. If there isn't an MS Word doc the
    contents of the review text (html)

    We could implement odf to pdf too, but it sounds like we would
    need to run openoffice as a service:
    http://www.artofsolving.com/opensource/pyodconverter
    """
    has_custom_pdf = hasattr(obj, "pdf") and obj.pdf.get_size() > 0
    if not has_custom_pdf:
        """
        If a pdf hasn't been attached to the review then we generate
        one instead
        """
        doc = obj.getDoc()
        if doc:
            pdf_blob = Blob()
            pdf_blob.open("w").writelines(wvPDF(doc.data))
            obj.generatedPdf = pdf_blob
        else:
            # Generate the pdf from the content of the review
            review = obj.getReview()
            # Insert the review into a template
            pdf_template = SimpleZpt("browser/templates/htmltopdf.pt")
            pdf_html = pdf_template(context={"review":review})
            # Generate the pdf file and save it as a blob
            pdf_blob = Blob()
            pdf_blob_writer = pdf_blob.open("w")
            pdf = ho.pisa.pisaDocument(
                StringIO.StringIO(pdf_html.encode("UTF-8")),
                pdf_blob_writer)
            pdf_blob_writer.close()
            if not pdf.err:
                obj.generatedPdf = pdf_blob

    pdf_blob = obj.get_review_pdf()
    if pdf_blob:
        settings = Settings(obj)
        if DateTime(settings.last_updated) < \
               DateTime(obj.ModificationDate()):
            swf = None
            try:
                pdf = openBlob(pdf_blob)
                swf = pdf2swf.convert(pdf.read())
                pdf.close()
                log.info("Converted pdf for %s" %obj.absolute_url())
            except Exception, e:
                log.error("Error converting pdf for %s : %s" \
                     %(obj.absolute_url(), e))
            if swf:
                blob = Blob()
                blob.open("w").writelines(swf)
                settings.data = blob
                settings.last_updated = DateTime().pCommonZ()
                settings.successfully_converted = True
