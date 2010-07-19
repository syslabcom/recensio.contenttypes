import logging
from DateTime import DateTime

from zope.annotation.interfaces import IAnnotations
from ZODB.blob import Blob

from Products.CMFCore.utils import getToolByName

from wc.pageturner.views import pdf2swf_subprocess
from wc.pageturner.settings import Settings
from wc.pageturner.interfaces import IPageTurnerSettings

from recensio.contenttypes import contenttypesMessageFactory as _

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')
pdf2swf = pdf2swf_subprocess()

def review_pdf_updated_eventhandler(obj, evt):
    """
    Update the swf version of a review pdf when it has been edited
    """
    pdf = obj.get_review_pdf()
    if pdf:
        settings = Settings(obj)
        if DateTime(settings.last_updated) < \
               DateTime(obj.ModificationDate()):
            try:
                swf = pdf2swf.convert(pdf.data)
                log.info("Converted pdf for %s" %obj.absolute_url())
            except exception, e:
                log.error("Error converting pdf for %s : %s" \
                     %(obj.absolute_url(), e))
            if swf:
                blob = Blob()
                blob.open("w").writelines(swf)
                settings.data = blob
                settings.last_updated = DateTime().pCommonZ()
                settings.successfully_converted = True
