import logging
from DateTime import DateTime

from zope.annotation.interfaces import IAnnotations
from ZODB.blob import Blob

from Products.CMFCore.utils import getToolByName

from plone.app.blob.utils import openBlob

from wc.pageturner.views import pdf2swf_subprocess
from wc.pageturner.settings import Settings
from wc.pageturner.interfaces import IPageTurnerSettings

from recensio.contenttypes import contenttypesMessageFactory as _

from helperutilities import wvPDF

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')
pdf2swf = pdf2swf_subprocess()

def review_pdf_updated_eventhandler(obj, evt):
    """
    Update the swf version of a review pdf when the review has been
    edited

    If there isn't a custom pdf version of the review, generate the
    pdf from the .doc file or the contents of the review text (html)
    """
    has_custom_pdf = hasattr(obj, "pdf") and obj.pdf.get_size() > 0
    if not has_custom_pdf:
        """
        """
        doc = obj.getDoc()
        if doc:
            pdf_blob = Blob()
            pdf_blob.open("w").writelines(wvPDF(doc.data))
            obj.generatedPdf = pdf_blob
        else:
            review = obj.getReview()

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
