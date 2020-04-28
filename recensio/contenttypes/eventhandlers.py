import logging
from recensio.contenttypes import interfaces
from Products.Archetypes.interfaces.event import IObjectInitializedEvent
from Products.CMFCore.utils import getToolByName

log = logging.getLogger("recensio.contenttypes/eventhandlers.py")


def review_pdf_updated_eventhandler(obj, evt):
    """Re-generate the pdf version of the review, then update the
    cover image of the pdf if necessary.
    """
    if not obj.REQUEST.get("pdf_file"):
        obj.update_generated_pdf()

    # Terrible hack, if this method gets called without a real
    # object, we assume that the caller wants htis to happen now
    interfaces.IReviewPDF(obj).generatePageImages(later=evt != None)
